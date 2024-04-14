"""Wrapper around llama.cpp embedding llm_models."""
import json
from typing import List
import requests

import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


from conf import AppConfig



class HttpEmbeddings():
    server_url: str = AppConfig.embedding_server
    model_name: str = AppConfig.embedding_name



    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        texts = list(map(lambda x: x.replace("\n", ""), texts))

        return self.get_response(texts)

    def embed_query(self, text: str) -> List[float]:

        text = text.replace("\n", "")
        texts = [text]
        if len(self.get_response(texts)) > 0:
            return self.get_response(texts)[0]
        else:
            return []

    def get_response(self, texts: List[str]) -> List[List[float]]:

        server_url = self.server_url
        requestBody = {"model_name": self.model_name, "texts": texts}
        responses = requests.post(server_url, json=requestBody)
        responsesJson = responses.json()
        if responsesJson.get("data"):
            return responsesJson["data"]["value"]
        return []
