__author__ = 'Sunny'

import copy
import re

from extrator.resume_51job.block import Block
from extrator.resume_51job.property import Property
from extrator.resume_51job.entity import Entity
from tools import tools

# relation extraction class
# 简历人手机、简历人邮箱、简历人QQ、简历人微信、家庭地址、家庭电话、教育经历、学校地址
# 工作经验、公司地址、应聘、参加培训、项目经历、校内荣誉、校内职务、在校实践经验
class Relation:
    def __init__(self):
        self.__RELATION_LIST = []
        self.__entity_list = []
        self.__block_res = ""
        self.__property_res = ""
        self.__TIME_PAT = re.compile(r"(?P<src_time>[\d]{4}-[\d]{2}-[\d]{2})", re.S)

    def set_entity_list(self, entity_list):
        self.__entity_list = entity_list

    def set_data(self, block_res, property_res):
        self.__block_res = block_res
        self.__property_res = property_res

    def get_extrator_res(self):
        # to get  relation extraction result
        self.__RELATION_LIST.extend(self.get_Person_Phone(self.__block_res, self.__property_res))
        self.__RELATION_LIST.extend(self.get_Person_Eml(self.__block_res, self.__property_res))
        self.__RELATION_LIST.extend(self.get_Person_QQ(self.__block_res, self.__property_res))
        self.__RELATION_LIST.extend(self.get_Person_Wechat(self.__block_res, self.__property_res))
        self.__RELATION_LIST.extend(self.get_Home_Adress(self.__block_res, self.__property_res))
        self.__RELATION_LIST.extend(self.get_Home_Tel(self.__block_res, self.__property_res))
        self.__RELATION_LIST.extend(self.get_Education_Exp(self.__block_res, self.__property_res))
        self.__RELATION_LIST.extend(self.get_School_Address(self.__block_res, self.__property_res))
        self.__RELATION_LIST.extend(self.get_Company_Adress(self.__block_res, self.__property_res))
        self.__RELATION_LIST.extend(self.get_Apply(self.__block_res, self.__property_res))
        self.__RELATION_LIST.extend(self.get_Attend_Training(self.__block_res, self.__property_res))
        self.__RELATION_LIST.extend(self.get_Project_Exp(self.__block_res, self.__property_res))
        self.__RELATION_LIST.extend(self.get_School_Honor(self.__block_res, self.__property_res))
        self.__RELATION_LIST.extend(self.get_School_Function(self.__block_res, self.__property_res))
        self.__RELATION_LIST.extend(self.get_School_Practice_Exp(self.__block_res, self.__property_res))
        return self.__RELATION_LIST

    def __get_person_entity(self, entity_list):
        for entity in entity_list:
            if entity["type"] == "person":
                return entity
        return {}

    # check whether time1 include time2
    def during_time(self, time1, time2):
        time1 = tools.format_time(time1)
        time2 = tools.format_time(time2)
        PAT1 = re.compile(r"(?P<year_s>[\d]{4})年(?P<month_s>\d{1,2})月(?P<day_s>\d{1,2})?日?-(?P<year_e>[\d]{4})年(?P<month_e>\d{1,2})月(?P<day_e>\d{1,2})?日?", re.S)
        PAT2 = re.compile(r"(?P<year_s>[\d]{4})年(?P<month_s>\d{1,2})月(?P<day_s>\d{1,2})?日?", re.S)
        # PAT = re.compile(r"(?P<year_s>[\d]{4})年(?P<month_s>\d{2})月(?P<day_s>\d{2})?日?", re.S)
        if time1.__contains__("-") and not time2.__contains__("-"):
            res1 = re.search(PAT1, time1)
            res2 = re.search(PAT2, time2)
            if int(res1.group("year_e")) > int(res2.group("year_s")):
                return False
            else:
                if int(res1.group("month_e")) > int(res2.group("month_s")):
                    return False
                else:
                    if res1.group("day_e") and res2.group("day_s"):
                        if int(res1.group("day_s")) > int(res2.group("day_s")):
                            return False
        elif not time1.__contains__("-") and time2.__contains__("-"):
            res1 = re.search(PAT2, time1)
            res2 = re.search(PAT1, time2)
            if int(res1.group("year_s")) < int(res2.group("year_s")):
                return False
            else:
                if int(res1.group("month_s")) < int(res2.group("month_s")):
                    return False
                else:
                    if res1.group("day_s") and res2.group("day_s"):
                        if int(res1.group("day_s")) < int(res2.group("day_s")):
                            return False
            if int(res1.group("year_s")) > int(res2.group("year_e")):
                return False
            else:
                if int(res1.group("month_s")) > int(res2.group("month_e")):
                    return False
                else:
                    if res1.group("day_s") and res2.group("day_e"):
                        if int(res1.group("day_s")) > int(res2.group("day_e")):
                            return False
        elif time1.__contains__("-") and time2.__contains__("-"):
            res1 = re.search(PAT1, time1)
            res2 = re.search(PAT1, time2)
            if int(res1.group("year_s")) < int(res2.group("year_s")):
                return False
            elif int(res1.group("year_s")) == int(res2.group("year_s")):
                if int(res1.group("month_s")) < int(res2.group("month_s")):
                    return False
                elif int(res1.group("month_s")) == int(res2.group("month_s")):
                    if res1.group("day_s") and res2.group("day_s"):
                        if int(res1.group("day_s")) < int(res2.group("day_s")):
                            return False
            if int(res1.group("year_e")) > int(res2.group("year_e")):
                return False
            elif int(res1.group("year_e")) == int(res2.group("year_e")):
                if int(res1.group("month_e")) > int(res2.group("month_e")):
                    return False
                elif int(res1.group("month_e")) == int(res2.group("month_e")):
                    if res1.group("day_e") and res2.group("day_e"):
                        if int(res1.group("day_e")) > int(res2.group("day_e")):
                            return False
        else:
            print("time", time1, time2)
            res1 = re.search(PAT2, time1)
            res2 = re.search(PAT2, time2)
            if int(res1.group("year_s")) > int(res2.group("year_s")):
                return False
            else:
                if int(res1.group("month_s")) > int(res2.group("month_s")):
                    return False
                else:
                    if res1.group("day_s") and res2.group("day_s"):
                        if int(res1.group("day_s")) > int(res2.group("day_s")):
                            return False
        return True


    def get_Person_Phone(self, block_res, property_res):
        '''
        :param block_res: block result dict
        :param property_res: property extraction result dict
        :return: "简历人手机" relation extraction result dict
        '''
        for entity in self.__entity_list:
            if entity["type"] == "tel":
                Person_Phone = copy.deepcopy(PERSON_PHONE)
                Person_Phone["from_node"] = self.__get_person_entity(self.__entity_list)["iri"]
                Person_Phone["to_node"] = entity["iri"]
                if "简历评语" in block_res and re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time"):
                     src_time = re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time")
                     Person_Phone["关联时间"] = src_time.split("-")[0] + "年" + src_time.split("-")[1] + "月" + src_time.split("-")[2] + "日"
                else:
                    Person_Phone["关联时间"] = "2018年1月"
                return [Person_Phone]
        return []



    def get_Person_Eml(self, block_res, property_res):
        # "简历人邮箱"
        for entity in self.__entity_list:
            if entity["type"] == "eml":
                Person_Eml = copy.deepcopy(PERSON_EML)
                Person_Eml["from_node"] = self.__get_person_entity(self.__entity_list)["iri"]
                Person_Eml["to_node"] = entity["iri"]
                if "简历评语" in block_res and re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time"):
                     src_time = re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time")
                     Person_Eml["关联时间"] = src_time.split("-")[0] + "年" + src_time.split("-")[1] + "月" + src_time.split("-")[2] + "日"
                else:
                    Person_Eml["关联时间"] = "2018年1月"
                return [Person_Eml]
        return []

    def get_Person_QQ(self, block_res, property_res):
        # "简历人QQ"
        for entity in self.__entity_list:
            if entity["type"] == "QQ":
                Person_Qq = copy.deepcopy(PERSON_QQ)
                Person_Qq["from_node"] = self.__get_person_entity(self.__entity_list)["iri"]
                Person_Qq["to_node"] = entity["iri"]
                if "简历评语" in block_res and re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time"):
                     src_time = re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time")
                     Person_Qq["关联时间"] = src_time.split("-")[0] + "年" + src_time.split("-")[1] + "月" + src_time.split("-")[2] + "日"
                else:
                    Person_Qq["关联时间"] = "2018年1月"
        return []

    def get_Person_Wechat(self, block_res, property_res):
        # "简历人微信"
        for entity in self.__entity_list:
            if entity["type"] == "wechat":
                Person_Wechat = copy.deepcopy(PERSON_WECHAT)
                Person_Wechat["from_node"] = self.__get_person_entity(self.__entity_list)["iri"]
                Person_Wechat["to_node"] = entity["iri"]
                if "简历评语" in block_res and re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time"):
                     src_time = re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time")
                     Person_Wechat["关联时间"] = src_time.split("-")[0] + "年" + src_time.split("-")[1] + "月" + src_time.split("-")[2] + "日"
                else:
                    Person_Wechat["关联时间"] = "2018年1月"
        return []

    def get_Home_Adress(self, block_res, property_res):
        # "家庭地址"
        for entity in self.__entity_list:
            if entity["type"] == "address" and entity["iri"].endswith("_01"):  # 后缀_01是家庭地址
                Home_Adress = copy.deepcopy(HOME_ADDRESS)
                Home_Adress["from_node"] = self.__get_person_entity(self.__entity_list)["iri"]
                Home_Adress["to_node"] = entity["iri"]
                if "简历评语" in block_res and re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time"):
                     src_time = re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time")
                     Home_Adress["关联时间"] = src_time.split("-")[0] + "年" + src_time.split("-")[1] + "月" + src_time.split("-")[2] + "日"
                else:
                    Home_Adress["关联时间"] = "2018年1月"
        return []

    def get_Home_Tel(self, block_res, property_res):
        # "家庭电话"
        for entity in self.__entity_list:
            if entity["type"] == "home_tel":
                Home_Tel = copy.deepcopy(HOME_TEL)
                Home_Tel["from_node"] = self.__get_person_entity(self.__entity_list)["iri"]
                Home_Tel["to_node"] = entity["iri"]
                if "简历评语" in block_res and re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time"):
                     src_time = re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time")
                     Home_Tel["关联时间"] = src_time.split("-")[0] + "年" + src_time.split("-")[1] + "月" + src_time.split("-")[2] + "日"
                else:
                    Home_Tel["关联时间"] = "2018年1月"
        return []

    def get_Education_Exp(self, block_res, property_res):
        # "教育经历"
        education_exp_list = []
        if "教育经历" in property_res.keys():
            for one_dict in property_res["教育经历"]:
                try:
                    Education_Exp = copy.deepcopy(EDUCATION_EXP)
                    Education_Exp["受教育时间"] = one_dict["educated_period"]
                    Education_Exp["学历/学位"] = one_dict["degree"]
                    Education_Exp["所学专业"] =one_dict["major"]
                    Education_Exp["招生性质"] = "" ###暂时未发现招生性质信息
                except:
                    continue
                try:
                    Education_Exp["专业描述"] = one_dict["major_description"]
                except:
                    pass
                to_node_iri = [entity["iri"] for entity in self.__entity_list
                               if entity["type"] == "school" and (entity["学校名称"] == one_dict["school_name"])]
                # print(self.__entity_list)
                Education_Exp["from_node"] = self.__get_person_entity(self.__entity_list)["iri"]
                Education_Exp["to_node"] = to_node_iri[0]
                if "简历评语" in block_res and re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time"):
                    src_time = re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time")
                    Education_Exp["关联时间"] = src_time.split("-")[0] + "年" + src_time.split("-")[1] + "月" + src_time.split("-")[2] + "日"
                else:
                    Education_Exp["关联时间"] = "2018年1月"
                education_exp_list.append(Education_Exp)
        return education_exp_list

    def get_Work_Exp(self, block_res, property_res):
        # "工作经验"
        res_list = []
        for entity in self.__entity_list:
            if entity["type"] == "company" and entity["iri"].split("_")[-2] == "02":
                Work_Exp = copy.deepcopy(WORK_EXP)
                Work_Exp["from_node"] = self.__get_person_entity(self.__entity_list)["iri"]
                Work_Exp["to_node"] = entity["iri"]
                for exp in property_res["工作经验"]:
                    if exp["company_name"] == entity["公司名称"]:
                        Work_Exp["工作职位"] = exp["work_position"]
                        Work_Exp["工作时间"] = exp["work_period"]
                        Work_Exp["工作时长"] = exp["work_duration"]
                        Work_Exp["工作部门"] = exp["department"]
                        Work_Exp["工作描述"] = exp["work_description"]
                        Work_Exp["下属人数"] = exp["company_capacity"]
                res_list.append(Work_Exp)
        return res_list

    def get_School_Address(self, block_res, property_res):
        # "学校地址"
        return []

    def get_Company_Adress(self, block_res, property_res):
        # "公司地址"
        return []

    def get_Apply(self, block_res, property_res):
        # "应聘"
        return []

    def get_Attend_Training(self, block_res, property_res):
        # "参加培训"
        res_list = []
        for entity in self.__entity_list:
            if entity["type"] == "company" and entity["iri"].split("_")[-2] == "03":
                Attend_Training = copy.deepcopy(ATTEND_TRAINING)
                Attend_Training["from_node"] = self.__get_person_entity(self.__entity_list)["iri"]
                Attend_Training["to_node"] = entity["iri"]
                for exp in property_res["培训经历"]:
                    if exp["training_organization"] == entity["公司名称"]:
                        Attend_Training["培训时间"] = exp["training_period"]
                        Attend_Training["培训课程"] = exp["training_courses"]
                        Attend_Training["培训地点"] = exp["training_address"]
                        Attend_Training["培训描述"] = exp["training_description"]
                res_list.append(Attend_Training)
        return res_list

    def get_Project_Exp(self, block_res, property_res):
        # "项目经历"
        res_list = []
        for entity in self.__entity_list:
            if entity["type"] == "company" and entity["iri"].split("_")[-2] == "04":
                Project_Exp = copy.deepcopy(PROJECT_EXP)
                Project_Exp["from_node"] = self.__get_person_entity(self.__entity_list)["iri"]
                Project_Exp["to_node"] = entity["iri"]
                for exp in property_res["项目经历"]:
                    if exp["company"] == entity["公司名称"]:
                        Project_Exp["项目时间"] = exp["project_period"]
                        Project_Exp["项目类型"] = exp["project_type"]
                        Project_Exp["责任描述"] = exp["duty_description"]
                        Project_Exp["项目描述"] = exp["project_description"]
                res_list.append(Project_Exp)
        return res_list

    def get_School_Honor(self, block_res, property_res):
        # "校内荣誉"
        school_honor_list = []
        if "校内荣誉" in property_res.keys():
            for one_dict in property_res["校内荣誉"]:
                School_Honor = copy.deepcopy(SCHOOL_HONOR)
                School_Honor["获荣誉时间"] = one_dict["honor_time"]
                School_Honor["奖项"] = one_dict["prize"]
                try:
                    School_Honor["级别"] =one_dict["level"]
                except:
                    pass
                school_name = ""
                for edu_experience in property_res["教育经历"]:
                    if self.during_time(one_dict["honor_time"],edu_experience["educated_period"]):
                        school_name = edu_experience["school_name"]

                to_node_iri = [entity["iri"] for  entity in  self.__entity_list
                               if entity["type"] == "school" and  entity["学校名称"] == school_name]
                if not to_node_iri:
                    return []
                School_Honor["from_node"] = self.__get_person_entity(self.__entity_list)["iri"]
                School_Honor["to_node"] = to_node_iri[0]
                if "简历评语" in block_res and re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time"):
                    src_time = re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time")
                    School_Honor["关联时间"] = src_time.split("-")[0] + "年" + src_time.split("-")[1] + "月" + src_time.split("-")[2] + "日"
                else:
                    School_Honor["关联时间"] = "2018年1月"
                school_honor_list.append(School_Honor)
        return school_honor_list

    def get_School_Function(self, block_res, property_res):
        # "校内职务"
        school_function_list = []
        if "校内职务" in property_res.keys():
            for one_dict in property_res["校内职务"]:
                School_Function = copy.deepcopy(SCHOOL_FUNCTION)
                School_Function["职务时间"] = one_dict["function_period"]
                School_Function["职务"] = one_dict["function"]
                try:
                    School_Function["职务描述"] = one_dict["function_description"]
                except:
                    pass
                school_name = ""
                for edu_experience in property_res["教育经历"]:
                    if self.during_time(one_dict["function_period"], edu_experience["educated_period"]):
                        school_name = edu_experience["school_name"]
                to_node_iri = [entity["iri"] for entity in self.__entity_list
                               if entity["type"] == "school" and entity["学校名称"] == school_name]
                if not to_node_iri:
                    return []
                School_Function["from_node"] = self.__get_person_entity(self.__entity_list)["iri"]
                School_Function["to_node"] = to_node_iri[0]
                if "简历评语" in block_res and re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time"):
                    src_time = re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time")
                    School_Function["关联时间"] = src_time.split("-")[0] + "年" + src_time.split("-")[1] + "月" + \
                                           src_time.split("-")[2] + "日"
                else:
                    School_Function["关联时间"] = "2018年1月"
                school_function_list.append(School_Function)
        return school_function_list

    def get_School_Practice_Exp(self, block_res, property_res):
        # "在校实践经验"
        school_practice_exp_list = []
        if "学生实践经验" in  property_res.keys():
            for one_dict in property_res["学生实践经验"]:
                School_Practice_Exp = copy.deepcopy(SCHOOL_PRACTICE_EXP)
                School_Practice_Exp["实践时间"] = one_dict["practice_period"]
                School_Practice_Exp["实践内容"] = one_dict["practice_content"]
                School_Practice_Exp["实践描述"] = one_dict["practice_description"]

                school_name = ""
                for edu_experience in property_res["教育经历"]:
                    try:
                        if self.during_time(one_dict["practice_period"], edu_experience["educated_period"]):
                            school_name = edu_experience["school_name"]
                    except:
                        print(one_dict["practice_period"], edu_experience["educated_period"])

                to_node_iri = [entity["iri"] for entity in self.__entity_list
                               if entity["type"] == "school" and entity["学校名称"] == school_name]
                School_Practice_Exp["from_node"] = self.__get_person_entity(self.__entity_list)["iri"]
                School_Practice_Exp["to_node"] = to_node_iri[0]
                if "简历评语" in block_res and re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time"):
                    src_time = re.search(self.__TIME_PAT, block_res["简历评语"]).group("src_time")
                    School_Practice_Exp["关联时间"] = src_time.split("-")[0] + "年" + src_time.split("-")[1] + "月" + \
                                           src_time.split("-")[2] + "日"
                else:
                    School_Practice_Exp["关联时间"] = "2018年1月"
                school_practice_exp_list.append(School_Practice_Exp)
        return school_practice_exp_list


