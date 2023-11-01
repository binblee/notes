def load_model(model_file_name):
    with open(model_file_name) as mf:
        lines = mf.readlines()

    vertex_count, face_count, edge_count = map(int, lines[1].split())
    print(vertex_count, face_count, edge_count)
    vertex_start = 2
    face_start = vertex_start + vertex_count
    vertexs = []
    for i in range(vertex_start, face_start):
        vx, vy, vz = map(float, lines[i].split())
        vertexs.append((vx, vy, vz))
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
    
