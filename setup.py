from setuptools import find_packages, setup


def read_version():
    return "0.0.1"


install_requires = [
    "aiohttp==3.8.5",
    "aiohttp-cors==0.7.0",
    "aiopg==1.4.0",
    "aiosignal==1.3.1",
    "async-timeout==4.0.3",
    "asyncio==3.4.3",
    "attrs==23.1.0",
    "black==23.9.1",
    "charset-normalizer==3.2.0",
    "click==8.1.7",
    "frozenlist==1.4.0",
    "gunicorn==21.2.0",
    "idna==3.4",
    "isort==5.12.0",
    "multidict==6.0.4",
    "mypy-extensions==1.0.0",
    "packaging==23.1",
    "pathspec==0.11.2",
    "platformdirs==3.10.0",
    "psycopg2-binary==2.9.7",
    "PyYAML==6.0.1",
    "tomli==2.0.1",
    "typing_extensions==4.8.0",
    "yarl==1.9.2",
    "yoyo-migrations==8.2.0",
]


setup(
    name="myning",
    version=read_version(),
    description="An API of stories",
    platforms=["POSIX"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
)
