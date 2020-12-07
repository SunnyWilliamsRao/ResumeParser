__author__ = "Sunny"

from extrator.resume_51job.block import Block
from extrator.resume_51job.property import Property
import copy


# entity extraction class
# person、QQ、wechat、eml、tel、home_tel
# address、school、company


class Entity:
    def __init__(self):
        self.__ontology = "http://ontology/"
        self.__resume_name = "4_"
        self.__Entity_List = []
        self.__resume_idx = 0
        self.__block_res = ""
        self.__property_res = ""

    # set resume number
    def set_idx(self, idx):
        self.__resume_idx = idx

    def set_data(self, block_res, property_res):
        self.__block_res = block_res
        self.__property_res = property_res

    # create entity iri (for KG)
    def get_iri(self, entity_type):  # ontology + iri_list_1[l]+ '#' + resume_name + num
        return (
            self.__ontology
            + entity_type
            + "#"
            + self.__resume_name
            + str(self.__resume_idx).zfill(8)
        )

    def get_extrator_res(self):
        # to get entity extration result dict
        self.__Entity_List.extend(
            self.get_Person(self.__block_res, self.__property_res)
        )
        self.__Entity_List.extend(self.get_Tel(self.__block_res, self.__property_res))
        self.__Entity_List.extend(self.get_Eml(self.__block_res, self.__property_res))
        self.__Entity_List.extend(self.get_QQ(self.__block_res, self.__property_res))
        self.__Entity_List.extend(
            self.get_Wechat(self.__block_res, self.__property_res)
        )
        self.__Entity_List.extend(
            self.get_Company(self.__block_res, self.__property_res)
        )
        self.__Entity_List.extend(
            self.get_Home_tel(self.__block_res, self.__property_res)
        )
        self.__Entity_List.extend(
            self.get_Address(self.__block_res, self.__property_res)
        )
        self.__Entity_List.extend(
            self.get_School(self.__block_res, self.__property_res)
        )

        return self.__Entity_List

    def get_Person(self, block_res, property_res):
        # Person entity
        """
        :param block_res:  block result dict
        :param property_res:  property extratcion result dict
        :return: Person entity dict
        """
        Person = copy.deepcopy(PERSON)  # deepcopy
        property_res_keys = property_res.keys()

        Person["iri"] = self.get_iri(Person["type"])

        if block_res["name"]:
            Person["姓名"] = block_res["name"]
        else:
            if "name" in property_res["HEADER"]:
                Person["姓名"] = property_res["HEADER"]["name"]

        if block_res["id"]:
            Person["ID"] = block_res["id"].lstrip("51job_")
        else:
            if "id" in property_res["HEADER"]:
                Person["ID"] = property_res["HEADER"]["id"]

        if block_res["hope_position"]:
            Person["期望职能"] = block_res["hope_position"]
        else:
            if "function" in property_res["HEADER"]:
                Person["期望职能"] = property_res["HEADER"]["hope_function"]
        if "work" in property_res["HEADER"]:
            Person["工作年限"] = property_res["HEADER"]["work"]

        if "gender" in property_res["HEADER"]:
            Person["性别"] = property_res["HEADER"]["gender"]
        if "age" in property_res["HEADER"]:
            Person["年龄"] = property_res["HEADER"]["age"]
        if "birthday" in property_res["HEADER"]:
            Person["出生日期"] = property_res["HEADER"]["birthday"]

        if "个人信息" in property_res_keys:
            if "household_country" in property_res["个人信息"]:
                Person["户口/国籍"] = property_res["个人信息"]["household_country"]
            if "height" in property_res["个人信息"]:
                Person["身高"] = property_res["个人信息"]["height"]
            if "marital_status" in property_res["个人信息"]:
                Person["婚姻状况"] = property_res["个人信息"]["marital_status"]
            if "political" in property_res["个人信息"]:
                Person["政治面貌"] = property_res["个人信息"]["political"]

        # TODO '证件号'
        # TODO '个人主页'
        # TODO '个人主页'
        if "自我评价" in property_res_keys:
            if "self_evalution" in property_res["自我评价"]:
                Person["自我评价"] = property_res["自我评价"]["self_evalution"]
        if block_res["hope_industry"]:
            Person["期望行业"] = block_res["hope_industry"]
        else:
            if "求职意向" in property_res_keys:
                if "hope_industry" in property_res["求职意向"]:
                    Person["期望行业"] = property_res["求职意向"]["hope_industry"]
        if "求职意向" in property_res_keys:
            if "hope_salary" in property_res["求职意向"]:
                Person["期望薪资"] = property_res["求职意向"]["hope_salary"]
            if "job_type" in property_res["求职意向"]:
                Person["工作类型"] = property_res["求职意向"]["job_type"]
        if "目前薪资" in property_res_keys:
            if "current_salary" in property_res["目前薪资"]:
                Person["目前薪资"] = property_res["目前薪资"]["current_salary"]
        if "目前年收入" in property_res_keys and Person["目前薪资"] == "null":
            if "current_salary" in property_res["目前年收入"]:
                Person["目前薪资"] = property_res["目前年收入"]["current_salary"]
        if "技能语言" in property_res_keys:
            if "speciality" in property_res["技能语言"]:
                Person["技能/语言"] = property_res["技能语言"]["speciality"]
        # TODO '兴趣爱好'
        # TODO '特长'  目前技能语言也算作特长
        if "技能语言" in property_res_keys:
            if "speciality" in property_res["技能语言"]:
                Person["特长"] = property_res["技能语言"]["speciality"]
        # TODO '职业目标'
        # TODO '特殊技能'
        # TODO '社会活动'
        if "校内荣誉" in property_res_keys:
            Person["荣誉"] = block_res["block"]["校内荣誉"].lstrip("校内荣誉\n")
        # TODO '宗教信仰'
        # TODO '推荐信'
        # TODO '专利'
        # TODO '获得荣誉' 获得荣誉与荣誉取值一样
        if "校内荣誉" in property_res_keys:
            Person["获得荣誉"] = block_res["block"]["校内荣誉"].lstrip("校内荣誉\n")
        # 统一返回列表
        return [Person]

    def get_Tel(self, block_res, property_res):
        # HEADER
        Tel = copy.deepcopy(TEL)
        property_res_keys = property_res.keys()

        Tel["iri"] = self.get_iri(Tel["type"])
        if "HEADER" in property_res_keys:
            if "tel" in property_res["HEADER"]:
                Tel["手机号"] = property_res["HEADER"]["tel"]
        return [Tel]

    def get_Eml(self, block_res, property_res):
        # HEADR
        Eml = copy.deepcopy(EML)
        property_res_keys = property_res.keys()

        Eml["iri"] = self.get_iri(Eml["type"])
        if "HEADER" in property_res_keys:
            if "eml" in property_res["HEADER"]:
                Eml["邮箱"] = property_res["HEADER"]["eml"]
        return [Eml]

    def get_QQ(self, block_res, property_res):
        # "个人信息"
        Qq = copy.deepcopy(QQ)
        property_res_keys = property_res.keys()

        Qq["iri"] = self.get_iri(Qq["type"])
        if "个人信息" in property_res_keys:
            if "QQ" in property_res["个人信息"]:
                Qq["QQ号"] = property_res["个人信息"]["QQ"]
        return [Qq]

    def get_Wechat(self, block_res, property_res):
        # "个人信息"
        Wechat = copy.deepcopy(WECHAT)
        property_res_keys = property_res.keys()

        Wechat["iri"] = self.get_iri(Wechat["type"])
        if "个人信息" in property_res_keys:
            if "wechat" in property_res["个人信息"]:
                Wechat["微信号"] = property_res["个人信息"]["wechat"]
        return [Wechat]

    def get_School(self, block_res, property_res):
        property_res_keys = property_res.keys()
        school_list = []
        if "教育经历" in property_res_keys:
            try:
                for one_dict in property_res["教育经历"]:
                    School = copy.deepcopy(SCHOOL)
                    School["学校名称"] = one_dict["school_name"]
                    School["iri"] = self.get_iri(School["type"])
                    if ("最高学历学位" in property_res_keys) and (
                        School["学校名称"] == property_res["最高学历学位"]["school_name"]
                    ):
                        School["iri"] = School["iri"] + "_01"
                    school_list.append(School)
            except Exception as e:
                print(
                    "(%s)(%s)中未提取信息行: " % (str(e.__class__.__name__), "教育经历")
                    + str(one_dict)
                )

        return school_list

    def get_Company(self, block_res, property_res):
        property_res_keys = property_res.keys()
        return_list = []
        if "最近工作" in property_res_keys:
            Company = copy.deepcopy(COMPANY)
            Company["iri"] = self.get_iri(Company["type"]) + "_01"
            if "company_name" in property_res["最近工作"]:
                Company["公司名称"] = property_res["最近工作"]["company_name"]
            if "hope_industry" in property_res["最近工作"]:
                Company["公司所属行业"] = property_res["最近工作"]["hope_industry"]
            return_list.append(Company)
        if "工作经验" in property_res_keys:
            num = 0
            for exp in property_res["工作经验"]:
                num += 1
                Company = copy.deepcopy(COMPANY)  # 公司实体深复制
                Company["iri"] = self.get_iri(Company["type"]) + "_02" + str(num)
                if "company_name" in exp:
                    Company["公司名称"] = exp["company_name"]
                if "company_industry" in exp:
                    Company["公司所属行业"] = exp["company_industry"]
                if "company_capacity" in exp:
                    Company["公司规模"] = exp["company_capacity"]
                if "company_type" in exp:
                    Company["公司类型"] = exp["home_tel"]
                if "company_tel" in exp:
                    Company["公司电话"] = exp["company_tel"]
                return_list.append(Company)
        if "培训经历" in property_res_keys:
            num = 0
            for exp in property_res["培训经历"]:
                num += 1
                Company = copy.deepcopy(COMPANY)
                Company["iri"] = self.get_iri(Company["type"]) + "_03" + str(num)
                if "training_organization" in exp:
                    Company["公司名称"] = exp["training_organization"]
                return_list.append(Company)
        if "项目经验" in property_res_keys:
            num = 0
            for exp in property_res["项目经验"]:
                num += 1
                Company = copy.deepcopy(COMPANY)
                Company["iri"] = self.get_iri(Company["type"]) + "_04" + str(num)
                if "所属公司" not in exp:
                    continue
                if "company" in exp:
                    Company["公司名称"] = exp["company"]
                return_list.append(Company)
        return return_list

    def get_Home_tel(self, block_res, property_res):
        # “个人信息”
        Home_tel = copy.deepcopy(HOME_TEL)
        property_res_keys = property_res.keys()

        Home_tel["iri"] = self.get_iri(Home_tel["type"])
        if "个人信息" in property_res_keys:
            if "home_tel" in property_res["个人信息"]:
                Home_tel["地址"] = property_res["个人信息"]["home_tel"]
        return [Home_tel]

    def get_Address(self, block_res, property_res):
        Address = copy.deepcopy(HOME_TEL)
        property_res_keys = property_res.keys()

        Address["iri"] = self.get_iri(Address["type"]) + "_01"
        if "个人信息" in property_res_keys:
            if "address" in property_res["个人信息"]:
                Address["家庭电话"] = property_res["个人信息"]["address"]
        return [Address]


