__author__ = "Sunny"

import sys

# import DataClue.log_conf as log_conf
# sys.excepthook = log_conf.my_exception_hook

# 字典树查找关键词
# dict tree to search key words


class cNode(object):
    def __init__(self):
        self.children = ""


# word ,message: UTF-8
class tree(object):
    def __init__(self, lWords):
        self.root = ""
        self.root = cNode()
        for sWord in lWords:
            self.addWord(sWord)

    def addWord(self, word):
        node = self.root
        iEnd = len(word) - 1
        for i in range(len(word)):
            if node.children == "":
                node.children = {}
                if i != iEnd:
                    node.children[word[i]] = (cNode(), False)
                else:
                    node.children[word[i]] = (cNode(), True)
            elif word[i] not in node.children:
                if i != iEnd:
                    node.children[word[i]] = (cNode(), False)
                else:
                    node.children[word[i]] = (cNode(), True)
            else:  # word[i] in node.children:
                if i == iEnd:
                    Next, bWord = node.children[word[i]]
                    node.children[word[i]] = (Next, True)
            node = node.children[word[i]][0]

    def isContain(self, sMsg):
        root = self.root
        iLen = len(sMsg)
        for i in range(iLen):
            p = root
            j = i
            while j < iLen and p.children != "" and sMsg[j] in p.children:
                (p, bWord) = p.children[sMsg[j]]
                if bWord:
                    return sMsg[i : j + 1]
                j = j + 1
        return False


if __name__ == "__main__":
    list_word = []
    with open(
        "key_words/resume_51job/block_name_key_words.txt", "r", encoding="utf-8"
    ) as file:
        file.readline()
        for line in file:
            if line:
                list_word.append(line.strip())
    pi = tree(list_word)
    print(list_word)
    if pi.isContain("自我评价")[0]:
        print(pi.isContain("自我评"))
        print("ok")
