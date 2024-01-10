import uvicorn
import psycopg2
from datetime import datetime

from fastapi import FastAPI, status

# иницилизация API
app = FastAPI()

# подключение к БД
conn = psycopg2.connect(
    database="db_name", 
    user="user", 
    password="password", 
    host="host", 
    port="port"
)

# эндпоинт проверки юзера в БД
# Входные данные: id юзера
# Выходные данные: count юзеров в БД
@app.get("/check_user/{user_id}")
async def check_user(user_id: int):
    with conn.cursor() as cur:
        cur.execute("select count(*) from tg_bot.users where user_id = (%s)", (user_id,))
        check = cur.fetchone()[0]
        conn.commit()

    return check
    

# эндпоинт записи юзера в БД
# Входные данные: id юзера, тг ник, полное имя, дата первого входа в бота
@app.post("/user_registration/{user_id}/{telegram_nickname}/{user_full_name}/{registration_date}")
async def user_registration(user_id: int, telegram_nickname: str, user_full_name: str, registration_date: str):

    with conn.cursor() as cur:
        cur.execute("""
            insert into tg_bot.users(user_id, telegram_nickname, user_full_name, registration_date) values(%s, %s, %s, %s)
        """,
        (user_id, telegram_nickname, user_full_name, registration_date)
        )
        conn.commit()

if __name__ == "__main__":

    # запуск локального сервера 127.0.0.1 - дефолтное значение хоста, 8080 - дефолтное значение портаы
    uvicorn.run(app, host="127.0.0.1", port=8080)