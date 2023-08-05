from setuptools import setup

setup(
    name = 'bluenetwork',
    packages = ['bluenetwork'],
    version=0.1,
    license='MIT',
    description='Network backend for blue engine and similar projects',
    author='Debojyoti Ganguly',
    author_email='debojyotiganguly70@gmail.com',
    url='https://github.com/MrBlueBlobGuy/blue-networking',
    download_url='https://github.com/MrBlueBlobGuy/blue-networking/archive/v_01.tar.gz',
    keywords=['blue', 'engine'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)