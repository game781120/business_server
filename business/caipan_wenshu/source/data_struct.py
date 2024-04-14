import signal
import threading
from datetime import datetime
import re
import time
from my_log.mylogger import logger

import json
from my_elastic import MyElasticSearch
from my_milvus import MyMilvus

from utils import xlsx_file_append as xlsx_append

from my_model import model_deal, OpenAITokenSize
from my_mysql import (query_wenshu_second_all,
                      query_wenshu_second_by_uuid,
                      insert_wenshu_second_v2,
                      update_wenshu_second_v2,
                      update_wenshu_second_is_es,
                      update_wenshu_second_is_mysql,
                      update_wenshu_second_is_milvus,
                      query_wenshu_third_moeny_by_uuid,
                      query_wenshu_like_info_by_case_reason,
                      query_wenshu_like_info_by_uuid,
                      insert_wenshu_third_info,
                      update_wenshu_third_info,

                      )

from business.caipan_wenshu.source.utils import (money_deal,
                                                 Api_key,
                                                 Api_base,
                                                 Model_name,
                                                 Location,
                                                 Damage,
                                                 Abstract,
                                                 PunishMoney,
                                                 ArticleMoney,
                                                 getSpecialBusinessData,
                                                 getFirstPrompt)

import multiprocessing
import psutil
import schedule

task_queue_waiting = multiprocessing.Queue(maxsize=20)
# 为了统计正在处理的任务数量，需要一个额外的队列
file_queue_processing = multiprocessing.Queue(maxsize=20)
processes = []


def process_deal(queue_waiting, file_queue):
    while True:
        # 获取当前进程的 PID
        current_process = psutil.Process()
        process_id = current_process.pid
        # 获取当前进程所在的 CPU 核心编号
        cpu_affinity = current_process.cpu_num()

        data = queue_waiting.get()

        msg = data.get("msg")
        uuid = data.get("uuid")
        tokens = data.get("tokens")
        is_exist = data.get("is_exist")
        case_reason = data.get("case_reason")
        logger.info(f"进程id {process_id} 开始处理数据 uuid = {uuid}")
        logger.info(f"msg={msg}")
        logger.info(f"model_name={Model_name}")
        logger.info(f"tokens={tokens}")

        start_time = time.time()
        start_time_str = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
        code, content = model_deal(content=msg,
                                   api_key=Api_key,
                                   api_base=Api_base,
                                   model_name=Model_name,
                                   is_stream=False)
        response_time = time.time()
        end_time_str = datetime.fromtimestamp(response_time).strftime('%Y-%m-%d %H:%M:%S')
        requests_step_time = (response_time - start_time) * 1000
        sub_time = f"{'{:.2f}'.format(requests_step_time)}"
        print(f"模型返回={code} {content}")

        if code != 200:
            data = [
                [uuid, process_id, start_time_str, end_time_str, Model_name, sub_time, tokens, f"错误 {code}", content,
                 msg]]
            file_queue.put(data)
            continue

        try:
            # 模型回来的数据不一定只包含json结构数据，有可能前面还有一些概要性的说明
            # 所以需要正则匹配一下，提取出完整的json结构数据
            pattern = r"\{.*?\}"
            match = re.search(pattern, content, flags=re.DOTALL)
            if match:
                content = match.group()

            content = content.replace('，', ',')
            content = content.replace('：', ':')
            content = content.replace('“', '"')
            content = content.replace('”', '"')
            # content = content.replace('\\*', 'x')

            # 用此代码来验证模型返回的数据是否是真正的json字符串
            # 以及对模型返回的数据的修正
            check_content = json.loads(content)
            if not check_content.get("涉案人员姓名"):
                logger.info(f"进程id={process_id} uuid = {uuid}  内容提取失败,需要重新提取")
                continue

            name0, name1, _ = getSpecialBusinessData(case_reason)
            if name0 and name1:
                if not check_content.get(f"{name0}") and not check_content.get(f"{name1}"):
                    del check_content[f"{name0}"]
                    del check_content[f"{name1}"]
                    del check_content["案发时间"]
                    del check_content["案发地点"]
                    logger.info(f"-------- 有修正数据 uuid = {uuid}")
            data = [
                [uuid, process_id, start_time_str, end_time_str, Model_name, sub_time, tokens, "正常", content, msg]]
            file_queue.put(data)
        except Exception as e:
            logger.info(f"进程id={process_id} uuid ={uuid} e ={e} 不是json格式 = {content}")
            data = [
                [uuid, process_id, start_time_str, end_time_str, Model_name, sub_time, tokens, f"错误: {e}", content,
                 msg]]
            file_queue.put(data)
            continue
        '''     
          模型返回已经是json字符串,如果没有前端输出格式的要求或者上面没有调用json.loads
          此处就不用再调用json.dumps,
          此处再调用json.dumps的目的是让其json数据缩进和不进行编码
          不进行编码的目的便于人工查看内容
        '''
        content = json.dumps(check_content, indent=4, ensure_ascii=False)

        if not is_exist:
            insert_wenshu_second_v2(uuid, case_reason, content)
        else:
            update_wenshu_second_v2(uuid, case_reason, content)

        logger.info(f"进程id {process_id} 数据处理完成 uuid = {uuid}")


def xlsx_file_deal(file_queue):
    file_name01 = "/home/ubuntu/yjq/poc_business_server/内容提取时性能数据20240410.xlsx"
    while True:
        data = file_queue.get()
        xlsx_append(file_name01, "数据", data)


