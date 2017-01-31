project ?= 'a4p'
version ?= 'auto'

develop:
	pip --version 2>&1> /dev/null || { \
	  echo "pip not installed. Installing..."; \
	  sudo easy_install pip; \
	}

	virtualenv --version 2>&1> /dev/null || { \
	  echo "virtualenv not installed. Installing..."; \
	  sudo pip install virtualenv; \
	}

	gaenv -h 2>&1> /dev/null || { \
	  echo "gaenv not installed. Installing..."; \
	  sudo pip install gaenv; \
	}

	$(MAKE) install

run-backend:
	dev_appserver.py --port=8088 .

run-frontend:
	cd frontend && ember serve

install:
	virtualenv env
	. env/bin/activate
	./env/bin/pip install \
	  --upgrade \
	  --allow-unverified dateutil \
	  --allow-external dateutil \
	  -r \
	  requirements.txt
	./env/bin/gaenv --lib lib --no-import

install-gae-sdk:
	mkdir -p /tmp/deps
	wget -nv -P /tmp/deps https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.49.zip
	unzip -qo -d ${HOME} /tmp/deps/google_appengine_1.9.49.zip
	mkdir -p vendor
	ln -s ${HOME}/google_appengine/google vendor/google
	
test:
	. env/bin/activate
	./env/bin/nosetests \
	  -v \
	  --rednose \
	  --nocapture \
	  --with-gae \
	  --gae-lib-root=$(HOME)/google_appengine \
	  --with-coverage \
	  --cover-erase \
	  --cover-html \
	  --cover-html-dir=htmlcov \
	  --cover-package=app \
	  app/

build:
	cd frontend && \
	  npm install && \
	  bower install && \
	  ember build

deploy:
	cd frontend && ember build
	gcloud app deploy \
	  -q \
	  --project=$(project) \
	  --version=$(version) \
	  --verbosity=error \
	  --no-promote \
	  app.yaml
	gcloud app deploy \
	  -q \
	  --project=$(project) \
	  --version=$(version) \
	  index.yaml

deploy-promote:
	gcloud app deploy \
	  -q \
	  --project=$(project) \
	  --version=$(version) \
	  --verbosity=error \
	  --promote \
	  app.yaml
