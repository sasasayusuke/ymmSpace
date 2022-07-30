import shutil
import datetime
import os
formatPath = "format"
jsn = {}

targetPath = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])
os.chdir(targetPath)
boxPath = "//".join(os.getcwd().split("\\")[:3])
boxPathList = ["C://Users//pc", "C://Users//Y-Sasaki", "C://Users//t.s"]
newPath = ("shida-" if boxPath == boxPathList[2] else "sasaki-") + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
shutil.copytree(formatPath, newPath)

files = os.listdir(".//" + newPath)

for file in files:
    with open(os.path.join(os.path.abspath(".//" + newPath), file), "r", encoding="utf_8_sig") as infile:
        content = infile.read()
    for p in boxPathList:
        content = content.replace(p.replace("/", "\\"), boxPath.replace("/", "\\"))
    with open(os.path.join(os.path.abspath(".//" + newPath), file), 'w', encoding="utf_8_sig") as outfile:
        outfile.write(content)
