import re
import subprocess
import json
import sys
import ctypes
import psutil
from multiprocessing import Pool, Manager, Lock
from colorama import init, Fore

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

# Устанавливаем заголовок консоли
def set_console_title(found=0, checked=0, total=0):
    progress = (checked / total) * 100 if total else 0
    ctypes.windll.kernel32.SetConsoleTitleW(f"Прогресс: {checked}/{total} ({progress:.2f}%) | Найдено: {found}")

# Устанавливаем высокий приоритет процесса
def set_high_priority():
    try:
        psutil.Process().nice(psutil.REALTIME_PRIORITY_CLASS)
    except Exception as e:
        print(f"Ошибка установки приоритета: {e}")

# Извлекаем Bitcoin-адреса из файла
def extract_addresses(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    addresses = set()
    for pattern in ADDRESS_PATTERNS.values():
        addresses.update(pattern.findall(content))
    
    return list(addresses)

# Проверяем баланс через Electrum RPC
def check_balance(address):
    try:
        result = subprocess.run(
            [ELECTRUM_PATH, 'getaddressbalance', address],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5
        )
        return result.returncode == 0, address, result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, address, "Timeout expired"

# Логируем результат проверки
def log_result(result, checked, found, total_addresses, lock):
    success, address, message = result
    with lock:
        checked.value += 1
        if success:
            try:
                balance_info = json.loads(message)
                confirmed = float(balance_info.get('confirmed', 0))
                log_message = f"{address}, Balance: {confirmed} BTC"
                if confirmed > 0:
                    found.value += 1
                    with open(OUTPUT_FILE, 'a', encoding='utf-8') as log:
                        log.write(log_message + '\n')
                    print(f"{Fore.GREEN}{log_message}")
                else:
                    print(log_message)
            except json.JSONDecodeError:
                print(f"{address}, Error: Invalid JSON response")
        else:
            print(f"{address}, Error: {message}")
        set_console_title(found.value, checked.value, total_addresses)

# Рабочая функция для процесса
def worker(args):
    address, checked, found, total_addresses, lock = args
    result = check_balance(address)
    log_result(result, checked, found, total_addresses, lock)

if __name__ == '__main__':
    set_high_priority()
    addresses = extract_addresses(INPUT_FILE)
    total_addresses = len(addresses)
    
    if total_addresses == 0:
        print("Нет адресов для проверки.")
        sys.exit(0)
    
    print(f"Найдено {total_addresses} адресов. Начинаем проверку...\n")
    set_console_title(0, 0, total_addresses)
    
    # Запускаем Electrum в режиме RPC
    subprocess.run([ELECTRUM_PATH, 'daemon', 'start'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    manager = Manager()
    checked = manager.Value('i', 0)
    found = manager.Value('i', 0)
    lock = manager.Lock()
    
    with Pool(processes=min(6, total_addresses)) as pool:
        pool.imap_unordered(worker, [(addr, checked, found, total_addresses, lock) for addr in addresses])
        pool.close()
        pool.join()
    
    set_console_title(found.value, total_addresses, total_addresses)
    print("\nПроверка завершена.")
