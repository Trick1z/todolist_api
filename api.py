from typing import Union
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, File, Response, status, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
import os
import base64
from dateutil import parser
import pytz
import io
import csv
from openpyxl import load_workbook
import hashlib
from bs4 import BeautifulSoup
load_dotenv()


# get DB
def get_DB():
    # deploy docker
    # connector = mysql.connector.connect(
    #     host='host.docker.internal',
    #     user='root',
    #     database='mydb'
    # )

    # localhost
    connector = mysql.connector.connect(
        host='localhost',
        user='root',
        database='todolist_db'
    )

    return connector


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# class gettime():
#     def time():
#         time = 
#         return 


class query():
    def get(order: String):
        try:
            conn = get_DB()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(order)
            data = cursor.fetchall()

            cursor.close()
            conn.close()

            if not data:
                return None
            else:
                return {
                    'msg': 200,
                    'data': data
                }

        except Exception as err:
            return {'msg': err, }

    def post(order: String):
        try:
            conn = get_DB()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(order)
            conn.commit()
            cursor.close()
            conn.close()

            return {'msg': "your task has been added !",
                    'status': 200}

        except Exception as err:
            return {'msg': err, }

    def put(order: String):
        try:
            cnx = get_DB()
            cursor = cnx.cursor()
            cursor.execute(order)
            cnx.commit()
            cursor.close()
            cnx.close()

            return {
                'msg': 'Success',
                'status': 200
            }
        except Exception as err:
            return {'msg': err, }


@app.get('/get.task')
def get_test():
    try:
        res = query.get(
            f"SELECT * FROM todolist_table WHERE del_frag = 'N' and success_frag = 'N'")

        return res
    except Exception as err:
        return {'msg': err}

@app.get('/get.task/success')
def get_test():
    try:
        res = query.get(
            f"SELECT * FROM todolist_table WHERE del_frag = 'N' and success_frag = 'Y'")

        return res
    except Exception as err:
        return {'msg': err}


class addTask(BaseModel):
    name: str
    desc: str


@app.post('/post.task')
def post_task(data: addTask):
    try:
        res = query.post(
            f"INSERT INTO todolist_table (list_name ,list_desc) VALUES ('{data.name}','{data.desc}')")

        return res

    except Exception as err:
        return {'msg': err}

# soft del


@app.put('/enp.{table}/{state}/{id}')
def soft_delete(table: str, id: int,state:str):
    try:
        res = query.put(
            f"UPDATE {table} SET {state} = 'Y' WHERE list_id = {id};")
        return res
    except Exception as err:
        return {'msg': err}
    
@app.put('/put.{table}/{id}')
def update_task_info(table : str ,id : int,data : addTask):
    try:
        res = query.put(f"UPDATE {table} SET list_name = '{data.name}', list_desc = '{data.desc}' WHERE list_id = {id}")
        return res
    except Exception as err:
        return {'msg': err}
