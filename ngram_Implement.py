def ngram_chi(original_resource_file_path, save_new_resource_file_path, N): #第一個參數為原始檔案路徑 第二參數為新儲存檔案路徑 第三參數為中文段幾字元( N>2 )
    with open(original_resource_file_path, "r", encoding="utf-8") as text:
        words = text.read().replace(" ", "").replace("\n", "")
    nlist = []
    for total in range(2, N + 1):   #斷 2 ~ N 字
        for a in range(len(words) - total + 1):
            nlist.append(words[a:a + total])
            save_ngram(save_new_resource_file_path, nlist)
            
#中文EX: 今天天氣真好  N = 3

# :今天 天天 天氣 氣真 真好 今天天 天天氣 天氣真 氣真好

def ngram_eng(original_resource_file_path, save_new_resource_file_path, N): #第一個參數為原始檔案路徑 第二參數為新儲存檔案路徑 第三參數為英文段幾字元( N>1 )
    with open(original_resource_file_path, "r", encoding='utf-8') as texts:
        sentence = texts.read()
    sentence = sentence.split()
    # 初始版本
    ''' 
        idxLst = [i for i, elem in enumerate(words) if elem == ' ']  # 針對句子的空格做編號
        idxLst.insert(0, 0)  # 將剛剛編號設定頭
        idxLst.append(len(words))  # 尾
        tgtLst = [words[i:j] for i, j in zip(idxLst, idxLst[1:])]
        tgtLst2 = list(map(lambda x: x[1:], tgtLst[1:]))
        tgtLst2.insert(0, tgtLst[0])
        for total in range(1, N + 1):
            for a in range(len(words) - total - len(idxLst) - 3):
                save_ngram(save_new_resource_file_path, tgtLst2, a, total)
        '''     #   同樣可以使用
    # 改良版本
    nlist = []
    for total in range(1, N + 1): #英文一個 單字也有意義 所以從1斷到N字
        for a in range(len(sentence) - total + 1):
            ss = " ".join(sentence[a:a + total])
            nlist.append(ss.strip())
    save_ngram(save_new_resource_file_path, nlist)
    
#英文測試EX: Today is good day.      N = 3

#: Today , is , good , day , Today is , is good , good day , Today is good , is good day

def save_ngram(save_new_resource_file_path, sentence):
    with open(save_new_resource_file_path, "a", encoding="utf-8") as file:
        file.write("\n".join(sentence))


def chinese_eng_break(resource, chinese_path, english_path):    #中英文本分割 第一參數 原始檔案參雜中英文  第二參數 擷取出的中文檔案儲存路徑 第三參數 擷取出的英文檔案儲存路徑
    eng = ''
    chi = ''
    other = ''
    with open(resource, "r", encoding="utf-8") as file:
        for content in file.readlines():
            for text in range(0, len(content)):
                # print(content[text])
                if content[text] == ' ':
                    if content[text - 1] == ' ':
                        pass
                    elif '\u0041' <= content[text - 1] <= '\u005a' or '\u0061' <= content[text - 1] <= '\u007a':
                        eng += ' '
                    elif '\u4e00' <= content[text] <= '\u9fcb':
                        chi += " "
                    else:
                        pass
                elif '\u4e00' <= content[text] <= '\u9fcb':  # 中文編碼(含擴充字元)
                    chi += content[text]
                    if eng[-1:] != ' ':
                        eng += ' '
                elif '\u0041' <= content[text] <= '\u005a' or '\u0061' <= content[text] <= '\u007a': 
                    '''  符號編碼ex: ":,.#$%&/" 20-2f  # 數字編碼 30~39  # 大小寫英文與符號編碼 大寫41-5a 小寫61-7a '''
                    eng += content[text]
                else:
                    if '\u4e00' <= content[text - 1] <= '\u9fcb':
                        chi += " "
                    other += content[text]  # 例外字元
    with open(chinese_path, "w+", encoding="utf-8") as file1:
        file1.write(chi)
    with open(english_path, "w+", encoding="utf-8") as file2:
        file2.write(eng)

# chinese_eng_break("斷詞測試原始檔案.txt", "chinese_gram.txt", "english_gram.txt")
