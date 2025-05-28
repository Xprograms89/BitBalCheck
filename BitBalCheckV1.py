import re
import subprocess
import json
import sys
import ctypes
import time
import psutil
from multiprocessing import Pool, Manager, Lock
from colorama import init, Fore

init(autoreset=True)

def set_console_title(found=0, checked=0, total=0):
    progress = (checked / total) * 100 if total else 0
    ctypes.windll.kernel32.SetConsoleTitleW(f"Прогресс: {checked}/{total} ({progress:.2f}%) | Найдено: {found}")

def set_high_priority():
    try:
        p = psutil.Process()
        p.nice(psutil.REALTIME_PRIORITY_CLASS)  # Устанавливаем реальный приоритет
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if proc.info['name'] in ('electrum-4.5.8.exe', 'python.exe'):
                psutil.Process(proc.info['pid']).nice(psutil.REALTIME_PRIORITY_CLASS)
    except Exception as e:
        print(f"Ошибка установки приоритета: {e}")

ADDRESS_PATTERNS = {
    "P2PKH": re.compile(r'\b1[a-km-zA-HJ-NP-Z1-9]{25,34}\b'),
    "P2SH": re.compile(r'\b3[a-km-zA-HJ-NP-Z1-9]{25,34}\b'),
    "P2WPKH": re.compile(r'\bbc1q[a-z0-9]{11,71}\b'),
    "P2TR": re.compile(r'\bbc1p[a-z0-9]{11,71}\b')
}

input_file = r'addresses.txt'
output_file = r'log.txt'

def extract_addresses(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    addresses = set()
    for pattern in ADDRESS_PATTERNS.values():
        addresses.update(pattern.findall(content))
    
    return list(addresses)

def check_balance(address):
    try:
        process = subprocess.Popen(
            ['C:\\Program Files (x86)\\Electrum\\electrum-4.5.8.exe', 'getaddressbalance', address],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = process.communicate(timeout=10)
        if process.returncode == 0:
            return True, address, stdout.strip()
        else:
            return False, address, stderr.strip()
    except subprocess.TimeoutExpired:
        process.kill()
        return False, address, "Timeout expired"
    except Exception as e:
        return False, address, f"Error: {str(e)}"

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
                    with open(output_file, 'a') as log:
                        log.write(log_message + '\n')
                    print(f"{Fore.GREEN}{log_message}")
                else:
                    print(log_message)
            except json.JSONDecodeError:
                print(f"{address}, Error: Invalid JSON response")
        else:
            print(f"{address}, Error: {message}")
        set_console_title(found.value, checked.value, total_addresses)

def worker(args):
    address, checked, found, total_addresses, lock = args
    result = check_balance(address)
    log_result(result, checked, found, total_addresses, lock)

if __name__ == '__main__':
    set_high_priority()
    addresses = extract_addresses(input_file)
    total_addresses = len(addresses)
    
    if total_addresses == 0:
        print("Нет адресов для проверки.")
        sys.exit(0)

    manager = Manager()
    checked = manager.Value('i', 0)
    found = manager.Value('i', 0)
    lock = manager.Lock()

    print(f"Найдено {total_addresses} адресов. Начинаем проверку...\n")
    set_console_title(0, 0, total_addresses)

    pool = Pool(min(11, total_addresses))
    pool.map(worker, [(addr, checked, found, total_addresses, lock) for addr in addresses])
    
    pool.close()
    pool.join()

    set_console_title(found.value, total_addresses, total_addresses)
    print("\nПроверка завершена.")
