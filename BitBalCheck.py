import re
import subprocess
import json
import sys
import ctypes
import psutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore
from threading import Lock

init(autoreset=True)

ADDRESS_PATTERNS = {
    "P2PKH": re.compile(r'\b1[a-km-zA-HJ-NP-Z1-9]{25,34}\b'),
    "P2SH": re.compile(r'\b3[a-km-zA-HJ-NP-Z1-9]{25,34}\b'),
    "P2WPKH": re.compile(r'\bbc1q[a-z0-9]{11,71}\b'),
    "P2TR": re.compile(r'\bbc1p[a-z0-9]{11,71}\b')
}

INPUT_FILE = r'addresses.txt'
OUTPUT_FILE = r'log.txt'
ELECTRUM_PATH = r'C:\Program Files (x86)\Electrum\electrum-4.5.8.exe'

lock = Lock()
found = 0
checked = 0
total_addresses = 0

def set_console_title():
    progress = (checked / total_addresses) * 100 if total_addresses else 0
    ctypes.windll.kernel32.SetConsoleTitleW(f"Прогресс: {checked}/{total_addresses} ({progress:.2f}%) | Найдено: {found}")

def set_high_priority():
    try:
        psutil.Process().nice(psutil.REALTIME_PRIORITY_CLASS)
    except Exception as e:
        print(f"Ошибка приоритета: {e}")

def extract_addresses(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    addresses = set()
    for pattern in ADDRESS_PATTERNS.values():
        addresses.update(pattern.findall(content))
    return list(addresses)

def check_balance(address, retries=2, delay=3, timeout=30):
    for attempt in range(retries):
        try:
            result = subprocess.run(
                [ELECTRUM_PATH, 'getaddressbalance', address],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0, address, result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
        except subprocess.TimeoutExpired:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                return False, address, "Timeout expired"
        except Exception as e:
            return False, address, f"Exception: {e}"

def log_result(success, address, message):
    global found, checked
    with lock:
        checked += 1
        if success:
            try:
                balance_info = json.loads(message)
                confirmed = float(balance_info.get('confirmed', 0))
                log_message = f"{address}, Balance: {confirmed} BTC"
                if confirmed > 0:
                    found += 1
                    with open(OUTPUT_FILE, 'a', encoding='utf-8') as log:
                        log.write(log_message + '\n')
                    print(f"{Fore.GREEN}{log_message}")
                else:
                    print(log_message)
            except json.JSONDecodeError:
                print(f"{address}, Error: Invalid JSON response")
        else:
            print(f"{address}, Error: {message}")
        set_console_title()

def stop_electrum_daemon():
    try:
        subprocess.run([ELECTRUM_PATH, 'daemon', 'stop'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Ошибка при остановке daemon: {e}")

def main():
    global total_addresses
    set_high_priority()
    addresses = extract_addresses(INPUT_FILE)
    total_addresses = len(addresses)

    if total_addresses == 0:
        print("Нет адресов для проверки.")
        sys.exit(0)

    print(f"Найдено {total_addresses} адресов. Начинаем проверку...\n")
    set_console_title()

    subprocess.run([ELECTRUM_PATH, 'daemon', 'start'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(check_balance, addr): addr for addr in addresses}
            for future in as_completed(futures):
                try:
                    result = future.result()
                    log_result(*result)
                except Exception as e:
                    print(f"Ошибка при обработке: {e}")
    except KeyboardInterrupt:
        print("\nПолучен сигнал прерывания, завершаем...")
    finally:
        stop_electrum_daemon()
        print("Daemon Electrum остановлен. Выход.")

    set_console_title()
    print("\nПроверка завершена.")

if __name__ == '__main__':
    main()
