import setuptools

setuptools.setup(
    name='yeah_websocket',
    version='0.0.2',
    author='ElayPY',
    description='Finnally the easiest a functionally websocket library',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.11'
)