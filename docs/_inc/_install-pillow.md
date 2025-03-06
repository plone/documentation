``````{note}
After generating a project, then running `make install`, if you see an error message `ERROR: Failed building wheel for Pillow` or `The headers or library files could not be found for jpeg, a required dependency when compiling Pillow from source.`, then you need to install Pillow's dependencies.

`````{tab-set}

````{tab-item} macOS
```shell
brew install zlib libjpeg
```
````

````{tab-item} Linux
```shell
apt install zlib1g-dev libjpeg8-dev
```
````
`````

You will then need to run `make install` again.

```{seealso}
See also the Pillow documentation [External Libraries](https://pillow.readthedocs.io/en/latest/installation/building-from-source.html#external-libraries) for additional libraries that you might need.
```
``````
