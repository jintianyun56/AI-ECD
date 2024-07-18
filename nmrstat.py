#!/usr/local/python37/bin/python3.7
# evaluate the averaged NMR chemical shifts
import os
import numpy as np
import pandas as pd
from glob import glob

def main():
    exp_files = glob('*_exp.txt')
    nmr_files = glob('*_avNMR.txt')

    if not exp_files or not nmr_files:
        print("Error: No matching files found.")
        sys.exit(1)

    for exp_file, nmr_file in zip(exp_files, nmr_files):
        fname1 = "t1.txt"
        fname2 = exp_file
        fname3 = "cal.txt"

        os.system(f"cp {nmr_file} {fname1}")
        os.system(f"sed -i '/Atom/d' {fname1}")
        os.system(f"awk -e '{{print $4}}' {fname1} > {fname3}")
        os.system(f"awk -e '{{print $1}}' {fname2} > {fname1}")
        os.system(f"mv {fname1} {fname2}")

        calnmr = pd.read_table(fname3, sep=",", header=None)
        expnmr = pd.read_table(fname2, sep=" ", header=None)
        cal = calnmr[0]
        exp = expnmr[0]
        nc = cal.shape[0]
        sortedcal = np.zeros(nc)

        for i in range(nc):
            sortedcal[i] = cal[i]

        scal = np.sort(sortedcal)
        sexp = np.sort(exp)
        deln = scal - sexp
        max1 = max(abs(deln))
        mad1 = np.mean(abs(deln))
        # unbiased std
        sd1 = np.std(deln, ddof=1)
        rmsd1 = np.sqrt(np.dot(deln, deln) / nc)
        # evaluate CMAD
        # ======
        linfit = np.polyfit(scal, sexp, 1)
        ccal = np.polyval(linfit, scal)
        cdeln = ccal - sexp
        cmad1 = np.mean(abs(cdeln))
        cmax1 = max(abs(cdeln))
        csd1 = np.std(cdeln, ddof=1)
        crmsd1 = np.sqrt(np.dot(cdeln, cdeln) / nc)
        # ======
        nx = np.zeros(4)
        nx = [sd1, mad1, max1, rmsd1]
        ncoef = [-1.8739405, -0.5968392, -0.0357457, -0.0381648]
        rslope = 7.28865101
        dis = np.dot(ncoef, nx) + rslope
        # os.system("rm "+fname1)
        os.system(f"rm {fname3}")

        print(f'   SD: {sd1:8.4f}\n  MAD: {mad1:8.4f}\n  MAX: {max1:8.4f}\n RMSD: {rmsd1:8.4f}')
        print(f'  CSD: {csd1:8.4f}\n CMAD: {cmad1:8.4f}\n CMAX: {cmax1:8.4f}\nCRMSD: {crmsd1:8.4f}')
        if dis > 0.0:
            print("==============================================")
            print(" This structure is likely correctly assigned!")
            print(f" '{nmr_file}' ")
            print(f'        Decision value: {dis:7.3f}     ')
            print("==============================================")
        else:
            print("======================================")
            print("   \033[1;31;40m Warning!!! incorrect structure!\033[0m")
            print(f" '{nmr_file}' ")
            print(f'       Decision value: {dis:7.3f}     ')
            print("======================================")

if __name__ == "__main__":
    main()
