__author__ = "Sunny"

import re

from extrator.resume_51job.block import Block
from extrator.resume_51job.property import Property
from extrator.resume_51job.entity import Entity
from extrator.resume_51job.relation import Relation
from re_pat import std_pat_51job as pat_51
from tools import tools


class Extractor:
    def __init__(self):
        self.block = Block()
        self.property = Property()

    def __preprocessor(self, text):
        text = re.sub(r" |\xa0|\u3000", "", text)
        text_split = text.split("\n")
        text_split = list(filter(lambda x: x, text_split))  # to filter  "\n"
        text = "\n".join(text_split)
        text = tools.english_para_filter(text)  # to filter English segment
        text = tools.garbled_filter(text)  # to filter garbled segment
        return text

    def block_extractor(self, resume_file):
        """
        :param resume_file: resume files path
        :return: block result dict
        """
        if re.findall(pat_51.FILE_NAME_PAT1, resume_file):
            (name, hope_position, Resume_ID) = re.findall(
                pat_51.FILE_NAME_PAT1, resume_file
            )[0]
            address = ""
            hope_industry = ""
        elif re.findall(pat_51.FILE_NAME_PAT2, resume_file):
            (hope_position, hope_industry, address, name, Resume_ID) = re.findall(
                pat_51.FILE_NAME_PAT2, resume_file
            )[0]
        block_res = {
            "id": "51job_" + Resume_ID,
            "name": name,
            "hope_position": hope_position,
            "address": address,
            "hope_industry": hope_industry,
            "block": "",
        }
        with open(resume_file, "r", encoding="utf-8") as f:
            text = self.__preprocessor(f.read())  # to preprocess before block
            block_res["block"] = self.block.block_split(text)
        return block_res

    def prop_extractor(self, block_res):
        """
        :param block_res:  block result dict
        :return:   property extraction result dict
        """
        prop_res = self.property.extrator(block_res)
        return prop_res

    def entity_extractor(self, block_res, prop_res, idx):
        """
        :param block_res: block result dict
        :param prop_res: property extraction result dict
        :param idx: resume number
        :return: entity extraction result dict
        """
        entity = Entity()

        entity.set_data(block_res, prop_res)
        entity.set_idx(idx)
        return entity.get_extrator_res()

    def relation_extractor(self, block_res, prop_res, entity_list):
        """
        :param block_res: block result dict
        :param prop_res: property extraction result dict
        :param entity_list: entity extraction result dict
        :return: relation extraction result dict
        """
        relation = Relation()
        relation.set_data(block_res, prop_res)
        relation.set_entity_list(entity_list)
        return relation.get_extrator_res()


if __name__ == "__main__":
    e = Extractor()
    # print(e.extractor(r"../../db/docx2txt/--51job_凌权(323983767).txt"))

