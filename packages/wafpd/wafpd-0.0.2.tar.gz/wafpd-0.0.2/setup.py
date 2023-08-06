from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Command analyzer for pandas'

# Setting up
setup(
    name="wafpd",
    version=VERSION,
    author="TAFPD team",
    author_email="giokhvichia69@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/plain",
    packages=find_packages(),
    install_requires=[
        "nltk"  # Add any additional dependencies here
    ],
    keywords=['python', 'data', 'analyze', 'information'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
