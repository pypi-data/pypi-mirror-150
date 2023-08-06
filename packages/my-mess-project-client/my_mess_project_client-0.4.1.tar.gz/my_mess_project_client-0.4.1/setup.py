from setuptools import setup, find_packages

setup(name="my_mess_project_client",
      version="0.4.1",
      description="Mess Client",
      author="Yaroslav Gusev",
      author_email="kireb83445@doerma.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
