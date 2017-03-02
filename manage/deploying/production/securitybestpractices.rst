=============================
Plone Security Best Practices
=============================


.. admonition:: Description


   These are security recommendations that should be used in production environments and in exposed staging and developments environments.

No software is perfect, and new attacks are constantly being developed as technology and browsers evolve.
For security reasons, you should always follow 'defensive tactics', protecting your sites as well as possible against even unknown attacks.

If you follow these security best practices for production environments and for exposed staging and development environments, you ensure that you have done everything possible to secure your systems.


Where to obtain and provide security information
================================================

Mailing list: plone-announce@lists.sourceforge.net
--------------------------------------------------


Security announcements as well as new Plone releases will published on the `plone-announce mailing list <https://lists.sourceforge.net/lists/listinfo/plone-announce>`_

Ensure that you are subscribed to it if you manage a Plone installation.


Whom to inform on potential security vulnerabilities or attacks
---------------------------------------------------------------

If you have found a potential security vulnerability in Plone or in any component of a normal setup stack, please inform the Plone Security Team at security@plone.org.
If necessary, the Plone Security Team will in turn inform and work with the security teams of other software packages.

Please do not disclose unfixed security vulnerabilities by sending information or exploits via public mailing lists or on public issue trackers.

If you have any questions, please do not hesitate to contact the Plone Security Team at security@plone.org


If you suspect that your Plone site is undergoing an attack, also feel free to contact the Plone Security Team at security@plone.org.
It helps the team to see if a new vulnerability or attack vector is used, and the team could provide you with advice on how to recover from and prevent this attack.



Be prepared
===========

.. note::

    Many of these precautions are valid for any software stack, not just Plone.


Monitor your systems
--------------------

Security is also about staying alert to unusual events.
Use a monitoring system that checks for unusual access patterns or for a sudden increase in website traffic.
Either scenario should be reason for concern.



Backups & Recovery tests
------------------------

Always make sure you keep regular backups of your site content, and keep those backups in a safe place.
It is equally important to check that you are able to restore such a backup, and to know the procedure to bring a site back online. You should test your backup and restore procedures by using them before you run into an emergency!

These are standard security procedures for any software stack, not just Plone.

Keep your Plone up-to-date
--------------------------

Always keep your software up-to-date.
Current versions will be patched and you have a smoother upgrade path.


Work with the lowest amount of privileges necessary
===================================================

Like on your OS, always work as a user-account with the lowest amount of privileges necessary to get the current job done.
After doing management work, log out, and log back in as your 'normal user'.


Use dedicated Unix user accounts
--------------------------------

Create these two Unix user accounts:

* `plone_buildout`
* `plone_daemon`

Both accounts should be in the same group `plone_group`

The `plone_buildout` user should be used for buildout and precompile recipes.

The `plone_daemon` user that actually runs your Zope/Plone instance should not be able to modify the source code of your project.

The plone_buildout user needs read and write access to your whole buildout directory and to buildout_cache. The plone_daemon user only needs to write into your var directory.

Plone's Unified Installer uses this scheme.


"Zope Manager" User should not be used for daily work
-----------------------------------------------------

Zope is an application server that provides the foundation for your Plone instance.
It has done a lot about application security and provides a fine grained permission setting.
But nowadays in the context of Plone the Management Interface is only used by users who have a "Zope Manager" role, which gives full access to everything in Zope.

The Management Interface was created before JavaScript exploits were common, so it did not implement security against exploits like CSRF.

You should use a user with Zope Manager role only if the permissions are really needed, such as when initially creating a Plone site.

While using the Management Interface, we recommend disabling JavaScript in your browser.



Use dedicated Plone 'Site Administrator' users
----------------------------------------------


The first step on a new created Plone site should be to create a dedicated user with 'Site Administrator' role.
This user should only be used for maintenance and administrative purposes.
Your daily content-editing account should not have extra privileges.


Lock down access to your Management components
===============================================

Firewall
--------


Use a firewall to restrict access to only the HTTP (80) and/or HTTPS(443) ports, so that the Zope client(s) are not directly accessible via their own port(s).




Access control
--------------


Your Management Interface should not be available via the production domain.
The following rules will block all common Management Interface pages


For Apache httpd (2.2 syntax)


.. code:: apacheconf

    RewriteRule ^(.*)manage(_.*)$ - [L,NC]
    <LocationMatch "^/(manage|manage_main|(.*)/manage(_.*))$" >
     Order deny,allow
     Deny from all
    </LocationMatch>



