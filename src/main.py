import os
import asyncio
import functools
from typing import Optional
from starlette.middleware.cors import CORSMiddleware

import click
from fastapi import FastAPI
from uvicorn import Server
from uvicorn import Config as UvicornConfig

from apps import router
from apps.context import db_ctx
from apps.context import config_ctx
from apps.middleware.connect import ConnectMiddleware
from config import Config
from config import ConsulConfig
from models.session import DBConnect

from utils.logger import load_logging_cfg

ENV_CONSUL_KEY = 'FLY_CONSUL_URL'


class App(Server):
    pass


def make_app(config: Optional[Config] = None) -> FastAPI:
    app = FastAPI()

    app.add_middleware(ConnectMiddleware)
    origins = config.origins if config and config.origins else []
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    @app.get("/health",
             name='health',
             tags=['Ping'])
    def health():
        return {'status': 'ok'}

    return app


def make_sync(func):
    """"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))

    return wrapper


@click.command()
@make_sync
@click.option('--config', '-c', type=str, help='config file path')
async def main(config: Optional[str] = None, ):
    log_cfg = load_logging_cfg()

    # load config
    if config:
        cfg = Config.from_file(config)
    elif consul_url := os.getenv(ENV_CONSUL_KEY):
        consul_cfg = ConsulConfig.from_url(consul_url)
        cfg = Config.from_consul(consul_cfg)
    else:
        raise ValueError('config not found')
    config_ctx.set(cfg)

    # initialize db, if you need db connection, uncomment this code TODO
    # _db = DBConnect(db_url=cfg.db_url, echo=False, pool_size=cfg.db_pool_size, pool_recycle=600,
    #                 pool_pre_ping=True,
    #                 pool_use_lifo=True, future=True)
    # db_ctx.set(_db)

    # create web api
    app = make_app(config=cfg)
    serve = App(config=UvicornConfig(app=app, host="0.0.0.0", port=cfg.port, log_config=log_cfg))

    api = asyncio.create_task(serve.serve())

    await asyncio.gather(api)


if __name__ == '__main__':
    main()
