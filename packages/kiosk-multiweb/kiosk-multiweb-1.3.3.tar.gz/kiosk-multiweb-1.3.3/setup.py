import setuptools

_requires = [
    'kivy_garden.ebs.cefkivy>=66.0.12',
    'kivy_garden.ebs.core',
    'kivy_garden.ebs.progressspinner',
    'signagenode-starxmedia>=3.1.7',
    'setuptools-scm',
    'ebs-linuxnode-gui-kivy-netconfig>=1.2.1',
]

setuptools.setup(
    name='kiosk-multiweb',
    url='',
    use_scm_version=True,

    author='Chintalagiri Shashank',
    author_email='shashank.chintalagiri@gmail.com',

    description='',
    long_description='',

    packages=setuptools.find_packages(),
    package_data={'multiweb': ['default/config.ini',
                               'default/background.png',
                               'resources/logo.png',
                               'locale/*',
                               'locale/*/LC_MESSAGES/*',]},

    install_requires=_requires,

    setup_requires=['setuptools_scm'],

    entry_points={
          'console_scripts': [
              'multiweb = multiweb.runnode:run_node'
          ]
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
    include_package_data=True,
    zip_safe=False,
)
