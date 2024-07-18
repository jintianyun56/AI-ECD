**AI ECD: One-Click Calculation of Complex Natural Product NMR and ECD**

**Introduction**

Complex natural products often require NMR and ECD calculations. Due to the limited quantum chemistry computing skills among many natural product professionals, these calculations can be quite challenging. To facilitate these computations and minimize operational steps, I designed a script with the help of ChatGPT that allows one-click NMR and ECD calculations for complex natural products. After numerous modifications and tests, this script can now automatically process calculation results, directly providing NMR and ECD outcomes upon completion. I am sharing this with fellow researchers and welcome your feedback and corrections.

For the installation of the script and its associated software and hardware, please refer to "Rocky Linux 9.3 System Installation and Gromacs, Gaussian, xtb, ORCA, SVM, and other programs installation."
Molclus Program: "Using Molclus for Cluster Configuration and Molecular Conformation Search"
Molclus PBS Job Submission Script: "Molclus PBS Job Submission Script"
SVM-M Complex Natural Product NMR Calculation: [GitHub Link](https://github.com/Anan-Wu-XMU/SVM-M)
ChatGPT: [ChatGPT Link](https://chat.openai.com/)

The script and associated input files are modified and created based on previous work. If you use this script for scientific research and publish your findings, proper citation would be greatly appreciated!

### 1. Introduction to the Molclus Lazy Script

The compressed file attached contains a 00autorunall.sh file, which is a simple combination of shell commands. Based on personal research needs and using ChatGPT, I input specific requirements to generate the necessary shell commands. By combining different command demands, this script was created. For a video guide, please visit "ChatGPT-Assisted Generation of Molclus Lazy Script: One-Click Calculation of Complex Natural Product NMR and ECD."

### 2. Script Dependencies

The script relies on programs such as Molclus 1.12, xtb -191025 and crest, Gaussian 16 A03, ORCA 5.04, Shermo 2.4, Multiwfn 3.8 (dev), etc. Ensure these programs are available on the server before running the script. Installation and usage references can be found in the relevant blogs by Sobereva:

- Molclus installation and usage: "Using Molclus for Cluster Configuration and Molecular Conformation Search"
- xtb installation: "Using Gaussian with Grimme's xtb for Transition State Search, IRC Generation, and Vibration Analysis"
- Gaussian installation: "Gaussian Installation Methods and Related Issues"
- ORCA installation: "Quantum Chemistry Program ORCA Installation Method"
- Shermo installation: "Using Shermo with Quantum Chemistry Programs for Thermodynamic Data Calculation"
- Multiwfn installation: "Multiwfn Installation Guide in Linux"

For Python, install the following libraries:
```sh
python -m pip install numpy pandas xlsxwriter Workbook glob openpyxl
```

Ensure these programs are in the system environment path for easy execution. After preparation, run the script (00autorunall.sh), which is a combination of simple shell commands, functioning in both CentOS 7.6 and CentOS Stream 9.

### 3. Initial Setup

After ensuring the dependent programs are operational:
- Unzip the package and grant execution permissions:
  ```sh
  unzip molclus112.zip
  cd molclus112
  chmod +x *
  ```
- Provide input files in the unzipped directory; missing input files will prompt an error message ("coord file does not exist"). Input files should include multiple conformations ("*_traj.xyz") and a single conformation ("*_traj2.xyz").
- Modify paths in 00autorunall.sh (lines 27, 37) for the xtb program crest and in 05_set.ini (line 15) for ORCA as per your system's setup.
- The script records execution time and sends an email notification upon completion. Set up mail functionality in your system and replace the email in the script with your own.
- Start the script with:
  ```sh
  ./00autorunall.sh
  ```
  For background execution:
  ```sh
  nohup ./00autorunall.sh &> output.txt &
  ```

For NMR results only, run:
```sh
./01_mol_nmr.sh
```
or for background execution:
```sh
nohup ./01_mol_nmr.sh &
```

### 4. Script Calculation Workflow

The script divides the calculation workflow into ten steps for management:

1. **Conformation Search**: Generate traj.xyz files using Gentor, Spartan, XTB, Gromacs, etc. Replace example traj.xyz files in the package with your own. Recommended to use Gromacs for conformation search due to its speed and ease of use.
   
2. **XTB Quick Optimization**: Sort initial conformations by energy for further Gaussian optimization. Modify crest path for first-time use.

3. **Gaussian Optimization**: Optimize the lowest energy conformations. Adjust parameters in 03_set.ini as needed.

4. **Vibration Analysis**: Perform vibration analysis to exclude structures with imaginary frequencies.

5. **ORCA Single Point Energy Calculation**: Use higher-level basis sets and functionals.

6. **NMR Calculation**: Calculate NMR for all conformations using three sets of basis sets and functionals.

7. **ECD Calculation**: Calculate ECD for the top 5 conformations using three sets of basis sets and functionals.

8. **Shermo Boltzmann Proportions**: Generate Boltzmann proportions for the top 15 and top 5 conformations.

9. **Multiwfn NMR Results**: Generate weighted NMR results using Multiwfn.

10. **Multiwfn ECD Results**: Generate weighted ECD results using Multiwfn.

An additional script, 01.sh, allows running each step separately for testing.

### 5. Notes

- For the detailed meaning of each command in 00autorunall.sh, consult ChatGPT and make necessary adjustments.
- Python script 09_H_nmrstat.py extracts methyl hydrogen numbers for NMR calculations. Modify the first line with your system's Python path.
- The script supports multiple conformations in a loop; ensure appropriate input files (e.g., 5112R3R4S_traj.xyz and 5112R3R4S_traj2.xyz).
- Adjust the number of conformations for NMR calculations based on computational resources.
- Use dp4.py to extract final NMR results into Excel.
- Use nmrstat.py and 004_motosvm.sh to compare calculated NMR data with experimental results.
- Example of a successful calculation: [Baidu Link](https://pan.baidu.com/s/18mwUEOtLENnRKP-YttBJVQ?pwd=qcl0) (Password: qcl0)

### Acknowledgments

Thanks to Dr. Cui from the First Institute of Oceanography, CAS, for the 09_H_nmrstat.py script and to all others who have contributed. If this script aids your research, proper citation is appreciated.

Thank you for your feedback and suggestions!
