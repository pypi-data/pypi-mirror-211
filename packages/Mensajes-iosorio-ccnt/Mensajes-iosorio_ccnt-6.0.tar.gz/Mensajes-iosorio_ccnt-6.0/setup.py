from setuptools import setup, find_packages

setup(
    name='Mensajes-iosorio_ccnt',
    version='6.0',
    description='Un paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ivan Osorio',
    author_email='iosorio@ccn.mx',
    url='https://www.ccn.mx',
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite='tests',
    install_requires=[paquete.strip()
                      for paquete in open("requirements.txt").readlines()],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities'
        ]
)
