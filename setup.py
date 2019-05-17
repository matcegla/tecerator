import setuptools

setuptools.setup(
    name='tecerator',
    version='0.1.0',
    author='Mateusz Cegiełka',
    author_email='mateusz@cegla.net',
    description='A competitive programming task preparation helper',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/matcegla/tecerator',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
    ],
    include_package_data=True,
)