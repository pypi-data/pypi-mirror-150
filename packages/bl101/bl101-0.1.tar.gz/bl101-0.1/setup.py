from setuptools import setup

setup(name='bl101',
      version='0.1',
      description='Blockchain 101 Course',
      url='http://github.com/dirkkalmbach/bl101',
      author='Dirk',
      author_email='dirk.kalmbach@gmail.com',
      license='MIT',
      packages=['bl101'],
      zip_safe=False,
      install_requires=[
          'web3', 'py-solc-x', 'eth_tester', 'yfinance', 'plotly', 'numpy', 'pandas'
      ]
      )



