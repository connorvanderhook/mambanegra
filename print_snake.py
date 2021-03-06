# Python3 program for traversing a matrix from column n-1 
import sys; 
  
# Function used for traversing over the given matrix 
def traverseMatrix(mat, n): 
  
    for i in range(n):  
        if i & 1: 
            for j in range(n): 
                print(str(mat[i][j])+ "", end = " ") 
        else: 
            for j in range(n-1, -1, -1): 
                print(str(mat[i][j])+ "", end = " ") 
  
# Driver function 
if __name__ == '__main__': 
  
    # number of rows and columns 
    n = 5
  
    # 5x5 matrix 
    mat =[ 
         [1,  2,  3,  4,  5], 
         [6,  7,  8,  9,  10], 
         [11, 12, 13, 14, 15], 
         [16, 17, 18, 19, 20], 
         [21, 22, 23, 24, 25] 
    ] 
  
    traverseMatrix(mat, n)
