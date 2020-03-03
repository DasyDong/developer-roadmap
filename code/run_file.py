# coding:utf-8
import time
import os

from mmap import mmap


def get_lines(fp):
    with open(fp, "r+") as f:
        for i in f:
            yield i


def get_lines_by_mmap(fp):
    with open(fp, "r+") as f:
        m = mmap(f.fileno(), 0)
        tmp = 0
        for i, char in enumerate(m):
            if char == b"\n":
                yield m[tmp:i+1]
                tmp = i+1
##################################################


def run_get_lines():

    b_time = time.clock()
    for i in range(10):
        for i in get_lines('README.md'):
            print(i)
    a_time = time.clock()
    print a_time - b_time
##################################################


def print_directory_contents(s_path):
    """
    这个函数接收文件夹的名称作为输入参数
    返回该文件夹中文件的路径
    以及其包含文件夹中文件的路径
    """
    import os
    for s_child in os.listdir(s_path):
        s_child_path = os.path.join(s_path, s_child)
        if os.path.isdir(s_child_path):
            print_directory_contents(s_child_path)
        else:
            print(s_child_path)
##################################################


def run_print_directory_contents():
    current_path = os.getcwd()
    # grand_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))

    print_directory_contents(current_path)


if __name__ == "__main__":
    run_print_directory_contents()
