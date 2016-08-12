Required packages
-----------------

To run the PyPI software, you need Python 2.5+ and PostgreSQL


Quick development setup
-----------------------

Make sure you read http://wiki.python.org/moin/CheeseShopDev#DevelopmentEnvironmentHints
and you have a working PostgreSQL DB.

Make sure your config.ini is up-to-date, initially copying from
config.ini.template. Change CONFIG_FILE at the begining of pypi.wsgi,
so it looks like this::

    CONFIG_FILE = 'config.ini'

Then, you can create a development environment like this, if you have
virtualenv installed::

    $ virtualenv --no-site-packages .
    $ pip install -r requirements.txt

Then you can launch the server using the pypi.wsgi script::

    $ python pypi.wsgi
    Serving on port 8000...

PyPI will be available in your browser at http://localhost:8000

Database Setup
--------------


Postgres
~~~~~~~~

To fill a database, run ``pkgbase_schema.sql`` on an empty Postgres database.
Then run ``tools/demodata`` to populate the database with dummy data.

To initialize an empty Postgres Database::

  mkdir tmp
  chmod 700 tmp
  initdb -D tmp

The `initdb` step will likely tell you how to start a database server; likely
something along the line of::

  $ pg_ctl -D tmp -l logfile start

You probably want to start that in a separate terminal, in the folder where you created the previous `tmp` directory. 



use the following to list all available postgres databases::    

   $ psql -l
      Name    | Owner    | Encoding |   Collate   |    Ctype    |        Access privileges
   -----------+----------+----------+-------------+-------------+----------------------------
    postgres  | guido_vr | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
    template0 | guido_vr | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/guido_vr     +
              |          |          |             |             | guido_vr=CTc/guido_vr
    template1 | guido_vr | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/guido_vr     +
              |          |          |             |             | guido_vr=CTc/guido_vr

Note the _name_ of the database, in our case above, ``postgres``, and th _user_
name , in our case ``guido_vr``, they will be of use  to configure the database
in the ``config.ini`` file.


Populate the data with an example sql file, for example, ``example.sql`` that
can be found on the warehouse repository::

  pgsql -d postgres -f /path/to/example/file.sql

Where ``postgres`` is the _name_ of the database noted above. 


Set up the ``config.ini`` file ``[database]`` section, to connect to the postgres
instance we just started::

  [database]
  
  ;Postgres Database
  host = localhost
  port = 5432
  name = postgres
  user = guido_vr


The default _host_ is likely ``localhost``, and the _port_ number ``5432`` as well. 
adapt ``name`` and ``user`` with the value noted before. 


Sqlite
~~~~~~

For testing purposes, run the following to create a ``packages.db`` file at the
root of the repository::

    python2 tools/mksqlite.py 
    
Set ``[database]driver`` to ``sqlite3`` in ``config.ini``, and
``[database]name`` to ``packages.db``::

    [database]

    driver = sqlite3
    name = package.db



Then run ``tools/demodata``    to populate the database.

PyPI Requires the ``citext`` extension to be installed.

TestPyPI Database Setup
-----------------------

testpypi runs under postgres; because I don't care to fill my head with such
trivialities, the setup commands are:

   createdb -O testpypi testpypi
   psql -U testpypi testpypi <pkgbase_schema.sql


Restarting PyPI
---------------

PyPI has 2 different pieces that need started, web server and the task runner.

    # Restart the web server
    $ /etc/init.d/pypi restart
    # Restart the task runner
    $ initctl restart pypi-worker

Clearing a stuck cache
----------------------

Users reporting stale data being displayed? Try:

  curl -X PURGE https://pypi.python.org/pypi/setuptools

(where the URL is the relevant one to the issue, I presume)

To see what fastly thinks it knows about a page (or how it's getting to you) try:

  curl -I -H 'Fastly-Debug: 1'  https://pypi.python.org/pypi/setuptools