PERSON_PHONE = {
    "rel_iri": "http://ontology/relation/access#简历人手机",
    "from_node": "null",
    "to_node": "null",
    "关联时间": "null",
    "关联来源": "null",
}
PERSON_EML = {
    "rel_iri": "http://ontology/relation/access#简历人邮箱",
    "from_node": "null",
    "to_node": "null",
    "关联时间": "null",
    "关联来源": "null",
}
PERSON_QQ = {
    "rel_iri": "http://ontology/relation/access#简历人QQ",
    "from_node": "null",
    "to_node": "null",
    "关联时间": "null",
    "关联来源": "null",
}
PERSON_WECHAT = {
    "rel_iri": "http://ontology/relation/access#简历人手机",
    "from_node": "null",
    "to_node": "null",
    "关联时间": "null",
    "关联来源": "null",
}
HOME_ADDRESS = {
    "rel_iri": "http://ontology/relation/access#简历人微信",
    "from_node": "null",
    "to_node": "null",
    "关联时间": "null",
    "关联来源": "null",
}
HOME_TEL = {
    "rel_iri": "http://ontology/relation/access#家庭地址",
    "from_node": "null",
    "to_node": "null",
    "关联时间": "null",
    "关联来源": "null",
}
EDUCATION_EXP = {
    "rel_iri": "http://ontology/relation/access#教育经历",
    "from_node": "null",
    "to_node": "null",
    "受教育时间": "null",
    "学历/学位": "null",
    "招生性质": "null",
    "所学专业": "null",
    "专业描述": "null",

}
WORK_EXP = {
    "rel_iri": "http://ontology/relation/access#工作经验",
    "from_node": "null",
    "to_node": "null",
    "工作职位": "null",
    "工作时间": "null",
    "工作时长": "null",
    "工作月薪": "null",
    "工作部门": "null",
    "工作描述": "null",
    "下属人数": "null",
    "汇报对象": "null",
    "离职原因": "null",
    "主要业绩": "null",
}
SCHOOL_ADDRESS = {
    "rel_iri": "http://ontology/relation/access#学校地址",
    "from_node": "null",
    "to_node": "null",
}
COMPANY_ADDRESS = {
    "rel_iri": "http://ontology/relation/access#公司地址",
    "from_node": "null",
    "to_node": "null",
}
APPLY = {
    "rel_iri": "http://ontology/relation/access#应聘",
    "from_node": "null",
    "to_node": "null",
    "投递时间": "null",
    "应聘职位": "null",
    "简历匹配": "null",
}
ATTEND_TRAINING = {
    "rel_iri": "http://ontology/relation/access#参加培训",
    "from_node": "null",
    "to_node": "null",
    "培训时间": "null",
    "培训课程": "null",
    "所获证书": "null",
    "培训地点": "null",
    "培训描述": "null",
}
PROJECT_EXP = {
    "rel_iri": "http://ontology/relation/access#项目经历",
    "from_node": "null",
    "to_node": "null",
    "项目时间": "null",
    "项目类型": "null",
    "项目描述": "null",
    "项目职务": "null",
    "责任描述": "null",
    "项目业绩": "null",
}
SCHOOL_HONOR = {
    "rel_iri": "http://ontology/relation/access#校内荣誉",
    "from_node": "null",
    "to_node": "null",
    "获荣誉时间": "null",
    "奖项": "null",
    "级别": "null",
}
SCHOOL_FUNCTION = {
    "rel_iri": "http://ontology/relation/access#校内职务",
    "from_node": "null",
    "to_node": "null",
    "职务时间": "null",
    "职务": "null",
    "职务描述": "null",
}
SCHOOL_PRACTICE_EXP = {
    "rel_iri": "http://ontology/relation/access#在校实践经验",
    "from_node": "null",
    "to_node": "null",
    "实践时间": "null",
    "实践内容": "null",
    "实践描述": "null",
}

if __name__ == '__main__':
    # PAT = re.compile(r"(?P<year_s>[\d]{4})年(?P<month_s>\d{2})月(?P<day_s>\d{2})?日?-(?P<year_e>[\d]{4})年(?P<month_e>\d{2})月(?P<day_e>\d{2})?日?", re.S)
    # print(re.search(PAT, "2012年01月-2012年03月").group("year_e"))
    r = Relation()
    # print(r.during_time("2011/10-2012/10","2011/10-2012/11"))
    # print(r.during_time("2011/10-2012/10","2011/10-2012/9"))
    # print(r.during_time("2011/10", "2011/10-2012/11"))
    # print(r.during_time("2012/12","2011/10-2012/11"))
    # print(r.during_time("2011/10-2012/10", "2012/10"))
    # print(r.during_time("2011/10-2012/10", "2012/9"))
    # print(r.during_time("2011/10", "2012/9"))
    print(r.during_time("2013/9--2014/12", "'2012/9--2016/7"))
