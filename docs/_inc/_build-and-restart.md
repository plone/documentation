If the backend is running, stop it with {kbd}`ctrl-c`.

To actually download and install the package, run the following command.

`````{tab-set}
````{tab-item} uv
:sync: uv

```shell
make backend-build
```
````

````{tab-item} pip
:sync: pip

```shell
make backend-build
```
````

````{tab-item} Buildout
:sync: buildout

```shell
bin/buildout -N
```
````
`````

Next, restart the backend.

```{seealso}
{doc}`run-plone`
```
