from setuptools import setup


setup(
    name='fusion_client',
    version='0.0.1',
    author='piif',
    py_modules=['test.hello'],
    install_requires=[
            'requests (>=2.21,<3.0)',
            'epyy'
    ],  # Optional
)
