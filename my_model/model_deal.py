import json
import brainai
from my_log.mylogger import logger


def model_deal(content, api_key, api_base, model_name, is_stream):
    chat_model_kwargs = {
        "api_key": api_key,
        "api_base": api_base,
        "object_name": "billing.v1.chat.completions",
        "model": f"{model_name}",
        "messages": [
            {
                "role": "user",
                "content": content,
            }
        ],
        "temperature": 0,
        "stream": is_stream
    }
    response = brainai.ChatCompletion.create(**chat_model_kwargs)
    if type(response) == brainai.error.APIError:
        return response.http_status, response.http_body

    data = json.loads(response)
    content = data['choices'][0]['message']['content']
    logger.info(f"模型返回={content}")
    return 200, content
