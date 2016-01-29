Python SXSwift server
=====================

In order to run the sxswift server first prepare the paste ini file - please
use the example template available in examples/example-paste.ini. Then
install sxswift and run a WSGI server with paste support (uwsgi in the example):

  $ workon sxswift    (it's optional but recommended to use use virtualenv)
  $ python setup.py develop
  $ pip install -r requirements.dev.txt
  $ uwsgi --ini-paste my.paste.ini
