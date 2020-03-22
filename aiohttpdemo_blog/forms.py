from aiohttpdemo_blog import db
from aiohttpdemo_blog.security import (
    check_password_hash,
    generate_password_hash,
)


async def validate_login_form(conn, form):

    username = form['username']
    password = form['password']

    if not username:
        return 'username is required'
    if not password:
        return 'password is required'

    user = await db.get_user_by_name(conn, username)

    if not user:
        return 'Invalid username'
    if not check_password_hash(password, user['password_hash']):
        return 'Invalid password'
    else:
        return None

    return 'error'


async def validate_sign_up_form(conn, form):
    fields = [
        'username',
        'email',
        'password',
        'password_2',
    ]
    for field in fields:
        if not form[field]:
            return f"{field} is required", {}

    if '@' not in form['email']:
        return 'Email is not valid', {}
    if form['password'] != form['password_2']:
        return 'Passwords are not equal', {}
    # todo Add check for user existence

    data = {field: form[field] for field in ('username', 'email')}
    data['password_hash'] = generate_password_hash(form['password'])

    return '', data
