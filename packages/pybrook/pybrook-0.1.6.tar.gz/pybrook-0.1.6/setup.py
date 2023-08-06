# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybrook', 'pybrook.consumers', 'pybrook.examples']

package_data = \
{'': ['*'], 'pybrook': ['frontend/*', 'frontend/build/*']}

install_requires = \
['fastapi>=0.95.2,<0.96.0',
 'gunicorn>=20.1.0,<21.0.0',
 'locust>=2.6.1,<3.0.0',
 'loguru>=0.7.0,<0.8.0',
 'orjson>=3.8.7,<4.0.0',
 'pydantic>=1.10.8,<2.0.0',
 'redis[asyncio]>=4.5.5,<5.0.0',
 'uvicorn[standard]>=0.22.0,<0.23.0',
 'uvloop>=0.17.0,<0.18.0',
 'watchdog>=3.0.0,<4.0.0']

entry_points = \
{'console_scripts': ['pybrook = pybrook.__main__:main']}

setup_kwargs = {
    'name': 'pybrook',
    'version': '0.1.6',
    'description': 'PyBrook - a real-time cloud computing framework for the Internet of Things.',
    'long_description': '[![PyPI](https://img.shields.io/pypi/v/pybrook?style=for-the-badge&color=purple)](https://pypi.org/project/pybrook/)\n[![docs](https://img.shields.io/badge/docs-mkdocs+mkdocstrings-lightblue?style=for-the-badge)](https://pybrook.github.io/pybrook/)\n![Python](https://img.shields.io/badge/python-3.7%2B-blue?style=for-the-badge)\n![Coverage](https://img.shields.io/badge/coverage-81%25-green?style=for-the-badge)\n\n# Introduction\n\nPyBrook - a real-time cloud computing framework for the Internet of Things.\nPyBrook enables users to define complex data processing models declaratively using the Python programming language.\nThe framework also provides a generic web interface that presents the collected data in real-time.\n\nPyBrook aims to make the development of real-time data processing services as easy as possible by utilising powerful \nmechanisms of the Python programming language and modern concepts like hot-reloading or deploying software in Linux Containers.\n\nA simple `docker-compose up` is enough to start playing with the framework.\n\n## Run demo with Docker\n\nIt is recommended to use `docker-compose` for learning (you can use the `docker-compose.yml` from the [project repository](https://github.com/pybrook/pybrook/blob/master/docker-compose.yml):\n\n```bash\ndocker-compose up\n```\n\nThis command will start all the services, including Redis with Redis Gears enabled.\n\nThe following services will be available:\n\n- OpenAPI docs (ReDoc): <http://localhost:8000/redoc> \n- OpenAPI docs (Swagger UI): <http://localhost:8000/docs> \n- PyBrook frontend: <http://localhost:8000/panel> \n- Locust panel for load testing: <http://localhost:8089>\n\nYou should probably visit the Locust panel first and start sending some reports.\n\n### Using your own model\n\nThe configured model is `pybrook.examples.demo`, but replacing it with your own is very easy.  \nFirst, you have to save your custom model somewhere. \nFor now, you can just copy the source of `pybrook.examples.demo` (attached below) and save it as `mymodel.py` in your working directory.\n\n??? example "Source of `pybrook.examples.demo`"\n\n    ```python linenums="1"\n    from datetime import datetime\n    from math import atan2, degrees\n    from typing import Optional, Sequence\n    \n    from pybrook.models import (\n        InReport,\n        OutReport,\n        PyBrook,\n        ReportField,\n        dependency,\n        historical_dependency,\n    )\n    \n    brook = PyBrook(\'redis://localhost\')\n    app = brook.app\n    \n    \n    @brook.input(\'ztm-report\', id_field=\'vehicle_number\')\n    class ZTMReport(InReport):\n        vehicle_number: int\n        time: datetime\n        lat: float\n        lon: float\n        brigade: str\n        line: str\n    \n    \n    @brook.output(\'location-report\')\n    class LocationReport(OutReport):\n        vehicle_number = ReportField(ZTMReport.vehicle_number)\n        lat = ReportField(ZTMReport.lat)\n        lon = ReportField(ZTMReport.lon)\n        line = ReportField(ZTMReport.line)\n        time = ReportField(ZTMReport.time)\n        brigade = ReportField(ZTMReport.brigade)\n    \n    \n    @brook.artificial_field()\n    def direction(lat_history: Sequence[float] = historical_dependency(\n        ZTMReport.lat, history_length=1),\n                        lon_history: Sequence[float] = historical_dependency(\n                            ZTMReport.lon, history_length=1),\n                        lat: float = dependency(ZTMReport.lat),\n                        lon: float = dependency(ZTMReport.lon)) -> Optional[float]:\n        prev_lat, = lat_history\n        prev_lon, = lon_history\n        if prev_lat and prev_lon:\n            return degrees(atan2(lon - prev_lon, lat - prev_lat))\n        else:\n            return None\n    \n    \n    @brook.output(\'direction-report\')\n    class DirectionReport(OutReport):\n        direction = ReportField(direction)\n    \n    \n    @brook.artificial_field()\n    async def counter(prev_values: Sequence[int] = historical_dependency(\n        \'counter\', history_length=1),\n                      time: datetime = dependency(ZTMReport.time)) -> int:\n        prev_value, = prev_values\n        if prev_value is None:\n            prev_value = -1\n        prev_value += 1\n        return prev_value\n    \n    \n    @brook.output(\'counter-report\')\n    class CounterReport(OutReport):\n        counter = ReportField(counter)\n    \n    \n    brook.set_meta(latitude_field=LocationReport.lat,\n                   longitude_field=LocationReport.lon,\n                   time_field=LocationReport.time,\n                   group_field=LocationReport.line,\n                   direction_field=DirectionReport.direction)\n    \n    if __name__ == \'__main__\':\n        brook.run()\n    ```\n\nAfter creating `mymodel.py`, you should add it to the `api` and `worker` containers, using a Docker volume.\nTo make PyBrook use `mymodel` instead of `pybrook.examples.demo`, you should also alter the arguments passed to `gunicorn` and `pybrook`. \nYou can simply add it to the default `docker-compose.yml`:\n\n```yaml hl_lines="20 21 10 11 12 13 14 24" linenums="1"\nservices:\n  api:\n    image: pybrook:latest\n    build:\n      context: .\n    environment:\n      REDIS_URL: redis://redis\n    ports:\n      - 8000:8000\n    volumes:\n      - ./mymodel.py:/src/mymodel.py\n    command: gunicorn mymodel:app \n          -w 4 -k uvicorn.workers.UvicornWorker \n          -b 0.0.0.0:8000\n  worker:\n    image: pybrook:latest\n    depends_on:\n      - api\n    environment:\n      REDIS_URL: redis://redis\n      DEFAULT_WORKERS: 8\n    volumes:\n      - ./mymodel.py:/src/mymodel.py\n    command: pybrook mymodel:brook\n  locust:\n    image: pybrook:latest\n    depends_on:\n      - api\n    ports:\n      - 8089:8089\n    command: locust -H http://api:8000\n  redis:\n    image: redislabs/redisgears:1.0.9\n```\n\nThen run `docker-compose up --build` again, to start PyBrook - this time using your own model.\n\n## Setup & Development\n\nYou can install the PyBrook from PyPi using `pip`:\n\n```bash\npip install pybrook\n```\n\n## Running all services manually, without Docker\n\nTo run the `pybrook.examples.demo` model, you have to start all the required services manually:\n\n```bash\n# Redis + Redis Gears\ndocker run --net=host -d redislabs/redisgears:1.0.9\n# HTTP API based on pybrook.examples.demo - uvicorn\nuvicorn pybrook.examples.demo:app --reload  \n# PyBrook workers based on pybrook.examples.demo \npybrook pybrook.examples.demo:brook -rg \n# Locust - load testing\nlocust -H http://localhost:8000\n```\n\n## Contributing\n\nPyBrook uses [poetry](https://python-poetry.org) for dependency management.\nTo install all its development dependencies, simply run this command:\n\n```bash\npoetry install\n```\n\n### Tests\n\n```bash\nmake test\n```\n\n### Code quality\n\nThe source code of PyBrook is formatted using yapf and isort.  \nTo run them with the correct settings, use the following command:\n\n```bash\nmake format\n```\n\nPyBrook uses `mypy` for type checking and `flake8` for linting.\nUse the following command to run them with the appropriate settings:\n\n```bash\nmake lint\n```',
    'author': 'Michał Rokita',
    'author_email': 'mrokita@mrokita.pl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pybrook/pybrook',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
