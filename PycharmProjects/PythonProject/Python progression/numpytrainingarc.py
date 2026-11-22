import numpy as np

treasure = np.array([
    [4,  0,  7,  2,  8],
    [1,  9,  3,  0,  5],
    [6,  2, 10,  4,  1],
    [0,  8,  5,  7,  3],
    [9,  1,  0,  6,  2]
])
print(treasure)

print("The sections refer to the 3x3 area of this table ")
top_left = treasure[0:3:1, 0:3:1]

print(top_left)
print("This is the total number of treasure "
      "available in the the top left section")
print(top_left.sum())

middle = treasure[1:4:1,1:4:1]
print(middle)
print("This is the total number of treasure "
      "available in the middle section")

print(middle.sum())

bottom_right = treasure[2:5:1,2:5:1]
print(bottom_right)
print("This is the total number of treasure"
      "available in the bottom right section")
print(bottom_right.sum())

