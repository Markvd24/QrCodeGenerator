from PIL import Image

im = Image.new(mode="1", size=(25, 25))

data = im.load()
for x in range(25):
    for y in range(25):
        data[x,y] = (3*(x//1) + 5*(y//1)) % 2

im.show()