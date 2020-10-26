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

def CheckNeighbors(X,Y,Z):
    
    final_array = np.zeros((Y,X,Z))
    rangeStart = 3
    rangeEnd = rangeStart+Y
    
    
    for i in range(X):
        for z in range(Z):
            final_array[i,:,z] = contents[rangeStart:rangeEnd:1]
            rangeStart += Y
            rangeEnd += Y
            
    for k in range(Z-1):
        for i in range(Y-1):
            for j in range(X-1):
                if final_array[i,j,k] != final_array[i,j+1,k]:
                    vert1 = [i+0.5,j+0.5,k+0.5]
                    vert2 = [i+0.5,j+0.5,k-0.5]
                    vert3 = [i-0.5,j+0.5,k-0.5]
                    vert4 = [i-0.5,j+0.5,k+0.5]
                    check_and_append(vert1, vert2, vert3, vert4)               
     
                if final_array[i,j,k] != final_array[i+1,j,k]:   
                    vert1 = [i+0.5,j-0.5,k-0.5]
                    vert2 = [i+0.5,j+0.5,k-0.5]
                    vert3 = [i+0.5,j+0.5,k+0.5]
                    vert4 = [i+0.5,j-0.5,k+0.5]
                    check_and_append(vert1, vert2, vert3, vert4) 
                
                if final_array[i,j,k] != final_array[i,j,k+1]:
                    vert1 = [i+0.5,j-0.5,k+0.5]
                    vert2 = [i+0.5,j+0.5,k+0.5]
                    vert3 = [i-0.5,j+0.5,k+0.5]
                    vert4 = [i-0.5,j-0.5,k+0.5]
                    check_and_append(vert1, vert2, vert3, vert4)             
            

def check_and_append(vert1, vert2, vert3, vert4):
    
    faces = []
    
    listVertices.append(vert1)
    listVertices.append(vert2)
    listVertices.append(vert3)
    listVertices.append(vert4)
    
    faces.append(listVertices.index(vert1)+1)
    faces.append(listVertices.index(vert2)+1)
    faces.append(listVertices.index(vert3)+1)
    faces.append(listVertices.index(vert4)+1)
    
    listFaces.append(faces[0:3:1])
    temp = np.array(faces)[[2,3,0]]
    listFaces.append(list(temp))
    temp1 = np.array(faces)[[2,1,0]]
    listFaces.append(list(temp1))
    temp2 = np.array(faces)[[0,3,2]] 
    listFaces.append(list(temp2))
        

def CreateFile():
    filename = "FigureNoColors"
    file = filename + '.obj'

    with open(file, 'w') as fp:
        fp.write('#List of all vertices \n')
        fp.write('\n')
        for vertex in listVertices:
            assert len(vertex) == 3, 'invalid vertex with %d dimensions found (%s)' % (len(vertex), file)
            fp.write('v' + ' ' + str(vertex[0]) + ' ' + str(vertex[1]) + ' ' + str(vertex[2]) + '\n')
            fp.write('\n')
            
        fp.write('#List of all faces \n')
        fp.write('\n')
        for face in listFaces:
            assert len(face) == 3, 'invalid face with %d dimensions found (%s)' % (len(face), file)
            fp.write('f' + ' ' + str(face[0]) + ' ' + str(face[1]) + ' ' + str(face[2]) + '\n')
            fp.write('\n')
        
#print('done')          
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Read PGM3 file and number of labels')
    parser.add_argument('File', help='input filename')
    parser.add_argument('numLabels', help='input number of labels', type = int)

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