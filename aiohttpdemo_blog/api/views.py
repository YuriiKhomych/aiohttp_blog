from aiohttp import web

from aiohttpdemo_blog.api.schemas import posts_schema
from aiohttpdemo_blog.blog import db


async def get_posts(request):
    """
        ---
        description: This end-point allow to test that service is up.
        tags:
        - Posts
        produces:
        - text/json
        responses:
            "200":
                description: successful operation. Return "pong" text
            "405":
                description: invalid HTTP Method
        """

    async with request.app['db_pool'].acquire() as conn:
        posts = await db.get_posts_with_joined_users(conn)
        result = posts_schema.dump(posts)

    return web.json_response({'posts': result})
