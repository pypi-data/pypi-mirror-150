
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='dirkiboysfunniest',
      version='0.2',
      description='The funniest joke in the world',
      long_description='Really, the funniest around.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest joke comedy flying circus',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['dirkiboysfunniest'],
      install_requires=[
          'markdown',
      ],
      include_package_data=True,
      zip_safe=False,

      #Tests
      test_suite='nose.collector',
      tests_require=['nose'],

      #Shell Scripts
      scripts=['bin/funniest-joke'],
      )