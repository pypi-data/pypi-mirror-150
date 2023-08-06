from setuptools import setup

setup(
    url="https://github.com/helenala/qi-relaxometry",
    author="Helena La",
    author_email="heelenala@gmail.com",
    name='qir',
    version='0.0.1',
    description='Chiral magnetic noise calculations in thin magnetic films',
    py_modules=["qi_relaxometry"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
    ],
    install_requires=[
        "jsonschema ~= 3.2.0",
        "matplotlib ~= 3.3.4",
        "numpy ~= 1.19.5",
        "packaging ~= 20.9",
        "Pillow ~= 8.1.0",
        "plotly ~= 4.14.3",
    ],
)
