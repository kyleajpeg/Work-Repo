import threading
import time
from turtle import *
import random

CHARLIST = [73, 109, 97, 103, 105, 110, 101, 32, 116, 97, 107, 105, 110, 103,
            32, 97, 32, 99, 108, 97, 115, 115, 32, 105, 110, 32, 112, 121, 116, 104, 111, 
            110, 32, 97, 110, 100, 32, 116, 104, 101, 121, 32, 100, 111, 110, 39, 116, 32, 116, 
            101, 97, 99, 104, 32, 121, 111, 117, 32, 108, 105, 115, 116, 32, 99, 111, 109, 112, 
            114, 101, 104, 101, 110, 115, 105, 111, 110, 10]
COLOR_CODES = [30, 31, 32, 33, 34, 35, 36, 37]
NUMBER_OF_THREADS = len(CHARLIST)

def print_char(index, lock):
    code = CHARLIST[index]
    char = chr(code)
    color_code = random.choice(COLOR_CODES)
    lock.acquire()
    print(f"\033[{color_code}m" + char, end="", flush=True)
    time.sleep(0.07)
    lock.release()

def main():
    threads = []
    lock = threading.Lock()
    for i in range(NUMBER_OF_THREADS):
        t = threading.Thread(target = print_char, args= (i, lock))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    time.sleep(3)
    fun_window()

def fun_window():
    colors = ['#ffdbaf', '#fff2e2', '#756046', '#443421', '#ffe8b2', '#edb86f', '#997138']
    colorvalue = random.choice(colors)
    bsize = random.randint(25,80)
    gh = random.randint(25,bsize)
    length = random.randint(150,450)
    xoffset = 0 - (length/2)
    hideturtle()
    setup(length + bsize + 225, bsize*4 + 205)
    title('Fun Window')
    speed(15)
    bgcolor('black')
    color('black')
    setx(xoffset)
    color(colorvalue) 
    begin_fill()
    circle(bsize)
    circle(0 - bsize)
    end_fill()
    begin_fill()
    sety(0 - gh)
    forward(length)
    end_fill()
    color('pink')
    begin_fill()
    circle(gh,180)
    end_fill()
    color(colorvalue)
    begin_fill()
    forward(length)
    sety(0)
    setpos(length + xoffset, 0 - gh)
    setpos(length + xoffset, gh)
    setpos(xoffset,0)
    end_fill()
    done() # credit https://github.com/OwlsNeck/python-cock-generator/blob/master/dick%20generator.py


if __name__ == "__main__":
    main()