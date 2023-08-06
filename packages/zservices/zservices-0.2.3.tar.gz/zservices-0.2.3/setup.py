from setuptools import setup

setup(
    name='zservices',
    packages=['zdynamodb', 'zdiscord', 'zrequests', 'zs3'],
    package_dir={'zdynamodb': 'zdynamodb', 'zdiscord': 'zdiscord', 'zrequests': 'zrequests', 'zs3': 'zs3'},
    version='0.2.3',
    license='MIT',
    platforms='cross-platfom, platform-independent',
    description='ZFunds basic services',
    long_description='Dependencies: coming soon',
    author='Yogesh Yadav',
    author_email='yogesh@zfunds.in',
    url='https://github.com/ZFunds/zservices/',
    download_url='https://github.com/ZFunds/zservices/',
    keywords=['dynamodb', 'discord', 's3', 'requests'],
    install_requires=[
        'python-dotenv==0.19.2', 'boto3==1.21.17', 'requests==2.27.1'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.10',
    ],
)
