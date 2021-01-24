from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile, askopenfilename
import zipfile
import shutil
import os
import requests
from PIL import Image


finalList = []

def getRating(file):
    url="https://eastus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/5d223f62-13e1-428b-a83f-4708a1e2cafe/classify/iterations/Iteration4/image"
    headers={'content-type':'application/octet-stream','Prediction-Key':'2d36364a0c854a8b8a204b798568dda5'}
    r =requests.post(url,data=open(file,"rb"),headers=headers)
    dict = r.json()

    rating = 0
    for i in range(len(dict["predictions"])):
        rating += dict["predictions"][i]["probability"] * int(dict["predictions"][i]["tagName"])

    return (rating)

def doTheThing(folderPath):
    length = len(os.listdir(folderPath))
    fp = os.listdir(folderPath)
    for i in range(length):
        if (fp[i].endswith(".jpg") or fp[i].endswith(".png") or fp[i].endswith(".jpeg")):
            rankings.append([fp[i], getRating("resized/"+fp[i])])
    finalList = sortArray(rankings)
    writeFile(finalList)



folder = "files/"
resized = "resized/"
rankings = []

for file in os.listdir(folder):
    file_path = os.path.join(folder, file)
    try:
        if (os.path.isfile(file_path) or os.path.islink(file_path)):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print("did an oopsie")

def openFile():
    filename = askopenfilename()

    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall("files/")

    files = os.listdir("files/")
    print(files)
    for i in files:
        if i.endswith(".jpg") or i.endswith(".jpeg") or i.endswith(".png"):
            img = Image.open("files/" +i,"r")
            basewidth = 178
            wpc = basewidth/float(img.size[0])
            hsize = int((float(img.size[1])*float(wpc)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            img.save("resized/"+i)
    doTheThing("resized/")

def sortArray(list):
    finalList = sorted(list, key= lambda x: x[1], reverse=True)
    return finalList

def writeFile(list):
    with open("output.txt", "w") as f:
        for i in list:
            print(i)
            f.write(str(i[0]) + ": you ranked " + str(i[1]) + "/10\n")
        f.close()



window = Tk()
window.title("Welcome to Dr. PP")
lbl = Label(window, text = "Please enter a zip file below, and please don't have spaces in the filenames:")
lbl2 = Label(window, text = "Check output.txt for your results")
btn = Button(window, text = "Select a file", command = lambda:openFile())

lbl.pack(side = TOP, pady = 10)
lbl2.pack(side = BOTTOM, pady = 10)
btn.pack(side = BOTTOM, pady = 10)
# lbl.grid(column =0, row=0)

window.mainloop()




