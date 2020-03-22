from aiohttpdemo_blog.api.views import get_posts


def api_setup_routes(app):
    app.router.add_get('/api/posts', get_posts, name='posts')