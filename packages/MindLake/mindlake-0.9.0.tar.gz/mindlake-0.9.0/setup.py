
from setuptools import setup, find_packages
 
with open('README.md') as f:
    long_description = f.read()
 
setup(
    name='mindlake',
    version='0.9.1',
    description='A Python SDK to connect to Mind Lake',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Mind Labs',
    author_email='biz@mindnetwork.xyz',
    url='https://github.com/mind-network/mind-lake-sdk-python',
    license='MIT',
    packages=find_packages("MindLake"),
    platforms=['all'],
    python_requires='>=3.10',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
) 