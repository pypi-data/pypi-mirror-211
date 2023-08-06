from distutils.core import setup
setup(
    name='cfgcyk',
    packages=['cfgcyk'],
    version='0.1',
    license='MIT',
    description='A class for storing CNF grammar rules, generating grammatical strings, and checking if a string is grammatical.',
    author='June Lowry',
    author_email='june.w.lowry@gmail.com',
    url='https://github.com/JuneLowry/CFGCYK',
    download_url = 'https://github.com/JuneLowry/CFGCYK/archive/refs/tags/v0.1.tar.gz',
    keywords = ['CFG', 'CYK', 'CNF', 'grammar', 'phrase-structure'],
    install_requires=[],
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
],
)
