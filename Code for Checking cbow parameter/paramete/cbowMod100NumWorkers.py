f = open("cbow100.txt", "r")

lines = f.readlines()

forStore = []
# for i in range(10):
#     storing = open("min_word_count_"+str(i+1)+".txt", "w")
#     forStore.append(storing)
for i in range(10):
    storing = open("num_workers_"+str(i+1)+".txt", "w")
    forStore.append(storing)

# num_features = 300        # 워드 벡터 특징값 수
# min_word_count = 10       # 단어에 대한 최소 빈도 수
# num_workers = 4           # 프로세스 개수
# context = 10              # 컨텍스트 윈도 크기
# downsampling = 1e-3       # 다운 샘플링 비율

i = 0
num_features = 100
min_word_count = 0
num_workers = 0
context = 0
downsampling = 0
acclgs = 0
accfor = 0
catlgs = 0
catfor = 0
cnt = 0

print(len(lines))
result_list = []

while True:
    if i >= len(lines)-1:
        break
    print(i)
    cnt += 1
    par = lines[i].split()
    acc1 = lines[i + 1].split()
    acc2 = lines[i + 2].split()
    cat = lines[i + 3].split()


    i = i+4
    if i < len(lines)-1:
        while True:
            i += 1
            if lines[i][0] == '(':
                break

    # print(par)
    # print(acc1)
    # print(acc2)
    # print(cat)
    #
    num_features = int(par[0][1:len(par[0])-1])
    min_word_count = int(par[1][:len(par[1])-1])
    num_workers = int(par[2][:len(par[2])-1])
    context = int(par[3][:len(par[3])-1])
    downsampling = float(par[4][:len(par[4])-1])

    acclgs = float(acc1[3])
    accfor = float(acc2[4])
    catlgs = int(cat[3])
    catfor = int(cat[1][:len(cat[1])-1])

    # print("num_features: " + str(num_features))
    # print("min_word_count: " + str(min_word_count))
    # print("num_workers: " + str(num_workers))
    # print("context: " + str(context))
    # print("downsampling : " + str(downsampling))
    #
    # print("accuracy lgs: " + str(acclgs) + ", forest: "+ str(accfor))
    # print("cat lgs: " + str(catlgs) + ", forest: "+str(catfor))

    if cnt % 400 == 1and cnt > 400:
        cnt = 1
    accuracy_avg = (acclgs + accfor) / 2
    cat_avg = (catlgs + catfor) / 2

    result_list.append([min_word_count, num_workers, context, downsampling, accuracy_avg, cat_avg])

    # string = str(cnt) + ", " + str(num_workers) + ", " + str(context) + ", " + str(downsampling) + ", " + str(accuracy_avg) + ", " + str(cat_avg) + "\n"
    # print(string)
    # forStore[min_word_count-1].write(string)

for i in range(10):
    cnt = 0
    for r in result_list:
        if r[1] == i+1:
            cnt += 1
            string = str(cnt) + ", " + str(r[0]) + ", " + str(r[2]) + ", " + str(r[3]) + ", " + str(r[4]) + ", " + str(r[5]) + "\n"
            forStore[i].write(string)