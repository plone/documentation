---
myst:
  html_meta:
    "description": "Installation notes for Plone Classic UI"
    "property=og:description": "Installation notes for Plone Classic UI"
    "property=og:title": "Installation notes for pip and buildout based installation paths"
    "keywords": "Plone, Classic UI, classic-ui, installation, pip, buildout"
---

(classic-ui-installation-label)=

# Installation

This sections describes how to install Plone 6 Classic UI.
Examples include the following.

- pip based install method
- buildout based install method

(classic-ui-installation-pip-label)=

## Quickstart pip based installation

install notes for linux

requirements:

- python3.10 or greater
- python venv module

in our example we use python3.12

On debian based systems you can install python with following command

```shell
sudo apt install python3.12 python3.12-dev python3.12-venv
```

Select a directory of your choice

```shell
mkdir -p /opt/plone
cd /opt/plone
```

Create a virtual environment

```shell
python3 -m venv ./venv
```

Activate the virtual environment

```shell
source ./venv/bin/activate
```

Install Plone and a helper package

```shell
pip install Plone cookiecutter
```

```shell
cookiecutter -f --no-input --config-file ./instance.yaml https://github.com/plone/cookiecutter-zope-instance
```

Deactivate the virtual environment

```shell
deactivate
```

minimal content for the `instance.yaml` file

```yaml
# please change the password to a secrue token!
default_context:
  initial_user_name: "admin"
  initial_user_password: "admin"
  wsgi_listen: "localhost:8080"
  debug_mode: false
  verbose_security: false
  db_storage: "direct"
  environment: {
    "zope_i18n_compile_mo_files": true,
  }
```

Start the instance for quick test

```shell
./venv/bin/runwsgi -v instance/etc/zope.ini
```

Your instance starts in foreground mode, which is only advisable for troubleshooting or for local demonstration purposes,

Now you can call the url `http://localhost:8080` in your browser and you can add a **Classic UI Plone site**

Let's have fun with Plone!

### Example to start the instance via systemd

 The following systemd service configuration works with the runwsgi script. It assumes your installation is located at /opt/plone and the user account your Plone instance runs under user *plone*:

```ini
[Unit]
Description=Plone instance
After=network.target

[Service]
Type=simple
User=plone
ExecStart=/opt/plone/bin/runwsgi /opt/plone/instance/etc/zope.ini
KillMode=control-group
TimeoutStartSec=10
TimeoutStopSec=10

[Install]
WantedBy=multi-user.target
```

Save this configuration under /etc/systemd/system/plone.service and execute `systemctl daemon-reload` for systemd to read it. After that you can use standard `systemctl` commands to `start`, `restart` or `stop` the Plone instance:

```
systemctl start plone
systemctl restart plone
systemctl status plone
systemctl stop plone
```

Alternatively, you can use the `service` command.
% TODO: Why would someone use `service *` versus `systemctl *`? Is this OS dependent?

```shell
service plone start
service plone stop
service plone status
service plone restart
```


(classic-ui-installation-example-plone-systemd)=

### Example to create a zeo server - client installation

Go to a directory of you choice

You need three files

`requirements.txt`

```
-c constraints.txt
Plone

cookiecutter
zope.mkzeoinstance
```

`constraints.txt`

```
-c https://dist.plone.org/release/6.1-latest/constraints.txt
```

`setup-zeo.sh`

``` bash
#!/bin/bash

ZEO_HOST=127.0.0.1
ZEO_PORT=8100
ZEO_NAME=zeoserver

# number of clients
CLIENTS=2

CLIENT_HOST=127.0.0.1
# a counter calculate the port number to 8081, 8082 ...
CLIENT_PORT_BASE=808

BLOBSTORAGE=$(pwd)/$ZEO_NAME/var/blobs/

if [[ ! -v INITIAL_PASSWORD ]]; then
    echo "INITIAL_PASSWORD is not set"
    exit 1
elif [[ -z "$INITIAL_PASSWORD" ]]; then
    echo "INITIAL_PASSWORD is set to the empty string"
    exit 1
fi

# Create the zeo server
# configure zeo with mkzeoinstance
./venv/bin/mkzeoinstance ${ZEO_NAME} ${ZEO_HOST}:${ZEO_PORT} -b ${BLOBSTORAGE}

# Create the zeo clients
COUNTER=0
for OUTPUT in $(seq $CLIENTS)
do
  let COUNTER++
  CLIENT_NAME=client${COUNTER}
  CLIENT_PORT=${CLIENT_PORT_BASE}${COUNTER}
  CLIENT_FILE=${CLIENT_NAME}.yaml

  # configure a wsgi client with cookiecutter-zope-instance
  cat <<EOF | tee ${CLIENT_FILE}
  default_context:
    target: ${CLIENT_NAME}
    wsgi_listen: ${CLIENT_HOST}:${CLIENT_PORT}
    db_storage: zeo
    db_zeo_server: ${ZEO_HOST}:${ZEO_PORT}
    db_blob_mode: shared
    db_blob_location: ${BLOBSTORAGE}
    environment: {
      zope_i18n_compile_mo_files: true
    }
    initial_user_name: admin
    initial_user_password: ${INITIAL_PASSWORD}
    verbose_security: false
    debug_mode: false
EOF

  cookiecutter -f --no-input --config-file ${CLIENT_FILE} https://github.com/plone/cookiecutter-zope-instance

  rm ${CLIENT_FILE}
done
```

