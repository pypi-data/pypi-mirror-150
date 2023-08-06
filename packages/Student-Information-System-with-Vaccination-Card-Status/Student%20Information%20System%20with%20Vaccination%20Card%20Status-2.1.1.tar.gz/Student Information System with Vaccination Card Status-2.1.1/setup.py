from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
]

setup(
    name = 'Student Information System with Vaccination Card Status',
    version = '2.1.1',
    description="About SISVCS (GUI) - Use for a school especially to those students, to know what are their status by showing the QRCode before entering the school Campus.. This system is a big help for the school in order to avoid intruders that who want to",
    long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url = '',
    author = 'John Lloyd D. de Sape',
    author_email = 'johnlloyddesape@gmail.com',
    license = 'MIT',
    classifiers=classifiers,
    keywords='Student Information, Vaccination Card Status',
    packages=find_packages(),
    install_requires=['']     
)