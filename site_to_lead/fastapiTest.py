from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel,Field
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
from pprint import pformat, pprint
from workBitrix import create_lead
from fastapi.staticfiles import StaticFiles
load_dotenv()
PORT = os.getenv('PORT')
HOST = os.getenv('HOST')
PAY_ENTY_ID = os.getenv('PAY_ENTY_ID')

app = FastAPI(
    title="site-to-lead System API",
    description="A pkGroup API\nЛоги можно посмотреть по пути /logs\nОчистить логи можно по пути /clear_logs\n",
    version="1.0"
)
app.mount("/static", StaticFiles(directory="static/"), name="static")
templates = Jinja2Templates(directory="templates")
logs = []

class LogEntry(BaseModel):
    log_entry: str
    log_level: str = 'INFO'

class PayData(BaseModel):
    event: str
    data: dict
    ts: int

class FieldValue(BaseModel):
    value: str

class PhoneEmailValue(BaseModel):
    VALUE: str
    VALUE_TYPE: str

class Fields(BaseModel):
    passport_serial: FieldValue = Field(..., alias='паспорт_серия')
    issued_by: FieldValue = Field(..., alias='Кем_выдан')
    issue_date: FieldValue = Field(..., alias='дата_выдачи')
    registered_street: FieldValue = Field(..., alias='зарегистрирован_улица')
    city: FieldValue = Field(..., alias='город')
    phone: FieldValue = Field(..., alias='телефон')
    email: FieldValue = Field(..., alias='email')
    passport_number: FieldValue = Field(..., alias='паспорт_номер')
    subdivision_code: FieldValue = Field(..., alias='код_подразделения')
    group: FieldValue = Field(..., alias='группа')
    certificate: FieldValue = Field(..., alias='справка')
    inn: FieldValue = Field(..., alias='ИНН')
    snils: FieldValue = Field(..., alias='Снилс')
    pc: FieldValue = Field(..., alias='пк')
    aaffcfg: FieldValue = Field(..., alias='aaffcfg')
    restrictions: FieldValue = Field(..., alias='ограничения')
    agreement: FieldValue = Field(..., alias='Согласие_на_обработку')

class RequestModel(BaseModel):
    fields: Fields
    submission_id: str

def send_log(message, level='INFO'):
    print(f'попали в send_log {message=}, {level=}')
    # requests.post(f'http://{HOST}:{PORT}/logs', json={'log_entry': message, 'log_level': level}, timeout=1)
    requests.post(f'http://127.0.0.1:{PORT}/logs', json={'log_entry': message, 'log_level': level}, timeout=1)
    print(f'вышли из send_log')