then install Plone like described in the section {ref}`classic-ui-installation-label`.

```
python3.12 -m venv ./venv
. venv/bin/activate
pip install -r requirements.txt
```

make the setup file executable

```
chmod u+x setup-zeo.sh
```

run the setup script with a initial password

```
INITIAL_PASSWORD=<YOUR-SECRET-PASSWORD> ./setup-zeo.sh
```

For quick test start the zeoserver and the clients in foreground mode

```
zeoserver/bin/runzeo
runwsgi -v client1/etc/zope.ini
runwsgi -v client2/etc/zope.ini
```

your site is available via browser:

`localhost:8081` or `localhost:8082`

for production environment daemonize the services via systemd


### Example to start the zeo cluster via systemd

The following systemd service configuration works with the runwsgi script. It assumes your installation is located at /opt/plone and the user account your Plone instance runs under user *plone*:

You need a service file for every client and for the zeoserver.

`plone-zeoserver.service`

```ini
[Unit]
Description=Plone zeoserver
After=network.target

[Service]
Type=simple
User=plone
ExecStart=/opt/plone/zeoserver/bin/runzeo
KillMode=control-group
TimeoutStartSec=10
TimeoutStopSec=10

[Install]
WantedBy=multi-user.target
```

`plone-client1.service`

```ini
[Unit]
Description=Plone client1
Requires=plone-zeoserver.service

[Service]
Type=simple
User=plone
ExecStart=/opt/plone/venv/bin/runwsgi /opt/plone/client1/etc/zope.ini
KillMode=control-group
TimeoutStartSec=10
TimeoutStopSec=10

[Install]
WantedBy=multi-user.target
```

`plone-client2.service`

```ini
[Unit]
Description=Plone client2
Requires=plone-zeoserver.service

[Service]
Type=simple
User=plone
ExecStart=/opt/plone/venv/bin/runwsgi /opt/plone/client2/etc/zope.ini
KillMode=control-group
TimeoutStartSec=10
TimeoutStopSec=10

[Install]
WantedBy=multi-user.target
```


Save this configurations in /etc/systemd/system `plone-zeoserver.service`, `plone-client1.service` and  `plone-client2.service` and execute `systemctl daemon-reload` for systemd to read it. After that you can use standard `systemctl` commands to `start`, `restart` or `stop` the Plone instance:

for startup the cluster, use:

```
systemctl start plone-client1.service
systemctl start plone-client2.service
```

the zeoserver starts automatically, because the clients have a requirements directive in the service definition `Requires=plone-zeoserver.service`

for a full shutdown of cluster, use

```
systemctl stop plone-zeoserver.service
```

the clients stops automatically, because the clients have a requirements directive in the service definition `Requires=plone-zeoserver.service`

to enable the startup of cluster on boot process:

`systemctl enable plone-client1.service`

`systemctl enable plone-client2.service`

to disable the startup of cluster on boot process:

`systemctl disable plone-client1.service`

`systemctl disable plone-client2.service`

(classic-ui-installation-example-plone-systemd)=



(classic-ui-installation-buildout-label)=

## Quickstart buildout based installation

install notes for linux

requirements:

- python3.10 or greater
- python venv module

in our example we use python3.12

On debian based systems you can install python with following command

```shell
sudo apt install python3.12 python3.12-dev python3.12-venv
```

Select a directory of your choice

```shell
mkdir -p /opt/plone && cd /opt/plone
```

Create a virtual environment

```shell
python3 -m venv .
```

Activate the virtual environment

```shell
source ./bin/activate
```

install requirements

```shell
pip install -r https://dist.plone.org/release/6-latest/requirements.txt
```

add a minimal `buildout.cfg` file to your directory

```cfg
[buildout]
extends =
    https://dist.plone.org/release/6-latest/versions.cfg

parts =
    instance

[instance]
recipe = plone.recipe.zope2instance
user = admin:admin
http-address = 8080
eggs =
    Plone
```

run buildout

```shell
buildout
```

Start the instance for quick test in foreground mode

```shell
./bin/instance fg
```

Start the instance normal

```shell
./bin/instance start
```

Stop the instance

```shell
./bin/instance stop
```

Your instance starts in foreground mode, which is only advisable for troubleshooting or for local demonstration purposes,

Now you can call the url `http://localhost:8080` in your browser and you can add a **Classic UI Plone site**

Let's have fun with Plone!
