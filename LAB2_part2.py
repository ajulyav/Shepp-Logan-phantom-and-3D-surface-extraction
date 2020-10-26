import numpy as np
import os
import argparse
import sys

#file = open("C:/Users/ajuly/OneDrive/Desktop/shepplogan.pgm3d", "r")
#contents =file.readlines()


#INIT SOME VARIABLES
vertices = []

listVertices = []
listFaces = []
SeenLabels = []
Colors = []
   
dctV = {}
dctF = {}
dctFaces = {}

def CheckNeighbors(X,Y,Z):
    
    final_array = np.zeros((Y,X,Z))
    rangeStart = 3
    rangeEnd = rangeStart+Y
    
    
    for i in range(X):
        for z in range(Z):
            final_array[i,:,z] = contents[rangeStart:rangeEnd:1]
            rangeStart += Y
            rangeEnd += Y
            
            
    keysDict = np.unique(final_array) 
    numberLabels = len(keysDict)
    
    for i in range(numberLabels):
        dctV['%s' % keysDict[i]] = []    
        dctF['%s' % keysDict[i]] = []    
        dctFaces['%s' % keysDict[i]] = []     
        
        
            
    for k in range(Z-1):
        for i in range(Y-1):
            for j in range(X-1):
    
                label = final_array[i,j,k]
                if label not in SeenLabels:
                    SeenLabels.append(label)
                    newColor = np.random.random_integers(0,255, size=(1,3))
                    Colors.append(newColor)
                
                if final_array[i,j,k] != final_array[i,j+1,k]:
                    vert1 = [i+0.5,j+0.5,k+0.5]
                    vert2 = [i+0.5,j+0.5,k-0.5]
                    vert3 = [i-0.5,j+0.5,k-0.5]
                    vert4 = [i-0.5,j+0.5,k+0.5]
                    check_and_append(final_array[i,j,k], vert1, vert2, vert3, vert4)    
                    
                if final_array[i,j,k] != final_array[i+1,j,k]:   
                    vert1 = [i+0.5,j-0.5,k-0.5]
                    vert2 = [i+0.5,j+0.5,k-0.5]
                    vert3 = [i+0.5,j+0.5,k+0.5]
                    vert4 = [i+0.5,j-0.5,k+0.5]
                    check_and_append(final_array[i,j,k], vert1, vert2, vert3, vert4) 
                
                if final_array[i,j,k] != final_array[i,j,k+1]:
                    vert1 = [i+0.5,j-0.5,k+0.5]
                    vert2 = [i+0.5,j+0.5,k+0.5]
                    vert3 = [i-0.5,j+0.5,k+0.5]
                    vert4 = [i-0.5,j-0.5,k+0.5]
                    check_and_append(final_array[i,j,k], vert1, vert2, vert3, vert4)         
            

def check_and_append(label_val, vert1, vert2, vert3, vert4):
    
    faces = []
    
    for key in dctV:
        if str(label_val) == key:
            lst = vert1  
            dctV[key].append(lst)
            lst = vert2  
            dctV[key].append(lst)
            lst = vert3
            dctV[key].append(lst)
            lst = vert4
            dctV[key].append(lst)
            IndexVal = len(dctV[key])
            faces = [IndexVal-3,IndexVal-2,IndexVal-1,IndexVal]
            lst = np.array(faces)[[0,1,2]]
            dctFaces[key].append(lst)
            lst = np.array(faces)[[2,3,0]]
            dctFaces[key].append(lst)
            lst = np.array(faces)[[2,1,0]]
            dctFaces[key].append(lst)
            lst = np.array(faces)[[0,3,2]]
            dctFaces[key].append(lst)
        

def CreateFile():
    
    filename = "MTLFile"
    
    file = filename + '.mtl'
    var1 = 1

    with open(file, 'w') as fp:
        for color in Colors:
            fp.write('newmtl Color%s' % var1)
            fp.write('\n')
            temp1 = color[0]
            fp.write('    Kd ' + str(temp1[0])+ " " + str(temp1[1]) + " " + str(temp1[2]))
            fp.write('\n')
            var1 += 1
            
            
    name_of_file = 1
    for label in SeenLabels:
        key = str(label)
        with open("{}label".format(name_of_file) + '.obj', "w") as f:
            f.write('mtllib MTLFile.mtl \n')
            f.write('usemtl Color%s \n' % name_of_file)
        
            f.write('#List of all vertices \n')
            f.write('\n')
            name_of_file+=1 
        
            
            listIterate = dctV[key] 
            for vertex in listIterate:
                f.write('v' + ' ' + str(vertex[0]) + ' ' + str(vertex[1]) + ' ' + str(vertex[2]) + '\n')
                f.write('\n')
                  
                
            f.write('#List of all faces \n')
            f.write('\n')
        
            listIterateFaces = dctFaces[key]     
            for face in listIterateFaces:
                f.write('f' + ' ' + str(face[0]) + ' ' + str(face[1]) + ' ' + str(face[2]) + '\n')
                f.write('\n')             
        
#print('done')          
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Read PGM3 file and number of labels')
    parser.add_argument('File', help='input filename')
    parser.add_argument('numLabels', help='input number of labels', type=int)

    args = parser.parse_args()
    
    
    try:
      file = open(args.File, "r")
      name, extension = os.path.splitext(args.File)
    except IOError:
      print ("Error: File does not appear to exist.")
      sys.exit(1)
  
    if extension != '.pgm3d': 
        print ("Wrong File Format! Should be PGM3D")
        sys.exit(1)
      
    #file = open(args.File, "r")
    contents = file.readlines()
    numberLabels = args.numLabels
    
    format_file = contents[0]
    sizes_imageSTR = contents[1]
    max_value = int(contents[2])

    XYZValues = sizes_imageSTR.split(" ")
    X = int(XYZValues[0])
    Y = int(XYZValues[1])
    Z = int(XYZValues[2])
    
    CheckNeighbors(X,Y,Z)
    CreateFile()
    
    print('Done')