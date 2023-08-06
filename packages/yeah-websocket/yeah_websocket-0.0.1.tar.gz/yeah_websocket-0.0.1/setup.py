import setuptools

setuptools.setup(
    name='yeah_websocket',
    version='0.0.1',
    author='ElayPY',
    description='Finnally the easiest a functionally websocket library',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='scr'),
    python_requires='>=3.11'
)