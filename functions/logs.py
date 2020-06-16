import time,datetime

def get_nowtime():
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

def logs_red(mess):
    print('\033[31m [' + get_nowtime() + '] ' + mess + ' \033[0m')
    return "success"

def logs_green(mess):
    print('\033[32m [' + get_nowtime() + '] ' + mess + ' \033[0m')
    return "success"

def logs_yellow(mess):
    print('\033[33m [' + get_nowtime() + '] ' + mess + ' \033[0m')
    return "success"

def logs_blue(mess):
    print('\033[34m [' + get_nowtime() + '] ' + mess + ' \033[0m')
    return "success"