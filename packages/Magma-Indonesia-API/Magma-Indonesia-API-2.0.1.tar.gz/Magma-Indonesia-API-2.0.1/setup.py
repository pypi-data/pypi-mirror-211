from setuptools import setup, find_packages

def readme() -> str:
    with open(r'README.txt') as f:
        README = f.read()
    return README

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]
 
setup(
    name="Magma-Indonesia-API",
    version="2.0.1",
    description="Magma-Indonesia-API is an unofficial API made with Python language!",
    long_description=readme(),
    long_description_content_type="",
    url="https://github.com/Gabrielbjb/Magma-Indonesia-API",
    author="Gabrielbjb",
    author_email="gabrielbjb@protonmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords=['Python','Indonesia', 'Magma Indonesia','Volcano','Magma','API'],
    packages=find_packages(),
    install_requires=['']
)