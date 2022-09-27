from PIL import Image, ImageOps


brightness_dict = {0: '___', 1: '░░░', 2: '▒▒▒', 3: '▓▓▓', 4: '███'}

img = ImageOps.exif_transpose(Image.open("test4.jpg")) # refer to https://pillow.readthedocs.io/en/latest/reference/ImageOps.html#PIL.ImageOps.exif_transpose
img_data = img.getdata()
img_lst = []
for i in img_data:
    tmp = i[0]*0.2125+i[1]*0.7174+i[2]*0.0721 ### Rec. 709-6 weights
    img_lst.append(tmp)
new_img = Image.new('L', img.size)
new_img.putdata(img_lst)
new_img_resized = new_img.resize((100, 100), Image.ANTIALIAS)
new_img_resized.save('result.jpg')
#new_img_resized.show()
new_img_calibrated = new_img_resized.quantize(4)
f = open('data.txt', 'wb')
for i in range(len(new_img_calibrated.getdata())):
    if i % 100 == 0:
        print()
        f.write(bytes('\n', encoding='utf-8'))
    f.write(bytes(brightness_dict[new_img_calibrated.getdata()[i]], encoding='utf-8'))
    f.flush()
    print((brightness_dict[new_img_calibrated.getdata()[i]]), end = '')
f.close()