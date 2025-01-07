# command for server startup: uvicorn main:app --reload

from fastapi import FastAPI
import psycopg
from pydantic import BaseModel
from datetime import datetime


# establish connection to db
conn = psycopg.connect("dbname=users user=postgres password=password")
curr = conn.cursor()
app = FastAPI()


class Item(BaseModel):
    first_name: str
    last_name: str
    account_number: int
    email: str


class UpdateItem(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    account_number: int
    email: str


@app.get('/users/')
def get_data():
    sql = curr.execute("SELECT * FROM users").fetchall()
    curr.close()
    conn.close()
    return sql



@app.post('/create/')
def create_data(item: Item):
    s1 = item.first_name
    s2 = datetime.now()
    s3 = item.last_name
    s4 = item.account_number
    s5 = item.email
    curr.execute("INSERT INTO users (first_name, created_at, last_name, account_number, email) VALUES (%s, %s, %s, %s, %s)", (s1, s2, s3, s4, s5))
    conn.commit()
    curr.close()
    conn.close()
    return item


@app.put('/update/')
def update_data(item: UpdateItem):
    s1 = item.first_name
    s2 = datetime.now()
    s3 = item.last_name
    s4 = item.account_number
    s5 = item.email
    s6 = item.user_id
    curr.execute("UPDATE users SET first_name=%s, created_at=%s, last_name=%s, account_number=%s, email=%s WHERE user_id=%s", (s1, s2, s3, s4, s5, s6))
    conn.commit()
    curr.close()
    conn.close()
    return item


@app.get('/delete/{id}')
def delete(id = {id}):
    curr.execute("DELETE FROM users WHERE user_id=%s", (id,))
    conn.commit()
    curr.close()
    conn.close()
    return "id " + id + " was deleted"
