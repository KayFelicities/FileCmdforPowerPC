"""files md5 chk"""
import hashlib
import os
import sys
import struct
import traceback


VERSION = 'V1.0 20180129'
MD5_BUF_SIZE = 1024*4

if getattr(sys, 'frozen', False):
    ZLIB_PATH = os.path.join(sys._MEIPASS, 'zlib.exe')
else:
    ZLIB_PATH = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'zlib.exe')
print('zlib path: ', ZLIB_PATH)


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
    work_path = os.path.dirname(file_path)
    print('Welcome to file md5 add tool. Designed by Kay.')
    print('version: %s'%VERSION)
    print('work path: ', work_path)
    print('file: ', os.path.basename(file_path))
    print('please wait...')

    md5 = get_md5(file_path)
    print('md5', md5)

    pre_len = os.path.getsize(file_path)
    os.system('copy ' + ZLIB_PATH + ' ' + os.path.join(work_path, 'zlib.exe'))
    os.chdir(work_path)
    os.system('zlib.exe d ' + os.path.basename(file_path))
    zfile_path = file_path + '.Z'
    post_len = os.path.getsize(zfile_path)
    print('pre size: {pre}, post size: {post}'.format(pre=pre_len, post=post_len))
    file_content = None
    with open(zfile_path, mode='rb') as file:
        file_content = file.read()
    with open(zfile_path, mode='wb') as file:
        file.seek(22, 0)
        pack_uint32 = struct.pack("I", pre_len)
        file.write(pack_uint32)
        file.seek(26, 0)
        pack_uint32 = struct.pack("I", post_len)
        file.write(pack_uint32)
        file.seek(54, 0)
        file.write(bytes().fromhex(md5))
        file.write(file_content)
    print('OK. Output file: ', os.path.basename(zfile_path))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main_proc(os.path.realpath(sys.argv[1]))
    else:
        print('未拖入文件！')
    os.system('pause')
