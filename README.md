<img src="https://github.com/Xprograms89/BitBalCheck/blob/main/Work.png" width="979">

# Скрипт BitBalCheck для многопоточной проверки балансов биткоин кошельков спомощью программы Electrum.

Найденые адреса подсвечиваются зеленым цветом и сохраняются в log.txt\
Строчки: with Pool(processes=min(11, total_addresses)) as pool: и pool = Pool(11) это количество потоков\
Launcher.bat это основной скрипт запуска чекера BitBalCheck.py\
Тестовый адрес для проверки: 16JjyXLhY3aniK4b5dXhPCR712Dy3srVQ8



### Виды адресов Bitcoin
p2pkh: 5KAZxSSxdBMgRWpjRGsVowxdDCMhmYGd6mZF3jxuQhVY1dyWonT\
p2pkh: L3BEThKaWgiH1CdgE93tADaWpq8Nwb1xLTfK16dkKbiwsaXbM7sx\
p2pkh: KwHemWD3JrBWRyy3vAvNZLhfL2RsQ11Sj26CjzrbUyMb3mq9n3bZ\
p2wpkh-p2sh: KwHemWD3JrBWRyy3vAvNZLhfL2RsQ11Sj26CjzrbUyMb3mq9n3bZ\
p2wpkh: KwHemWD3JrBWRyy3vAvNZLhfL2RsQ11Sj26CjzrbUyMb3mq9n3bZ\
p2wpkh: L3BEThKaWgiH1CdgE93tADaWpq8Nwb1xLTfK16dkKbiwsaXbM7sx

Legacy (P2PKH): Начинается с цифры 1. Пример: 1N4Qbzg6LSXUXyXu2MDuGfzxwMA7do8AyL\
Script (P2SH): Начинается с цифры 3. Пример: 3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy\
SegWit (P2WPKH): Начинается с комбинации bc1q. Пример: bc1qfg9t7fwn0atn4yf9spca5502vk8dyhq8a9aqd8\
Taproot (P2TR): Начинается с комбинации bc1p. Пример: bc1peu5hzzyj8cnqm05le6ag7uwry0ysmtf3v4uuxv3v8hqhvsatca8ss2vuwx

## Donate
*   **Bitcoin:** `bc1qngs6nyzh9mpcgn5f3vpsqqg90m4evxqxpk4gwr`
*   **Ethereum:** `0x846C0F2857743309B43DB4f7Ba7db91aaAfd7E55`
*   **Dogecoin:** `DQyXW6EM2ajNX5jseAar3vYEv3hyi7xWUf`
