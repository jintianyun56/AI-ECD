#!/bin/bash

# 循环处理每个文件
for ((i = 1; i <= 3; i++)); do
    # 构造文件名通配符
    cal_file="*_09_CNMRdata0${i}.txt"

    # 循环处理匹配的文件
    for file in $cal_file; do
        # 提取文件名中的编号部分
        base_name="${file%_09_CNMRdata0${i}.txt}"

        # 复制exp.txt为相应的*_exp.txt
        cp exp.txt "${base_name}0${i}_exp.txt"

        # 提取"Weighted data:"后面的所有内容到新文件中，排除包含该行的内容
        awk '/Weighted data:/{p=1; next} p && !/^$/{print}' "$file" > "${base_name}0${i}_avNMR.txt"
    done
done

./nmrstat.py | tee "${base_name}_re.txt"
