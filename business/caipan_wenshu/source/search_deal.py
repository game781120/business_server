import random
import time

from my_elastic import MyElasticSearch
from my_mysql import (query_wenshu_third_by_info,
                      query_wenshu_info_by_uuids,
                      query_wenshu_third_case_type,
                      query_wenshu_second_case_type

                      )

from my_milvus import MyMilvus
from business.caipan_wenshu.source.utils import (Abstract,
                                                 Car,
                                                 getSpecialBusinessData,
                                                 getSpecialBusinessDataV2,
                                                 getFirstPrompt,
                                                 get_case_reason, Damage)
from my_log.mylogger import logger
import brainai
import json
import re
from my_model import model_deal
from business.caipan_wenshu.source.utils import (money_deal, Api_key,
                                                 Api_base,
                                                 Model_name,
                                                 Azure_model_name)
from business.caipan_wenshu.source import (data_cleaning_first,
                                           data_to_es_milvus_mysql)


def send_deal(content, stream):
    chat_model_kwargs = {
        "api_key": "",
        "api_base": "http://10.0.36.13:8888/brain/",
        "object_name": "knowledge.api.chat.wenshu_chat",
        "model": "azure-gpt-3.5-turbo-16k",
        "question": content,
        "temperature": 0,
        "stream": stream,
        "res_json": 1,
    }
    print(f"chat_model_kwargs={json.dumps(chat_model_kwargs, indent=4)}")
    response = brainai.ChatCompletion.create(**chat_model_kwargs)
    if stream:
        for chunk in response:
            data = json.loads(chunk)
            print(f"{json.dumps(data, indent=4, ensure_ascii=False)}")
    else:
        data = json.loads(response)
        print(data)
    return response

def recall_data_001(case_reason, content):
    money_str, article_str, _ = getSpecialBusinessData(case_reason)
    print(f"money_str={money_str} article_str={article_str}")
    new_content = getSpecialBusinessDataV2(case_reason, content)
    print(f"new_content={new_content}")
    json_data = json.loads(new_content)
    # 物品信息
    article = json_data.get(f"{article_str}")
    # 现金金额
    money_value = json_data.get(f"{money_str}")
    print(f"money_value={money_value}")
    # 物品价值
    article_money_value = json_data.get("物品价值")
    print(f"article_money_value={article_money_value}")
    money_uuids_set = set()  # 排重
    article_uuids_set = set()
    money = None
    article_money = None
    if money_value:
        money = money_deal(money_value)
    if article_money_value:
        article_money = money_deal(article_money_value)
    if not money and not article_money and article:
        print(f"从涉案物品中再重新提取 article={article}")
        article_money = money_deal(article)
        print(f"从涉案物品中再重新提取到 物品价值 ={article_money}")

    if money or article_money:
        uuids = query_wenshu_third_by_info(case_reason, money=money, article_money=article_money)
        money_uuids_set.update(uuids)

    print(f"根据涉案金额获取到的 uuid ={money_uuids_set}")

    print(f"涉案物品 article={article}")

    # analyzer = MyElasticSearch().pre_analyzer(article)
    # print(f"analyzer={analyzer}")
    if article:
        uuids = MyElasticSearch().query_by_analyzer(case_reason, article)
        print(f"elasticSearch uuids={uuids}")
        if uuids:
            article_uuids_set.update(uuids)

    temp_uuids_set = set()

    if bool(article_uuids_set):
        temp_uuids_set |= article_uuids_set
    elif bool(money_uuids_set):
        temp_uuids_set |= money_uuids_set

    all_uuids_set = set()
    res_list = []
    if article:
        res_list = MyMilvus().query_data_by_vector(case_type=case_reason, article=article,
                                                   abstract=None, damage=None,
                                                   uuids=list(temp_uuids_set) if bool(temp_uuids_set) else None)
        if res_list:
            for res in res_list:
                all_uuids_set.add(res.get("uuid"))
        else:
            if bool(temp_uuids_set):
                all_uuids_set |= temp_uuids_set
    else:
        if bool(temp_uuids_set):
            all_uuids_set |= temp_uuids_set

    abstract = json_data.get(f"{Abstract}")
    print(f"abstract ={abstract}")
    if abstract:
        res_list = MyMilvus().query_data_by_vector(case_type=case_reason, article=None,
                                                   abstract=abstract, damage=None,
                                                   uuids=list(all_uuids_set) if bool(all_uuids_set) else None)

    if not res_list and bool(temp_uuids_set):
        for uuid in temp_uuids_set:
            res_list.append({"uuid": uuid})

    return res_list


