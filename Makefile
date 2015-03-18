production:
	rm -rf thumbnails
	venv/bin/pip install -Ur requirements.txt
	venv/bin/pip install -e git+git@github.com:relekang/python-thumbnails.git#egg=thumbnails
	sudo supervisorctl restart thumbnails.lkng.me
