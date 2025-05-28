
![Иллюстрация к проекту](https://github.com/Xprograms89/BitBalCheck/blob/main/Work.png)
Скрипт BitBalCheck для многопоточной проверки балансов биткоин кошельков спомощью программы Electrum.

Найденые адреса подсвечиваются зеленым цветом и сохраняются в log.txt

Строчки:
with Pool(processes=min(11, total_addresses)) as pool:
и
pool = Pool(11)
это количество потоков

Launcher.bat
это основной скрипт запуска чекера BitBalCheck.py

Тестовый адрес для проверки: 16JjyXLhY3aniK4b5dXhPCR712Dy3srVQ8




p2pkh:5KAZxSSxdBMgRWpjRGsVowxdDCMhmYGd6mZF3jxuQhVY1dyWonT
p2pkh:L3BEThKaWgiH1CdgE93tADaWpq8Nwb1xLTfK16dkKbiwsaXbM7sx
p2pkh:KwHemWD3JrBWRyy3vAvNZLhfL2RsQ11Sj26CjzrbUyMb3mq9n3bZ
p2wpkh-p2sh:KwHemWD3JrBWRyy3vAvNZLhfL2RsQ11Sj26CjzrbUyMb3mq9n3bZ
p2wpkh:KwHemWD3JrBWRyy3vAvNZLhfL2RsQ11Sj26CjzrbUyMb3mq9n3bZ
p2wpkh:L3BEThKaWgiH1CdgE93tADaWpq8Nwb1xLTfK16dkKbiwsaXbM7sx



Виды адресов:
Legacy (P2PKH): начинается с цифры 1. Пример: 1N4Qbzg6LSXUXyXu2MDuGfzxwMA7do8AyL.
Script (P2SH): начинается с цифры 3. Пример: 3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy.
SegWit (P2WPKH): начинается с комбинации “bc1q”. Пример: bc1qfg9t7fwn0atn4yf9spca5502vk8dyhq8a9aqd8.
Taproot (P2TR): начинается с комбинации “bc1p”. Пример: bc1peu5hzzyj8cnqm05le6ag7uwry0ysmtf3v4uuxv3v8hqhvsatca8ss2vuwx

donate:
Bitcoin: bc1qz0d9730havlcxdlnjy5x6tqgjm74mkc2n3d8ed
Ethereum: 0xbfB5cA523FBA25c712Ec1F580f0eCC3E0e7cD400
Dogecoin: DQ9pAGAGpJ7TNapsAyhxs6oZBn7wEp6Apx
