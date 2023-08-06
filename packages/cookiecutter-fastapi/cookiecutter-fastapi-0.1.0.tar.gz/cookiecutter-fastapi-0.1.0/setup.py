# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests']

package_data = \
{'': ['*']}

install_requires = \
['cookiecutter>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'cookiecutter-fastapi',
    'version': '0.1.0',
    'description': 'Cookiecutter for fastapi projects',
    'long_description': "# Fastapi Cookiecutter\n\nA [Cookiecutter]() for fastapi projects, inspired by [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django).\n\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Tobi-De/cookiecutter-fastapi/blob/master/LICENSE)\n[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\n## Features\n\n- [x] Use [fastapi-users](https://github.com/fastapi-users/fastapi-users) for users authentication and management\n- [x] [Pydantic](https://pydantic-docs.helpmanual.io/) for settings management\n- [x] Include a cli tool built with [typer](https://github.com/tiangolo/typer) to simplify project management\n- [x] [Pre-commit](https://pre-commit.com/) integration included by default\n- [x] [Tortoise-orm](https://tortoise.github.io/) and [aerich](https://github.com/tortoise/aerich) database setup by default but switchable\n- [x] [Fastapi-pagination](https://github.com/uriyyo/fastapi-pagination) included by default\n- [x] Run tests with unittest or [pytest](https://docs.pytest.org/en/7.1.x/)\n- [x] Sending emails using [aiosmtplib](https://aiosmtplib.readthedocs.io/en/stable/client.html)\n- [x] Optional integration with [sentry](https://docs.sentry.io/platforms/python/) for error logging\n- [ ] [Docker](https://www.docker.com/) and [docker-compose](https://github.com/docker/compose) for and production using [Traefik](https://github.com/traefik/traefik)\n- [ ] Optional setup of HTML templates rendering using [jinja2](https://jinja.palletsprojects.com/en/3.1.x/)\n- [ ] Optional static files serving using [whitenoise](http://whitenoise.evans.io/en/stable/)\n- [ ] [Procfile](https://devcenter.heroku.com/articles/procfile) for deploying to heroku\n- [ ] Optional integration with [fastapi-storages](https://github.com/Tobi-De/fastapi-storages) for media files storage\n- [ ] Implement the Health [Check API pattern](https://microservices.io/patterns/observability/health-check-api.html) on your FastAPI application\n- [ ] Renders fastapi projects with 100% starting test coverage\n\n### Task queues manager options\n\n - [x] [Arq](https://github.com/samuelcolvin/arq)\n - [ ] [Procrastinate](https://github.com/procrastinate-org/procrastinate)\n - [ ] [Celery](https://github.com/celery/celery)\n\n### Database options\n\n- [x] [Tortoise ORM](https://tortoise.github.io/)\n- [ ] [RedisOM](https://github.com/redis/redis-om-python)\n- [ ] [Beanie](https://github.com/roman-right/beanie)\n- [ ] [SQLModel](https://github.com/tiangolo/sqlmodel)\n\n\n## Usage\n\nInstall the cookiecutter package:\n\n```shell\npip install cookiecutter\n```\n\nNow run it against this repo:\n\n```shell\ncookiecutter https://github.com/Tobi-De/cookiecutter-fastapi\n```\n\nYou'll be prompted for some values. Provide them, then a fastapi project will be created for you.\n",
    'author': 'Tobi-De',
    'author_email': 'tobidegnon@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tobi-De/cookiecutter-fastapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
