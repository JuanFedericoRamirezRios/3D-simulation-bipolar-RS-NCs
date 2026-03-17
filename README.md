
##### Compile: 
```bash
pyinstaller --onefile --add-binary "CalcsCpp.dll;." 3D_RRAM_NCs_DCmode.py
```
# 3D-simulation-bipolar-RS-NCs
3D simulation of Resistive switching memory of oxides with conductive-nanocrystals embedded. The simulation emulates the DC voltage stimulus (voltage sweep). If you use this software, cite: https://doi.org/10.3390/chips4010011

## The simulation model
The simulation model is explained in [3D-simulation-model](https://doi.org/10.3390/chips4010011).

## Simulation conditions
The simulation conditions can be specified in the initValues.txt before running **3D_RRAM_NCs_DCmode** or selected via the graphical user interface (GUI). A description of each feature is defined in [3D-simulation-model](https://doi.org/10.3390/chips4010011).

## GUI
The graphical user interface to change the values of simulation is:

<img src="AttachmentsREADME/GUI.png" alt="GUI" width="800"/>

### Where:
#### 1st row of GUI:
- $N_{LRS}$: Conductive state ($N_S$), *NOT CONDUCTIVITY*, at Low Resistive State (LRS).
- $N_{HRS}$: $N_S$ at High Resistive State (HRS).
- $N_{FS}$: $N_S$ at Fresh State (FS).
- $V_{FORMING}$: Voltage needed for the FORMING.
- $V_{RESET}$: Voltage that achieve the RESET.
- $V_{SET}$: Voltage where the SET occurs.
- $K_{LRS}-$: Enhancement factor for LRS at Vnegative.
- $K_{LRS}+$: Enhancement factor for LRS at Vpositive.

#### 2nd row of GUI:
- $\gamma_{SET}$: Enhancement coefficient of generation probability during SET and FORMING.
- $\gamma_{RESET}$: Enhancement coefficient of generation probability during RESET.
- $\varphi_{drift}$: Enhancement coefficient for the drift of $O_{ion}$.
- $I_{compliance}$ during the FORMING process.
- $I_{compliance}$ during the RESET process.
- $I_{compliance}$ during the SET process.
- $K_{HRS}-$: Enhancement factor for HRS at Vnegative.
- $K_{HRS}+$: Enhancement factor for HRS at Vpositive.

#### 3rd row of GUI:
- $V_{Oinit}$: Initial number of oxygen vacancies ($V_O$).
- $t_{init}$: Time to generate or recombine $V_O$.
- $E_{Oe}M$: Migration barrier for oxygen ion ($O_{ion}$) from equilibrium in the oxide matrix.
- $E_{Om}$: Migration barrier for $O_{ion}$ during their migration.
- $L_O$: Decaying length of the $O_{ion}$ concentration.
- $\beta_R$: Coefficient for the recombination.
- $Rth$: Thermal resistance of (conductive filaments) CFs.
- $a_0$: Attenuation length of the electron wave function.
#### 4th row of GUI:
- $a$: Mesh size.
- $A$: Device area.
- $E_{Oe}I$: Migration barrier for oxygen ion ($O_{ion}$) from equilibrium in the interface oxide/nanocrystals.
- Number of sweep cycles ($0 V \to (V_{FORMING}\text{ or }V_{SET}) \to 0 V \to V_{RESET} \to 0 V$).
- $\varepsilon$: Relative electrical permittivity.
- $\phi_{LRS}$: Potential of the trap levels for charge conductivity at LRS.
- $\phi_{HRS}$: Potential of the trap levels for charge conductivity at HRS.

- Experiment: Name of OPTIONAL plain text file with the experimental $I-V$ results to compare with $I-V$ simulated. The format must be:

&emsp;1st line: V (V)`tab`I (A)

&emsp;2nd line: 1st voltage`tab`1st current

&emsp;3rd line: 2nd voltage`tab`2nd current

&emsp; &emsp; &emsp; &emsp; &emsp; ...

- Structure: Name of plain text file with nanocrystals configuration. With:

&emsp;0 → Not $V_O$.

&emsp;1 → $V_O$.

&emsp;2 → Fixed $V_O$, these are the nanocrystals.

Examples in the files: [3D_1NC_structure.txt](3D_1NC_structure.txt) and [3D_woNC_structure.txt](3D_woNC_structure.txt).
I recommend using my repository: https://github.com/JuanFedericoRamirezRios/Generate-3D-Nanocrystals-configurations
- Out file: Name of out data simulation results (**WARNING**: If this exists, it will be replaced).
- Seed: Seed of the random number generator. It is ranlux24 engine.
- SIMULATE button: Simulate the cycles and show the simulation results of $N_S-V$ and $I-V$, if the *Experiment* file exists, it is include in the $I-V$ graph. Additional, it generates or replaces the *Out file* with the results of simulation.
- SIMULATE + SAVE Vos button: It action, simulate and creates the folder *configurations* (**WARNING**: If this exists, it will be replaced) with the plain text files of each 3D $V_O$ configuration during the simulation. This files can open by [ifrit-setup-win64.rar](ifrit-setup-win64.rar). Additional, it generates or replaces the *Out file* with the results of simulation.


