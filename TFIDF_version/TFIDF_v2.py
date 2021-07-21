import os
from collections import Counter
import math

def TFIDF(path, new_path):
    count_list = []
    count_value_list = []
    all_file = os.listdir(path)
    all_file.sort(key=lambda x: int(x[:-4]))
    for n, archive in enumerate(all_file):
        position = path + archive  # '\\'
        with open(position, 'r', encoding='utf-8-sig') as f:
            read_term = f.read().splitlines()
            count = Counter(read_term)
            count_value_list.append(sum(count.values()))
            count2 = {x: count[x] for x in count if count[x] > 1}
            count_list.append(count2)

    for n, count in enumerate(count_list):
        # count2 = {x: count[x] for x in count if count[x] > 1}

        TF = {word: count[word] / count_value_list[n] for word in count}
        IDF = {word: (math.log(len(count_list) / ((sum(1 for count in count_list if word in count.keys())) + 1))) for word in count.keys()}
        TF_IDF = {word: score * IDF[word] for word, score in TF.items() if word in IDF}
        # TF_IDF = sorted(TF_IDF.items(), key=lambda x: x[1], reverse=True)  # [:20]

        with open(new_path + str(n + 1) + ".csv", 'w', encoding='utf-8-sig') as f:
            # f.write("Words,TFIDF\n")
            # for t in TF_IDF:
            #     f.write(','.join(str(s) for s in t) + '\n')
            # f.write("Words,TF,IDF,TFIDF\n")
            for F, ID, t in zip(TF.items(), IDF.items(), TF_IDF.items()):
                # print(t[0] + "," + str(F[1]) + "," + str(ID[1]) + "," + str(t[1]))
                # f.write(','.join(str(s) for s in t) + '\n')
                f.write(t[0] + "," + str(F[1]) + "," + str(ID[1]) + "," + str(t[1]) + "\n")

        with open(new_path + str(n + 1) + ".csv", 'r', encoding='utf-8-sig') as fr:
            datasorts = fr.read().splitlines()
        datasorted = []
        for splitdata in datasorts:
            datasorted.append(splitdata.split(",", maxsplit=3))
        del datasorts
        data_sort = sorted(datasorted, key=lambda data: data[3], reverse=True)  # 針對各檔排序後輸出
        del datasorted
        with open(new_path + str(n + 1) + ".csv", 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(["Words", "TF", "IDF", "TFIDF"])
            writer.writerows(data_sort)