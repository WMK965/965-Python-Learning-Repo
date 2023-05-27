import chardet


data = open(file="./resources/444.txt", mode='rb')
result = chardet.detect(data.read())
result = result["encoding"]
print(result)
