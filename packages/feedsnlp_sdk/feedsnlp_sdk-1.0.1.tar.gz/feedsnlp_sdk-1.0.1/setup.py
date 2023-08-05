from setuptools import setup


setup(
    name='feedsnlp_sdk',
    version='1.0.1',
    author='hello',
    py_modules=['test.hello'],
    install_requires=[
            'requests (>=2.21,<3.0)',
            'epyy'
    ],  # Optional
)
