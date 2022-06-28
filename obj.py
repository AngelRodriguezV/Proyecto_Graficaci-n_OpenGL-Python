import numpy as np

# Clase para leer un archivo .obj
class OBJ:

    buffer = []

    @staticmethod
    def search_data(data_values, coordinates, skip, data_type):
        for d in data_values:
            if d == skip:
                continue
            if data_type == 'float':
                coordinates.append(float(d))
            elif data_type == 'int':
                coordinates.append(int(d)-1)


    @staticmethod 
    def create_sorted_vertex_buffer(indices_data, vertices, textures, normals, color):
        for i, ind in enumerate(indices_data):
            if i % 3 == 0: 
                start = ind * 3
                end = start + 3
                OBJ.buffer.extend(vertices[start:end])
            elif i % 3 == 1: 
                start = ind * 2
                end = start + 2
                OBJ.buffer.extend(textures[start:end])
            elif i % 3 == 2: 
                start = ind * 3
                end = start + 3
                OBJ.buffer.extend(normals[start:end])
                OBJ.buffer.extend(color)


    @staticmethod 
    def create_unsorted_vertex_buffer(indices_data, vertices, textures, normals, color):
        num_verts = len(vertices) // 3

        for i1 in range(num_verts):
            start = i1 * 3
            end = start + 3
            OBJ.buffer.extend(vertices[start:end])

            for i2, data in enumerate(indices_data):
                if i2 % 3 == 0 and data == i1:
                    start = indices_data[i2 + 1] * 2
                    end = start + 2
                    OBJ.buffer.extend(textures[start:end])

                    start = indices_data[i2 + 2] * 3
                    end = start + 3
                    OBJ.buffer.extend(normals[start:end])
                    
                    break


    @staticmethod
    def show_buffer_data(buffer):
        for i in range(len(buffer)//8):
            start = i * 8
            end = start + 8
            print(buffer[start:end])


    @staticmethod
    def load_model(file, sorted=True, color:list=[1.0, 1.0, 1.0]):
        vert_coords = [] 
        tex_coords = [] 
        norm_coords = [] 
        all_indices = [] 
        indices = [] 


        with open(file, 'r') as f:
            line = f.readline()
            while line:
                values = line.split()
                if values[0] == 'v':
                    OBJ.search_data(values, vert_coords, 'v', 'float')
                elif values[0] == 'vt':
                    OBJ.search_data(values, tex_coords, 'vt', 'float')
                elif values[0] == 'vn':
                    OBJ.search_data(values, norm_coords, 'vn', 'float')
                elif values[0] == 'f':
                    for value in values[1:]:
                        val = value.split('/')
                        OBJ.search_data(val, all_indices, 'f', 'int')
                        indices.append(int(val[0])-1)

                line = f.readline()

        if sorted:
            OBJ.create_sorted_vertex_buffer(all_indices, vert_coords, tex_coords, norm_coords, color)
        else:
            OBJ.create_unsorted_vertex_buffer(all_indices, vert_coords, tex_coords, norm_coords, color)

        buffer = OBJ.buffer.copy() 
        OBJ.buffer = [] 

        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32'), vert_coords

    """#Metodo para obtener los valores de cada linea
    @staticmethod
    def search_data(values:list, coords:list, skip:str, data_type:str='float'):
        for value in values:
            if value == skip:
                continue
            if data_type == 'float':
                coords.append(float(value))
            if data_type == 'int':
                coords.append(int(value)-1)

    # Este metodo crea el buffer de vertices ordenado
    @staticmethod
    def create_sorted_vertex_buffer(indices:list,vertices:list,textures:list,normals:list,color:list):
        for i, ind in enumerate(indices):
            # Agrega los vertices
            if i % 3 == 0: 
                start = ind * 3
                end = start + 3
                OBJ.buffer.extend(vertices[start:end])
            # Agrega las coordenadas de la textura
            elif i % 3 == 0:
                start = ind * 2
                end = start + 2
                OBJ.buffer.extend(textures[start:end])
            # Agregamos el vector de normals
            elif i % 3 == 2:
                start = ind * 3
                end = start + 3
                OBJ.buffer.extend(normals[start:end])
                OBJ.buffer.extend(color)

    #Metodo para leer el archivo .obj
    @staticmethod
    def load_obj(path:str,color:list=[1.0, 1.0, 1.0]):
        # Coordenadas de los vertices
        vertices_coords = []
        # Coordenadas de las texturas
        texture_coords = []
        # Coordenadas de las normales
        normals_coords = []
        # Indices del objeto en general
        indices = []
        # Leemos el archivo y obtenemos los datos 
        with open(path, 'r') as file:
            for line in file.readlines():
                values = line.split()
                if values[0] == 'v':
                    OBJ.search_data(values, vertices_coords,'v')
                elif values[0] == 'vt':
                    OBJ.search_data(values, texture_coords,'vt')
                elif values[0] == 'vn':
                    OBJ.search_data(values, normals_coords, 'vn')
                elif values[0] == 'f':
                    for value in values[1:]:
                        OBJ.search_data(value.split('/'), indices, 'f', 'int')
        # Creamos el buffer
        OBJ.create_sorted_vertex_buffer(indices, vertices_coords, texture_coords, normals_coords, color)
        # Obtenemos el buffer y lo almacenamos
        buffer = OBJ.buffer.copy()
        # Restablecemos el buffer estatico
        OBJ.buffer = []

        return np.array(indices, dtype='uint32'), np.array(buffer, dtype='float32')"""