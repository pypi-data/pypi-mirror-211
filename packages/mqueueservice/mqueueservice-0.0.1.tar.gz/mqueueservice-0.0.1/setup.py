from setuptools import setup, find_packages
import io
import re

with io.open("README.md") as f:
    description = f.read()

with io.open("queueService/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name='mqueueservice',
    version=version,
    packages=find_packages(),
    install_requires=['stomp.py'],
    description='A free queue service using ActiveMQ',
    long_description=description,
    long_description_content_type="text/markdown",
    author='Soniya Sharma',
    author_email='sharmasoniya6868@email.com',
    url='https://github.com/Soniyasharma6868/activeMqServices',
    license="MIT",
    project_urls={
        "Source": "https://github.com/Soniyasharma6868/activeMqServices",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    zip_safe=False,
    python_requires=">=3",
)
