#!/usr/bin/env python
# encoding: utf-8

import cheat_engine
import threading
import os
import log

"""
四项资源(float)：
0x_______0:
食物(4Bytes)            木材(4Bytes)                石头(4Bytes)                黄金(4Bytes)
人口上限差值(4Bytes)    xx                          xx                          xx
xx                      xx                          xx                          当前人口数(4Bytes)
"""


BASE_FOOD_ADDR = 0x007A5FEC     # 食物的基址
TIMER = None
TIMER_INTERVAL = 3


def write_value(hProcess, addr, value):
    cheat_engine.write_process(
        hProcess,
        addr,
        cheat_engine.float_to_hex(value),
        4
    )


def freeze_mem(hProcess, info):
    """
    锁定内存：定时修改内存的值
    """

    value = cheat_engine.read_process(hProcess, BASE_FOOD_ADDR, 4)
    FOOD_ADDR = None
    if value:
        food_point = value + 0xA8           # 当前食物地址指针 = 基址 + 偏移地址
        FOOD_ADDR = cheat_engine.read_process(hProcess, food_point, 4)
        # log.puts('food_point %x, FOOD_ADDR: %x' % (food_point, FOOD_ADDR))
    if FOOD_ADDR:
        write_value(hProcess, FOOD_ADDR + 0, 90000)
        write_value(hProcess, FOOD_ADDR + 4, 90000)
        write_value(hProcess, FOOD_ADDR + 8, 90000)
        write_value(hProcess, FOOD_ADDR + 12, 90000)
        write_value(hProcess, FOOD_ADDR + 16, 180)
        write_value(hProcess, FOOD_ADDR + 44, 100)

    TIMER = threading.Timer(TIMER_INTERVAL, freeze_mem, [hProcess, info])
    TIMER.start()


def print_help():
    log.puts(u'q - 退出')
    log.puts(u'h - 查看该帮助')


def main():
    # 获取帝国时代2的游戏进程
    processes = cheat_engine.list_process()
    pid = None
    for process_name in processes:
        if process_name.startswith('age2') and process_name.endswith('.exe'):
            pid = processes[process_name]

    if not pid:
        log.puts(u'游戏没有启动')
        os._exit(1)

    info = cheat_engine.get_system_info()
    if not info:
        return

    log.puts(u'当前游戏进程：%s' % pid)
    hProcess = cheat_engine.inject_process(pid)
    if not hProcess:
        return

    TIMER = threading.Timer(TIMER_INTERVAL, freeze_mem, [hProcess, info])
    TIMER.start()

    print_help()
    while True:
        log.puts(u'请输入指令：')
        op = raw_input()
        if op == 'q':
            cheat_engine.close_process(hProcess)
            os._exit(1)
        elif op == 'h':
            print_help()

    cheat_engine.close_process(hProcess)


if __name__ == '__main__':
    main()
