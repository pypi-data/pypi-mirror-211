# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloud', 'cloud.application']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0',
 'pydantic>=1.10.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['gdcloudlib = cloud:application']}

setup_kwargs = {
    'name': 'gdcloudlib',
    'version': '0.0.1',
    'description': '',
    'long_description': '# Библиотека для работы с облачными инструментами\n\n- Создание API-gw\n- Работа с файлами на S3\n- Чтение и запись сообщений в очередь\n- Работа с DinamoDB\n\n## ФИЧА0: Работа в качестве библиотеки Python\n## ФИЧА1: Загрузка изображений в S3\n## ФИЧА2: Создание API-GW\n## ФИЧА3: Генерация приложений API-GW из шаблона\n## ФИЧА3: Создание Function',
    'author': 'Nikolay Baryshnikov',
    'author_email': 'root@k0d.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/p141592',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