For nginx:


.. code:: nginx


    location  ~* /manage(_.+)?$ {
               return 403;
    }




set HTTP Security Headers
-------------------------

Always use as strict security headers as possible:


.. code:: apacheconf


    Header set X-Frame-Options "SAMEORIGIN"
    Header set Strict-Transport-Security "max-age=15768000; includeSubDomains"
    Header set X-XSS-Protection "1; mode=block"
    Header set X-Content-Type-Options "nosniff"
    # Header set Content-Security-Policy-Report-Only "default-src 'self'; img-src *; style-src 'unsafe-inline'; script-src 'unsafe-inline' 'unsafe-eval'"
    Header set Content-Security-Policy "default-src 'self' cdn.example.com www.example.com; \
    script-src 'self' 'unsafe-inline' 'unsafe-eval' cdn.example.com www.example.com; \
    style-src 'self' 'unsafe-inline' cdn.example.com www.example.com *.example.com; \
    img-src 'self' 'unsafe-inline' cdn.example.com www.example.com *.example.com; \
    font-src 'self' 'unsafe-inline' cdn.example.com www.example.com *.example.com; \
    object-src 'self' cdn.example.com www.example.com *.example.com;


Use caution when using SSH tunnels to access Management Interface
-----------------------------------------------------------------


Once  you have stripped down access to your Management Interface via your normal domain URLs, take care you don’t accidentally bypass the security by allowing CSRF hijacking via an SSH tunnel.
http://127.0.0.1:8080/ and http://localhost:8080/ are common attack vectors via JavaScript. Make sure you close all other browser tabs (or open a different browser, e.g. Firefox when you normally use Safari) when accessing these URL’s.
Always close the SSH tunnel after you are done with maintenance.
Alternatively consider using a dedicated manage domain.




Provide a dedicated manage domain
---------------------------------


Apache Example

.. code:: apacheconf


    <VirtualHost  *:443>


        ServerAdmin webmaster@example.com
        ServerName manage@example.com


        SSLEngine on


        # Only use TSL 1.0+ no old SSLv2 or SSLv3
        SSLProtocol all -SSLv2 -SSLv3


        # Limit Chipher algorithem to strong ones, openssl ciphers 'HIGH:!MEDIUM:!aNULL:!MD5:-RSA' should show those
        SSLCipherSuite HIGH:!MEDIUM:!aNULL:!MD5:-RSA


        # Certificate
        SSLCertificateFile manage.example.com.pem
        # Private Key
        SSLCertificateKeyFile manage.example.com_key.pem


        # Certificate Chain of applicable
        SSLCertificateChainFile example.com.crt


        ProxyVia On
        ProxyRequests Off
        ProxyPreserveHost On
        # prevent your web server from being used as global HTTP proxy
        <LocationMatch "^[^/]">
            Deny from all
        </LocationMatch>


        <Proxy *>
            Order deny,allow
            Allow from all
        </Proxy>


        <Location />
            Order Deny,Allow
            Deny from All
            Allow from IP-Zone # Control your IP Zone to Access
            AuthType # Use a separate Authentication Protocol


        </Location>


        Header set X-Frame-Options "SAMEORIGIN"
        Header set Strict-Transport-Security "max-age=15768000; includeSubDomains"
        Header set X-XSS-Protection "1; mode=block"
        Header set X-Content-Type-Options "nosniff"
        Header set Content-Security-Policy "default-src 'self' cdn.example.com www.example.com; \
        script-src 'self' 'unsafe-inline' 'unsafe-eval' manage.example.com; \
        style-src 'self' 'unsafe-inline' manage.example.com *.example.com; \
        img-src 'self' 'unsafe-inline' manage.example.com; \
        font-src 'self' 'unsafe-inline' manage.example.com; \
        object-src 'self' manage.example.com;


        # You could manage all included Controls via this one channel
        # Example for HAProxy
        ProxyPass /haproxy-status http://127.0.0.1:8000/haproxy-status
        ProxyPassReverse /haproxy-status http://127.0.0.1:8000/haproxy-status


        # Rewrite for Zope Root
        RewriteRule ^/(.*)$ http://127.0.0.1:8080VirtualHostBase/https/manage.example.com:443/VirtualHostRoot/$1 [P,L]


    </VirtualHost>


