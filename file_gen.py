import datetime
import random
import os
import sys
import time

def gen_random_name(path):
    basename = f"{path}/FILE"

    if not os.path.exists(path):
        npath = os.path.join(os.getcwd(), path)
        os.makedirs(npath)
        basename = f"{npath}/FILE"

    suffix = datetime.datetime.now().strftime("%f")
    return "_".join([basename, suffix])

def generate_file(name, s_min, s_max):
    size = random.randint(s_min, s_max)
    with open(name, 'wb') as f:
        f.seek(size) # in bytes
        f.write(b'0')
    
    with open(name, 'wb') as f:
        f.write(b'0' * size)

KB_UNIT = 1000
MB_UNIT = KB_UNIT * 1000
GROUPS = [
        { 'min': 1, 'max': KB_UNIT * 10 }, 
        { 'min': KB_UNIT * 10, 'max': MB_UNIT }, 
        { 'min': MB_UNIT, 'max': MB_UNIT * 10 }
        ]

def generate_files(n, group, path):
    MIN = GROUPS[group]['min']
    MAX = GROUPS[group]['max']
    for i in range(n):
        cdir = os.getcwd()
        ranname = gen_random_name(path)
        filename = os.path.join(cdir, ranname)
        print(f"Filename: {filename}")
        generate_file(filename, MIN, MAX)

if __name__ == "__main__":
    group = int(sys.argv[1])
    n = int(sys.argv[2])
    path = sys.argv[3]
    generate_files(n, group, path)
