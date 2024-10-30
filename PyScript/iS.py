import requests
from bs4 import BeautifulSoup
import os

dirname = "outsimages"
prefix = "hom4ikSleep"
imageCount = 30000

if dirname not in os.listdir():
    os.mkdir(dirname)

def getInt(stroka):
    a = stroka[len(prefix + "_img"):-5]
    return int(a)

def maxi():
    listik = os.listdir(dirname)
    l = max([getInt(name) for name in listik if os.path.isfile(dirname + "/" + name)])
    return l


l = maxi() + 1
print("Files: " + str(l))

i = l
while True:
    if (i > l + imageCount):
        break
    
    print("i = " + str(i))

    try:
        page = requests.get("https://thispersondoesnotexist.com/")
        souped = BeautifulSoup(page.content, "html.parser")
        file = open("./" + dirname + "/" + prefix + "_img" + str(i) + ".jpeg", 'wb')
        file.write(page.content)
        file.close()
        i += 1
    except Exception as e:
        print("\t" + str(e))
        print("I almost falled, but arised again and continue image getting\n")
        # continue
