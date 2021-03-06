import numpy as np

def matching_pursuit(xs, Dt, k, zs):
  
    #Performs recursive matching pursuit 
 
    if k == 0:
        return zs

    num_xs = len(xs)
    num_ds = len(Dt)

    for x_index in xrange(num_xs):
        x = xs[x_index]

        max_inner_product = 0
        max_z_index = None

        for i in xrange(num_ds):
            di = Dt[i]
            ip = np.dot(di, x)
            if abs(ip) > abs(max_inner_product):
                max_inner_product = ip
                max_z_index = i

        if max_z_index != None:
            zs[x_index][max_z_index] += max_inner_product

        
        xs[x_index] -= (max_inner_product * np.transpose(Dt[max_z_index]))

    return matching_pursuit(xs, Dt, k-1, zs)


def orthogonal_matching_pursuit(xs, Dt, D, k, zs, selected):
    
    #Performs recursive orthogonal matching pursuit 
  

    if k == 0:
        return zs

    num_xs = len(xs)
    num_ds = len(Dt)

    for x_index in xrange(num_xs):
        x = xs[x_index]

        max_inner_product = 0
        max_z_index = None

        for i in xrange(num_ds):
            di = Dt[i]
            ip = np.dot(di, x)
            if abs(ip) > abs(max_inner_product):
                max_inner_product = ip
                max_z_index = i

        if max_z_index != None:
            zs[x_index][max_z_index] += max_inner_product

           
            selected[x_index].append(max_z_index)

            
            gamma, _, _, _  = np.linalg.lstsq(D[:,selected[x_index]], x)
            xs[x_index] = xs[x_index] - np.dot(D[:,selected[x_index]], gamma)

    return orthogonal_matching_pursuit(xs, Dt, D, k-1, zs, selected)

def sparsify (matrix, dictionary, k):
    
    #Generates sparse codes for each of the rows in matrix
   

    num_atoms = len(dictionary)
    num_vectors = len(matrix)

    
    cpy_matrix = [None] * num_vectors
    for i in xrange(num_vectors):
        cpy_matrix[i] = np.zeros(len(matrix[i]), dtype=np.double)
        for j in xrange(len(matrix[i])):
            cpy_matrix[i][j] = matrix[i][j]

    sparse_codes = [None] * num_vectors
    selected = [None] * num_vectors

    for i in xrange(num_vectors):
        sparse_codes[i] = np.zeros(num_atoms, dtype=np.double)
        selected[i] = np.zeros(num_atoms, dtype=np.double)

    Dt = dictionary
    D = np.transpose(Dt)

    results = matching_pursuit(cpy_matrix, Dt, k, sparse_codes)

    return results

def sparsify_omp (matrix, dictionary, k):
    
    #Generates sparse codes for each of the rows in matrix
   

    num_atoms = len(dictionary)
    num_vectors = len(matrix)

    # Copy the matrix
    cpy_matrix = [None] * num_vectors
    for i in xrange(num_vectors):
        cpy_matrix[i] = np.zeros(len(matrix[i]), dtype=np.double)
        for j in xrange(len(matrix[i])):
            cpy_matrix[i][j] = matrix[i][j]

    sparse_codes = [None] * num_vectors
    selected = [None] * num_vectors

    for i in xrange(num_vectors):
        sparse_codes[i] = np.zeros(num_atoms, dtype=np.double)
        selected[i] = []

    Dt = dictionary
    D = np.transpose(Dt)

    results = orthogonal_matching_pursuit(cpy_matrix, Dt, D, k, sparse_codes, selected)

    return results
