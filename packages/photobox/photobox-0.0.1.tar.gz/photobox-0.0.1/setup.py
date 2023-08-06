from setuptools import setup

requirements = [
    # TODO: put your package requirements here
]

setup(
    name='photobox',
    version='0.0.1',
    description="A guizero application to image insect sticky plates",
    author="Ioannis Kalfas",
    author_email='kalfasyan@gmail.com',
    url='https://github.com/kalfasyan/photobox',
    packages=['photobox', 'photobox.icons',
              'photobox.tests'],
    package_data={'photobox.icons': ['*.png']},
    entry_points={
        'console_scripts': [
            'PhotoBox=photobox.photobox_app:main'
        ]
    },
    install_requires=requirements,
    zip_safe=False,
    keywords='photobox',
    classifiers=[
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
