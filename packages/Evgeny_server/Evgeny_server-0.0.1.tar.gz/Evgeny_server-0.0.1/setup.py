from setuptools import find_packages, setup

setup(name="Evgeny_server",
      version="0.0.1",
      description="mess_server",
      author="Evgeny Monakhov",
      author_email="iv.iv@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