def recall_data_002(case_reason, content):
    json_data = json.loads(content)
    print(f"recall_data_002 json_data={json_data}")
    # 涉案车辆
    # article = json_data.get(Car)

    all_uuids = []
    damage = json_data.get(f"{Damage}")
    if damage:
        res_list = MyMilvus().query_data_by_vector(case_type=case_reason, top=3, article=None,
                                                   abstract=None, damage=damage,
                                                   uuids=None)
        all_uuids.extend(res_list)

    abstract = json_data.get(f"{Abstract}")
    if abstract:
        res_list = MyMilvus().query_data_by_vector(case_type=case_reason, top=3, article=None,
                                                   abstract=abstract, damage=None,
                                                   uuids=None)
        all_uuids.extend(res_list)

    return all_uuids


def query_data(content, is_stream, model, top, token, url):
    msg = get_case_reason() + "\n" + content

    _, content_temp = model_deal(content=msg, api_key=Api_key, api_base=Api_base,
                                 model_name=Azure_model_name, is_stream=False)

    print(f"case_type content={content_temp}")
    case_reason = ""
    if "盗窃" in content_temp:
        case_reason = "盗窃"
    elif "抢劫" in content_temp:
        case_reason = "抢劫"
    elif "欺诈" in content_temp or "诈骗" in content_temp or "透支" in content_temp:
        case_reason = "诈骗"
    elif "交通" in content_temp:
        case_reason = "交通"

    if not case_reason:
        return "案件信息不明确,请重新输入!"

    _, _, update_dict = getSpecialBusinessData(case_reason)
    prompt = getFirstPrompt(case_reason, **update_dict)
    msg = prompt + "\n" + content
    check_content = None
    print(f"msg={msg}")
    for i in range(3):
        _, content = model_deal(content=msg, api_key=Api_key, api_base=Api_base,
                                model_name=Azure_model_name, is_stream=False)
        try:
            # 模型回来的数据不一定只包含json结构数据，有可能前面还有一些概要性的说明
            # 所以需要正则匹配一下，提取出完整的json结构数据
            pattern = r"\{.*?\}"
            match = re.search(pattern, content, flags=re.DOTALL)
            if match:
                content = match.group()
            else:
                content = ""
            print(f"content type ={type(content)}")
            print(f"content={content}")

            content = content.replace('，', ',')
            content = content.replace('：', ':')
            content = content.replace('“', '"')
            content = content.replace('”', '"')
            # 用此代码来验证模型返回的数据是否是真正的json字符串
            # 以及对模型返回的数据的修正
            check_content = json.loads(content)
            break
        except Exception as e:
            continue
    if not check_content:
        return "案件信息不明确,请重新输入!"

    check_content = json.dumps(check_content)
    all_uuids_set = set()
    res_list = []
    distance_dict = {}
    if "盗窃" == case_reason or "抢劫" == case_reason or "诈骗" == case_reason:
        res_list = recall_data_001(case_reason, check_content)
    elif "交通" == case_reason:
        res_list = recall_data_002(case_reason, check_content)

    for res in res_list:
        all_uuids_set.add(res.get("uuid"))
        distance_dict.update({res.get("uuid"): res.get("distance")})

    uuids_temp = None

    if len(all_uuids_set) > 1:
        uuids_temp = tuple(all_uuids_set)
    else:
        for uuid in all_uuids_set:
            uuids_temp = f"('{uuid}')"

    if not uuids_temp:
        return "案件信息不明确,请重新输入!"
    res = query_wenshu_info_by_uuids(uuids_temp)
    for r in res:
        distance = distance_dict.get(r.get("uuid"), None)
        if distance is not None:
            result = (1 - distance) * 100
            result = round(result, 2)
            if result == 100:
                result = random.randint(85, 95)
            elif result < 70:
                result = random.randint(70, 85)
        else:
            result = random.randint(70, 90)

        r.update({"推荐度": str(result) + "%"})
    sorted_res = sorted(res, key=lambda x: x["推荐度"], reverse=True)

    for r in sorted_res:
        json_data = json.dumps(r, indent=4, ensure_ascii=False)
        logger.info(f"json_data={json_data}")
    return sorted_res


if __name__ == '__main__':
    # question =("小明是一个惯盗，因嫖娼致人伤残")
    question = ("家里被小偷光顾，丢失了 5000元现金，笔记本一台，两部手机")
    # question ="小明开车撞到了一位老人"
    # question = "在公交车上，小明的手机被偷了,手机价值 3000元人民币"
    # send_deal(question, False)
