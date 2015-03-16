import os

from flask import Flask, render_template
from flask.ext.cache import Cache
from thumbnails import engines, get_thumbnail
from helpers import thumbnails_path

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.debug = True
save = engines.get_current_engine().engine_save_image

URL = 'https://unsplash.imgix.net/photo-1422405153578-4bd676b19036' \
      '?q=75&fm=jpg&s=5ecc4c704ea97d85ea550f84a1499228'

os.makedirs(thumbnails_path(None), exist_ok=True)

for size in ['200x200', '200', 'x200']:
    save(
        get_thumbnail(URL, size).image,
        thumbnails_path('no-crop-{}.jpg'.format(size))
    )
for crop in ['top', 'right', 'bottom', 'left', 'center']:
    save(
        get_thumbnail(URL, '200x200', crop).image,
        thumbnails_path('crop-{}-200x200.jpg'.format(crop))
    )


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
