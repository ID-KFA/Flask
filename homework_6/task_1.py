"""
Необходимо создать базу данных для интернет-магазина. База данных должна
состоять из трёх таблиц: товары, заказы и пользователи.
— Таблица «Товары» должна содержать информацию о доступных товарах, их
описаниях и ценах.
— Таблица «Заказы» должна содержать информацию о заказах, сделанных
пользователями.
— Таблица «Пользователи» должна содержать информацию о зарегистрированных
пользователях магазина.
• Таблица пользователей должна содержать следующие поля:
id (PRIMARY KEY),
имя, фамилия, адрес электронной почты и пароль.
• Таблица заказов должна содержать следующие поля:
id (PRIMARY KEY), id
пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
заказа.
• Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название,
описание и цена.

Создайте модели pydantic для получения новых данных и возврата существующих в
БД для каждой из трёх таблиц (итого шесть моделей).
Реализуйте CRUD операции для каждой из таблиц через создание маршрутов,
REST API (итого 15 маршрутов).
* Чтение всех
* Чтение одного
* Запись
* Изменение
* Удаление

"""

import databases
import sqlalchemy

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import pandas as pd
from fastapi.templating import Jinja2Templates
from typing import List

DATABASE_URL = "sqlite:///onlineshop.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(40)),
    sqlalchemy.Column("surname", sqlalchemy.String(40)),
    sqlalchemy.Column("email", sqlalchemy.String(120)),
    sqlalchemy.Column("password", sqlalchemy.String(5)),
)

goods = sqlalchemy.Table(
    "goods",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(40)),
    sqlalchemy.Column("description", sqlalchemy.String(200)),
    sqlalchemy.Column("price", sqlalchemy.Float),

)

orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey(users.c.id)),
    sqlalchemy.Column("goods_id", sqlalchemy.ForeignKey(goods.c.id)),
    sqlalchemy.Column("date", sqlalchemy.String(40)),
    sqlalchemy.Column("status", sqlalchemy.String(40)),

)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class User(BaseModel):
    id: int
    name: str = Field(max_length=40)
    surname: str = Field(max_length=40)
    email: str = Field(max_length=120)
    password: str = Field(max_length=5)


class UserIn(BaseModel):
    name: str = Field(max_length=40)
    surname: str = Field(max_length=40)
    email: str = Field(max_length=120)
    password: str = Field(max_length=5)


class Goods(BaseModel):
    id: int
    name: str = Field(max_length=40)
    description: str = Field(max_length=200)
    price: float


class GoodsIn(BaseModel):
    name: str = Field(max_length=40)
    description: str = Field(max_length=200)
    price: float


class Order(BaseModel):
    id: int
    user_id: int
    goods_id: int
    date: str = Field(max_length=40)
    status: str = Field(max_length=40)


class OrderIn(BaseModel):
    user_id: int
    goods_id: int
    date: str = Field(max_length=40)
    status: str = Field(max_length=40)


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(**user.model_dump())
    record_id = await database.execute(query)
    return {**user.model_dump(), "id": record_id}


@app.get("/users/", response_model=List[User])
async def read_user(request: Request):
    query = users.select()
    user_table = pd.DataFrame(
        [user for user in await database.fetch_all(query)]).to_html()
    return templates.TemplateResponse("users.html",
                                      {"request": request,
                                       "table": user_table})


@app.post("/goods/", response_model=Goods)
async def create_goods(good: GoodsIn):
    query = goods.insert().values(**good.model_dump())
    record_id = await database.execute(query)
    return {**good.model_dump(), "id": record_id}


@app.get("/goods/", response_model=List[Goods])
async def read_goods(request: Request):
    query = goods.select()
    goods_table = pd.DataFrame(
        [goods for goods in await database.fetch_all(query)]).to_html()
    return templates.TemplateResponse("goods.html",
                                      {"request": request,
                                       "table": goods_table})


@app.post("/orders/", response_model=Order)
async def create_orders(order: OrderIn):
    query = orders.insert().values(**order.model_dump())
    record_id = await database.execute(query)
    return {**order.model_dump(), "id": record_id}


@app.get("/orders/", response_model=List[Order])
async def read_orders(request: Request):
    query = orders.select()
    orders_table = pd.DataFrame(
        [orders for orders in await database.fetch_all(query)]).to_html()
    return templates.TemplateResponse("orders.html",
                                      {"request": request,
                                       "table": orders_table})


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, request: Request):
    query = users.select().where(users.c.id == user_id)
    user_table = pd.DataFrame(
        [await database.fetch_one(query)]).to_html()
    return templates.TemplateResponse("users.html",
                                      {"request": request,
                                       "table": user_table})


@app.get("/goods/{goods_id}", response_model=Goods)
async def read_goods(goods_id: int, request: Request):
    query = goods.select().where(goods.c.id == goods_id)
    goods_table = pd.DataFrame(
        [await database.fetch_one(query)]).to_html()
    return templates.TemplateResponse("goods.html",
                                      {"request": request,
                                       "table": goods_table})


@app.get("/orders/{order_id}", response_model=Order)
async def read_orders(order_id: int, request: Request):
    query = orders.select().where(orders.c.id == order_id)
    orders_table = pd.DataFrame(
        [await database.fetch_one(query)]).to_html()
    return templates.TemplateResponse("orders.html",
                                      {"request": request,
                                       "table": orders_table})


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(
        **new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@app.put("/goods/{goods_id}", response_model=Goods)
async def update_goods(goods_id: int, new_goods: GoodsIn):
    query = goods.update().where(goods.c.id == goods_id).values(
        **new_goods.model_dump())
    await database.execute(query)
    return {**new_goods.model_dump(), "id": goods_id}


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(
        **new_order.model_dump())
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


@app.delete("/goods/{goods_id}")
async def delete_goods(goods_id: int):
    query = goods.delete().where(goods.c.id == goods_id)
    await database.execute(query)
    return {'message': 'Goods deleted'}


@app.delete("/orders/{order_id}")
async def delete_orders(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}
