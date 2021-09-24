text_file_path = "Emotion Cause.txt"

content = []
cnt = 0
with open(text_file_path, 'r', encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        first = line.split('<')
        second = first[1].split('>')
        third = first[2].split('>')
        fourth = first[3].split('>')
        emotion = second[0]
        sentence = second[1] + third[1] + fourth[1];
        cause = third[1]
        content.append([emotion, sentence, cause])
        cnt += 1

print(content)

f = open("Emotion Cause Data.txt", "w")
f2 = open("Emotion Cause Data with no Cause.txt", "w")
data = "emotion\tsentence\tcause\n"
data2 = "emotion\tsentence\n"
f.write(data)
f2.write(data2)
for i in range(cnt):
    data = content[i][0] + "\t" + content[i][1] + "\t" + content[i][2] + "\n"
    data2 = content[i][0] + "\t" + content[i][1] + "\n"
    f.write(data)
    f2.write(data2)
f.close()
f2.close()
# f = open("No Cause Data.txt", "w")
# data = "emotion\tsentence\n"
# f.write(data)
# for i in range(cnt):
#     data = content[i][0]+"\t"+content[i][1]+"\n"
#     f.write(data)
#
# f.close()