@app.post("/submit")
async def submit_form(request: Request, data: RequestModel):
    pprint(request.__dict__)
    print('data_------------------')
    pprint(data.__dict__)
    # Assuming 'name' is provided in the request or generated somehow
    name = ["Last", "First", "Second"]
    print('name', name)
    print(f'{data.fields.passport_serial.value=}')
    print(f'{data.fields.issued_by.value=}')
    print(f'{data.fields.issue_date.value=}')
    print(f'{data.fields.registered_street.value=}')
    print(f'{data.fields.city.value=}')
    print(f'{data.fields.phone.value=}')
    print(f'{data.fields.email.value=}')
    print(f'{data.fields.passport_number.value=}')
    print(f'{data.fields.subdivision_code.value=}')
    print(f'{data.fields.group.value=}')
    print(f'{data.fields.certificate.value=}')
    print(f'{data.fields.inn.value=}')
    print(f'{data.fields.snils.value=}')
    print(f'{data.fields.pc.value=}')

    print(f'{data.fields.aaffcfg.value=}')
    print(f'{data.fields.restrictions.value=}')
    print(f'{data.fields.agreement.value=}')
    print(f'{data.submission_id=}')
    # update_deal(data)


    
    fields = {
        'TITLE': 'Заявка с сайта',
        'UF_CRM_PSPRT_SERIAL': data.fields.passport_serial.value,
        'UF_CRM_PSPRT_ISSUED': data.fields.issued_by.value,
        'UF_CRM_PSPRT_DATE': data.fields.issue_date.value,
        'UF_CRM_REG_STREET': data.fields.registered_street.value,
        'UF_CRM_REG_CITY': data.fields.city.value,
        'PHONE': [{
            'VALUE': data.fields.phone.value,
            'VALUE_TYPE': 'WORK'
        }],
        'EMAIL': [{
            'VALUE': data.fields.email.value,
            'VALUE_TYPE': 'WORK'
        }],
        'UF_CRM_PSPRT_NUMBER': data.fields.passport_number.value,
        'UF_CRM_PSPRT_CODE': data.fields.subdivision_code.value,
        'LAST_NAME': name[0],
        'NAME': name[1],
        'SECOND_NAME': name[2],
        'UF_CRM_DSBLT_GROUP': data.fields.group.value,
        'UF_CRM_DSBLT_CERT': data.fields.certificate.value,
        'UF_CRM_TAX_CERT': data.fields.inn.value,
        'UF_CRM_PENSION_CERT': data.fields.snils.value,
        'UF_CRM_SKILL_PC': data.fields.pc.value,
        'UF_CRM_SKILL_WORK': data.fields.aaffcfg.value,
        'UF_CRM_DISABILITY': data.fields.restrictions.value,
        'UF_CRM_AGREEMENT': 'Y' if data.fields.agreement.value == 'on' else 'N',
        'UF_CRM_SUBMISSION_ID': data.submission_id,
    }
    # fields = {
    #     'TITLE': 'Заявка с сайта',
    #     'UF_CRM_PSPRT_SERIAL': data.fields.паспорт_серия.value,
    #     'UF_CRM_PSPRT_ISSUED': data.fields.Кем_выдан.value,
    #     'UF_CRM_PSPRT_DATE': data.fields.дата_выдачи.value,
    #     'UF_CRM_REG_STREET': data.fields.зарегистрирован_улица.value,
    #     'UF_CRM_REG_CITY': data.fields.город.value,
    #     'PHONE': [{
    #         'VALUE': data.fields.телефон.value,
    #         'VALUE_TYPE': 'WORK'
    #     }],
    #     'EMAIL': [{
    #         'VALUE': data.fields.email.value,
    #         'VALUE_TYPE': 'WORK'
    #     }],
    #     'UF_CRM_PSPRT_NUMBER': data.fields.паспорт_номер.value,
    #     'UF_CRM_PSPRT_CODE': data.fields.код_подразделения.value,
    #     'LAST_NAME': name[0],
    #     'NAME': name[1],
    #     'SECOND_NAME': name[2],
    #     'UF_CRM_DSBLT_GROUP': data.fields.группа.value,
    #     'UF_CRM_DSBLT_CERT': data.fields.справка.value,
    #     'UF_CRM_TAX_CERT': data.fields.ИНН.value,
    #     'UF_CRM_PENSION_CERT': data.fields.Снилс.value,
    #     'UF_CRM_SKILL_PC': data.fields.пк.value,
    #     'UF_CRM_SKILL_WORK': data.fields.aaffcfg.value,
    #     'UF_CRM_DISABILITY': data.fields.ограничения.value,
    #     'UF_CRM_AGREEMENT': 'Y' if data.fields.Согласие_на_обработку.value == 'on' else 'N',
    #     'UF_CRM_SUBMISSION_ID': data.submission_id,
    # }
    pprint(fields)
    send_log(fields, 'DEBUG')
    
    # create_lead(fields)
    
    return {"fields": 'fields'}










#работа с логами

def log_counts_by_level(logs: list) -> dict:
    counts = {'DEBUG': 0, 'INFO': 0, 'WARNING': 0, 'ERROR': 0}
    for log in logs:
        counts[log['level']] += 1
    return counts

def log_counts_by_minute(logs: list) -> dict:
    counts_by_minute = {}
    for log in logs:
        timestamp_minute = log['timestamp'][:16]  # Обрезаем до минут
        if timestamp_minute in counts_by_minute:
            counts_by_minute[timestamp_minute][log['level']] += 1
        else:
            counts_by_minute[timestamp_minute] = {'DEBUG': 0, 'INFO': 0, 'WARNING': 0, 'ERROR': 0}
            counts_by_minute[timestamp_minute][log['level']] += 1
    return counts_by_minute




@app.post("/logs")
async def add_log(log: Request):
    global logs

    pprint(log.__dict__)
    json = await log.json()
    log_entry=json.get('log_entry')
    log_level = json.get('log_level')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    if len(logs) >= 100:
        logs.pop(0)
    logs.append({'timestamp': timestamp, 'level': log_level, 'message': log_entry})
    return {"message": "Лог записан!"}

@app.get("/logs", response_class=HTMLResponse)
async def view_logs(request: Request):
    global logs
    for log in logs:
        if isinstance(log['message'], dict) or isinstance(log['message'], list):
            log['message'] = pformat(log['message'])

    logs.reverse()
    counts_log = log_counts_by_level(logs)
    counts_log = log_counts_by_minute(logs)
    pprint(counts_log)
    return templates.TemplateResponse("index.html", {"request": request, "logs": logs, "log_counts": counts_log})

@app.post("/clear_logs")
async def clear_logs():
    global logs
    logs.clear()
    return {"message": "Логи очищены!"}

@app.post("/")
async def handle_post_request(request: Request):
    data = await request.form()
    pprint(data)
    domain = request.query_params.get('DOMAIN')
    protocol = request.query_params.get('PROTOCOL')
    lang = request.query_params.get('LANG')
    app_sid = request.query_params.get('APP_SID')

    # здесь можно добавить код для обработки параметров из запроса
    # например, сохранить их в базу данных или выполнить какие-то другие действия

    return {"message": "Request processed successfully"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=HOST, port=int(PORT))
   
    # send_log(fields, 'DEBUG')