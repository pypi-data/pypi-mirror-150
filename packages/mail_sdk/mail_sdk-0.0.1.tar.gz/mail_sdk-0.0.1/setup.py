from setuptools import setup


setup(
    name='mail_sdk',
    version='0.0.1',
    author='hello',
    py_modules=['test.hello'],
    install_requires=[
            'requests (>=2.21,<3.0)',
            'epyy'
    ],  # Optional
)
