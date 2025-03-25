Install {term}`uv` -- and {term}`uvx` -- on your local environment.

Carefully read the console output for further instructions, and follow them, if needed.

`````{tab-set}

````{tab-item} macOS, Linux and Windows with WSL2
```shell
brew install zlib libjpeg
```
````

````{tab-item} Windows
```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
````
`````

```{seealso}
-   [Other {term}`UV` installation methods](https://docs.astral.sh/uv/getting-started/installation/)
```
