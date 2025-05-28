<img src="https://github.com/Xprograms89/BitBalCheck/blob/main/Work.png" width="979">

# BitBalCheck

Скрипт **BitBalCheck** предназначен для многопоточной проверки балансов биткоин-кошельков с помощью программы Electrum.

- Найденные адреса подсвечиваются зелёным цветом и сохраняются в файл `log.txt`.
- Количество потоков задаётся в строках:
  ```python
  with Pool(processes=min(11, total_addresses)) as pool:
и

pool = Pool(11)
Launcher.bat — основной скрипт для запуска чекера BitBalCheck.py.
Тестовый адрес для проверки
16JjyXLhY3aniK4b5dXhPCR712Dy3srVQ8
Примеры адресов
p2pkh:5KAZxSSxdBMgRWpjRGsVowxdDCMhmYGd6mZF3jxuQhVY1dyWonT
p2pkh:L3BEThKaWgiH1CdgE93tADaWpq8Nwb1xLTfK16dkKbiwsaXbM7sx
p2pkh:KwHemWD3JrBWRyy3vAvNZLhfL2RsQ11Sj26CjzrbUyMb3mq9n3bZ
p2wpkh-p2sh:KwHemWD3JrBWRyy3vAvNZLhfL2RsQ11Sj26CjzrbUyMb3mq9n3bZ
p2wpkh:KwHemWD3JrBWRyy3vAvNZLhfL2RsQ11Sj26CjzrbUyMb3mq9n3bZ
p2wpkh:L3BEThKaWgiH1CdgE93tADaWpq8Nwb1xLTfK16dkKbiwsaXbM7sx
Виды биткоин-адресов
Тип	Формат (начинается с)	Пример
Legacy (P2PKH)	1	1N4Qbzg6LSXUXyXu2MDuGfzxwMA7do8AyL
Script (P2SH)	3	3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy
SegWit (P2WPKH)	bc1q	bc1qfg9t7fwn0atn4yf9spca5502vk8dyhq8a9aqd8
Taproot (P2TR)	bc1p	bc1peu5hzzyj8cnqm05le6ag7uwry0ysmtf3v4uuxv3v8hqhvsatca8ss2vuwx
Donate
Валюта	Адрес
Bitcoin	bc1qz0d9730havlcxdlnjy5x6tqgjm74mkc2n3d8ed
Ethereum	0xbfB5cA523FBA25c712Ec1F580f0eCC3E0e7cD400
Dogecoin	DQ9pAGAGpJ7TNapsAyhxs6oZBn7wEp6Apx
