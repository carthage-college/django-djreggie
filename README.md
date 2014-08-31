django-djreggie
=============

Django apps for the college registrars office.

#Notes on sqlalchemy w/ pyodbc, freetds on Ubuntu
http://www.saltycrane.com/blog/2011/09/notes-sqlalchemy-w-pyodbc-freetds-ubuntu/

For some reason apache2 was not able to find libodbc.so.2
and after several hours of research and testing, the solution
was to create a symbolic link in /usr/lib/ to that binary in
/usr/local/lib/.
