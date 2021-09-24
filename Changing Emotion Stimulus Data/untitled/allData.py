text_file_path = "No Cause.txt"
content = []
cnt = 0
with open(text_file_path, 'r', encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        first = line.split('<')
        second = first[1].split('>')
        content.append(second)
        cnt+=1


f = open("No Cause Data.txt", "w")
data = "emotion\tsentence\n"
f.write(data)
for i in range(cnt):
    data = content[i][0]+"\t"+content[i][1]+"\n"
    f.write(data)

f.close()