"""
 * Python 3.11

 * 3D simulation bipolar Resistive Switching. We assume NCs like fixed oxigen vacancies.

 * If you use this software please cite: https://doi.org/10.3390/chips4010011

 * Compile: pyinstaller --onefile --add-binary "CalcsCpp.dll;." 2D_RRAM_NCs_DCmode.py

 * GPL-3.0 license
"""

import tkinter as tk
import pandas as pd
import NumericControlsFede as NC
import os
import glob
import matplotlib.pyplot as ppt
import PythonUtilitiesFede as pu
import matplotlib.colors
import numpy as np
import ctypes

class MAIN_FRAME(tk.Tk):
    def __init__(s):
        super().__init__()
        s.title("2D_Simulation_RRAM_BIPOLAR") 
        s.geometry(f"{1500}x{580}")
        s.protocol("WM_DELETE_WINDOW", s.CloseProgram)

        s.SetSharedLib()

        print("")

        s.minIview = 1e-18 # Amp

        valuesInitPath = "initValues.txt"

        s.SetDefectVals()

        s.ReadInitValues(valuesInitPath, 34)

        # s.PrintValues()
        s.CreateGUI()
    
    def SetSharedLib(s):
        path = os.path.dirname(os.path.realpath(__file__))
        handle = ctypes.CDLL(path + "/CalcsCpp.dll", winmode=0) # winmode=0: Use unicode.

        s.InitSimulator = handle.InitSimulator
        s.InitSimulator.argtypes = [ctypes.c_char_p, ctypes.c_bool] # c_char_p: c_char pointer

        s.SetContProc = handle.SetContProc
        s.SetContProc.argtypes = [ctypes.c_int]
        
        s.Forming = handle.Forming
        s.Forming.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]

        s.SetProcess = handle.SetProcess
        s.SetProcess.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]

        s.ResetProcess = handle.ResetProcess
        s.ResetProcess.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]

        s.SweepProcess = handle.SweepProcess
        s.SweepProcess.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]

        

        s.FreeSimulatorMemory = handle.FreeSimulatorMemory

    def SetDefectVals(s):
        s.textExp = tk.StringVar(); s.textExp.set("Zs11_expe_01_cycle.dat")
        s.textStructure = tk.StringVar(); s.textStructure.set("Zs11_3D_structure.txt")
        s.textOutput = tk.StringVar(); s.textOutput.set("outFileZs11_00_RESET.dat")
        s.seed = [3]

        s.N_LRS = [6.0]    # u.a. # self: N_LRS is a list of the class MAIN_FRAME
        s.N_HRS = [-20.0]   # u.a.
        s.Nfresh = [-56.0]  # u.a.
        s.Vforming = [20.0] # V
        s.Vreset = [-20.0]   # V
        s.Vset = [20.0]      # V
        s.Khrs = [8.0e-16]  # u.a.
        s.Klrs = [7.0e-27]  # u.a. * cm3

        s.gammaSET = [3.0]
        s.gammaRESET = [0.4]
        s.phiDrift = [8.0]
        s.complIforming = [0.01] # Amp
        s.complIreset = [0.01]   # Amp
        s.complIset = [0.01]   # Amp
        s.a = [0.325E-7]           # cm
        s.A = [10.0E-3]            # cm2

        s.numVoIni = [0]
        s.stepTime0 = [5.0E-6] # sec
        s.EoeMatrix = [1.0]          # eV
        s.EoeInter = [4.5]
        s.Eom = [1.0]          # eV
        s.Lo = [5.4]           # const. lattice a: [Lo] = a.
        s.beta0 = [6.0E6]
        s.Rth = [8.0e6]  # K/W
        s.Ao = [0.33E-7] # cm

        s.cycles = [1]
        s.Nc = [2.94E18] # 1/cm3  For ZnO: 2.94e18 <- Park 2020: Electrical Defect State Distribution in Single Crystal ZnO Schottky Barrier Diodes
        s.u = [200.0]   # cm2/(V sec)
        s.epsilon = [8.5]
        s.phit = [0.1] # V
        # self.Easclc = [0.1] # eV . Ea = phit.

    def ReadInitValues(s, filePath, numParams) -> None:
        params = pu.LoadParams(filePath)
        if params == None:
            return
        if len(params) != numParams:
            print(f"Warning: The number of params in {filePath} is not {numParams}. Values by defect.")
            return
        s.PassInitValues(params)

    def PassInitValues(s, p):
        try:
            s.textExp.set(p[0])
            s.textStructure.set(p[1])
            s.textOutput.set(p[2])
            s.seed[0] = int(p[3])
            if s.seed[0] < 1: 
                print("Warning: seed must be > 0, now seed = 1")
                s.seed[0] = 1

            s.N_LRS[0] = float(p[4])
            s.N_HRS[0] = float(p[5])
            s.Nfresh[0] = float(p[6])
            s.Vforming[0] = float(p[7])
            s.Vreset[0] = float(p[8])
            s.Vset[0] = float(p[9])
            s.Khrs[0] = float(p[10])
            s.Klrs[0] = float(p[11])

            s.gammaSET[0] = float(p[12])
            s.gammaRESET[0] = float(p[13])
            s.phiDrift[0] = float(p[14])
            s.complIforming[0] = float(p[15])
            s.complIreset[0] = float(p[16])
            s.complIset[0] = float(p[17])
            s.a[0] = float(p[18])
            s.A[0] = float(p[19])

            s.numVoIni[0] = int(p[20])
            s.stepTime0[0] = float(p[21])
            s.EoeMatrix[0] = float(p[22])
            s.EoeInter[0] = float(p[23])
            s.Eom[0] = float(p[24])
            s.Lo[0] = float(p[25])
            s.beta0[0] = float(p[26])
            s.Rth[0] = float(p[27])
            s.Ao[0] = float(p[28])

            s.cycles[0] = int(p[29])
            s.Nc[0] = float(p[30])
            s.u[0] = float(p[31])
            s.epsilon[0] = float(p[32])
            s.phit[0] = float(p[33])
            
        except ValueError as e:
            print("Error:", e)
    
    def PrintValues(s):
        print(
            "textExp =", s.textExp.get(), "\n",
            "textStructure =", s.textStructure.get(), "\n",
            "textOutput =", s.textOutput.get(), "\n",
            "seed =", s.seed[0], "\n",

            "N_LRS =", s.N_LRS[0], "\n",
            "N_HRS =", s.N_HRS[0], "\n",
            "Nfresh =", s.Nfresh[0], "\n",
            "Vforming =", s.Vforming[0], "\n",
            "Vreset =", s.Vreset[0], "\n",
            "Vset =", s.Vset[0], "\n",
            "Khrs =", s.Khrs[0], "\n",
            "Klrs =", s.Klrs[0], "\n",

            "gammaSET =", s.gammaSET[0], "\n",
            "gammaRESET =", s.gammaRESET[0], "\n",
            "phiDrift =", s.phiDrift[0], "\n",
            "complIforming =", s.complIforming[0], "\n",
            "complIreset =", s.complIreset[0], "\n",
            "complIset =", s.complIset[0], "\n",
            "a =", s.a[0], "\n",
            "A =", s.A[0], "\n",

            "numVoIni =", s.numVoIni[0], "\n",
            "stepTime0 =", s.stepTime0[0], "\n",
            "EoeMatrix =", s.EoeMatrix[0], "\n",
            "EoeInter =", s.EoeInter[0], "\n",
            "Eom =", s.Eom[0], "\n",
            "Lo =", s.Lo[0], "\n",
            "beta0 =", s.beta0[0], "\n",
            "Rth =", s.Rth[0], "\n",
            "Ao =", s.Ao[0], "\n",

            "cycles =", s.cycles[0], "\n",
            "Nc =", s.Nc[0], "\n",
            "u =", s.u[0], "\n",
            "epsilon =", s.epsilon[0], "\n",
            "phit =", s.phit[0], "\n"
        )

    def CreateGUI(s):
        for n in range(8): # from 0 to 7
            s.columnconfigure(n, weight = 1)
        for n in range(4):
            s.rowconfigure(n, weight = 1)

        N_LRSControls = NC.CONTROLS_VALUE(master = s, name = "N_LRS", units = "au", value = s.N_LRS)
        N_LRSControls.grid(column = 0, row = 0, sticky = "nsew") # nsew: north, south, east y west.

        N_HRSControls = NC.CONTROLS_VALUE(master = s, name = "N_HRS", units = "au", value = s.N_HRS)
        N_HRSControls.grid(column = 1, row = 0, sticky = "nsew")

        NfreshControls = NC.CONTROLS_VALUE(master = s, name = "Nfresh", units = "au", value = s.Nfresh)
        NfreshControls.grid(column = 2, row = 0, sticky = "nsew")

        VformingControls = NC.CONTROLS_VALUE(master = s, name = "Vforming", units = "V", value = s.Vforming)
        VformingControls.grid(column = 3, row = 0, sticky = "nsew")

        VresetControls = NC.CONTROLS_VALUE(master = s, name = "Vreset", units = "V", value = s.Vreset)
        VresetControls.grid(column = 4, row = 0, sticky = "nsew")

        VsetControls = NC.CONTROLS_VALUE(master = s, name = "Vreset", units = "V", value = s.Vset)
        VsetControls.grid(column = 5, row = 0, sticky = "nsew")

        KhrsControls = NC.CONTROLS_SCIENTIFIC(master = s, name = "K_HRS", units = "au", value = s.Khrs)
        KhrsControls.grid(column = 6, row = 0, sticky = "nsew")

        KlrsControls = NC.CONTROLS_SCIENTIFIC(master = s, name = "K_LRS", units = "au-cm3", value = s.Klrs)
        KlrsControls.grid(column = 7, row = 0, sticky = "nsew")

        ########################

        # hframe2 = tk.Frame(s)
        # hframe2.pack(fill = "both", expand = True)

        gammaSETcontrols = NC.CONTROLS_VALUE(master = s, name = "gamSET", units = "", value = s.gammaSET)
        gammaSETcontrols.grid(column = 0, row = 1, sticky = "nsew")

        gammaRESETcontrols = NC.CONTROLS_VALUE(master = s, name = "gamRESET", units = "", value = s.gammaRESET)
        gammaRESETcontrols.grid(column = 1, row = 1, sticky = "nsew")

        phiDriftControls = NC.CONTROLS_VALUE(master = s, name = "phiDrift", units = "", value = s.phiDrift)
        phiDriftControls.grid(column = 2, row = 1, sticky = "nsew")

        complIformingControls = NC.CONTROLS_SCIENTIFIC(master = s, name = "IcomplForming", units = "A", value = s.complIforming)
        complIformingControls.grid(column = 3, row = 1, sticky = "nsew")

        complIresetControls = NC.CONTROLS_SCIENTIFIC(master = s, name = "IcomplReset", units = "A", value = s.complIreset)
        complIresetControls.grid(column = 4, row = 1, sticky = "nsew")

        complIsetControls = NC.CONTROLS_SCIENTIFIC(master = s, name = "IcomplSet", units = "A", value = s.complIset)
        complIsetControls.grid(column = 5, row = 1, sticky = "nsew")

        aControls = NC.CONTROLS_VALUE(master = s, name = "a", units = "cm", value = s.a)
        aControls.grid(column = 6, row = 1, sticky = "nsew")

        Acontrols = NC.CONTROLS_SCIENTIFIC(master = s, name = "A", units = "cm2", value = s.A)
        Acontrols.grid(column = 7, row = 1, sticky = "nsew")

        ########################

        # hframe3 = tk.Frame(s)
        # hframe3.pack(fill = "both", expand = True)

        numVoIniControls = NC.CONTROLS_VALUE(master = s, name = "VoIni", units = "", value = s.numVoIni)
        numVoIniControls.grid(column = 0, row = 2, sticky = "nsew")

        stepTime0Controls = NC.CONTROLS_SCIENTIFIC(master = s, name = "t_ini", units = "s", value = s.stepTime0)
        stepTime0Controls.grid(column = 1, row = 2, sticky = "nsew")

        EoeControls = NC.CONTROLS_VALUE(master = s, name = "E_OeM", units = "eV", value = s.EoeMatrix)
        EoeControls.grid(column = 2, row = 2, sticky = "nsew")

        EomControls = NC.CONTROLS_VALUE(master = s, name = "E_Om", units = "eV", value = s.Eom)
        EomControls.grid(column = 3, row = 2, sticky = "nsew")

        LoControls = NC.CONTROLS_VALUE(master = s, name = "L_O", units = "a", value = s.Lo)
        LoControls.grid(column = 4, row = 2, sticky = "nsew")

        beta0Controls = NC.CONTROLS_SCIENTIFIC(master = s, name = "Bo", units = "", value = s.beta0)
        beta0Controls.grid(column = 5, row = 2, sticky = "nsew")
        
        RthControls = NC.CONTROLS_SCIENTIFIC(master = s, name = "Rth", units = "K/W", value = s.Rth)
        RthControls.grid(column = 6, row = 2, sticky = "nsew")

        AoControls = NC.CONTROLS_VALUE(master = s, name = "Ao", units = "cm", value = s.Ao)
        AoControls.grid(column = 7, row = 2, sticky = "nsew")

        ########################

        # hframe4 = tk.Frame(s)
        # hframe4.pack(fill = "both", expand = True)

        cyclesControls = NC.CONTROLS_VALUE(master = s, name = "cycles", units = "", value = s.cycles)
        cyclesControls.grid(column = 0, row = 3, sticky = "nsew")

        NcControls = NC.CONTROLS_SCIENTIFIC(master = s, name = "Nc", units = "/cm3", value = s.Nc)
        NcControls.grid(column = 1, row = 3, sticky = "nsew")

        uControls = NC.CONTROLS_VALUE(master = s, name = "u", units = "cm2/V-s", value = s.u)
        uControls.grid(column = 2, row = 3, sticky = "nsew")

        epsilonControls = NC.CONTROLS_VALUE(master = s, name = "perm", units = "", value = s.epsilon)
        epsilonControls.grid(column = 3, row = 3, sticky = "nsew")

        phitControls = NC.CONTROLS_VALUE(master = s, name = "phit", units = "´V", value = s.phit)
        phitControls.grid(column = 4, row = 3, sticky = "nsew")

        vFrame1 = tk.Frame(s)
        vFrame1.grid(column = 6, row = 3, sticky = "nsew")

        hFrame5 = tk.Frame(vFrame1)
        hFrame5.pack(anchor = "n", expand = True)
        expLabel = tk.Label(master = hFrame5, text = "Experiment:")
        expLabel.pack(side = "left", fill = "x", expand = True)
        expTextEntry = tk.Entry(master = hFrame5, textvariable = s.textExp) # textExp pass as reference
        expTextEntry.pack(side = "left", fill = "x", expand = True)

        hFrame6 = tk.Frame(vFrame1)
        hFrame6.pack(anchor = "c", expand = True)
        structureLabel = tk.Label(master = hFrame6, text = "Structure:")
        structureLabel.pack(side = "left", fill = "x", expand = True)
        structureTextEntry = tk.Entry(master = hFrame6, textvariable = s.textStructure)
        structureTextEntry.pack(side = "left", fill = "x", expand = True)

        hFrame7 = tk.Frame(vFrame1)
        hFrame7.pack(anchor = "s", expand = True)
        outputLabel = tk.Label(master = hFrame7, text = "Out file:")
        outputLabel.pack(side = "left", fill = "x", expand = True)
        outputTextEntry = tk.Entry(master = hFrame7, textvariable = s.textOutput)
        outputTextEntry.pack(side = "left", fill = "x", expand = True)

        vFrame2 = tk.Frame(s)
        vFrame2.grid(column = 7, row = 3, sticky = "nsew")

        hFrame8 = tk.Frame(vFrame2)
        hFrame8.pack(anchor = "s", expand = True)
        seedLabel = tk.Label(master = hFrame8, text = "Seed:")
        seedLabel.pack(side = "left", fill = "x", expand = True)
        s.textSeed = tk.StringVar()
        s.textSeed.set(s.seed[0])
        seedTextEntry = tk.Entry(master = hFrame8, textvariable = s.textSeed)
        seedTextEntry.pack(side = "left", fill = "x", expand = True)
        seedTextEntry.bind("<KeyRelease>", s.ChangeSeed)

        s.simulateButton = tk.Button(master = vFrame2, text = "SIMULATE", command = s.Simulate)
        s.simulateButton.pack(expand = True)

        s.drawButton = tk.Button(master = vFrame2, text = "SIMULATE + SAVE Vos", command = s.SimulateDraw)
        s.drawButton.pack(expand = True)
        
    def ChangeSeed(s, *args):
        try:
            newValue = int(s.textSeed.get())
        except ValueError:
            s.textSeed.set(str(s.seed[0]))
            return
        if(newValue >= 1):
            s.seed[0] = newValue
        else:
            s.seed[0] = 1
            s.textSeed.set("1")
    
    def Simulate(s, drawSim = False):
        ppt.close("Vo configs")

        s.simulateButton.config(state = "disabled")
        s.drawButton.config(state = "disabled")

        s.WriteValsOutFile()

        s.InitSimulator(s.textOutput.get().encode(), drawSim)
        s.SetContProc(0)
        s.Forming(0.0, s.Vforming[0], 0.1)
        s.SetContProc(1)
        s.ResetProcess(0.0, s.Vreset[0], -0.1)

        s.FreeSimulatorMemory()

        s.DrawData()
        print()

        s.simulateButton.config(state = "active")
        s.drawButton.config(state = "active")

    def WriteValsOutFile(s):
        if os.path.exists(s.textOutput.get()):            
            os.remove(s.textOutput.get())
        s.outFile = open(s.textOutput.get(), mode = "x") # "x" create a writable file
        s.outFile.write("Experimental data: " + s.textExp.get() + "\n")
        s.outFile.write("Structure layers: " + s.textStructure.get() + "\n")
        s.outFile.write("Seed of random number generator: " + str(s.seed[0]) + "\n")
        s.outFile.write("\n")
        s.outFile.write("N_LRS: " + str(s.N_LRS[0]) + "\n")
        s.outFile.write("N_HRS: " + str(s.N_HRS[0]) + "\n")
        s.outFile.write("Nfresh: " + str(s.Nfresh[0]) + "\n")
        s.outFile.write("Vforming: " + str(s.Vforming[0]) + " V\n")
        s.outFile.write("Vreset: " + str(s.Vreset[0]) + " V\n")
        s.outFile.write("Vset: " + str(s.Vset[0]) + " V\n")
        s.outFile.write("Khrs: " + str(s.Khrs[0]) + " a.u.\n")
        s.outFile.write("Klrs: " + str(s.Klrs[0]) + " a.u. cm3\n")
        s.outFile.write("\n")
        s.outFile.write("gammaSET for generation probb.: " + str(s.gammaSET[0]) + "\n")
        s.outFile.write("gammaRESET for generation probb.: " + str(s.gammaRESET[0]) + "\n")
        s.outFile.write("phiDrift oxygen migrat: " + str(s.phiDrift[0]) + "\n")
        s.outFile.write("I compliance FORMING: " + str(s.complIforming[0]) + " A\n")
        s.outFile.write("I compliance RESET: " + str(s.complIreset[0]) + " A\n")
        s.outFile.write("I compliance SET: " + str(s.complIset[0]) + " A\n")
        s.outFile.write("a const. lattice: " + str(s.a[0]) + " cm\n")
        s.outFile.write("A Area device: " + str(s.A[0]) + " cm2\n")
        s.outFile.write("\n")
        s.outFile.write("Vo_ini Num initial Vos: " + str(s.numVoIni[0]) + "\n")
        s.outFile.write("t_0 gener-recomb: " + str(s.stepTime0[0]) + " s\n")
        s.outFile.write("E_Oe oxygen equilib. in ox. matrix: "  + str(s.EoeMatrix[0]) + " eV\n")
        s.outFile.write("E_Oe oxygen equilib. in NCs/Ox.: "  + str(s.EoeInter[0]) + " eV\n")
        s.outFile.write("E_Om oxygen migrat.: "  + str(s.Eom[0]) + " eV\n")
        s.outFile.write("L_O decaying oxig. ion: "  + str(s.Lo[0]) + " a\n")
        s.outFile.write("beta0 recomb. factor: " + str(s.beta0[0]) + "\n")
        s.outFile.write("Rth thermal resistance: " + str(s.Rth[0]) + " K/W\n")
        s.outFile.write("Ao atten. electron wave: " + str(s.Ao[0]) + " cm\n")
        s.outFile.write("\n")
        s.outFile.write("Num cycles: " + str(s.cycles[0]) + "\n")
        s.outFile.write("Nc: " + str(s.Nc[0]) + " /cm3\n")
        s.outFile.write("u: " + str(s.u[0]) + " cm2/(V s)\n")
        s.outFile.write("perm Relative dielect. const.: " + str(s.epsilon[0]) + "\n")
        s.outFile.write("phi_t (Eg - trapVo) into Eg: " + str(s.phit[0]) + " V\n")
        s.outFile.write("\n")
        s.outFile.close()

    def SimulateDraw(s):
        s.Simulate(drawSim=True)
    
    def DrawData(s):
        return
    
    
    
    def CloseProgram(s):
        ppt.close("I Vs V")
        ppt.close("Ns Vs V") 
        ppt.close("Vo configs")
        s.destroy()

if __name__ == "__main__":
    

    App = MAIN_FRAME()
    App.mainloop()