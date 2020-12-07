__author__ = "Sunny"

from win32com import client as wc
import os


def doc2docx(doc_file_path, docx_file_path):
    """batch file conversion

    Arguments:
        doc_file_path {[type]} -- str
        docx_file_path {[type]} -- str
    """
    doc_abspath = os.path.abspath(doc_file_path)
    docx_abspath = os.path.abspath(docx_file_path)
    word = wc.Dispatch("Word.Application")
    doc = word.Documents.Open(doc_abspath)
    doc.SaveAs(docx_abspath, 12)
    doc.Close()
    word.Quit()


if __name__ == "__main__":
    doc_path = r"../db/doc"
    docx_path = r"../db/docx"
    for file in os.listdir(doc_path):
        doc_file_path = os.path.join(doc_path, file)
        docx_file_path = os.path.join(docx_path, file + "x")
        try:
            doc2docx(doc_file_path, docx_file_path)
            print(doc_file_path)
        except Exception as e:
            print(e)
            continue
