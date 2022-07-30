import pathlib
import json
import shutil
import datetime
import os


customisePath = "customise.json"
formatPath = "format"

ymm = {}
jsn = {}
template = {
    "IsBold": False,
    "IsItalic": False,
    "Scale": 1.0,
    "IsLineBreak": True,
    "HasDecoration": False
}

targetPath = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])
os.chdir(targetPath)

newPath = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
shutil.copytree(formatPath, newPath)

with open(pathlib.Path(customisePath).absolute(), "r", encoding="utf_8") as setting:
    jsn = json.load(setting)

path = pathlib.Path('./' + newPath).glob('*.ymmp')
for p in path:
    with open(p.absolute(), "r", encoding="utf_8_sig") as infile:
        ymm = json.load(infile)

    for item in ymm["Timeline"]["Items"]:
        if "CharacterName" in item.keys() and item["CharacterName"] in jsn["Characters"]:
            sentence = item["Serif"].split("\r\n")
            # 制限行, 制限列
            limitR = 5
            limitC = 180
            if len(sentence) <= limitR:
                # デコレーション初期化
                item["Decorations"] = []
                length = 0
                for num in range(len(sentence), limitR):
                    if (num == limitR - 1):
                        sentence.append(" " * limitC + ".")
                    else:
                        sentence.append("")

                for i in range(len(sentence)):
                    decoLine = jsn["IdDeco"].copy()
                    newline = template.copy()
                    newline["IsLineBreak"] = True
                    newline["Length"] = 2
                    textLine = template.copy()

                    # 1行目テキスト
                    if (i == 0):
                        length = len(sentence[i])
                        decoLine["Length"] = length
                        newline["Start"] = length
                        item["Decorations"].append(decoLine)
                        item["Decorations"].append(newline)
                        length = length + 2
                    # 最終行テキスト
                    elif (i == limitR - 1):
                        textLine["Start"] = length
                        textLine["Length"] = len(sentence[i]) - 1
                        length = length + len(sentence[i]) - 1

                        #textLine2 = template.copy()
                        #textLine2["Start"] = length
                        #textLine2["Length"] = 1
                        #textLine2["Foreground"] = "#111111",

                        item["Decorations"].append(textLine)
                        #item["Decorations"].append(textLine2)
                    else:
                        textLine["Start"] = length
                        textLine["Length"] = len(sentence[i])
                        length = length + len(sentence[i])
                        newline["Start"] = length
                        item["Decorations"].append(textLine)
                        item["Decorations"].append(newline)
                        length = length + 2
                h = item["Hatsuon"].split("\r\n")
                h[0] = ""
                item["Serif"] = "\r\n".join(sentence)
                item["Hatsuon"] = "\r\n".join(h)
                del item["VoiceCache"]

    with open(p.absolute(), 'w', encoding="utf_8_sig") as outfile:
        json.dump(ymm, outfile, ensure_ascii=False, indent=2)
