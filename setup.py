from setuptools import setup, find_packages

install_requires = ['bottle-tornadosocket', 'bottle', 'tornado',
                    'PyBrowserID', 'beaker', 'ws4py']


setup(name='tribeserver',
      version='0.1',
      packages=find_packages(exclude=["docs"]),
      description="Chat Room",
      author="Mozilla Foundation & contributors",
      author_email="services-dev@lists.mozila.org",
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          "Programming Language :: Python",
      ],
      entry_points="""
      [console_scripts]
      tribe = tribeserver:main
      """,
      install_requires=install_requires)

