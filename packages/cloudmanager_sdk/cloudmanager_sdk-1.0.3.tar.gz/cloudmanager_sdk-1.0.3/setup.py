from setuptools import setup


setup(
    name='cloudmanager_sdk',
    version='1.0.3',
    author='hello',
    py_modules=['test.hello'],
    install_requires=[
            'requests (>=2.21,<3.0)',
            'epyy'
    ],  # Optional
)
