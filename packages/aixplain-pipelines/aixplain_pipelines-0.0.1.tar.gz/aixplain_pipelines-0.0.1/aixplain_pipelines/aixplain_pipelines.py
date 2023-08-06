__author__='thiagocastroferreira'

"""
Author: Duraikrishna Selvaraju and Thiago Castro Ferreira
Date: May 9th 2022
Description:
    Pipeline Class
    
"""

import logging

import aixplain_pipelines.execution as execution
from aixplain_pipelines.utils.config import PIPELINES_RUN_URL

class Pipeline:
    def __init__(self, api_key:str, url:str=PIPELINES_RUN_URL):
        """
        params:
        ---
            api_key: API key of the pipeline
            url: API endpoint
        """
        self.url = url
        self.api_key = api_key


    def run(self, data:str, name:str="pipeline_process"):
        """
        params:
        ---
            data: link to the input data
            name: name to the process
        """
        logging.info(f"Started pipeline run with process name: {name}")
        result = execution.run(self.url, self.api_key, data, name=name)
        logging.info(f"Completed pipeline run with process name: {name}")
        return result