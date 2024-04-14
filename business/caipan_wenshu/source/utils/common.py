from my_log.mylogger import logger
import re

Api_key = "RBbNKRkaNaOu78agDa03055224864b88A071067fA99177Fb"
#Api_base = "https://brain.thundersoft.com/brain"
Api_base = "http://47.95.199.154:8888/brain"
#Api_key = "00PPHhdCuv4Jjfpe4249A48cCe4c4bAe8c47C62d41709458"
#Api_base = "https://gpt.thundersoft.com/brain"

#Model_name = "rubik-law-chat"
Model_name = "rubik6-chat"
#Model_name = "rubik-chat"
Azure_model_name = "azure-gpt-3.5-turbo-16k"



# 这里定义的常量主要用来上层业务使用,如果有变动或增加，只修改此脚本文件中的数据即可
# 注意下面的提示词保持一致（以后要优化下面的提示词(getFirstPrompt)代码）
Location = "案发地点"
Damage = "受害人伤害情况"
Abstract = "案情概括"
PunishMoney = "处罚金额"
ArticleMoney = "物品价值"
Car = "涉案车辆"


# 获取特定的业务数据
def getSpecialBusinessData(case_reason):
    name0 = ""
    name1 = ""
    update_dict = {}
    if "抢劫" in case_reason:
        name0 = "抢劫金额"
        name1 = "抢劫物品"
        update_dict.update({"涉案现金": f"{name0}"})
        update_dict.update({"涉案物品": f"{name1}"})
    elif "盗窃" in case_reason or "失窃" in case_reason:
        name0 = "盗窃现金"
        name1 = "盗窃物品"
        update_dict.update({"涉案现金": f"{name0}"})
        update_dict.update({"涉案物品": f"{name1}"})
    elif "诈骗" in case_reason:
        name0 = "诈骗现金"
        name1 = "诈骗物品"
        update_dict.update({"涉案现金": f"{name0}"})
        update_dict.update({"涉案物品": f"{name1}"})
    elif "交通" in case_reason:
        name0 = "被告人共赔付金额"
        name1 = "涉案车辆"

    return name0, name1, update_dict


def getSpecialBusinessDataV2(case_reason, content):
    name0 = ""
    name1 = ""
    if "抢劫" in case_reason:
        name0 = "抢劫金额"
        name1 = "抢劫物品"
    elif "盗窃" in case_reason:
        name0 = "盗窃现金"
        name1 = "盗窃物品"
    elif "诈骗" in case_reason:
        name0 = "诈骗现金"
        name1 = "诈骗物品"
    elif "交通" in case_reason:
        return content

    content = content.replace("涉案现金", name0)
    content = content.replace("涉案物品", name1)
    return content

def get_case_reason():
    return "请根据下面的内容，说出案件的类型，内容如下："

