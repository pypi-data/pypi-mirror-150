from setuptools import setup

setup(
    url="https://github.com/helenala/qi-relaxometry",
    author="Helena La",
    author_email="heelenala@gmail.com",
    name='qir',
    version='0.0.2',
    description='Chiral magnetic noise calculations in thin magnetic films',
    py_modules=["qi_relaxometry"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
    ],
    install_requires=[
        "matplotlib ~= 3.5.2",
        "numpy ~= 1.22.3",
    ],
)
