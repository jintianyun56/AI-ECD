#!/bin/bash

start_time=$(date +%s)   # 记录脚本开始时间




# 切换到当前脚本所在的目录
cd "$(dirname "$0")"

# 循环处理每个 *_traj.xyz 文件
for traj_file in *_traj.xyz; do
  # 获取不带扩展名的文件名
  base_name="${traj_file%_traj.xyz}"  
  # 检查文件是否存在
     
  if [ -e "$traj_file" ]; then
    
    
     #08制作Shermo的输入文件
  	 find . -type f -name "${base_name}_09_*.txt" -delete
     find . -type f -name "${base_name}_08_*.txt" -delete
     
     # 获取文件列表
     freq_files=(${base_name}_04_freq_gau00*.log)
     sp_files=(${base_name}_05_sp_orca00*.log)
     
     # 获取当前目录路径
     current_path=$(pwd)
     
     # 确保至少有一个文件匹配条件
     if [ ${#freq_files[@]} -gt 0 ]; then
         # 创建文件并写入数据
         for ((i = 0; i < ${#freq_files[@]}; i++)); do
             freq_file=${freq_files[$i]}
             sp_file=${sp_files[$i]}
             
             # 提取文件名和路径，写入文件
             freq_path="${current_path}/${freq_file}"
             sp_energy=$(grep "FINAL SINGLE POINT ENERGY" "$sp_file" | awk '{print $5}')
             echo "${current_path}/${freq_file};${sp_energy}" >> "${base_name}_08_sher00_input.txt"
         done
     else
         echo "没有找到 $freq_files 匹配文件"
     fi
     head -n 5 "${base_name}_08_sher00_input.txt" > "${base_name}_08_sher01_input.txt"
     head -n 5 "${base_name}_08_sher00_input.txt" > "${base_name}_08_sher02_input.txt"

     
     # 08_shermo01.sh获得NMR的比例，08_shermo02.sh获得ECD的比例                          
     Shermo "${base_name}_08_sher00_input.txt" | tee "${base_name}_08_sher00rate.txt" 
     Shermo "${base_name}_08_sher01_input.txt" | tee "${base_name}_08_sher01rate.txt" 
     Shermo "${base_name}_08_sher02_input.txt" | tee "${base_name}_08_sher02rate.txt" 
     
     grep "Boltzmann weight=" "${base_name}_08_sher01rate.txt"  | awk '{print substr($0,length($0)-7)/100}' > "${base_name}_08_ecdrate01.txt"
     grep "Boltzmann weight=" "${base_name}_08_sher02rate.txt"  | awk '{print substr($0,length($0)-7)/100}' > "${base_name}_08_ecdrate02.txt"
     grep "Boltzmann weight=" "${base_name}_08_sher01rate.txt"  | awk '{print substr($0, length($0)-7)}' > "${base_name}_08_nmrrate.txt"
     
    
     #制作Multiwfn计算NMR的输入文件
     
     
     #具体的NMR标度参数，在这个网站上有汇总：http://cheshirenmr.info
     #制作Multiwfn命令的输入文件，提取甲基氢的编号
    ./09_H_nmrstat.py "${base_name}_traj2.xyz"
    mv -f location_H01.txt "${base_name}_09_H01_nmr.txt"
    mv -f location_H02.txt "${base_name}_09_H02_nmr.txt"
    mv -f location_H03.txt "${base_name}_09_H03_nmr.txt"
 
     
     
     #制作Multiwfn读取Gaussian结果的输入文件，提取甲基氢的编号
     
     # 获取文件列表
     nmr_files=(${base_name}_06_nmr01_gau00*.log)
     
     # 获取当前目录路径
     current_path=$(pwd)
     
     # 确保至少有一个文件匹配条件
     if [ ${#nmr_files[@]} -gt 0 ]; then
         # 创建文件并写入数据
         for file in "${nmr_files[@]}"; do
             # 提取当前目录路径和文件名，组合写入文件
             echo "\"${current_path}/${file}\"" >> "${base_name}_09_nmr00_file.txt"
         done
     else
         echo "没有找到匹配文件"
     fi
     
     head -n 5 "${base_name}_08_nmrrate.txt" > "${base_name}_08_nmrrate00.txt"
     head -n 5 "${base_name}_09_nmr00_file.txt" > "${base_name}_09_nmr01_file.txt"
     
     paste "${base_name}_09_nmr01_file.txt" "${base_name}_08_nmrrate00.txt" > "${base_name}_09_nmr01_rate.txt"


     
     
     sed 's/06_nmr01_/06_nmr02_/g' "${base_name}_09_nmr01_rate.txt" > "${base_name}_09_nmr02_rate.txt"
     sed 's/06_nmr01_/06_nmr03_/g' "${base_name}_09_nmr01_rate.txt" > "${base_name}_09_nmr03_rate.txt"
     
     #Multiwfn获得三组泛函权重之后的NMR结果
     #09_nmr01_mul.sh 
     mv -f "${base_name}_09_nmr01_rate.txt" multiple.txt
     
     Multiwfn multiple.txt < "${base_name}_09_H01_nmr.txt"
     
     awk '/Weighted data:/{p=1; next} p && !/^$/{print}' "NMRdata.txt" > "${base_name}_09_HWeighted01.txt"
     mv -f NMRdata.txt "${base_name}_09_HNMRdata01.txt"
     
     
     Multiwfn multiple.txt < 09_C01_nmr.txt
     awk '/Weighted data:/{p=1; next} p && !/^$/{print}' "NMRdata.txt" > "${base_name}_09_CWeighted01.txt"
     mv -f NMRdata.txt "${base_name}_09_CNMRdata01.txt"
     
     mv -f multiple.txt "${base_name}_09_nmr01_rate.txt" 
     
     #09_nmr02_mul.sh
     mv -f "${base_name}_09_nmr02_rate.txt" multiple.txt
     
     Multiwfn multiple.txt < "${base_name}_09_H02_nmr.txt"
     awk '/Weighted data:/{p=1; next} p && !/^$/{print}' "NMRdata.txt" > "${base_name}_09_HWeighted02.txt"
     mv -f NMRdata.txt "${base_name}_09_HNMRdata02.txt"
     
     Multiwfn multiple.txt < 09_C02_nmr.txt
     awk '/Weighted data:/{p=1; next} p && !/^$/{print}' "NMRdata.txt" > "${base_name}_09_CWeighted02.txt"
     mv -f NMRdata.txt "${base_name}_09_CNMRdata02.txt"
     
     mv -f multiple.txt "${base_name}_09_nmr02_rate.txt" 
     
     #09_nmr03_mul.sh
     
     mv -f "${base_name}_09_nmr03_rate.txt"  multiple.txt
     
     Multiwfn multiple.txt < "${base_name}_09_H03_nmr.txt"
     awk '/Weighted data:/{p=1; next} p && !/^$/{print}' "NMRdata.txt" > "${base_name}_09_HWeighted03.txt"
     mv -f NMRdata.txt "${base_name}_09_HNMRdata03.txt"
     
     Multiwfn multiple.txt < 09_C03_nmr.txt
     awk '/Weighted data:/{p=1; next} p && !/^$/{print}' "NMRdata.txt" > "${base_name}_09_CWeighted03.txt"
     mv -f NMRdata.txt "${base_name}_09_CNMRdata03.txt"
     
     mv -f multiple.txt "${base_name}_09_nmr03_rate.txt" 
    
  else
     echo "文件 $traj_file 不存在。"
  fi
done

./dp4.py
./extract_en.py

# 计算脚本运行时间（以秒为单位）
end_time=$(date +%s)
runtime=$((end_time - start_time))

# 将秒数转换成小时
hours=$((runtime / 3600))
minutes=$((runtime / 60))
hostname=$(hostname)

echo "$hostname $hours 小时 $minutes 分钟 molclus+ done" | s-nail -s "$hostname $hours 小时 $minutes 分钟 molclus+ done" 944671929@qq.com




