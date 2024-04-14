import brainai
import json
from file_parse import file_parse
model_api_key = "RBbNKRkaNaOu78agDa03055224864b88A071067fA99177Fb"
model_api_base = "https://brain.thundersoft.com/brain"
knowledge_api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJhcGlLZXlcIjpcIm45aG1NTFc0WXNMdUNJSDZFMTU1RmQ4MEI3MWQ0YzZhQThEZUMzQzk5NzhiQTU3NlwiLFwiY3JlYXRlVGltZVwiOlwiMFwiLFwiZW1haWxcIjpcIlwiLFwiaWRcIjoyODcsXCJtb2JpbGVcIjpcIjEzMDExMDMzNzk2XCIsXCJwYXNzd29yZFwiOlwiXCIsXCJwd2RUaW1lXCI6XCIxNzAxNDE4Nzk4MzgxXCIsXCJyZW1hcmtcIjpcIlwiLFwicm9sZXNcIjpbe1wiaWRcIjozLFwibmFtZVwiOlwi5pmu6YCa55So5oi3XCJ9XSxcInN0YXR1c1wiOjEsXCJ0ZW5hbnRJZFwiOjAsXCJ0ZW5hbnROYW1lXCI6XCJcIixcInR5cGVcIjpcInVzZXJcIixcInVzZXJOb1wiOlwidTEzMFwiLFwidXNlcm5hbWVcIjpcIuWnmuW7uua4oFwiLFwid2FybmluZ1wiOlwiMFwiLFwiZ2VuX3RpbWVcIjoxNzA5NTM5MjM2NDY2fSIsImV4cCI6MTcxMjEzMTIzNn0.J2KH3PhbkIJ4ViQpZcnRY7QN-eWuJgX40p__A41dLwQ"
knowledge_api_base = "http://10.0.36.13:8888/brain"
stream = False

title = ["主要完成情况","存在的问题","下一步的计划"]

if __name__ == '__main__':
    file_content_list = file_parse()
    for key, file_cont in file_content_list.items():
        if key == 0:
            continue
        #print(f"---key:{key} file_cont :\n{file_cont}\n")

        #cc = f"请根据下面的文本内容进行以述职报告的形式输出，并且以 ‘{title[key - 1]}’ 作为输出的标题,文本内容如下：\n {file_cont}"
        print("\n\n\n")
        cc = f"请根据下面的文本内容以 ‘{title[key - 1]}’ 为主题进行重新整理，并以‘{title[key - 1]}’作为输出的标题,文本内容如下：\n {file_cont}"
        print(f'{cc}')
        # 基于模型聊天
        chat_model_kwargs = {
            "api_key": model_api_key,
            "api_base": model_api_base,
            "object_name": "billing.v1.chat.completions",
            "model": "azure-gpt-3.5-turbo-16k",
            "messages": [
                {
                    "role": "user",
                    "content": cc,
                }
            ],
            "temperature": 0,
            "stream": stream
        }
        #print(f"reques={json.dumps(chat_model_kwargs, ensure_ascii=False)}")
        response = brainai.ChatCompletion.create(**chat_model_kwargs)
        data = json.loads(response)
        content = data['choices'][0]['message']['content']
        print(content)

        # json_str = response.replace('\\', '')
        # response =json.dumps(json_str,indent=4,ensure_ascii=False)


        # 将JSON字符串转换为Python字典
        #data = json.loads(json_str)
        # print("------------------")
        # print(response)
        # print("------------------")

        # for chunk in response:
        #     print(f"{json.dumps(chunk,ensure_ascii=False)}")