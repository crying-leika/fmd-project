import pandas as pd 
from PIL import Image, ImageDraw
import io

def img_concat(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

df = pd.read_parquet('train-00000-of-00003.parquet') 
for i in range(2,3):
    file = open("condimg" + str(i) + ".jpeg", 'wb')
    file.write(df.head()['conditioning_image'][i]['bytes'])
    file.close()
    img = Image.open(io.BytesIO(df.head()['image'][i]['bytes']))
    img_marks = Image.open(io.BytesIO(df.head()['conditioning_image'][i]['bytes']))
    #img = Image.open(r"img" + str(i) + ".jpeg") 
    red, grn, blu = img.split()
    print(img.size)
    #img.show()
    zerg = grn.point(lambda a: a * 0.5)
    #zerb = grn.point(lambda a: a * 0.5)
    #imblend = Image.blend(img, img_marks, 0.6)
    darkened = img.point(lambda a: a * 0.5)
    redmask, grnmask, blumask = img_marks.split()
    #print("mode is", redmask.mode)
    monochrome  = Image.frombytes("L",redmask.size,redmask.tobytes() + grnmask.tobytes() + blumask.tobytes())
    mask = Image.merge("RGB", (redmask, redmask, redmask))
    # mask = Image.merge("RGB", 
    #                 (
    #                     Image.merge("RGB", (redmask,redmask,redmask)),
    #                     Image.merge("RGB", (grnmask,grnmask,grnmask)),
    #                     Image.merge("RGB", (blumask,blumask,blumask))
    #                 ))
    
    dst = img_concat(img_marks, monochrome)
    #dst.show()
    img_marks.show()
    print(len(img_marks.histogram()))
    arr = img_marks.histogram()
    colorids = []
    for i in range(0, 256):
        if arr[1 * i] > 0 or arr[2 * i] > 0 or arr[3 * i]:
            colorids.append((1 * i,  2 * i, arr[3 * i]))
    
    s = set()
    for x in range(0, img_marks.width, 4):
        for y in range(0, img_marks.height, 4):
            s.add(img_marks.getpixel((x, y)))
    extractedVis = Image.new("RGB", img_marks.size, (0,0,0))
    exVisDraw = ImageDraw.Draw(extractedVis)
    rectsize = 4
    for el in s:
        if el == (0,0,0):
            continue
        midvec = (0, 0)
        cnteqs = 0
        for x in range(0, img_marks.width, 4):
            for y in range(0, img_marks.height, 4):
                if el == img_marks.getpixel((x, y)) :
                    #print(el, img_marks.getpixel((x, y)))
                    cnteqs += 1
                    midvec = midvec[0] + x, midvec[1] + y
        midv = midvec[0] / cnteqs, midvec[1] / cnteqs
        rectangl = [(midv[0] - rectsize, midv[1] - rectsize), 
                    (midv[0] + rectsize, midv[1] + rectsize) ]
        exVisDraw.rectangle(rectangl, el)
        #print("mid", midv)
    extractedVis.show()

        
    


    # show the plotting graph of an image
    # imadd = zerg
    # imadd = zerg.paste(img_marks)
    #redmerg = Image.merge("RGB", (red, zerg, zerb))
    #red.show()
    #redmerg.show()
    #imadd.show()
