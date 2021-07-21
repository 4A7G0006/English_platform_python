import os
from collections import Counter
import math

Encoding = 'utf-8-sig'


def TFIDF(path, new_path):
    count_list = []
    count_value_list = []
    all_file = os.listdir(path)
    all_file.sort(key=lambda x: int(x[:-4]))
    for n, archive in enumerate(all_file):
        position = path + '\\' + archive
        with open(position, 'r', encoding='utf-8-sig') as f:
            read_term = f.read().splitlines()
            count = Counter(read_term)
            count_value_list.append(sum(count.values()))
            count2 = {x: count[x] for x in count if count[x] > 1}
            count_list.append(count2)

    for n, count in enumerate(count_list):
        #count2 = {x: count[x] for x in count if count[x] > 1}

        TF = {word: count[word] / count_value_list[n] for word in count}
        IDF = {word: (math.log(len(count_list) / ((sum(1 for count in count_list if word in count.keys())) + 1))) for word in count.keys()}
        TF_IDF = {word: score * IDF[word] for word, score in TF.items() if word in IDF}
        # TF_IDF = sorted(TF_IDF.items(), key=lambda x: x[1], reverse=True)[:20]
        temp = list(map(lambda x: x[0] + "," + str(x[1]) + "," + str(x[2]) + "," + str(x[3]), zip(TF.keys(), TF.values(), IDF.values(), TF_IDF.values())))
        with open(new_path + str(n + 1) + ".csv", 'w', encoding=Encoding) as f:
            f.write("文法\計算,TF,IDF,TFIDF\n")
            for t in temp:
                f.write(''.join(str(s) for s in t+"\n") )


TFIDF(r"E:\test_re", r"E:\test\\")
