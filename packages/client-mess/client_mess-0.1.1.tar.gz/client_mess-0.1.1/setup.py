from setuptools import setup, find_packages

setup(name="client_mess",
      version="0.1.1",
      description="Client",
      author="Dmitry Bykov",
      author_email="dmitrij-bykov91@bk.ru",
      packages=find_packages(),
      install_requires=["PyQt5", "sqlalchemy", "pycryptodome", "pycryptodomex"],
      )
