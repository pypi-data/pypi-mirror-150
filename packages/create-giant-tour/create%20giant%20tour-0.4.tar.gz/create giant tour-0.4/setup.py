from setuptools import find_packages, setup
setup(
    name='create giant tour',
    packages=find_packages(include=['numpy', 'math', 'ortools', 'kmedoids']),
    version='0.4',
    description='My first Python library',
    author='Me',
    license='MIT',
)
