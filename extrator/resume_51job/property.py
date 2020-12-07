__author__ = 'Sunny'

import re
import json

from tools.dict_tree import tree
from tools import tools
class Property:
    def __init__(self):
        self.prop_keywords = r"./tools/key_words/51job/key_words_in_block.txt"
        self.tree = self.__build_tree()

    # build property keywords dict tree
    def __build_tree(self):
        list_word = []
        with open(self.prop_keywords, 'r', encoding='utf-8') as file:
            # file.readline()
            for line in file:
                if line:
                    list_word.append(line.strip())
        return tree(list_word)

    def check_prop(self, line):
        '''
        :param line: single line  from resume text
        :return: bool, whether the line is property keyword
        '''
        line = re.sub(r" |/|", "", line)  # to filter " ", '/'
        res = self.tree.isContain(line)
        if not res:
            return False
        if not re.findall(r":|：", line):  # it is not property keywords if it doesn't include ":"
            return False
        # just keep Chinese characters and English alphabet
        line = re.sub(r"[^\u4e00-\u9fa5|\u0041-\u005a|\u0061-\u007a]", "", line)
        # remove space and other special bytes, property keywords should be start of line
        if not line.index(res) == 0:
            return False
        return res

    def prop_split(self, text):
        '''
        :param text: text segment
        :return: property segment dict
        '''
        prop_split_res = {}
        prop_keywords = ["TIME_CONTENT"]
        idx = 0
        prop_text = ""
        lines = text.split("\n")
        for line_count, line in enumerate(lines):
            check_res = self.check_prop(line)
            if check_res:
                if self.check_prop(lines[line_count + 1]):  # continue if next line is property keyword
                    continue
                # print(check_res)
                prop_keywords.append(check_res)
                idx += 1
                # the first time match block keyword, then segment from that line to the first line
                # belongs to HEADER block
                if idx == 1:
                    prop_split_res[prop_keywords[idx-1]] = prop_text
                prop_text = ""
                # for property keywords, just keep Chinese characters and English alphabet
                line = re.sub(r"[^\u4e00-\u9fa5|\u0041-\u005a|\u0061-\u007a]", "", line)
            prop_text += line + "\n"  # keep "\n" in segment, and replace "\n" with 3 "&"
        else:  # get the last segment here
            prop_split_res[prop_keywords[idx]] = prop_text
        return prop_split_res

    def extrator(self, block_dict):
        '''
        :param block_dict: property segment dict
        :return: property dict
        '''
        prop_dict = {}
        for block_name in block_dict.keys():
            if block_name == "HEADER":
                prop_dict.setdefault(block_name, {})
                block_text = block_dict[block_name]
                block_text = re.sub(r'：\n', r'：', block_text)
                block_split = block_text.rstrip("\n").split('\n')
                try:
                    for line in block_split:
                        line = line.strip().replace(u'\u3000',u'').replace(u'\xa0',u'')  ##去除简历中如"户　口" "电　话"等关键字中间的空格
                        if "：" in line:
                            key, value = tools.proc_the_kv(line)
                            prop_dict[block_name][key] = value
                        elif len(line) == 2 or len(line) == 3:
                            prop_dict[block_name]['name'] = line
                        elif "ID" in line:
                            prop_dict[block_name]['id'] = (re.search(r':(\d*)', line).group(1))
                        else:
                            work = re.search(r'(\d-?\d?)年工作经验', line)
                            gender = re.search(r'(男|女)', line)
                            age = re.search(r'(\d*)岁', line)
                            birthday = re.search(r'(\d{4})年(\d*)月(\d*)日', line)
                            # print('work:',work, 'gender:',gender, 'age:',age ,'birthday:',birthday)
                            prop_dict[block_name]['work'] = work.group(1)
                            prop_dict[block_name]['gender'] = gender.group(1)
                            prop_dict[block_name]['age'] = age.group(1)
                            prop_dict[block_name]['birthday'] = birthday.group()
                except Exception as e:
                    print(e)
            elif block_name == "个人信息":
                """“家庭地址： \n上海市虹口区九龙路515号1205室 (邮编：200080)”，
                """
                prop_dict.setdefault(block_name, {})
                block_text = block_dict[block_name].lstrip("个人信息\n")
                block_text = re.sub(r'：\n', r'：', block_text)
                block_text = re.sub(r'： \n', r'：', block_text)
                block_split = block_text.rstrip("\n").split('\n')
                try:
                    for line in block_split:
                        if "：" in line:
                            key, value = tools.proc_the_kv(line)
                            prop_dict[block_name][key] = value
                        else:
                            print("(%s)中未提取信息行: "%block_name+ line)
                except Exception as e:
                   print(e)
            # elif block_name == "最高学历学位":
            #     prop_dict.setdefault(block_name, {})
            #     block_text = block_dict[block_name].lstrip("最高学历学位\n")
            #     block_split = block_text.rstrip("\n").split("\n")
            #     for line_num, line in enumerate(block_split):
            #         if line.startswith("专业"):
            #             prop_dict[block_name]["major"] = block_split[line_num+1]
            #         elif line.startswith("学校"):
            #             prop_dict[block_name]["school_name"] = block_split[line_num+1]
            #         elif line.startswith("学历/学位"):
            #             prop_dict[block_name]["degree"] = block_split[line_num+1]
            # elif block_name == "学历":
            #     prop_dict.setdefault(block_name, {})
            #     block_text = block_dict[block_name]
            #     block_text = re.sub(r'：\n', r'：', block_text)
            #     block_split = block_text.rstrip('\n').split('\n')
            #     # print(blo ck_split)
            #     try:
            #         for line in block_split:  ###分为包含完整键值对的行、包含最近工作的行两部分
            #             line = line.strip().replace(u'\u3000', u'').replace(u'\xa0', u'')  ##去除关键字中间的空格
            #             if "：" in line:
            #                 key, value = tools.proc_the_kv(line)
            #                 prop_dict[block_name][key] = value
            #             else:
            #                 pass
            #                 ##print("(%s)中未提取信息行: "%block_name+ line)
            #     except Exception as e:
            #         print(e)
            elif block_name in ["学历" , "最高学历学位"]:
                prop_dict.setdefault("最高学历学位",{}) # “最高学历学位”
                block_text = block_dict[block_name]
                block_name = "最高学历学位"
                block_text = re.sub(r'：\n', r'：', block_text)
                block_split = block_text.rstrip('\n').split('\n')
                # print(blo ck_split)
                try:
                    for line in block_split:
                        line = line.strip().replace(u'\u3000', u'').replace(u'\xa0', u'')  # remove space
                        if "：" in line:
                            key, value = tools.proc_the_kv(line)
                            prop_dict[block_name][key] = value
                        else:
                            pass
                except Exception as e:
                    print(e)
            elif block_name == "求职意向":
                prop_dict.setdefault(block_name, {})
                block_text = block_dict[block_name].lstrip('求职意向\n')
                block_text = re.sub(r'：\n', r'：', block_text)
                block_split = block_text.rstrip().split('\n')
                try:
                    for line in block_split:
                        line = line.strip().replace(u'\u3000', u'').replace(u'\xa0', u'')  ##去除关键字中间的空格
                        if "：" in line:
                            key, value = tools.proc_the_kv(line)
                            prop_dict[block_name][key] = value
                        else:
                            pass
                except Exception as e:
                    print(e)

            elif block_name == "最近工作":
                prop_dict.setdefault(block_name, {})
                block_text = block_dict[block_name]
                block_text = re.sub(r'：\n', r'：', block_text)
                block_split = block_text.rstrip('\n').split('\n')
                # print(block_split)
                try:
                    for line in block_split:
                        line = line.strip().replace(u'\u3000', u'').replace(u'\xa0', u'')
                        if "：" in line:
                            key, value = tools.proc_the_kv(line)
                            prop_dict[block_name][key] = value
                        else:
                            work_time = re.search('最近工作[ （|\[]+(.*?)[\]| ）]', line)  # match '()', '[]'
                            if work_time is None:
                                pas
                            else:
                                #print(line)
                                prop_dict[block_name]["work_time"] = work_time.group(1)
                except Exception as e:
                    print(e)
            elif block_name == "目前薪资":
                prop_dict.setdefault(block_name, {})
                block_text = block_dict[block_name].lstrip("目前薪资\n")
                prop_dict[block_name]['current_salary'] = block_text.replace("\n", "")
            elif block_name == "目前年收入":
                prop_dict.setdefault(block_name, {})
                block_text = block_dict[block_name].lstrip("目前年收入\n")
                prop_dict[block_name]['current_salary'] = block_text.replace("\n", "")
            elif block_name == "自我评价":
                prop_dict.setdefault(block_name, {})
                block_text = block_dict[block_name].lstrip("自我评价\n")
                prop_dict[block_name]['self_evalution'] = block_text.replace("\n", "")
            if block_name == "工作经验":
                prop_dict.setdefault(block_name, [])
                block_text = block_dict[block_name].lstrip("工作经验\n")
                block_split = block_text.rstrip("\n").split("\n")
                flag_line_num = 0
                for line_num, line in enumerate(block_split):
                    #eg: 2015 /10--2016 /7：北京中关村软件园 [ 9个月]
                    if tools.isTime(line) and line.__contains__("："):
                        #print("Ok:time1")
                        new_dict = {}
                        prop_dict[block_name].append(new_dict)
                        flag_line_num = line_num
                        flag = "time1"
                        if line.__contains__("："):
                            split_res = line.replace(" ", "").split("：")
                            prop_dict[block_name][-1]["work_period"]=(split_res[0])

                            if split_res[1].split("[")[0].__contains__("("):
                                prop_dict[block_name][-1]["company_name"]=(split_res[1].split("[")[0].split("(")[0])
                                prop_dict[block_name][-1]["company_capacity"]=(
                                    split_res[1].split("[")[0].split("(")[1].rstrip(")"))
                            else:
                                prop_dict[block_name][-1]["company_name"]=(split_res[1].split("[")[0])
                            prop_dict[block_name][-1]["work_duration"]=(split_res[1].split("[")[1].rstrip("]"))
                    elif tools.isTime(line) and not line.__contains__("："):
                        #print("OK:time2")
                        new_dict = {}
                        prop_dict[block_name].append(new_dict)
                        flag_line_num = line_num
                        flag = "time2"
                        prop_dict[block_name][-1]["work_period"]=(line)
                    elif line.startswith("所属行业"):
                        flag_line_num = line_num
                        flag = "所属行业"
                    elif line.startswith("工作描述"):
                        flag_line_num = line_num
                        flag = "工作描述"
                        prop_dict[block_name][-1]["work_describtion"] = ""
                    else:
                        if flag == "time2":
                            if line_num == flag_line_num + 1:
                                # eg: 上海外电国际贸易有限公司 (4年 4个月 )
                                if line.__contains__("("):
                                    prop_dict[block_name][-1]["company_name"]=(line.replace(" ", "").split("(")[0])
                                    prop_dict[block_name][-1]["work_duration"]=(
                                        line.replace(" ", "").split("(")[1].rstrip(")"))
                                else:
                                    prop_dict[block_name][-1]["company_name"]=(line)
                            if line_num == flag_line_num + 2:
                                # eg: 贸易/进出口|50-150人|外资(非欧美)
                                if line.__contains__("|"):
                                    prop_dict[block_name][-1]["company_industry"]=(line.split("|")[0])
                                    prop_dict[block_name][-1]["company_capacity"]=(line.split("|")[1])
                                else:
                                    pass
                            if line_num == flag_line_num + 3:
                                prop_dict[block_name][-1]["department"]=(line)
                            if line_num == flag_line_num + 4:
                                prop_dict[block_name][-1]["work_positon"]=(line)
                        elif flag == "所属行业":
                            if line_num == flag_line_num + 1:
                                prop_dict[block_name][-1]["company_industry"]=(line)
                            elif line_num == flag_line_num + 2:
                                prop_dict[block_name][-1]["department"]=(line)
                            elif line_num == flag_line_num + 3:
                                prop_dict[block_name][-1]["work_positon"]=(line)
                            elif line_num == flag_line_num + 4:
                                prop_dict[block_name][-1]["work_describtion"]=(line)
                            else:
                                prop_dict[block_name][-1]["work_describtion"] += line
                        elif flag == "工作经验":
                            prop_dict[block_name][-1]["work_describtion"] += line
            if block_name == "项目经验":
                prop_dict.setdefault(block_name, [])
                block_text = block_dict[block_name].lstrip("项目经验\n")
                block_split = block_text.rstrip("\n").split("\n")
                flag_line_num = 0
                for line_num, line in enumerate(block_split):
                    if tools.isTime(line):
                        flag_line_num = line_num
                        new_dict = {}
                        flag = "time"
                        prop_dict[block_name].append(new_dict)
                        if line.__contains__("："):
                            prop_dict[block_name][-1]["project_period"] = line.split("：")[0]
                            prop_dict[block_name][-1]["project_type"] = line.split("：")[1]
                        else:
                            prop_dict[block_name][-1]["project_period"] = line
                    elif line.startswith("所属公司"):
                        flag_line_num = line_num
                        flag = "所属公司"
                    elif line.startswith("硬件环境"):
                        flag_line_num = line_num
                        flag = "硬件环境"
                    elif line.startswith("软件环境"):
                        flag_line_num = line_num
                        flag = "软件环境"
                    elif line.startswith("开发工具"):
                        flag_line_num = line_num
                        flag = "开发工具"
                    elif line.startswith("项目描述"):
                        flag_line_num = line_num
                        flag = "项目描述"
                    elif line.startswith("责任描述"):
                        flag_line_num = line_num
                        flag = "责任描述"
                    else:
                        if line_num == flag_line_num+1:
                            if flag == "time":
                                prop_dict[block_name][-1]["project_type"] = line
                            elif flag == "所属公司":
                                prop_dict[block_name][-1]["company"] = line
                            elif flag == "硬件环境":
                                prop_dict[block_name][-1]["hardware"] = line
                            elif flag =="软件环境":
                                prop_dict[block_name][-1]["software"] = line
                            elif flag =="开发工具":
                                prop_dict[block_name][-1]["development_tools"] = line
                            elif flag =="项目描述":
                                prop_dict[block_name][-1]["project_description"] = line
                            elif flag =="责任描述":
                                prop_dict[block_name][-1]["duty_description"] = line
                        else:
                            if flag == "项目描述":
                                prop_dict[block_name][-1]["project_description"] +=line
                            elif flag == "责任描述":
                                prop_dict[block_name][-1]["duty_description"] +=line
                            else:
                                print("(%s)中未提取信息行: " % (block_name) + line)
            elif block_name == "教育经历":
                try:
                    prop_dict.setdefault(block_name, [])
                    block_text = block_dict[block_name].lstrip("教育经历\n")
                    block_split = block_text.rstrip("\n").split("\n")
                    flag_line_num = 0
                    for line_num, line in enumerate(block_split):
                        if tools.isTime(line):
                            flag_line_num = line_num
                            new_educate = {}
                            prop_dict[block_name].append(new_educate)
                            prop_dict[block_name][-1]["educated_period"] = line
                        else:
                            if line_num == flag_line_num + 1:
                                prop_dict[block_name][-1]["school_name"] = line
                            elif line_num == flag_line_num + 2:
                                if line.__contains__("|"):  # eg：大专:酒店管理
                                    prop_dict[block_name][-1]["degree"] = line.split("|")[0]
                                    prop_dict[block_name][-1]["major"] = line.split("|")[1]
                                else:
                                    prop_dict[block_name][-1]["degree"] = line
                            elif line_num == flag_line_num + 3:
                                if "major" not in prop_dict[block_name][-1]:
                                    prop_dict[block_name][-1]["major"] = line
                                else:
                                    prop_dict[block_name][-1]["major_description"] = line
                            elif line_num == flag_line_num + 4:
                                prop_dict[block_name][-1]["major_description"] = line
                            else:
                                prop_dict[block_name][-1]["major_description"] += line
                except:
                    pass
            elif block_name == "在校情况":
                prop_dict.setdefault(block_name, {})
                pass
            elif block_name == "培训经历":
                prop_dict.setdefault(block_name, [])
                block_text = block_dict[block_name].lstrip("培训经历\n")
                block_split = block_text.rstrip("\n").split("\n")
                flag_line_num = 0
                for line_num, line in enumerate(block_split):
                    if tools.isTime(line):
                        flag_line_num = line_num
                        new_dict = {}
                        flag = "time"
                        prop_dict[block_name].append(new_dict)
                        prop_dict[block_name][-1]["training_period"] = line.replace(" ", "")  # 有必要移除空格？
                    elif line.startswith("培训地点"):
                        flag_line_num = line_num
                        flag = "培训地点"
                    elif line.startswith("培训描述"):
                        flag_line_num = line_num
                        flag = "培训描述"
                    elif line.startswith("培训机构"):
                        flag_line_num = line_num
                        flag = "培训机构"
                    else:
                        if line_num == flag_line_num+1:
                            if flag == "time":
                                prop_dict[block_name][-1]["training_courses"] = line
                            elif flag == "培训地点":
                                prop_dict[block_name][-1]["training_address"] = line
                            elif flag == "培训描述":
                                prop_dict[block_name][-1]["training_description"] = line
                            elif flag =="培训机构":
                                prop_dict[block_name][-1]["training_organization"] = line
                        else:
                            if flag == "培训描述":
                                prop_dict[block_name][-1]["training_description"] +=line
                            else:
                                print("(%s)中未提取信息行: " % (block_name) + line)
            elif block_name == "技能特长":
                prop_dict.setdefault(block_name, {})
                pass
            if block_name == "所获奖项":
                prop_dict.setdefault(block_name,[] )
                block_text = block_dict[block_name].lstrip("所获奖项\n")
                block_split = block_text.rstrip("\n").split("\n")
                for line_num, line in enumerate(block_split):
                    if tools.isTime(line):
                        flag_line_num = line_num
                        new_dict = {}
                        prop_dict[block_name].append(new_dict)
                        prop_dict[block_name][-1]["honor_time"] = line.replace(" ", "")
                    else:
                        if line_num == flag_line_num +1:
                            prop_dict[block_name][-1]["prize"]  = line
                        elif line_num == flag_line_num + 2 :
                            prop_dict[block_name][-1]["level"] = line
            elif block_name == "语言能力":
                prop_dict.setdefault(block_name, {})
                block_text = block_dict[block_name].lstrip("语言能力\n")
                prop_dict[block_name]["skills_language"] = block_text
            elif block_name == "IT技能":
                prop_dict.setdefault(block_name, {})
                block_text = block_dict[block_name]
                try:
                    prop_dict[block_name]["speciality"] == block_text
                except Exception as e:
                    print(e)
                    prop_dict[block_name].setdefault("speciality", block_text)
            elif block_name == "最近工作":
                prop_dict.setdefault(block_name, {})
                block_text = block_dict[block_name].lstrip("最近工作\n")
                block_split = block_text.rstrip("\n").split("\n")
                for line_num, line in enumerate(block_split):
                    if tools.isTime(line):
                        prop_dict[block_name]["work_period"] = block_split[0].replace(" ", "").strip("[]")
                    elif line.replace(" ", "") == "公司":
                        prop_dict[block_name]["company_name"] == block_split[line_num+1]
                    elif line.replace(" ", "") == "行业":
                        prop_dict[block_name]["company_industry"] == block_split[line_num+1]
                    elif line.replace(" ", "") == "职位":
                        prop_dict[block_name]["work_positon"] == block_split[line_num+1]
            elif block_name == "学生实践经验":
                prop_dict.setdefault(block_name, [])
                block_text = block_dict[block_name].lstrip("学生实践经验\n")
                block_split = block_text.rstrip("\n").split("\n")
                flag_line_num = 0
                for line_num, line in enumerate(block_split):
                    if tools.isTime(line):
                        flag_line_num = line_num
                        new_dict = {}
                        prop_dict[block_name].append(new_dict)
                        prop_dict[block_name][-1]["practice_period"] = line.replace(" ", "")
                    elif line_num == flag_line_num+1:
                        prop_dict[block_name][-1]["practice_content"] = line
                    elif line_num == flag_line_num+2:
                        prop_dict[block_name][-1]["practice_description"] = line
                    else:
                        prop_dict[block_name][-1]["practice_description"] += line
            elif block_name == "校内职务":
                prop_dict.setdefault(block_name, [])
                block_text = block_dict[block_name].lstrip("校内职务\n")
                block_split = block_text.rstrip("\n").split("\n")
                flag_line_num = 0
                for line_num, line in enumerate(block_split):
                    if tools.isTime(line):
                        flag_line_num = line_num
                        new_dict = {}
                        flag = "time"

                        prop_dict[block_name].append(new_dict)
                        prop_dict[block_name][-1]["function_period"] = line.replace(" ", "")
                    elif line.startswith("职务描述"):
                        flag_line_num = line_num
                        flag = "职务描述"
                    else:
                        if flag == "time":
                            if line_num == flag_line_num+1:
                                prop_dict[block_name][-1]["function"] = line
                            elif line_num == flag_line_num+2:
                                prop_dict[block_name][-1]["function_description"] = line
                            else:
                                prop_dict[block_name][-1]["function_description"] += line
                        elif flag =="职务描述":
                            if line_num == flag_line_num+1:
                                prop_dict[block_name][-1]["function_description"] = line
                            else:
                                prop_dict[block_name][-1]["function_description"] += line
                        else:
                            print("(%s)中未提取信息行: " % (block_name) + line)
            elif block_name == "证书":
                prop_dict.setdefault(block_name, {})
                block_text = block_dict[block_name].lstrip("证书\n")
                block_split = block_text.rstrip("\n").split("\n")
                prop_dict[block_name]["cert_time"] = []
                prop_dict[block_name]["cert_name"] = []
                prop_dict[block_name]["cert_score"] = []
                for line_num, line in enumerate(block_split):
                    if tools.isTime(line):
                        prop_dict[block_name]["cert_time"].append(line.replace(" ", ""))
                        try:
                            prop_dict[block_name]["cert_name"].append(block_split[line_num+1])
                        except Exception as e:
                            print(e)
                            prop_dict[block_name]["cert_name"].append("")
                        try:
                            if tools.isTime(block_split[line_num+2]):
                                prop_dict[block_name]["cert_score"].append("")
                            else:
                                if len(block_split[line_num+2]) <= 4:  # eg: "分数", "合格", "优秀"
                                    prop_dict[block_name]["cert_score"].append(block_split[line_num+2])
                                else:
                                    prop_dict[block_name]["cert_score"].append("")
                        except Exception as e:
                            print(e)
                            prop_dict[block_name]["cert_score"].append("")
                        # eg:    #大学英语四级 （463）
                        tmp = prop_dict[block_name]["cert_name"][-1]
                        if re.findall(r"\(|（|\[|【", tmp):
                            prop_dict[block_name]["cert_name"].pop(-1)
                            prop_dict[block_name]["cert_score"].pop(-1)
                            sep = re.findall(r"\(|（|\[|【", tmp)[0]
                            prop_dict[block_name]["cert_score"].append(re.sub(r"\)|）|\]|】", "", tmp.split(sep)[1]))  # 去掉反括号
                            prop_dict[block_name]["cert_name"].append(tmp.split(sep)[0])
            if block_name == "校内荣誉":
                prop_dict.setdefault(block_name,[] )
                block_text = block_dict[block_name].lstrip("校内荣誉\n")
                block_split = block_text.rstrip("\n").split("\n")
                for line_num, line in enumerate(block_split):
                    if tools.isTime(line):
                        flag_line_num = line_num
                        new_dict = {}
                        prop_dict[block_name].append(new_dict)
                        prop_dict[block_name][-1]["honor_time"] = line.replace(" ", "")
                    else:
                        if line_num == flag_line_num +1:
                            prop_dict[block_name][-1]["prize"]  = line
                        if line_num == flag_line_num + 2 and len(line) <= 6:
                            prop_dict[block_name][-1]["level"] = line

            elif block_name == "技能语言":
                prop_dict.setdefault(block_name, {})
                block_text = block_dict[block_name].lstrip("技能语言\n")
                prop_dict[block_name]["speciality"] = block_text
            elif block_name == "其他信息":
                prop_dict.setdefault(block_name, {"special_skill": ""})
                block_text = block_dict[block_name].lstrip("其他信息\n")
                block_split = block_text.rstrip("\n").split("\n")
                for line_num, line in enumerate(block_split):
                    if line.startswith("特殊技能"):
                        prop_dict[block_name]["special_skill"] == "".join(block_split[line_num+1:])
            elif block_name == "附加信息":
                prop_dict.setdefault(block_name, {})
                block_text = block_dict[block_name].lstrip("附加信息\n")
                block_split = block_text.rstrip("\n").split("\n")
                if block_split[0] == "特长":
                    prop_dict[block_name]["speciality"] == "".join(block_split[1:])
        return prop_dict



if __name__ == '__main__':
    p = Property()
    block_json_file = r"../../db/res/51job_block.json"
    prop_json_file = r"../../db/res/51job_prop.json"
    out_file = open(prop_json_file, "a", encoding="utf-8")
    with open(block_json_file, "r", encoding="utf-8") as f:
        for line in f:
            json_file = json.loads(line.strip())
            json.dump(p.extrator(json_file["block"]), out_file, ensure_ascii=False)
            out_file.write("\n")
            # print(p.extrator(json_file["block"]))

    out_file.close()

#
