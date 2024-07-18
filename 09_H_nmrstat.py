#!/usr/local/python37/bin/python3.7
# evaluate the averaged NMR chemical shifts
import sys
import numpy as np
import glob
import shutil

def process_file(filename):
    # 读取文件数据
    with open(filename, 'r') as file:
        lines = file.readlines()

    # 提取元素和坐标信息
    elements, x, y, z = [], [], [], []

    for line in lines[2:]:
        data = line.split()
        elements.append(data[0])
        x.append(float(data[1]))
        y.append(float(data[2]))
        z.append(float(data[3]))

    elements = np.array(elements)
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    # 寻找C和H的索引
    c_indices = np.where(np.array([element.startswith('C') for element in elements]))[0] + 1
    h_indices = np.where(np.array([element.startswith('H') for element in elements]))[0] + 1
    
    # 距离判断值
    ref = 1.2

    num_ch3 = 0
    loc_c, loc_h = [], []

    for i in c_indices:
        count = 0
        loc_h_temp = []

        for j in h_indices:
            dis = np.sqrt((x[i-1] - x[j-1])**2 + (y[i-1] - y[j-1])**2 + (z[i-1] - z[j-1])**2)

            if dis <= ref:
                count += 1
                loc_h_temp.append(j)

        if count == 3:
            num_ch3 += 1
            loc_c.append(i)
            loc_h.append(loc_h_temp)

    # 保存结果到文件
    with open('location_C.txt', 'w') as fid_c:
        for i, c_val in enumerate(loc_c):
            fid_c.write(f"10\n{c_val}\n")
            if i < len(loc_c) - 1:
                fid_c.write('\n')

    with open('location_H.txt', 'w') as fid_h:
        for idx, h_list in enumerate(loc_h):
            fid_h.write('10\n')
            fid_h.write(','.join(map(str, h_list)) + '\n' if idx < len(loc_h) - 1 else ','.join(map(str, h_list)))

    print(f'Results saved in location_C.txt and location_H.txt.')

    # 复制 location_H.txt
    shutil.copy('location_H.txt', 'location_H01.txt')
    shutil.copy('location_H.txt', 'location_H02.txt')
    shutil.copy('location_H.txt', 'location_H03.txt')

    # 添加内容到文件开头
    content_to_add_start = """11
7
y
6
H
7
2
-1.0784,31.8723
"""

    with open('location_H02.txt', 'r') as loc_h_file:
        loc_h_content = loc_h_file.read()

    with open('location_H02.txt', 'w') as loc_h_file:
        loc_h_file.write(content_to_add_start + loc_h_content)

    print('Content added to the beginning of location_H02.txt.')

    # 添加内容到文件末尾
    content_to_add_end = """
-2
-10
q
"""

    with open('location_H02.txt', 'a') as loc_h_file:
        loc_h_file.write(content_to_add_end)

    print('Content added to the end of location_H02.txt.')

    # 添加内容到文件开头
    content_to_add_start = """11
7
y
6
H
7
2
-1.0936,31.8018
"""

    with open('location_H03.txt', 'r') as loc_h_file:
        loc_h_content = loc_h_file.read()

    with open('location_H03.txt', 'w') as loc_h_file:
        loc_h_file.write(content_to_add_start + loc_h_content)

    print('Content added to the beginning of location_H03.txt.')

    # 添加内容到文件末尾
    content_to_add_end = """
-2
-10
q
"""

    with open('location_H03.txt', 'a') as loc_h_file:
        loc_h_file.write(content_to_add_end)

    print('Content added to the end of location_H03.txt.')

    # 添加内容到文件开头
    content_to_add_start = """11
7
y
6
H
7
2
-1.0157,32.2109
"""

    with open('location_H01.txt', 'r') as loc_h_file:
        loc_h_content = loc_h_file.read()

    with open('location_H01.txt', 'w') as loc_h_file:
        loc_h_file.write(content_to_add_start + loc_h_content)

    print('Content added to the beginning of location_H01.txt.')

    # 添加内容到文件末尾
    content_to_add_end = """
-2
-10
q
"""

    with open('location_H01.txt', 'a') as loc_h_file:
        loc_h_file.write(content_to_add_end)

    print('Content added to the end of location_H01.txt.')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python my_script.py <filename_pattern>")
        sys.exit(1)

    filename_pattern = sys.argv[1]
    file_list = glob.glob(filename_pattern)

    if not file_list:
        print(f"No files found matching pattern: {filename_pattern}")
        sys.exit(1)

    for filename in file_list:
        process_file(filename)

import os

# 要删除的文件列表
files_to_delete = ['location_H.txt', 'location_C.txt']

# 删除文件
for file_to_delete in files_to_delete:
    try:
        os.remove(file_to_delete)
        print(f"{file_to_delete} 已成功删除")
    except FileNotFoundError:
        print(f"{file_to_delete} 不存在")
    except Exception as e:
        print(f"删除 {file_to_delete} 时发生错误: {e}")


