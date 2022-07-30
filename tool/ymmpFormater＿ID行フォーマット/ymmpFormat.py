import pathlib
import json
import shutil
import datetime

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
nl = "\r\n"

with open(pathlib.Path(customisePath).absolute(), "r", encoding="utf_8") as setting:
    jsn = json.load(setting)


newPath = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
shutil.copytree(formatPath, newPath)

path = pathlib.Path('./' + newPath).glob('*.ymmp')
for p in path:
    with open(p.absolute(), "r", encoding="utf_8_sig") as infile:
        ymm = json.load(infile)

    for item in ymm["Timeline"]["Items"]:
        if "CharacterName" in item.keys() and item["CharacterName"] in jsn["Characters"]:
            sentence = item["Serif"].split(nl)
            # 制限行, 制限列
            limitR = 5
            limitC = 130
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
                        textLine["Length"] = length + len(sentence[i])
                        item["Decorations"].append(textLine)
                    else:
                        textLine["Start"] = length
                        length = length + len(sentence[i])
                        textLine["Length"] = length
                        newline["Start"] = length
                        item["Decorations"].append(textLine)
                        item["Decorations"].append(newline)
                        length = length + 2
                h = item["Hatsuon"].split(nl)
                h[0] = ""
                item["Serif"] = nl.join(sentence)
                item["Hatsuon"] = nl.join(h)
                del item["VoiceCache"]

    with open(p.absolute(), 'w', encoding="utf_8_sig") as outfile:
        json.dump(ymm, outfile, ensure_ascii=False, indent=2)
