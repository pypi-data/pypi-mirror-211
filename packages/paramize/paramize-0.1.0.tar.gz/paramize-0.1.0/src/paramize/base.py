# Copyright 2023 Wingify Software Pvt. Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from langchain.prompts import PromptTemplate
from typing import Dict, Union, Any, List
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult
import requests, json
from langchain.callbacks.utils import (
    BaseMetadataCallbackHandler,
    flatten_dict,
)
from langchain.prompts.base import (
    DEFAULT_FORMATTER_MAPPING
)
import os
from copy import deepcopy

# BASE_URL = "http://localhost:3000"
BASE_URL = "https://beta-app.paramize.com"

class ParamizeConfig:
    _instance = None

    def __init__(self, api_key):
        self.api_key = api_key
        ParamizeConfig._instance = self

    @staticmethod
    def get_instance():
        if ParamizeConfig._instance is None:
            raise Exception("ParamizeConfig instance does not exist")
        return ParamizeConfig._instance

    # def getApiKey(self):
    #     return self.api_key


class ParamizePromptTemplate(PromptTemplate):
    prompt_template:str = None
    variation_hash:str = None
    input_variables_with_values:object = None

    def format(self, **kwargs: Any) -> str:
        kwargs = self._merge_partial_and_user_variables(**kwargs)
        self.input_variables_with_values = deepcopy(kwargs)

        # Make request to get variations
        try:
            # print("ParamizeConfig: ", ParamizeConfig.get_instance().api_key)
            data = ParamizeConnectionService.getVariations(self.template)
            data = data['data']
            # select any element fron our templateArray that we received from BE
            self.prompt_template = self.template
            self.template = data['variation_template'] # This contains variation_template
            self.variation_hash = data['variation_hash']
            # print('\n Data: ', data)
        except Exception as e:
            print("\n\nError: ", e)
            # print('\n\n\n')

        return DEFAULT_FORMATTER_MAPPING[self.template_format](self.template, **kwargs)

class ParamizeCallbackHandler(BaseMetadataCallbackHandler, BaseCallbackHandler):

    def __init__(self, prompt, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.callback_columns: list = []
        self.prompt:ParamizePromptTemplate = prompt

    def _init_resp(self) -> Dict:
        return {k: None for k in self.callback_columns}

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        # When llm starts
        resp = self._init_resp()
        resp.update({"action": "on_llm_start"})
        resp.update(flatten_dict(serialized))
        resp.update({"run_id": f"{str(kwargs['run_id'])}"})
        resp.update({"parent_run_id": f"{str(kwargs['parent_run_id'])}"})
        resp.update(self.get_custom_callback_meta())

        for prompt in prompts:
            prompt_resp = deepcopy(resp)
            prompt_resp["formatted_prompt"] = prompt
            prompt_resp["variation_template"] = self.prompt.template #this has variation_template
            prompt_resp["variation_hash"] = self.prompt.variation_hash
            prompt_resp["prompt_template"] = self.prompt.prompt_template #write as template
            prompt_resp["input_variables"] = self.prompt.input_variables_with_values
            prompt_resp["hashed_key"] = ParamizeConfig.get_instance().api_key
            self.on_llm_start_records.append(prompt_resp)

        data = self.on_llm_start_records[0]
        # print(f"Data ; {data}")
        ParamizeConnectionService.makePostRequest(data=data, actionUrl="setLlmStart")

        # print(f"on_llm_start -> {self.on_llm_start_records[0]}")

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        resp = self._init_resp()
        resp.update({"action": "on_llm_end"})
        resp.update(flatten_dict(response.llm_output or {}))
        resp.update(self.get_custom_callback_meta())
        resp.update({"run_id": f"{str(kwargs['run_id'])}"})
        resp.update({"parent_run_id": f"{str(kwargs['parent_run_id'])}"})

        for generations in response.generations:
            for generation in generations:
                generation_resp = deepcopy(resp)
                generation_resp.update(flatten_dict(generation.dict()))
                self.on_llm_end_records.append(generation_resp)

        data = self.on_llm_end_records[0]
        ParamizeConnectionService.makePostRequest(data=data, actionUrl="setLlmEnd")
        # print(f"on_llm_end -> {self.on_llm_end_records[0]}")

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when LLM errors."""


class ParamizeConnectionService:
    def __init__(self) -> None:
        self.PARAMIZE_API_KEY = os.environ["PARAMIZE_API_KEY"] or ParamizeConfig.get_instance().api_key

    def getVariations(prompt_template) -> json:
        try:
            URL = BASE_URL + "/api/v1/request-variations/getVariationsFromAI"
            # defining a params dict for the parameters to be sent to the API
            body = {'prompt_template': prompt_template}
            headers =  {"Content-Type":"application/json", 'Authorization': 'Bearer ' + ParamizeConfig.get_instance().api_key}
            # sending get request and saving the response as response object
            r = requests.post(url = URL, data = json.dumps(body), headers= headers)
            # extracting data in json format
            data = r.json()
            # print('\n Data: ', data)
            return data
        except Exception as e:
            print('\n\n Error: ', e)

    def makePostRequest(data, actionUrl):
        try:
            URL = BASE_URL + "/api/v1/langchain/" + actionUrl
            # defining a params dict for the parameters to be sent to the API
            body = data
            headers =  {"Content-Type":"application/json", 'Authorization': 'Bearer ' + ParamizeConfig.get_instance().api_key}
            # sending get request and saving the response as response object
            r = requests.post(url = URL, data = json.dumps(body), headers= headers)
            # extracting data in json format
            # print('\n Post response: ', r)
            data = r.json()
            return data
        except Exception as e:
            print('\n\n Error: ', e)
