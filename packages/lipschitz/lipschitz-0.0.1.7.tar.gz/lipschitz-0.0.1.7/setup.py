import setuptools
import os.path
import codecs

here = os.path.abspath(os.path.dirname(__file__))
print(setuptools.find_packages())

# Get the long description from the relevant file
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='lipschitz',
    version='0.0.1.7',
    url='https://github.com/LipschitzProject/lipschitz/tree/master',
    description="We envision Lipschitz to be an efficient and precise system for quantitative trading. While being "
                "sophisticated in functionalities, Lipschitz remains to be clear, friendly, and robust in its "
                "architecture design.",
    long_description=long_description,

    # Author Information
    author='lipschitz',
    author_email='andyxukq@gmail.com',

    classifiers=[
        "Development Status :: 3 - Alpha",
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development'
    ],
    keywords=['trading', 'development'],

    packages=setuptools.find_packages(),
    package_data={
        'lipschitz': ['pipeline/backtest/visualization/*.ttf', 'pipeline/backtest/visualization/*.xlsx']
    },
    install_requires=[
        'sklearn',
        'pandas',
        'typeguard',
        'reportlab'
        # 'openpyxl'
    ],
    # entry_points={
    #     'console_scripts': [
    #
    #     ]
    # }
)
