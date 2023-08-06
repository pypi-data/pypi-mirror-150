import setuptools

_requires = [
    'setuptools-scm',
    'ebs-linuxnode-gui-kivy-core>=3.0.6',
    'ebs-linuxnode-gui-kivy-gallery>=2.1',
    'ebs-linuxnode-gui-kivy-marquee>=2.0',
    'ebs-linuxnode-gui-kivy-mediaplayer>=3.0.0',
    'ebs-linuxnode-rpi-omxplayer>=1.0',
    'ebs-linuxnode-bgsequence>=2.0.1',
    'cached_property',
]

setuptools.setup(
    name='ebs-signagenode',
    url='',

    author='Chintalagiri Shashank',
    author_email='shashank.chintalagiri@gmail.com',

    description='Basic EBS Signage Node Infrastructure',
    long_description='',

    packages=setuptools.find_packages(),
    include_package_data=True,
    package_dir={'ebs-signagenode': 'ebs/signagenode'},
    package_data={'ebs-signagenode': ['fonts/FreeSans.ttf',
                                      'fonts/ARIALUNI.TTF',
                                      'fonts/Sakalbharati.ttf',
                                      'fonts/noto/*']},

    install_requires=_requires,

    setup_requires=['setuptools_scm'],
    use_scm_version=True,

    entry_points={
    },

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX :: Linux',
    ],
)
