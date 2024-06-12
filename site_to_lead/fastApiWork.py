from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict, Union
from pprint import pprint
# app = FastAPI()

import requests
import os
from dotenv import load_dotenv
load_dotenv()
PORT = os.getenv('PORT')
HOST = os.getenv('HOST')
PAY_ENTY_ID = os.getenv('PAY_ENTY_ID')
class LogEntry(BaseModel):
    log_entry: str
    log_level: str = 'INFO'

def send_log(message, level='INFO'):
    a=requests.post(f'http://{HOST}:{PORT}/logs', json={'log_entry': message, 'log_level': level})
    # b=LogEntry(log_entry=str(message), log_level=level)
    # b.log_entry = message
    # b.log_level = level

    # a=requests.post(f'http://{HOST}:{PORT}/logs', json=b)
    pprint(a.text)
fields = {'EMAIL': [{'VALUE': 'string', 'VALUE_TYPE': 'WORK'}],
        'LAST_NAME': 'Last',
        'NAME': 'First',
        'PHONE': [{'VALUE': 'string', 'VALUE_TYPE': 'WORK'}],
        'SECOND_NAME': 'Second',
        'TITLE': 'Заявка с сайта',
        'UF_CRM_AGREEMENT': 'N',
        'UF_CRM_DISABILITY': 'string',
        'UF_CRM_DSBLT_CERT': 'string',
        'UF_CRM_DSBLT_GROUP': 'string',
        'UF_CRM_PENSION_CERT': 'string',
        'UF_CRM_PSPRT_CODE': 'string',
        'UF_CRM_PSPRT_DATE': 'string',
        'UF_CRM_PSPRT_ISSUED': 'string',
        'UF_CRM_PSPRT_NUMBER': 'string',
        'UF_CRM_PSPRT_SERIAL': 'string',
        'UF_CRM_REG_CITY': 'string',
        'UF_CRM_REG_STREET': 'string',
        'UF_CRM_SKILL_PC': 'string',
        'UF_CRM_SKILL_WORK': 'string',
        'UF_CRM_SUBMISSION_ID': 'string',
        'UF_CRM_TAX_CERT': 'string'}
send_log(fields, 'DEBUG')