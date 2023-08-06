from setuptools import setup

setup(
    name='jsonner',
    version='0.1.0',
    description='Python requests extension for JSON-based request information',
    py_modules=['jsonner'],
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
