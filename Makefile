production:
	rm -rf thumbnails
	pip install -Ur requirements.txt
	pip install -e git+git@github.com:relekang/python-thumbnails.git#egg=thumbnails
	sudo supervisorctl restart thumbnails.lkng.me
