import secrets
import os
from flask import current_app

def save_profile_pic(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    filename = random_hex + f_ext
    filepath = os.path.join(current_app.root_path, 'static/profile_pics', filename)
    file.save(filepath)
    return filename

def save_post_pic(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    filename = random_hex + f_ext
    filepath = os.path.join(current_app.root_path, 'static/post_pics', filename)
    file.save(filepath)
    return filename