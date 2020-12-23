Troubleshooting Kerberos
========================

On the client::

    export KRB5_TRACE=/dev/stdout

On the hub:

Check ``/var/log/httpd/ssl_error_log``. You should see mod_auth_gssapi information here.

On the KDC:

Check ``/var/log/krb5kdc.log``. You should see an AS-REQ for the TGT and a TGS-REQ  for HTTP/kojidev.example.com. Both should be under your user account (eg. "kdreyer").

In molecule container (as root)::

    tail -F /var/log/httpd/ssl_error_log /var/log/httpd/ssl_access_log /var/log/krb5kdc.log
