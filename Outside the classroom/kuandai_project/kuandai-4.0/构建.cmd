@echo off
chcp 65001
pyinstaller -F -i main.ico main.py -p nuoyis_webautomatic_function.py -n 诺依阁的宽带自动登录
pause