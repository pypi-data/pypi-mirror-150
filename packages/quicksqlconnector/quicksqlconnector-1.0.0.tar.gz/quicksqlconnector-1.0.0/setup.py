from setuptools import setup, find_packages
readme = open ('README.txt')

setup(
    name='quicksqlconnector',
    version='1.0.0',
    license='MIT',
    license_files='LICENCE',
    author="Anas Raza",
    author_email='mailtoanas@duck.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Anas-Dew/QuickSQL',
    keywords='quicksqlconnector, sql, database, mysql',
    install_requires=[
          'mysql-connector-python',
      ],
    description='Use MySQLServer like a layman. Super easy to use MySQL with Python',
    long_description=readme.read()

)