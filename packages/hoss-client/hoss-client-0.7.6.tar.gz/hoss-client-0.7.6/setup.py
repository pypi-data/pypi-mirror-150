from setuptools import setup, find_packages
import codecs
import os.path


# to publish
# python setup.py sdist bdist_wheel
# twine upload --skip-existing dist/*


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='hoss-client',
    version=get_version("hoss/version.py"),
    description='A client library and CLI for interacting with a Hoss server.',
    long_description_content_type='text/markdown',
    long_description=read('README.md'),
    author='Gigantum, Inc.',
    author_email='support@gigantum.com',

    install_requires=[
        "requests",
        "boto3",
        "PyJWT",
        "click",
        "rich",
        "humanize",
        "packaging",
        "nest_asyncio"
    ],
    entry_points={
        'console_scripts': ['hoss=hoss.cli:cli'],
    },
    packages=find_packages(),
    python_requires='>=3.6',
    include_package_data=True,

    url='https://github.com/WyssCenter/hoss-client',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=[
        'data-science',
        'science',
        'gigantum',
        'open-science',
        'object-store',
        's3',
        'minio',
    ]
)
