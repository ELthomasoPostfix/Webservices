from typing import Union
from fastapi import FastAPI


def create_app(test_config=None) -> FastAPI:
    # create and configure the app
    app = FastAPI()

    print(type(app))

    return app


app = create_app()
