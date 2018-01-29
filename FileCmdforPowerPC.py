"""files md5 chk"""
import hashlib
import re
import os
import sys
import struct
import traceback


VERSION = 'V1.0 20180129'
MD5_BUF_SIZE = 1024*4

if getattr(sys, 'frozen', False):
    WORKING_DIR_PATH = os.path.dirname(sys.executable)
else:
    WORKING_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

CFG_FILE_PATH = os.path.join(WORKING_DIR_PATH, 'cfg.txt')


def get_md5(path):
    """calc md5 of file"""
    md5 = hashlib.md5()
    with open(path, 'rb') as file:
        while True:
            buf = file.read(MD5_BUF_SIZE)
            if buf:
                md5.update(buf)
            else:
                break
    return md5.hexdigest()


def main_proc(file_path):
    """main proc  22  uint32  26 uint32  54 md5"""
    print('Welcome to file md5 add tool. Designed by Kay.')
    print('version: %s'%VERSION)
    print('work path: ', WORKING_DIR_PATH)
    print('file: ', os.path.basename(file_path))
    print('please wait...')

    pre_len = 0
    post_len = 0
    try:
        with open(CFG_FILE_PATH) as cfg_file:
            cfg_str = cfg_file.read()
            cfg_str = re.sub(r'\s', '', cfg_str)
            match = re.match(r'len1[=:-：](\d+).*?len2[=:-：](\d+)', cfg_str)
            if match:
                pre_len = int(match.group(1))
                post_len = int(match.group(2))
                print('len1:', pre_len, ', len2:', post_len)
            else:
                print('ERROR: cfg file format err!\n')
    except Exception:
        traceback.print_exc()
        print('ERROR: cfg file not found')
        with open(CFG_FILE_PATH, 'w') as cfg_file:
            cfg_file.write('len1=0\nlen2=0\n')

    md5 = get_md5(file_path)
    print('md5', md5)
    file_content = None
    with open(file_path, mode='rb') as file:
        file_content = file.read()
    with open(file_path + '.z', mode='wb') as file:
        file.seek(22, 0)
        pack_uint32 = struct.pack("I", pre_len)
        file.write(pack_uint32)
        file.seek(26, 0)
        pack_uint32 = struct.pack("I", post_len)
        file.write(pack_uint32)
        file.seek(54, 0)
        file.write(bytes().fromhex(md5))
        file.write(file_content)
    print('OK. Output file: ', os.path.basename(file_path) + '.z')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main_proc(sys.argv[1])
    else:
        print('未拖入文件！')
    os.system('pause')
