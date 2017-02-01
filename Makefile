prod_version ?= prod
project ?= a4x-prod
staging_version ?= staging
GITHUB_USERNAME ?= $(CIRCLE_PROJECT_USERNAME)
GITHUB_REPO ?= $(CIRCLE_PROJECT_REPONAME)
GITHUB_COMMIT ?= $(CIRCLE_SHA1)
GITHUB_ACCESS_TOKEN ?=

develop:
	pip install grow
	grow install

test:
	grow build

stage:
	PATH=$(PATH):$(HOME)/bin grow build
	gcloud app deploy \
	  -q \
	  --project=$(project) \
	  --version=$(staging_version) \
	  --verbosity=error \
	  --no-promote \
	  app.yaml

deploy:
	PATH=$(PATH):$(HOME)/bin grow build
	gcloud app deploy \
	  -q \
	  --project=$(project) \
	  --version=$(prod_version) \
	  --verbosity=error \
	  --promote \
	  app.yaml

run-gae:
	dev_appserver.py --allow_skipped_files=true .

update-github-commit-status:
	curl "https://api.github.com/repos/$(GITHUB_USERNAME)/$(GITHUB_REPO)/statuses/$(GITHUB_COMMIT)" \
	    -H "Content-Type: application/json" \
	    -H "Authorization: token $(GITHUB_ACCESS_TOKEN)" \
	    -X POST \
	    -d "{\"state\": \"success\", \"context\": \"grow\", \"description\": \"View staging ⟶\", \"target_url\": \"https://$(staging_version)-dot-$(project).appspot.com\"}"
