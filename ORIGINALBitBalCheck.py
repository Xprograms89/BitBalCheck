import re
import subprocess
import json
import sys
import ctypes
from multiprocessing import Pool
from colorama import init, Fore

# Инициализация colorama для корректной работы в Windows
init(autoreset=True)

# Установка заголовка окна консоли (Windows)
def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

# Регулярные выражения для биткойн-адресов
ADDRESS_PATTERNS = {
    "P2PKH": re.compile(r'\b1[a-km-zA-HJ-NP-Z1-9]{25,34}\b'),
    "P2SH": re.compile(r'\b3[a-km-zA-HJ-NP-Z1-9]{25,34}\b'),
    "P2WPKH": re.compile(r'\bbc1q[a-z0-9]{11,71}\b'),
    "P2TR": re.compile(r'\bbc1p[a-z0-9]{11,71}\b')
}

input_file = r'addresses.txt'
output_file = r'log.txt'

def extract_addresses(filename):
    """Извлекает биткойн-адреса из файла по заданным регулярным выражениям."""
    with open(filename, 'r') as f:
        content = f.read()
    
    addresses = set()
    for pattern in ADDRESS_PATTERNS.values():
        addresses.update(pattern.findall(content))
    
    return list(addresses)

def check_balance(address):
    """Запускает процесс проверки баланса адреса через Electrum."""
    result = subprocess.run(
        ['C:\\Program Files (x86)\\Electrum\\electrum-4.5.8.exe', 'getaddressbalance', address],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        return True, address, result.stdout.strip()
    else:
        return False, address, result.stderr.strip()

def log_result(result):
    """Обрабатывает и логирует результаты проверки баланса."""
    success, address, message = result
    global checked, total_addresses

    checked += 1
    progress = (checked / total_addresses) * 100
    set_console_title(f"Прогресс: {checked}/{total_addresses} ({progress:.2f}%)")

    if success:
        try:
            balance_info = json.loads(message)
            confirmed = float(balance_info.get('confirmed', 0))
            log_message = f"{address}, Balance: {confirmed} BTC"
            
            if confirmed > 0:
                with open(output_file, 'a') as log:
                    log.write(log_message + '\n')
                print(f"{Fore.GREEN}{log_message}")  # Зеленый цвет для найденных с балансом
            else:
                print(log_message)
        except json.JSONDecodeError:
            log_message = f"{address}, Error: Invalid JSON response"
            print(log_message)
    else:
        log_message = f"{address}, Error: {message}"
        print(log_message)

def worker(address):
    return check_balance(address)

if __name__ == '__main__':
    addresses = extract_addresses(input_file)
    total_addresses = len(addresses)
    checked = 0

    print(f"Найдено {total_addresses} адресов. Начинаем проверку...\n")
    set_console_title("Прогресс: 0%")

    pool = Pool(11)
    for address in addresses:
        pool.apply_async(worker, args=(address,), callback=log_result)
    
    pool.close()
    pool.join()

    set_console_title("Проверка завершена")
    print("\nПроверка завершена.")
