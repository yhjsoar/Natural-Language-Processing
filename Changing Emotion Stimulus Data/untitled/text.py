text_file_path = "prince.txt"
new_text_content = []
with open(text_file_path, 'r', encoding="utf-8") as f:
    lines = f.readlines()
    sentence = ''
    for line in lines:
        line = line.lstrip()
        if "[Picture" not in line:
            line = line.replace("\n", " ")
            line = line.replace("  ", " ")
            while line.find(".") != -1:
                sentence = sentence + line[:line.find(".")+1]
                line = line[line.find(".")+1:]
                new_text_content.append(sentence)
                sentence = ''
            sentence += line

sencond_text_content = []
last_idx = 0
now_idx = 0
for line in new_text_content:
    line = line.lstrip()
    line = line.replace("  ", " ")
    # print("line: "+line+"\nlast sentence:")
    # for i in range(last_idx, now_idx):
    #     print(sencond_text_content[i])
    last_idx = now_idx
    if line.find("?") == -1:
        sencond_text_content.append(line)
        now_idx += 1
    else:
        while line.find("?") != -1:
            sencond_text_content.append(line[:line.find("?") + 1])
            line = line[line.find("?")+1:]
            now_idx += 1
        sencond_text_content.append(line)
        now_idx += 1

result = []
for line in new_text_content:
    line = line.lstrip()
    line = line.replace("  ", " ")
    if line.find("!") == -1:
        result.append(line)
    else:
        while line.find("!") != -1:
            result.append(line[:line.find("!") + 1])
            line = line[line.find("!")+1:]
        result.append(line)

for line in result:
    print(line)