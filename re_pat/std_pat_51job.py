__author__ = "Sunny"
import re


# the feature of resume file name
# 2 patterns as follow:


# examples：[('吴含蕾', '财务主管总帐会计', '656562916')]、[('吴含蕾', '', '656562916')]
FILE_NAME_PAT1 = re.compile(
    r"51job_(?P<name>[^_\(\)]{2,4})_?-?(?P<hope_position>.{2,10})?\((?P<Resume_ID>[\d]{5,10})\)",
    re.S,
)
# examples：
# "51job.com申请贵公司PHP高级开发工程师（上海）－戴超4220692646"
# "51job.com申请贵公司PHP高级开发工程师（变配电）（上海）－戴超4220692646"
FILE_NAME_PAT2 = re.compile(
    r"51job\.com申请贵公司(?P<hope_position>.*?(?=（))（?(?P<hope_industry>.*?)?）?"
    r"（(?P<address>.*?)）－(?P<name>[^_()\d]{2,4})(?P<Resume_ID>[\d]{5,10})",
    re.S,
)

