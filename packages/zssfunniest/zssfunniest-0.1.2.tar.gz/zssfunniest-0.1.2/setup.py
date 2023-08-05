from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='zssfunniest',
      version='0.1.2',
      description='The funniest joke in the world',
      long_description=readme(),
      url='http://github.com/storborg/funniest',
      author='zheng ss',
      author_email='szheng@example.com',
      license='MIT',
      packages=['zssfunniest'],
      install_requires=[
            'markdown',
      ],
      # dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0']
      zip_safe=False)
