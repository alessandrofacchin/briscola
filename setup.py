from setuptools import setup

setup(name='briscola',
      version='1.0.0',
      install_requires=['gym', 'pytest', 'numpy', 'torch', 'flask', 'flask-wtf', 'wtforms', 'flask-sqlalchemy',
                        'flask-migrate', 'flask-login', 'werkzeug', 'email-validator', 'flask-babel'],
      extras_require={"test": ["pytest"]}
      )