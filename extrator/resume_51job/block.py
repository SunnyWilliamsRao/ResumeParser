__author__ = "Sunny"

import re
from tools.dict_tree import tree


class Block:
    def __init__(self):
        self.block_keywords = r"./tools/key_words/51job/block_name_key_words.txt"
        self.tree = self.build_tree()

    # build block keywords dict tree
    def build_tree(self):
        list_word = []
        with open(self.block_keywords, "r", encoding="utf-8") as file:
            file.readline()
            for line in file:
                if line:
                    list_word.append(line.strip())
        return tree(list_word)

    # check whether a line includes block keywords
    def check_bolck(self, line):
        line = re.sub(r" |/", "", line)  # to remove " ", '/'
        res = self.tree.isContain(line)
        if not res:  # if not contain
            return False
        # print(line)
        # if line.__contains__(":") or line.__contains__("："):  # if include ":",  it is not block keyword
        #     return False
        line = re.sub(
            r"[^\u4e00-\u9fa5|\u0041-\u005a|\u0061-\u007a]", "", line
        )  # just keep Chinese characters and English alphabet
        # print("before", res)
        if (
            not line.index(res) == 0
        ):  # remove space and other special bytes, block keywords should be start of line
            return False
        return res

        # ur[^\u4e00-\u9fa5]

    def block_split(self, text):
        """
        :param text: whole text
        :return: block result dict
        """
        block_split_res = {}
        block_keywords = ["HEADER"]
        idx = 0
        block_text = ""
        lines = text.split("\n")
        for line_count, line in enumerate(lines):
            check_res = self.check_bolck(line)
            if check_res:
                try:
                    if self.check_bolck(
                        lines[line_count + 1]
                    ):  # 　continue if next line is block keyword
                        continue
                except:
                    continue
                if (
                    check_res == "学历" and block_keywords[-1] == "最高学历学位"
                ):  # don't repeat after extracting degree information
                    block_text += line + "\n"
                    continue
                # print(check_res)
                block_keywords.append(check_res)
                idx += 1
                if (
                    idx == 1
                ):  # the first time match block keyword, then segment from that line to the first line
                    # belongs to HEADER block
                    block_split_res[block_keywords[idx - 1]] = block_text
                else:
                    block_split_res[block_keywords[idx - 1]] = block_text
                block_text = ""
                line = re.sub(
                    r"[^\u4e00-\u9fa5|\u0041-\u005a|\u0061-\u007a]", "", line
                )  # for block keywords, just keep Chinese characters and English alphabet
            block_text += (
                line + "\n"
            )  # keep "\n" in segment, and replace "\n" with 3 "&"
        else:  # get the last segment here
            block_split_res[block_keywords[idx]] = block_text
        return block_split_res


if __name__ == "__main__":
    block = Block()
    block_tree = block.build_tree()
    print(block_tree.isContain("adsda最高学历学位dasds"))
    # s = block.block_split()
    # print(s)
