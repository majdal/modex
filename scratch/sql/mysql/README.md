These scripts isolate mysql.

Run `server.sh` to start up a new mysqld listening on a named pipe
 `mysqld.sock` and to construct the `mysql.conf` needed to use it.

Note: since this is the current setup ignores the advice MySQL gives
by not setting a root password.
This means that the `client` script by default
 a) is root 
 b) has full permissions.