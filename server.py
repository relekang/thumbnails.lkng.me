import os

from flask import Flask, render_template
from flask.ext.cache import Cache

import thumbnails
import thumbnails.backends

from helpers import thumbnails_path

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.debug = True
save = thumbnails.backends.get_engine().engine_save_image

URL = 'https://unsplash.imgix.net/photo-1422405153578-4bd676b19036' \
      '?q=75&fm=jpg&s=5ecc4c704ea97d85ea550f84a1499228'

os.makedirs(thumbnails_path(None), exist_ok=True)

for size in ['200x200', '200', 'x200']:
    path = 'no-crop-{}.jpg'.format(size)
    save(
        thumbnails.get_thumbnail(URL, size).image,
        thumbnails_path(path)
    )
    print(path)

for crop in ['top', 'right', 'bottom', 'left', 'center']:
    path = 'crop-{}-200x200.jpg'.format(crop)
    save(
        thumbnails.get_thumbnail(URL, '200x200', crop).image,
        thumbnails_path(path)
    )
    print(path)

for crop in ['20 20', '20 50', '60 60', '0 100', '50 50']:
    path = 'crop-{}-200x200.jpg'.format(crop.replace(' ', '_'))
    save(
        thumbnails.get_thumbnail(URL, '200x200', crop).image,
        thumbnails_path(path)
    )
    print(path)


@app.route("/")
@cache.cached(timeout=50)
def index():
    images = []
    files = os.listdir(thumbnails_path(None))
    files.sort()
    for f in files:
        images.append({
            'url': '/thumbnails/{}'.format(f),
            'title': f.replace('.jpg', '')
        })

    return render_template('index.html', thumbnails=images)
