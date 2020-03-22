import logging

import aiohttp_jinja2
import jinja2
import aioredis

from aiohttp import web
from aiohttp_security import SessionIdentityPolicy
from aiohttp_security import authorized_userid
from aiohttp_security import setup as setup_security
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
from aiohttp_swagger import setup_swagger

from aiohttpdemo_blog.api.routes import api_setup_routes
from aiohttpdemo_blog.blog.db_auth import DBAuthorizationPolicy
from aiohttpdemo_blog.blog.db import init_db
from aiohttpdemo_blog.blog.routes import blog_setup_routes
from aiohttpdemo_blog.blog.settings import load_config, PACKAGE_NAME


log = logging.getLogger(__name__)


async def setup_redis(app):

    pool = await aioredis.create_redis_pool((
        app['config']['redis']['REDIS_HOST'],
        app['config']['redis']['REDIS_PORT']
    ))

    async def close_redis(app):
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_redis)
    app['redis_pool'] = pool
    return pool


async def current_user_ctx_processor(request):
    username = await authorized_userid(request)
    is_anonymous = not bool(username)
    return {'current_user': {'is_anonymous': is_anonymous}}


def setup_routes(app):
    blog_setup_routes(app=app)
    api_setup_routes(app=app)


async def init_app(config):

    app = web.Application()

    app['config'] = config

    setup_routes(app)

    db_pool = await init_db(app)

    redis_pool = await setup_redis(app)
    setup_session(app, RedisStorage(redis_pool))

    # needs to be after session setup because of `current_user_ctx_processor`
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader(PACKAGE_NAME),
        context_processors=[current_user_ctx_processor],
    )

    setup_security(
        app,
        SessionIdentityPolicy(),
        DBAuthorizationPolicy(db_pool)
    )

    setup_swagger(
        app,
        description="Blog API",
        title="My Custom Title",
        api_version="1.0.0",
        contact="my.custom.contact@example.com",
    )

    log.debug(app['config'])

    return app


def main(configpath):
    config = load_config(configpath)
    logging.basicConfig(level=logging.DEBUG)
    app = init_app(config)
    web.run_app(app)
