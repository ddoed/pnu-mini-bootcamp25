from dataclasses import dataclass
from fastapi import FastAPI
from enum import Enum

@dataclass
class SignupParams:
    login_id: str
    password: str

@dataclass
class RequestArticle:
    id: int
    title: str
    body: str

@dataclass
class RequestAddComment:
    body: str

@dataclass
class Post:
    id: int
    title: str

@dataclass
class PostResp:
    posts: list[Post]
    err: str | None = None

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

# Path Parameter
# Path Parameter를 사용하는 API는 반드시 해당 인자를 받아야 함
# product_id를 타입 지정 가능
@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {
        "product_id": product_id,
        "name": "Product Name"
    }

# fastapi는 먼저 정의된 Path를 우선으로 라우팅 처리
@app.get("/products/first")
def get_first_product():
    return {
        "product_id": 1
    }

# Enum을 사용한 Path Parameter
class CarType(str, Enum):
    Truck = "truck"
    Sedan = "sedan"
    SUV = "suv"

@app.get("/cars/{car_type}")
def get_car(car_type: CarType):
    return {
        "car_type": car_type
    }

# Query Parameter
# http://localhost:8000/products?q=apple
# Path Parameter가 아닌 인자가 정의되면 자동으로 Query Parameter로 처리
# Query Parameter는 선택적으로 받을 수 있음 -> Optional 형태로 타입을 명시하는 것이 좋음
# FastAPI가 핸들러 함수 인자로 정의된 타입에 맞춰 자동으로 변환
@app.get('/products')
def get_products(q: str | None = None):
    products = {"products": [{"name": "Product 1"}, {"name": "Product 2"}]}
    if q:
        products.update({"q": q})
    return products

# Request Body + Path Parameter
@app.post('/articles/{article_id}/comments')
def add_comments(article_id: int, req: RequestAddComment):
    return {
        "article_id": article_id,
        "comment": req.body
    }

# Request Body
@app.post('/auth/signup')
def auth_signup(params: SignupParams):
    return params
