__author__ = "Sunny"

import os
import docx2txt

"""
model function：docx to txt

"""


def docx_parser(docx_file_path, txt_file_path):
    """
    batch file conversion

    :param docx_file_path: path where docx files are
    :param txt_file_path: path where result txt files want to save
    :return: none
    """
    f = open(txt_file_path, "a", encoding="utf-8", errors="ignore")
    text = docx2txt.process(docx_file_path)
    text = text.replace("\t", "")
    for line in filter(lambda x: x is not "", text.split("\n")):
        f.write(line)
        f.write("\n")
    f.close()


if __name__ == "__main__":
    docx_path = "../db/docx"
    txt_path = "../db/docx2txt"
    if not os.path.exists(txt_path):
        os.mkdir(txt_path)
    for docx in os.listdir(docx_path):

        docx_file_path = os.path.join(docx_path, docx)
        txt_file_path = os.path.join(txt_path, docx[:-5] + ".txt")
        try:
            docx_parser(docx_file_path, txt_file_path)
        except:
            continue

