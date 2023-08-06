from setuptools import setup, find_packages

setup(name='server_chat_pyqt_test',
      version='0.16',
      description='Server packet',
      packages=find_packages(),  # ,Будем искать пакеты тут(включаем авто поиск пакетов)
      author_email='test@mail.ru',
      author='test',
      install_requeres=['PyQt5', 'sqlalchemy', 'pycruptodome', 'pycryptodomex']
      # зависимости которые нужно до установить
      )