import os

from flask import Flask, render_template
from flask.ext.cache import Cache

import thumbnails

from helpers import thumbnails_path

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.debug = True

URL = 'https://unsplash.imgix.net/photo-1422405153578-4bd676b19036' \
      '?q=75&fm=jpg&s=5ecc4c704ea97d85ea550f84a1499228'

os.makedirs(thumbnails_path(None), exist_ok=True)
images = []

for size in ['200x200', '200', 'x200']:
    path = 'no-crop-{}.jpg'.format(size)
    images.append({
        'title': path,
        'thumb': thumbnails.get_thumbnail(URL, size)
    })
    print(path)

for crop in ['top', 'right', 'bottom', 'left', 'center']:
    path = 'crop-{}-200x200.jpg'.format(crop)
    images.append({
        'title': path,
        'thumb': thumbnails.get_thumbnail(URL, '200x200', crop)
    })
    print(path)

# for crop in ['20 20', '20 50', '60 60', '0 100', '50 50']:
#     path = 'crop-{}-200x200.jpg'.format(crop.replace(' ', '_'))
#     images.append({
#         'title': path,
#         'thumb': thumbnails.get_thumbnail(URL, '200x200', crop)
#     })
#     print(path)


@app.route("/")
@cache.cached(timeout=50)
def index():
    return render_template('index.html', thumbnails=images)
