'''
Fuction to simulate sensor MLX90615
By Roberto Colistete Jr.
'''
n_reads_MLX90615 = 0
def Read_MLX90615_Temperatures():
    global n_reads_MLX90615
    n_reads_MLX90615 += 1
    if (n_reads_MLX90615 % 34) > 17: # 17 medidas com temperatura ambiente, 17 com temperature de pessoa
        return (3650, 2500) # Tobject = 36.50 C, Tambient = 25.00 C
    else:
        return (2500, 2500) # Tobject = 25.50 C, Tambient = 25.00 C