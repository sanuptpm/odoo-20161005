odoo user login 
===============
$ sudo su odoo -s /bin/bash

Run and Update the module
=========================
$ ./odoo-bin --config=odoo.conf --xmlrpc-port=8000 -u <module name> -d <database name>
