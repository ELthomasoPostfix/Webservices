from typing import Union
from fastapi import FastAPI


def create_app(test_config=None) -> FastAPI:
    # create and configure the app
    app = FastAPI()

    print(type(app))

    return app


app = create_app()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}