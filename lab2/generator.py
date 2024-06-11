import math
 
class RandomNumberGenerator:
    def __init__(self, seedVaule=None):
        self.__seed=seedVaule
    def nextInt(self, low, high):
        m = 2147483647
        a = 16807
        b = 127773
        c = 2836
        k = int(self.__seed / b)
        self.__seed = a * (self.__seed % b) - k * c;
        if self.__seed < 0:
            self.__seed = self.__seed + m
        value_0_1 = self.__seed
        value_0_1 =  value_0_1/m
        return low + int(math.floor(value_0_1 * (high - low + 1)))
    def nextFloat(self, low, high):
        low*=100000
        high*=100000
        val = self.nextInt(low,high)/100000.0
        return val
 
rng = RandomNumberGenerator(4133241)
 
N = 10
 
def generate_matrix(size, rng):
    return [[rng.nextInt(1, 50) for _ in range(size)] for _ in range(size)]
 
matrix1 = generate_matrix(N, rng)
matrix2 = generate_matrix(N, rng)
 
def save_matrices_to_dat_file(w, d, filename="JGKK.dat"):
    with open(filename, "w") as file:
        file.write(f"n = {N};\n\n")
        file.write("w = [\n")
        for row in matrix1:
            file.write("[")
            file.write(", ".join(map(str, row)) + "],\n")
        file.write("];\n\n")
 
        file.write("d = [\n")
        for row in matrix2:
            file.write("[")
            file.write(", ".join(map(str, row)) + "],\n")
        file.write("];\n")
 
save_matrices_to_dat_file(matrix1, matrix2) 