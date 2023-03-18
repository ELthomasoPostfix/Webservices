from flask import Flask
from flask_restful import Api
from typing import Mapping, Any




def create_app(test_config: Mapping[str, Any]=None):
    """The app factory used in the run script to start the
    backend api.

    :param test_config: If not None, then this config will be
    used. Else, the config specified in config.py will be used.
    :return: The app instance
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # NO database will be used.
    # ==> Uncomment if it is actually used
    #
    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # Flask RESTful API
    api = Api(app, prefix="/api")


    return app
