import os
import psutil
import subprocess


def alt():
    "someProgram" in (p.name() for p in psutil.process_iter())

def main():
    output = subprocess.check_output(('TASKLIST', '/FO', 'CSV')).decode()
    output = output.replace('"', '').split('\r\n')
    keys = output[0].split(',')
    proc_list = [i.split(',') for i in output[1:] if i]
    proc_dict = dict((i[0], dict(zip(keys[1:], i[1:]))) for i in proc_list)
    for name, values in sorted(proc_dict.items(), key=lambda x: x[0].lower()):
        print('%s: %s' % (name, values))


if __name__ == '__main__':
    main()