def getFirstPrompt(case_reason,**kwargs):

    if "交通" in case_reason:
        prompt = """
                # Role: 法律案件信息提取员

                ## Profile:
                - Language: 中文
                - Description: 信息提取员的职责是从案件信息，提取出格式化的项目信息，方便对信息进行存储和加工。

                ### OutputFormat
                {
                    "涉案总人数": "",
                    "涉案人员姓名": "",
                    "涉案人员职业": "",
                    "涉案人员年龄": "",    
                    "案发时间": "",
                    "案发地点": "",
                    "涉案车辆": "",
                    "是否逃逸": "",
                    "是否酒驾": "",
                    "受害人姓名": "",    
                    "受害人伤害情况": "",
                    "判决时间": "",
                    "服刑时间": "",
                    "被告人共赔付金额": "",
                    "保险公司赔付金额": "",
                    "是否自首": "",
                    "案情概括": "",
                    "案件类型": ""
                }

                ## Rules
                1. 输出内容必须为标准的 json 格式
                2. 务必保证所有字段是在案例信息中真实存在的
                3. '案情概括' 不要超出 150 个汉字
                4. 输出内容必须为标准的 json 格式

                ## Initialization
                作为角色 <Role>, 严格遵守 <Rules>, 仅输出 <OutputFormat> 中规定的字段。

                # 案件信息
                """
        for old_value, new_value in kwargs.items():
            prompt = prompt.replace(old_value, new_value)

        logger.info(f"getFirstPrompt ={prompt}")
        return prompt + "\n"
    elif "纠纷" in case_reason:
        prompt = """
                # Role: 法律案件信息提取员
                ## Profile:
                - Language: 中文
                - Description: 信息提取员的职责是从案件信息，提取出格式化的项目信息，方便对信息进行存储和加工。
                ### OutputFormat
                {
                    "涉案总人数": "",
                    "涉案人员姓名": "",
                    "涉案人员职业": "",
                    "涉案人员年龄": "",    
                    "涉案时间": "",
                    "涉案地点": "",
                    "涉案金额": "",
                    "涉案物品": "",
                    "物品价值": "",
                    "涉案人姓名": "", 
                    "判决时间": "",
                    "服刑时间": "",
                    "处罚金额": "",
                    "是否自首": "",
                    "案情概括": "",
                    "案件类型": ""
                }

                ## Rules
                1. 务必保证所有字段是在案例信息中真实存在的
                2. '案发时间' 是罪犯的作案时间,不是其它的时间,可能会有多个,不要遗漏
                3. '案情概括' 不要超出 200 个汉字
                4. 输出内容必须为标准的 json 格式

                ## Initialization
                作为角色 <Role>, 严格遵守 <Rules>, 仅输出 <OutputFormat> 中规定的字段。

                # 案件信息
                """
        return prompt + "\n"
    else:
        prompt = """
        # Role: 法律案件信息提取员
    
        ## Profile:
        - Language: 中文
        - Description: 信息提取员的职责是从案件信息，提取出格式化的项目信息，方便对信息进行存储和加工。
    
        ### OutputFormat
        {
            "涉案总人数": "",
            "涉案人员姓名": "",
            "涉案人员职业": "",
            "涉案人员年龄": "",    
            "案发时间": "",
            "案发地点": "",
            "涉案现金": "",
            "涉案物品": "",
            "物品价值": "",
            "受害人姓名": "",    
            "受害人伤害情况": "",
            "判决时间": "",
            "服刑时间": "",
            "处罚金额": "",
            "是否自首": "",
            "案情概括": "",
            "案件类型": ""
        }
    
        ## Rules
        1. 输出内容必须为标准的 json 格式
        2. 务必保证所有字段是在案例信息中真实存在的
        3. '案发时间' 是罪犯的作案时间,不是其它的时间,可能会有多个,不要遗漏
        4. '案情概括' 不要超出 150 个汉字
        5. 输出内容必须为标准的 json 格式
        
        ## Initialization
        作为角色 <Role>, 严格遵守 <Rules>, 仅输出 <OutputFormat> 中规定的字段。
    
        # 案件信息
        """
        for old_value, new_value in kwargs.items():
            prompt = prompt.replace(old_value, new_value)

        logger.info(f"getFirstPrompt ={prompt}")
        return prompt + "\n"


def getSecondPrompt(**kwargs):
    prompt = """
    # Role: 数据处理

    ## Profile:
    - Language: 中文
    - Description: 对数据进行二次处理,并按格式化的要求输出。

    ### OutputFormat
    {
        "案发时间": "",
        "案发地点": "",
        "涉案现金": "",
        "涉案物品": "",
        "物品价值": "",
        "受害人伤害情况": "",
        "处罚金额": "",
        "是否自首": "",        
    }

    ## Rules
    1. 输出内容必须为标准的 json 格式
    2. 务必保证所有字段是在案例信息中真实存在的
    3. '案发时间' 是罪犯的作案时间,不是其它的时间,可能会有多个,不要遗漏
    4. '案情概括' 不要超出 150 个汉字
    5. 请直接输出 json 格式的内容

    ## Initialization
    作为角色 <Role>, 严格遵守 <Rules>, 仅输出 <OutputFormat> 中规定的字段。

    # 案件信息
    """
    for old_value, new_value in kwargs.items():
        prompt = prompt.replace(old_value, new_value)

    logger.info(f"getSecondPrompt ={prompt}")
    return prompt + "\n"


def money_deal(value):
    pattern = r'\d+(?:\.\d+)?'
    money = 0
    if isinstance(value, list):
        for v1 in value:
            if isinstance(v1, dict):
                for _, v2 in v1.items():
                    if isinstance(v2, int) or isinstance(v2, float):
                        money += v2
                    else:
                        match = re.findall(pattern, v2)
                        for m1 in match:
                            money += float(m1)
            else:
                if isinstance(v1, int) or isinstance(v1, float):
                    money += v1
                else:
                    match = re.findall(pattern, v1)
                    for m1 in match:
                        money += float(m1)
    elif isinstance(value, dict):
        for _, v1 in value.items():
            if isinstance(v1, int) or isinstance(v1, float):
                money += v1
            else:
                match = re.findall(pattern, v1)
                for m1 in match:
                    money += float(m1)
    elif isinstance(value, int) or isinstance(value, float):
        money += value
    else:
        match = re.findall(pattern, value)
        for m1 in match:
            money += float(m1)

    return money

