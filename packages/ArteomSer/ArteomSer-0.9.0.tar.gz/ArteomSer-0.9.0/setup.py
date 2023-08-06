from setuptools import setup, find_packages


setup(
    name="ArteomSer",
    version="0.9.0",
    description="JSON and XLM serializer",
    author="Arteom Maksimchikau",
    author_email="maksimchikov03@mail.ru",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
    'console_scripts': [ 
        'serializer = Am_serialize.serializer:main' 
    ] 
},
)