import os
from flask import current_app

def delete_profile_pic(picture):
    if not picture or picture == "default.png":
        return 
    
    pic_path = os.path.join(current_app.root_path, "static", "profile_pics", picture)

    if os.path.exists(pic_path):
        os.remove(pic_path)
    else:
        current_app.logger.warning(f"Profile picture file not found: {picture}")