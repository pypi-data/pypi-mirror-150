from setuptools import setup, find_packages


setup(
    name="learn_mess_app_server",
    version="0.0.1",
    description="learn_mess_app_server",
    author="Chizhikov Roman",
    author_email="nod3223@ya.ru",
    packages=find_packages(),
    install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
)
