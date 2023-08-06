from setuptools import setup, find_packages

setup(name="server_mess",
      version="0.1.1",
      description="Server",
      author="Dmitry Bykov",
      author_email="dmitrij-bykov91@bk.ru",
      packages=find_packages(),
      install_requires=["PyQt5", "sqlalchemy", "pycryptodome", "pycryptodomex"],
      )
