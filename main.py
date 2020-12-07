__author__ = "Sunny"

import os
import re
import json

from re_pat import std_pat_51job as pat_51
from extrator.resume_51job import extrator_51job


def main():
    extractor = extrator_51job.Extractor()
    resume_path = r"./db/docx2txt"
    block_res_path = "./db/res/51job_block.json"
    property_res_path = "./db/res/51job_prop.json"
    entity_res_path = "./db/res/51job_entity.json"
    relation_res_path = "./db/res/51job_relation.json"
    idx = 0  # resume number
    for file in os.listdir(resume_path):
        if not file:
            continue
        try:
            pat_res1 = re.findall(pat_51.FILE_NAME_PAT1, file)
            pat_res2 = re.findall(pat_51.FILE_NAME_PAT2, file)
        except Exception as e:
            print(e)
        if (not pat_res1) and (not pat_res2):
            continue
        file_with_path = os.path.join(resume_path, file)
        idx += 1  # resume number
        block_res = extractor.block_extractor(file_with_path)
        # to save block result
        with open(block_res_path, "a", encoding="utf-8") as out_file1:
            json.dump(block_res, out_file1, ensure_ascii=False)
            out_file1.write("\n")
        property_res = extractor.prop_extractor(block_res["block"])
        # to save extraction result
        with open(property_res_path, "a", encoding="utf-8") as out_file2:
            json.dump(property_res, out_file2, ensure_ascii=False)
            out_file2.write("\n")
        entity_list = extractor.entity_extractor(block_res, property_res, idx)
        # to save entity extraction result
        with open(entity_res_path, "a", encoding="utf-8") as out_file3:
            for entity in entity_list:
                json.dump(entity, out_file3, ensure_ascii=False)
                out_file3.write("\n")
        # to save relation extraction result
        relation_list = extractor.relation_extractor(
            block_res, property_res, entity_list
        )
        with open(relation_res_path, "a", encoding="utf-8") as out_file4:
            for relation in relation_list:
                json.dump(relation, out_file4, ensure_ascii=False)
                out_file4.write("\n")


if __name__ == "__main__":
    main()

