import os

dirname = '.'
files = os.listdir(dirname)

temp = map(lambda name: os.path.join(dirname, name), files)

print(list(temp))