#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by zj on 2022/04/22 
# Task:

import glob
import hashlib
import logging
import os
import re
import time
from datetime import datetime


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是半角数字"""
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False


def is_Qnumber(uchar):
    """判断一个unicode是否是全角数字"""
    if uchar >= u'\uff10' and uchar <= u'\uff19':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是半角英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def is_Qalphabet(uchar):
    """判断一个unicode是否是全角英文字母"""
    if (uchar >= u'\uff21' and uchar <= u'\uff3a') or (uchar >= u'\uff41' and uchar <= u'\uff5a'):
        return True
    else:
        return False


def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False


def Q2B(uchar):
    """单个字符 全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
        return uchar
    return chr(inside_code)


def B2Q(uchar):
    """单个字符 半角转全角"""
    inside_code = ord(uchar)
    if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符
        return uchar
    if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为: 半角 = 全角 - 0xfee0
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return chr(inside_code)


def stringQ2B(ustring):
    """把字符串全角转半角"""
    return "".join([Q2B(uchar) for uchar in ustring])


def stringpartQ2B(ustring):
    """把字符串中数字和字母全角转半角"""
    return "".join([Q2B(uchar) if is_Qnumber(uchar) or is_Qalphabet(uchar) else uchar for uchar in ustring])


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class AverageMeter(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def makedirs_if_not_exists(dirname):
    dirname = os.path.abspath(dirname)
    assert not os.path.isfile(dirname), '‘{}’ 存在同名文件！'.format(dirname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def makedirs(dirname):
    return makedirs_if_not_exists(dirname)


def remove_file_path_prefix(file_path: str, prefix: str):
    if not prefix.endswith('/'):
        prefix += '/'
    return file_path.replace(prefix, '')


def delete_earlier_model(root, file_name, keeps=3, log=True):
    files = glob.glob(os.path.join(root, file_name))
    files = sorted(files, key=os.path.getctime, reverse=True)
    files_deleted = files[keeps:]
    # print([os.path.basename(x) for x in files])
    if len(files_deleted) != 0:
        if log:
            print('Deleting files in {} ...'.format(root))
        for f in files_deleted:
            os.remove(f)
            if log:
                print("File ‘{}’ have been deleted.".format(os.path.basename(f)))


def delete_0_dir(dir_root):
    """
    删除目录下的空白目录。
    :param dir_root:
    :return:
    """
    root, dirs, _ = next(os.walk(dir_root))
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        files_ = os.listdir(dir_path)
        len_ = len(files_)
        if len_ == 0:
            os.rmdir(dir_path)  # 目录为空时才可以删除，否则报错
            print("目录 '{}' 已被删除。".format(dir))
        elif len_ == 1:
            if files_[0][:7] == 'logger_' and files_[0].endswith('.log'):
                os.remove(os.path.join(dir_path, files_[0]))
                os.rmdir(dir_path)  # 目录为空时才可以删除，否则报错
                print("目录 '{}' 已被删除。".format(dir))


def get_file_path_list(dir_path, ext=None):
    """
    从给定目录中获取所有文件的路径

    :param dir_path: 路径名
    :return: 该路径下的所有文件路径(path)列表
    """
    if ext:
        patt = re.compile(r".*{}$".format(ext))

    file_path_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if ext:
                result = patt.search(file)
                if not result:
                    continue
            path = os.path.join(root, file)
            file_path_list.append(path)
    # print("'{}'目录中文件个数 : {}".format(os.path.basename(dir_path), len(file_path_list)))
    return file_path_list


def setup_logger(logger_name, log_root=None, log_file_save_basename=None, level=logging.INFO, screen=True,
                 tofile=False):
    '''set up logger'''
    lg = logging.getLogger(logger_name)
    formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] %(message)s',
                                  datefmt='%Y-%m-%d %I:%M:%S %p')
    lg.setLevel(level)
    if tofile and log_root:
        if not os.path.exists(log_root):
            os.makedirs(log_root)
        if log_file_save_basename:
            log_file = os.path.join(log_root, log_file_save_basename)
        else:
            log_file = os.path.join(log_root, f'{get_time_str()}.log')

        fh = logging.FileHandler(log_file, mode='a')
        fh.setFormatter(formatter)
        lg.addHandler(fh)
    if screen:
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        lg.addHandler(sh)


def get_time_int():
    return int(time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())))


# def get_time_str():
#     return time.strftime("%m%d%H%M%S%Y", time.localtime(time.time()))

def get_time_str():
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))


def main():
    pass


if __name__ == '__main__':
    start = datetime.now()
    print("Start time is {}".format(start))
    main()
    end = datetime.now()
    print("End time is {}".format(end))
    print("\nTotal running time is {}s".format((end - start).seconds))
    print("\nCongratulations!!!")
