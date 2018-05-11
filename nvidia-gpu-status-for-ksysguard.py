#!/usr/bin/env python3

# Ref: https://techbase.kde.org/Development/Tutorials/Sensors#Protocol

import subprocess
import xml.etree.ElementTree as ET

supported_query = {
    'Temperature': lambda gpu: gpu.find('./temperature/gpu_temp').text.split(' ')[0],
    'Utilization': lambda gpu: gpu.find('./utilization/gpu_util').text.split(' ')[0],
    'Memory_Used': lambda gpu: gpu.find('./fb_memory_usage/used').text.split(' ')[0]}

def make_cmd(gpu_id, key):
    return f'{gpu_id}_{key}'

def break_cmd(cmd):
    return cmd.split('_', maxsplit=1)


if __name__ == '__main__':
    print('ksysguardd 1.2.0')
    keys = supported_query.keys()
    while True:
        cmd = input('ksysguardd> ')
        info = ET.fromstring(subprocess.check_output(['nvidia-smi', '-q', '-x']))
        if cmd == 'monitors':
            for gpu in info.findall('gpu'):
                gpu_id = gpu.attrib['id']
                for key in keys:
                    print(f'{make_cmd(gpu_id, key)}\tfloat')
        else:
            gpu_id, key = break_cmd(cmd)
            if key.endswith('?'):
                print(f'{make_cmd(gpu_id, key[:-1])}\t0\t0')
            else:
                gpu = info.find(f'.//gpu/[@id="{gpu_id}"]')
                result = supported_query[key](gpu)
                print(result)
