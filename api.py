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


def query_get(order: String):

    cnx = get_DB()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(order)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    if not rows:
        return None
        # return {"message": 404, "data": None}
    else:
        return rows


def query_post(order: String):
    cnx = get_DB()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(order)
    cnx.commit()
    cursor.close()
    cnx.close()
    
    return {"msg" : 200 , "status" : "Task Added!"}


def query_put(order: String):
    cnx = get_DB()
    cursor = cnx.cursor()
    cursor.execute(order)
    cnx.commit()
    cursor.close()
    cnx.close()

    return {"message": 200, "status": "state has been change"}



# model


class addData (BaseModel):
    list_name: str
    list_desc:str
class editData (BaseModel):
    list_id: int
    list_name: str
    list_desc:str


# models

@app.get('/get.todolist')
def get_todo_list():
    try:
        res = query_get(f"SELECT * FROM todolist_table WHERE del_frag ='N' and success_frag ='N'")
        return res

    except Exception as err:
        return err
    
@app.get('/get.todolist_success')
def get_todo_list_s():
    try:
        res = query_get(f"SELECT * FROM todolist_table WHERE del_frag ='N' and success_frag ='Y'")
        return res

    except Exception as err:
        return err


    
    
@app.put('/put.edit_todolist')
def put_editlist(data : editData):
    
    try:
        res = query_put(f"UPDATE todolist_table SET list_name = '{data.list_name}' , list_desc = '{data.list_desc}' WHERE list_id = {data.list_id};")
        return res
    except Exception as err :
        return err
    

@app.put('/set.{path}_frag/{id}')
# del_frag & success_frag
def set_status(path:str,id:int):
    try:
        res = query_put(f"UPDATE todolist_table SET {path}_frag = 'Y' WHERE list_id = {id}")
        return res
    except Exception as err:
        return err


@app.post('/post.todolist')
def add_task(data: addData):
    try:
        # print(f"data {data}")
        res = query_post(f"INSERT INTO todolist_table (list_name , list_desc) VALUES ('{data.list_name}','{data.list_desc}');")
        
        return res
    except Exception as err:
        return err
    




