import datetime
import time
from typing import List

from openpyxl import load_workbook

import os
import sys

# parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(parent_dir)

from utils import xlsx_file_parsing as xlsx_parsing
from my_mysql import createMysqlConnect, inserData, query_wenshu_by_case_num_case_name

import uuid


def xlsx_file_to_table(file_name, ws, max_rows, first_line_ignore):
    cnx = createMysqlConnect()
    i = 0
    head: List[str] = []
    for datas in xlsx_parsing(file_name, max_rows, ws):
        for row_data in datas:
            i += 1
            if first_line_ignore and i == 1:
                head.extend(row_data)
                print(f"head={head}")
                continue

            if query_wenshu_by_case_num_case_name(row_data[1], row_data[2]):
                print(f"重复 case_num ={row_data[1]}, case_name= {row_data[2]}")
                continue

            # uid = uuid.uuid4()
            # row_data.insert(0, str(uid))
            # print(f"row_data={row_data}")
            #
            # try:
            #     inserData(cnx, row_data)
            #     print(f"案号[{uid}] 成功写入库")
            # except Exception as e:
            #     print(f"{e} 案号[{uid}]")

    cnx.close()


if __name__ == '__main__':
    file_name = "/home/ubuntu/yjq/poc_business_server/business/caipan_wenshu/files/source_files/test.xlsx"
    xlsx_file_to_table(file_name, "Sheet1", 100, True)
