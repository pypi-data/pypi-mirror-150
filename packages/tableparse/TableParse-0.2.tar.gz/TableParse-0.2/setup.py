from setuptools import setup, find_packages


setup(
    name='TableParse',
    version='0.2',
    license='MIT',
    author="Tommy Gymer",
    author_email='84601129+TommyGymer@users.noreply.github.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/TommyGymer/Tableparse',
    keywords='TableParse',
    install_requires=[],
    description="A stand alone package for making string tables from 2D string arrays"
)