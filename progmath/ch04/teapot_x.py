from transforms import *
from math import *

def load_triangles():
    with open('teapot.off') as mf:
        lines = mf.readlines()

    vertex_count, face_count, edge_count = map(int, lines[1].split())
    vertex_start = 2
    face_start = vertex_start + vertex_count
    vertexs = []
    for i in range(vertex_start, face_start):
        v = tuple(map(float, lines[i].split()))
        vertexs.append(scale_by(2)(rotate_x_by(-pi/2)(translate_by((-0.5,0,-0.6))(v))))
    triangles = []
    for i in range(face_start, face_start+face_count):
        line = lines[i].split()
        if line[0] == '4':
            ecount, idx0, idx1, idx2, idx3 = map(int, line)
            triangles.append(list((vertexs[idx0], vertexs[idx1], vertexs[idx2])))
            triangles.append(list((vertexs[idx2], vertexs[idx3], vertexs[idx0])))
        elif line[0] == '3':
            triangles.append(list((vertexs[idx0], vertexs[idx1], vertexs[idx2])))
        else:
            print("error load file")
    
    return(triangles)
    
