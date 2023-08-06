from setuptools import setup, find_packages


setup(
    name="Brigadir_Ser",
    version="1.0.0",
    description="JSON and XLM serializer",
    author="Maksim Piacherski",
    author_email="murzikelite@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [ 
            'serializer = MySerializer.serializer:main' 
        ],
    },
)