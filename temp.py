import numpy as np

L = [[2.73351472, 0.47539713, 3.63280356, 1.4787706, 3.13661701],
     [1.40305914, 2.27134829, 2.73437132, 1.88939679, 0.0384238],
     [1.56666697, -0.40088431, 0.54893762, 3.3776724, 2.27490386]]
arr = np.array(L)
arr1 = np.array((arr[0][1], arr[1][1], arr[2][1]))
arr1 = arr1.reshape(3, 1)
arr2 = np.array((arr[1][2:5], arr[2][2:5]))
arr3 = np.array((arr[0][1:5:2], arr[2][1:5:2])).flatten()
arr4 = arr[np.where(np.logical_and(arr >= 2.5, arr <= 3.5))]
arr5 = arr[np.where(np.logical_or(arr >= 3, arr <= 0))]
print(f'''arr1= {arr1}
arr2= {arr2}
arr3= {arr3.flatten()}
arr4= {arr4}
arr5= {arr5}''')