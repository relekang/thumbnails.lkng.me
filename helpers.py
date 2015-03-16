import os.path


def thumbnails_path(name):
    if name is None:
        return os.path.join(os.path.dirname(__file__), 'thumbnails')
    return os.path.join(os.path.dirname(__file__), 'thumbnails', name)
