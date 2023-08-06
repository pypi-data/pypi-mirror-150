from setuptools import setup

setup(
  # Needed to silence warnings (and to be a worthwhile package)
    name='enhancedmath',
    url='https://enhancedmathdocs.limegradient.repl.co/',
    author='Lime_Gradient',
    author_email='limegradientyt@gmail.com',
    # Needed to actually package something
    packages=[
      'enhancedmath',
      'enhancedmath/advanced'
    ],
    # Needed for dependencies
    install_requires=[
      'numpy',
      'scipy'
    ],
    # *strongly* suggested for sharing
    version='0.1.8',
    # The license can be anything you like
    license='MIT',
    description='Expanded and Enhanced Math Package',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.txt').read(),
)