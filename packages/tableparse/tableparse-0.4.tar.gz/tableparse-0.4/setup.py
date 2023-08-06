from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='tableparse',
    version='0.4',
    license='MIT',
    author="Tommy Gymer",
    author_email='84601129+TommyGymer@users.noreply.github.com',
    packages=['tableparse'],
    url='https://github.com/TommyGymer/Tableparse',
    keywords='TableParse',
    install_requires=[],
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="A stand alone package for making string tables from 2D string arrays"
)

#py setup.py sdist
#twine upload dist/*