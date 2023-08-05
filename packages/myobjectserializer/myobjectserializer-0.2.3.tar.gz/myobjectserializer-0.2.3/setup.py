from setuptools import setup

setup(
    name='myobjectserializer',
    version='0.2.3',
    packages=[
        "lab3.serializer.src"
    ],
    entry_points={
        'console_scripts': [
            "custom-serialize = lab3.serializer.custom:main"
        ]
    },
    license='MIT',
    author='WilderWine',
    author_email='vernikon72@gmail.com',
    description='Python JSON and XML serializer',
)
