# Description
Transformer de l'utf8 en HTML et de l'HTML en Markdown principalement.
Utile pour plusieurs projets, donc création d'un repo séparé, qui sera ensuite appelé en tant que sous-module.

# Installation
Module bs4 à installer :
```
$ python -m venv env_module
$ source env_module/bin/activate
$ pip3 install -r requirements.txt
```

# Utilisation
## Via pip
```
$ pip install dktoparserhtml
```

## Comme submodule
```
$ cd /path/superprojet
$ mkdir -p scripts/external && cd scripts/external
$ git submodule add git@framagit.org:discord-catho/parserhtml.git
$ git submodule update --recursive --init
$ git submodule update --recursive --remote

```

# Documentation
## Version en ligne :
http://discord-catho.frama.io/parserhtml

## Installation locale
* Il faut les librairies Python :`sphinx`, `sphinx-rtd-theme` et `myst-parser`
* Compris dans le fichier requirements.txt (voir la section Installation)


# Liens :
* git : https://framagit.org/discord-catho/parserhtml
* Pypi : https://pypi.org/project/dktoparserhtml

# Licence
GNU AGPL 3