def sigint_handler(signum, frame):
    logger.info('Signal received, stopping processes...')
    for p in processes:
        p.terminate()
        p.join(timeout=5)


def data_cleaning_first(case_reason):
    for i in range(10):
        p = multiprocessing.Process(target=process_deal, args=(task_queue_waiting, file_queue_processing))
        p.start()
        processes.append(p)

    p = multiprocessing.Process(target=xlsx_file_deal, args=(file_queue_processing,))
    p.start()
    processes.append(p)

    # 注册SIGINT信号处理函数
    signal.signal(signal.SIGINT, sigint_handler)

    _, _, update_dict = getSpecialBusinessData(case_reason)
    prompt = getFirstPrompt(case_reason, **update_dict)
    data_dict = query_wenshu_like_info_by_case_reason(case_reason)
    i = 0
    for uuid, value in data_dict.items():
        temp_dict = query_wenshu_second_by_uuid(uuid)
        is_model = 0
        is_exist = False
        for _, temp_value in temp_dict.items():
            is_model = temp_value.get('is_model', None)
            break
        # if is_model == 1:
        #     continue
        if temp_dict:
            is_exist = True
        i += 1
        if i >= 3:
            break

        msg = prompt + value.get('full_text')
        tokens = OpenAITokenSize().calc_token_size("gpt-3.5-turbo", msg)
        data_temp = {"uuid": uuid, "is_exist": is_exist, "tokens": tokens, "case_reason": value.get('case_reason'),
                     "msg": msg}
        logger.info(f"加入队列 {uuid}  {tokens}   主进程")
        task_queue_waiting.put(data_temp)

    # 等待所有子进程完成
    for p in processes:
        p.join()

    logger.info('All processes finished')


def data_into_wenshu_third(uuid, type_name, money_value, punish_money_value, article_money_value):
    money = None
    punish_money = None
    article_money = None
    if money_value:
        money = money_deal(money_value)
    if punish_money_value:
        punish_money = money_deal(punish_money_value)
    if article_money_value:
        article_money = money_deal(article_money_value)
    if money or punish_money or article_money:
        # 如果有涉案金额和处罚金额,便写入mysql
        res = query_wenshu_third_moeny_by_uuid(uuid)
        try:
            if not res:
                insert_wenshu_third_info(uuid, type_name=type_name,
                                         money=money, article_money=article_money,
                                         punish_money=punish_money)
            else:
                update_wenshu_third_info(uuid, type_name=type_name,
                                         money=money, article_money=article_money,
                                         punish_money=punish_money)

        except Exception as e:
            logger.info(f"data_into_wenshu_third uuid = {uuid} e={e}")
            return False
    return True


def run_schedule(stop_event):
    # 每隔5分钟执行一次落盘操作
    schedule.every(5).minutes.do(MyMilvus().flush_collection)
    while not stop_event.is_set():
        schedule.run_pending()
        time.sleep(3)


def data_to_es_milvus_mysql():
    # 在新线程中运行定时任务
    stop_event = threading.Event()
    th = threading.Thread(target=run_schedule, args=(stop_event,))
    th.start()

    data_dict = query_wenshu_second_all()
    # data_dict = query_wenshu_second_by_uuid("00339096-ecf6-45db-b4ae-6cab9be2d5b9")
    for uuid, value in data_dict.items():

        type_name = value.get('type_name')
        text0, text1, _ = getSpecialBusinessData(type_name)
        is_es = value.get('is_es')
        is_milvus = value.get('is_milvus')
        is_mysql = value.get('is_mysql')
        content = value.get('content')
        content_json = None
        try:
            content_json = json.loads(content)
        except Exception as e:
            logger.info(f"uuid={uuid} e={e}")
        if not content_json:
            continue

        data = {"uuid": uuid,
                "caseType": type_name,
                "location": content_json.get(f"{Location}"),
                "article": content_json.get(f"{text1}"),
                "special": "",
                "damage": content_json.get(f"{Damage}"),
                "abstract": content_json.get(f"{Abstract}")
                }
        logger.info(f"uuid={uuid} is_es={is_es} is_milvus={is_milvus} is_mysql={is_mysql}")
        if is_es != 1:
            try:
                if not MyElasticSearch().query_by_uuid(uuid):
                    MyElasticSearch().insert_data(uuid, data)
                    logger.info(f"es insert_data 成功 uuid={uuid}")
                else:
                    MyElasticSearch().update_data(uuid, data)
                    logger.info(f"es update_data 成功 uuid={uuid}")
            except Exception as e:
                logger.info(f"data={data} es处理异常 {e}")
                continue
            update_wenshu_second_is_es(uuid)

        if is_milvus != 1:
            try:
                MyMilvus().delete_data(uuid)
                MyMilvus().insert_data(data)
                update_wenshu_second_is_milvus(uuid)
            except Exception as e:
                logger.info(f"data={data}  milvus处理异常 {e}")
                continue

        if is_mysql != 1:
            money = content_json.get(f"{text0}")
            punish_money = content_json.get(f"{PunishMoney}")
            article_money = content_json.get(f"{ArticleMoney}")
            if data_into_wenshu_third(uuid, type_name, money, punish_money, article_money):
                update_wenshu_second_is_mysql(uuid)

    time.sleep(5)
    # 执行最后一次落盘
    MyMilvus().flush_collection()
    stop_event.set()

    # 主线程等待子线程退出
    th.join()
    print('Subthread joined')


if __name__ == '__main__':
    data_cleaning_first("抢劫")
    # data_to_es_milvus_mysql()
