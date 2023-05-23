import os
import glob
while True:
    data = input()
    print("\n")
    data = data.rsplit('/', 1)
    maxpic = int(str(data[1]).split('.')[0])
    suffix = '.png'
    for i in range(1, maxpic + 1):
        print(data[0] + f"/{i}" + suffix)
    print("\n")
    path = 'C:/Users/965/Downloads'
    for infile in glob.glob(os.path.join(path, '*.png')):
        os.remove(infile)
