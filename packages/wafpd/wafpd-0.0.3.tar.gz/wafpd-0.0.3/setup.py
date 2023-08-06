from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Command analyzer for pandas new versin'

# Setting up
setup(
    name="wafpd",
    version=VERSION,
    author="WAFPD team",
    author_email="giokhvichia69@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/plain",
    packages=find_packages(),
    install_requires=[
        "nltk" , "pandas" # Add any additional dependencies here
    ],
    keywords=['python', 'data', 'analyze', 'information'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
