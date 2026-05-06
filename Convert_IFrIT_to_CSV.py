import tkinter as tk
import numpy as np
import os
# import random as rn

class MAIN_FRAME(tk.Tk):
    def __init__(s):
        super().__init__()
        
        

        # fileNames = []
        with os.scandir() as files:
            fileNames = [n.name for n in files if n.is_file() and n.name.endswith('.txt')]
            # for n in files:
            #     fileNames.append(n.name)
        
        for n in fileNames:
            s.Generate_csv(fileName = n, withEdges = True)
            print()

    def Generate_csv(s, fileName, withEdges = False):
        voxels = []
        print("Read IFrIT file:", end = ' ')
        file = open(fileName)
        print(file.name)
        dimensions = file.readline()
        Xs = int(list(dimensions.split(" "))[0])
        Ys = int(list(dimensions.split(" "))[1])
        Zs = int(list(dimensions.split(" "))[2])
        print('Xs =', Xs, 'Ys =', Ys, 'Zs =', Zs)
        for z in range(Zs-1, -1, -1): # From Zs-1 to 0, step -1.
            for y in range(Ys):
                for x in range(Xs):
                    VoState = file.readline()
                    if not VoState: # It is the final of file
                        print('Data incomplete')
                        return
                    VoState = int(VoState)
                    if VoState == 0: # If this site is not a Vo
                        continue
                    else:
                        voxels.append([x, y, z, VoState])
        file.close()

        if(withEdges):
            # Remove edges:
            nVoxel = int(0)
            while nVoxel < len(voxels):
                if (voxels[nVoxel][0]) == 0 or (voxels[nVoxel][0] == Xs-1) or (voxels[nVoxel][1] == 0) or (voxels[nVoxel][1] == Ys-1) or (voxels[nVoxel][2] == 0) or (voxels[nVoxel][2] == Zs-1):
                    del voxels[nVoxel] # This decrement len(voxels)
                else: 
                    nVoxel = nVoxel + 1 
            for nVoxel in range(len(voxels)): # Move coordenates to 0, 0, 0
                voxels[nVoxel][0] = voxels[nVoxel][0] - 1
                voxels[nVoxel][1] = voxels[nVoxel][1] - 1
                voxels[nVoxel][2] = voxels[nVoxel][2] - 1
            print('New size after remove edges:', 'Xs =', Xs-2, 'Ys =', Ys-2, 'Zs =', Zs-2)
        
        fileName = fileName[:-4] + '.csv' # Change the extension
        print("Writing csv file:", fileName)
        np.savetxt(fileName, voxels, fmt = '%i', delimiter = ',', header="x,y,z,VoState", comments='') # fmt = '%i': Integer format. comments='' avoid '# ' in the header.

if __name__ == "__main__":
    App = MAIN_FRAME()
    App.mainloop()

