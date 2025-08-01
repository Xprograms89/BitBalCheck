import re
import subprocess
import json
import sys
import ctypes
import psutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore
from threading import Lock, Event

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
pause_event = Event()
pause_event.set()

found = 0
checked = 0
total_addresses = 0

RESTART_INTERVAL = 5000
MAX_WORKERS = 10

def set_console_title():
    progress = (checked / total_addresses) * 100 if total_addresses else 0
    title = f"Прогресс: {checked}/{total_addresses} ({progress:.2f}%) | Найдено: {found}"
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def set_high_priority():
    psutil.Process().nice(psutil.REALTIME_PRIORITY_CLASS)

def extract_addresses(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    addresses = set()
    for pattern in ADDRESS_PATTERNS.values():
        addresses.update(pattern.findall(content))
    return list(addresses)

def check_balance(address):
    pause_event.wait()
    result = subprocess.run(
        [ELECTRUM_PATH, 'getaddressbalance', address],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=30
    )
    if result.returncode == 0:
        return True, address, result.stdout.strip()
    else:
        return False, address, result.stderr.strip()

def log_result(success, address, message):
    global found, checked
    with lock:
        checked += 1
        if success:
            balance_info = json.loads(message)
            confirmed = float(balance_info.get('confirmed', 0))
            log_message = f"{address}, Balance: {confirmed} BTC"
            if confirmed > 0:
                found += 1
                with open(OUTPUT_FILE, 'a', encoding='utf-8') as log:
                    log.write(log_message + '\n')
                print(Fore.GREEN + log_message)
            else:
                print(log_message)
        else:
            print(Fore.RED + f"{address}, Error: {message}")
        set_console_title()

def restart_electrum_exe():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and 'electrum' in proc.info['name'].lower():
            proc.kill()
    time.sleep(2)
    subprocess.Popen([ELECTRUM_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(Fore.YELLOW + "[!] Electrum GUI перезапущен")

def process_addresses(addresses):
    i = 0
    n = len(addresses)
    while i < n:
        batch = addresses[i:i+RESTART_INTERVAL]
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(check_balance, addr): addr for addr in batch}
            for future in as_completed(futures):
                result = future.result()
                log_result(*result)
        i += RESTART_INTERVAL

        # Перезапуск только если есть еще адреса для обработки
        if i < n:
            print(Fore.YELLOW + "[*] Приостановка на время перезапуска Electrum...")
            pause_event.clear()
            restart_electrum_exe()
            time.sleep(6)
            pause_event.set()
            print(Fore.YELLOW + "[*] Потоки возобновлены.")

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

    process_addresses(addresses)

    set_console_title()
    print("\nПроверка завершена.")

if __name__ == '__main__':
    main()