PERSON = {
    "iri": "null",
    "type": "person",
    "ID": "null",
    "姓名": "null",
    "性别": "null",
    "年龄": "null",
    "出生日期": "null",
    "户口/国籍": "null",
    "身高": "null",
    "婚姻状况": "null",
    "政治面貌": "null",
    "工作年限": "null",
    "证件号": "null",
    "个人主页": "null",
    "个人标签": "null",
    "自我评价": "null",
    "期望薪资": "null",
    "期望职能": "null",
    "期望行业": "null",
    "工作类型": "null",
    "目前薪资": "null",
    "技能/语言": "null",
    "兴趣爱好": "null",
    "特长": "null",
    "职业目标": "null",
    "特殊技能": "null",
    "社会活动": "null",
    "荣誉": "null",
    "宗教信仰": "null",
    "推荐信": "null",
    "专利": "null",
    "获得荣誉": "null",
}
TEL = {"iri": "null", "type": "tel", "手机号": "null"}
EML = {"iri": "null", "type": "eml", "邮箱": "null"}
QQ = {"iri": "null", "type": "QQ", "QQ号": "null"}
WECHAT = {"iri": "null", "type": "wechat", "微信号": "null"}
HOME_TEL = {"iri": "null", "type": "home_tel", "家庭电话": "null"}
ADDRESS = {"iri": "null", "type": "address", "地址": "null"}
SCHOOL = {
    "iri": "null",
    "type": "school",
    "学校名称": "null",
    "院校类型": "null",
    "学历层次": "null",
    "院校特性": "null",
    "院校隶属": "null",
}
COMPANY = {
    "iri": "null",
    "type": "company",
    "公司名称": "null",
    "公司所属行业": "null",
    "公司规模": "null",
    "公司类型": "null",
    "公司电话": "null",
}
