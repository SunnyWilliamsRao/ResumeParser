__author__ = "Sunny"

import re
import jieba

# recognize wheather onr line is time, support following format
# 2013/7-至今、2008/8-2013/7、2011/6、2019年、2019年4月、2019年4月14日
def isTime(line):
    PAT1 = re.compile(r"[\d]{4}年([\d]{1,2}?月)?([\d]{1,2}[日|号])?", re.S)
    PAT2 = re.compile(r"[\d]{4}/[\d]{1,2}-至今", re.S)
    PAT3 = re.compile(r"[\d]{4}/[\d]{1,2}-[\d]{4}/[\d]{1,2}", re.S)
    PAT4 = re.compile(r"[\d]{4}/[\d]{1,2}", re.S)
    line = re.sub(r" ", "", line)  # 去掉空格
    if re.findall(PAT1, line):
        return True
    elif re.findall(PAT2, line):
        return True
    elif re.findall(PAT3, line):
        return True
    elif re.findall(PAT4, line):
        return True
    return False


def format_time(line):
    # format time
    # 2013/7-至今 、2008/8-2013/7 、2011/6、2019年4月4号
    line = re.sub(r" ", "", line)  # remove space
    # just keep one "-"
    if line.count("-") >= 2:
        line = line[: line.index("-") + 1] + line[line.index("-") + 1 :].replace(
            "-", ""
        )
    if re.findall(r"[\d]{4}年([\d]{1,2}?月)?([\d]{1,2}[日号])?", line):
        line = line.replace("号", "日")  # 号 变成 日
        if "至今" in line:
            line = line.replace("至今", "2018年1月")
    else:
        if "至今" in line:
            line = line.replace("至今", "2018/1")
        line_split = line.split("-")
        line = ""
        if len(line_split) == 1:
            for idx, item in enumerate(line_split[0].split("/")):
                line += item + ["年", "月", "日"][idx]
        elif len(line_split) == 2:
            start_split = line_split[0].split("/")
            end_split = line_split[1].split("/")
            start = ""
            end = ""
            for idx, item in enumerate(start_split):
                start += item + ["年", "月", "日"][idx]
            for idx, item in enumerate(end_split):
                end += item + ["年", "月", "日"][idx]
            line = start + "-" + end
    return line


def isEmail(line):
    """
    >>> isEmail("13031334@qq.com")
    True
    >>> isEmail("$33345@164.con")
    False
    >>> isEmail("15056838741")
    False
    """
    pattern = (
        r"^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$"
    )
    if re.match(pattern, line):
        return True
    return False


def isQQ(line):
    """
    >>> isQQ('1303139691')
    True
    >>> isQQ("279894745")
    True
    >>> isQQ("dkei5542")
    False
    """
    pattern = r"\d{3,12}"
    if re.match(pattern, line):
        return True
    return False


def isPhone(line):
    """
    >>> isPhone('15056972883')
    True
    >>> isPhone('010-4445363')
    True
    >>> isPhone('1234523@qq.com')
    False
    """
    pattern = r"(\(?0\d{2,3}[)-]?)?\d{7,12}$"
    if re.match(pattern, line):
        return True
    return False


def english_para_filter(text):
    """to filter English segment in txt file

    Arguments:
        text {[str]} -- text segment of txt file
    """
    N = 3
    split_res = text.split("\n")
    for line_num, line in enumerate(split_res[:-2]):
        # for 3 connected lines, if there is no chinese character, it is English segment
        for i in range(N):
            if re.sub(r"[^\u4e00-\u9fa5]", "", split_res[line_num + i]):
                break
        else:
            return "\n".join(split_res[:line_num])
    return text


def garbled_filter(text):
    """to filter garbled segment in txt file

    Arguments:
        text {[str]} -- text segment of txt file
    """
    N = 3
    split_res = text.split("\n")
    for line_num, line in enumerate(split_res[:-2]):
        # for 3 connected lines, if ratio of the length of line and the length of word cut result
        # list less than 1.3, it is garbled string

        for i in range(N):
            if (
                len(split_res[line_num + i])
                / len(list(jieba.cut(split_res[line_num + i])))
                > 1.3
            ):
                break
        else:
            return "\n".join(split_res[:line_num])
    return text


name_dic = {
    # 最近工作中出现关键字
    "职位": "function",
    "公司": "company_name",
    "行业": "industry",
    "最近工作": "current_work",
    ## 个人信息中出现关键字
    "身高": "height",
    "户口/国籍": "household_country",
    "QQ号": "QQ",
    "微信号": "wechat",
    "婚姻状况": "marital_status",
    "家庭电话": "home_tel",
    "家庭地址": "address",
    "政治面貌": "political",
    ##"个人主页": "homepage"   ##出现次数较少，可以考虑忽略
    ##学历中出现的关键字
    "学历": "degree",
    "学历/学位": "degree",
    "专业": "major",
    "学校": "school_name",
    "目前薪资": "current_salary",
    ###求职意向中出现关键字
    "到岗时间": "time",
    "工作性质": "gzxz",
    "希望行业": "hope_industry",
    "行业": "hope_industry",
    "目标地点": "mbdd",
    "地点": "mbdd",
    "期望薪资": "hope_salary",
    "目标职能": "hope_function",
    "职能": "hope_function",
    "求职状态": "qzzt",
    "工作类型": "job_type",
    "关键字": "key_word",
    # Head部分用到的关键字
    "应聘职位": "hope_function",
    "应聘公司": "company_name",
    "投递时间": "delivery_time",
    "更新时间": "updata_time",
    "居住地": "address",
    "户口": "household_country",
    "电话": "tel",
    "E-mail": "eml",
    "匹配度": "resume_match",
    "简历与应聘职位匹配度": "resume_match",
    # 项目经验
    "所属公司": "ssgz",
    "项目描述": "project_description",
    "责任描述": "duty_description",
}

s


def proc_the_kv(info):
    """parse k-v format string

    Arguments:
        info {[str]} --  key-value format string in txt file
    """
    kv_list = info.split("：")
    if len(kv_list) == 2:
        key = kv_list[0]
        val = kv_list[1]
        return name_dic[key], val
    else:
        key = kv_list[0]
        val = "".join(kv_list[1:])
        return name_dic[key], val


if __name__ == "__main__":
    st = """目前正在找工作
18382456300
84040024@qq.com
 男 | 38岁（1979年5月7日 ） | 现居住成都-金牛区 | 14年工作经验"""
    print(english_para_filter(st))
    st1 = """18382456300
84040024@qq.com
 男 | 38岁（1979年5月7日 ） | 现居住成都-金牛区 | 14年工作经验
最近工作 （4年 1个月 ）
职　位："""
    print(garbled_filter(st1))
    print(
        len("男|38（1979年5月7日）|现居住成都-金牛区|14年工作经验")
        / len(list(jieba.cut("男|38岁（1979年5月7日 ）|现居住成都-金牛区|14年工作经验")))
    )
    print(len("最近工作 （4年 1个月 ）") / len(list(jieba.cut("最近工作（4年1个月）"))))
    print(len("职　位：") / len(list(jieba.cut("职位："))))
