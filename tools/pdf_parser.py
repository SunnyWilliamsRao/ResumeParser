import sys
import importlib

importlib.reload(sys)
import os
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


"""
model function：pdf to txt

"""


def pdf_parser(pdf_file_path, txt_file_path):
    """
    :param pdf_file_path: path where pdf files are
    :param txt_file_path: path where result txt files want to save
    :return: None
    """
    fp = open(pdf_file_path, "rb")  # mode "rb" to read input file
    # create a pdf parser
    praser = PDFParser(fp)
    # create a empty pdf file handler
    doc = PDFDocument()
    # link pdf parser and pdf file handler
    praser.set_document(doc)
    doc.set_parser(praser)

    # apply init password
    # if no password, create a empty string
    doc.initialize()

    # chcek wheather file coule be converted to txt
    # True, continue; False over
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # create PDF Resource Manager
        rsrcmgr = PDFResourceManager()
        # create PDF device Manager
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # create PDFPageInterpreter
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        f = open(txt_file_path, "a", encoding="utf-8", errors="ignore")
        # pages loop
        for page in doc.get_pages():  # docx.get_pages()
            interpreter.process_page(page)
            layout = device.get_result()
            # layout is a LTPage object, which includes all parse results, such as LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal
            for x in layout:
                if isinstance(x, LTTextBoxHorizontal):
                    results = x.get_text()
                    f.write(results.strip())
                    f.write("\n")
        f.close()
    fp.close()


if __name__ == "__main__":
    pdf_path = r"../db/pdf"
    txt_path = "../db/pdf2txt"
    if not os.path.exists(txt_path):
        os.mkdir(txt_path)
    for pdf in os.listdir(pdf_path):
        pdf_file_path = os.path.join(pdf_path, pdf)
        txt_file_path = os.path.join(txt_path, pdf[:-4] + ".txt")
        try:
            pdf_parser(pdf_file_path, txt_file_path)
            print(pdf_file_path)
        except Exception as e:
            # os.remove(pdf_file_path)  # 出错的文件就删掉
            print(e)
            continue
