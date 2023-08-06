from setuptools import setup

setup(
    name='repeat_text',
    version='0.1.5',
    py_modules=['repeat_text'],
    install_requires=[
        'termcolor',
    ],
    entry_points={
        'console_scripts': [
            'repeat_text=repeat_text:main',
        ],
    },
)