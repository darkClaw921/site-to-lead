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
from typing import List, Dict
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





def send_log(message, level='INFO'):
    print(f'попали в send_log {message=}, {level=}')
    # requests.post(f'http://{HOST}:{PORT}/logs', json={'log_entry': message, 'log_level': level}, timeout=1)
    requests.post(f'http://127.0.0.1:{PORT}/logs', json={'log_entry': message, 'log_level': level}, timeout=2)
    print(f'вышли из send_log')





@app.post("/submit")
async def submit_form(data: Request):
    # pprint(request.__dict__)
    # print('data_------------------')
    # # pprint(data.__dict__)
    # Assuming 'name' is provided in the request or generated somehow
    # Splitting the full name into parts
    data=await data.form()
    full_name = data['fields[ФИО][value]']
    name_parts = full_name.split(' ')

    # Ensure there are enough parts; if not, fill with empty strings
    if len(name_parts) < 3:
        name_parts += [''] * (3 - len(name_parts))

    last_name, first_name, second_name = name_parts[0], name_parts[1], name_parts[2]

    print('name', last_name, first_name, second_name)
    print(f"{data.get('fields[паспорт номер][value]')=}")
    print(f"{data.get('fields[Кем выдан][value]')=}")
    print(f"{data.get('fields[дата выдачи][value]')=}")
    print(f"{data.get('fields[зарегистрирован улица][value]')=}")
    print(f"{data.get('fields[город][value]')=}")
    print(f"{data.get('fields[телефон][value]')=}")
    print(f"{data.get('fields[email][value]')=}")
    print(f"{data.get('fields[паспорт серия][value]')=}")
    print(f"{data.get('fields[код подразделения][value]')=}")
    print(f"{data.get('fields[группа][value]')=}")
    print(f"{data.get('fields[справка][value]')=}")
    print(f"{data.get('fields[ИНН][value]')=}")
    print(f"{data.get('fields[Снилс][value]')=}")
    print(f"{data.get('fields[пк][value]')=}")
    print(f"{data.get('fields[aaffcfg][value]')=}")
    print(f"{data.get('fields[ограничения][value]')=}")
    print(f"{data.get('fields[Согласие на обработку][value]')=}")
    print(f"{data.get('submission_id')=}")
    # update_deal(data)
    
    # print(f"{data['fields[дата выдачи][value]']=}")
    # print(f"{data['fields[зарегистрирован улица][value]']=}")
    # print(f"{data['fields[город][value]']=}")
    # print(f"{data['fields[телефон][value]']=}")
    # print(f"{data['fields[email][value]']=}")
    # print(f"{data['fields[паспорт серия][value]']=}")
    # print(f"{data['fields[код подразделения][value]']=}")
    # print(f"{data['fields[группа][value]']=}")
    # print(f"{data['fields[справка][value]']=}")
    # print(f"{data['fields[ИНН][value]']=}")
    # print(f"{data['fields[Снилс][value]']=}")
    # print(f"{data['fields[пк][value]']=}")
    # print(f"{data['fields[aaffcfg][value]']=}")
    # print(f"{data['fields[ограничения][value]']=}")
    # print(f"{data['fields[Согласие на обработку][value]']=}")
    # print(f"{data['submission_id']=}")
    # update_deal(data)



    fields={
        'TITLE': 'Заявка с сайта',
        'UF_CRM_PSPRT_SERIAL': data.get('fields[паспорт серия][value]'),
        'UF_CRM_PSPRT_ISSUED': data.get('fields[Кем выдан][value]'),    
        'UF_CRM_PSPRT_DATE': data.get('fields[дата выдачи][value]'),
        'UF_CRM_REG_STREET': data.get('fields[зарегистрирован улица][value]'),
        'UF_CRM_REG_CITY': data.get('fields[город][value]'),
        'PHONE': [{
            'VALUE': data.get('fields[телефон][value]'),
            'VALUE_TYPE': 'WORK'
        }],
        'EMAIL': [{
            'VALUE': data.get('fields[email][value]'),
            'VALUE_TYPE': 'WORK'
        }],
        'UF_CRM_PSPRT_NUMBER': data.get('fields[паспорт номер][value]'),
        'UF_CRM_PSPRT_CODE': data.get('fields[код подразделения][value]'),
        'LAST_NAME': last_name,
        'NAME': first_name,
        'SECOND_NAME': second_name,
        'UF_CRM_DSBLT_GROUP': data.get('fields[группа][value]'),
        'UF_CRM_DSBLT_CERT': data.get('fields[справка][value]'),
        'UF_CRM_TAX_CERT': data.get('fields[ИНН][value]'),
        'UF_CRM_PENSION_CERT': data.get('fields[Снилс][value]'),
        'UF_CRM_SKILL_PC': data.get('fields[пк][value]'),
        'UF_CRM_SKILL_WORK': data.get('fields[aaffcfg][value]'),
        'UF_CRM_DISABILITY': data.get('fields[ограничения][value]'),
        'UF_CRM_AGREEMENT': 'Y' if data.get('fields[Согласие на обработку][value]') == 'on' else 'N',
        'UF_CRM_SUBMISSION_ID': data.get('submission_id'),

        
    }
    # fields={
    #     'TITLE': 'Заявка с сайта',
    #     'UF_CRM_PSPRT_SERIAL': data['fields[паспорт серия][value]'],
    #     'UF_CRM_PSPRT_ISSUED': data['fields[Кем выдан][value]'],
    #     'UF_CRM_PSPRT_DATE': data['fields[дата выдачи][value]'],
    #     'UF_CRM_REG_STREET': data['fields[зарегистрирован улица][value]'],
    #     'UF_CRM_REG_CITY': data['fields[город][value]'],
    #     'PHONE': [{
    #         'VALUE': data['fields[телефон][value]'],
    #         'VALUE_TYPE': 'WORK'
    #     }],
    #     'EMAIL': [{
    #         'VALUE': data['fields[email][value]'],
    #         'VALUE_TYPE': 'WORK'
    #     }],
    #     'UF_CRM_PSPRT_NUMBER': data['fields[паспорт номер][value]'],
    #     'UF_CRM_PSPRT_CODE': data['fields[код подразделения][value]'],
    #     'LAST_NAME': last_name,
    #     'NAME': first_name,
    #     'SECOND_NAME': second_name,
    #     'UF_CRM_DSBLT_GROUP': data['fields[группа][value]'],
    #     'UF_CRM_DSBLT_CERT': data['fields[справка][value]'],
    #     'UF_CRM_TAX_CERT': data['fields[ИНН][value]'],
    #     'UF_CRM_PENSION_CERT': data['fields[Снилс][value]'],
    #     'UF_CRM_SKILL_PC': data['fields[пк][value]'],
    #     'UF_CRM_SKILL_WORK': data['fields[aaffcfg][value]'],
    #     'UF_CRM_DISABILITY': data['fields[ограничения][value]'],
    #     'UF_CRM_AGREEMENT': 'Y' if data['fields[Согласие на обработку][value]'] == 'on' else 'N',
    #     'UF_CRM_SUBMISSION_ID': data['submission_id'],
# 
    # }
    
    
    pprint(fields)
    create_lead(fields)

    try:
        send_log(f'Заявка от {first_name}', 'DEBUG')
    except Exception as e:
        send_log(f'Ошибка отправки лога: {e}', 'ERROR')

    return {"fields": 'OK'}






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

    # pprint(log.__dict__)
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