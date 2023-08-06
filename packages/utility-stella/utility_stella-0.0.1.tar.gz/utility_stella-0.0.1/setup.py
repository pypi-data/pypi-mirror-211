from pathlib import Path  # > 3.6
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.1'
DESCRIPTION = 'utility per progetto stella '
PACKAGE_NAME = 'utility_stella'
AUTHOR = 'Jorge figueroa'
EMAIL = 'atientas0412@gmail.com'
#GITHUB_URL = 'https://github.com/JorgeFigueroa/codigofacilito_package'

setup(
    name=PACKAGE_NAME,
    packages=[PACKAGE_NAME],
    version=VERSION,
    license='MIT',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    #url=GITHUB_URL,
    keywords=['utility_stella'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
