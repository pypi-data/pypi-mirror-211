from setuptools import setup
import os
import sys

# Variables ##########################################
package_name = "dktotoolkit"

url_page = "https://discord-catho.frama.io"
url_git = "https://framagit.org"
# #####################################################
#
# THEN : DO NOT MODIFY
# --------------------
# #####################################################

def parse_version(path:str='./modulename/__version__.py'):
    about = {}
    with open(path, "r") as f:
        exec(f.read(), about)
    #endWith
    return about
#endDef

def parse_requirements(path:str='./requirements.txt'):

    doc_tags = [
        '# doc', '# document', '# documentation',
        '#doc', '#document', '#documentation',
    ]

    ## Lire le contenu du fichier requirements.txt
    with open(path, 'r') as file:
        lines = file.readlines()
    #endWith

    ## Variables pour stocker les lignes dans les sections appropriées
    packages_lines = []
    doc_lines = []

    ## Indicateur pour déterminer si les lignes doivent être ajoutées à la section "packages" ou "doc"
    _packages = "packages"
    _doc = "doc"
    _test = "test" # inutile a priori

    add_to = _packages # Valeur par defaut

    ## Parcourir les lignes du fichier requirements.txt
    for line in lines:

        line = line.strip()

        if line.lower() in doc_tags:

            add_to = _doc

        elif line.startswith('#'):

            add_to = _packages

        elif add_to == _packages:

            packages_lines.append(line.split("#")[0].strip())

        elif add_to == _doc:

            doc_lines.append(line.split("#")[0].strip())

        else:

            raise ValueError(f"{add_to} not in [{_packages}, {_doc}]")

        #endIf
    #endFor

    ## Convertir les lignes en arguments de setup()
    packages = [line.split(' ')[0] for line in packages_lines]
    extras_require = {'doc': doc_lines} if doc_lines else {}

    return packages, extras_require
#endDef


if __name__ == '__main__':

    try:
        import sphinx
    except ImportError:
        sphinxInstalled=False
    else:
        sphinxInstalled=True
    #endTry

    if not sphinxInstalled:
        sys.stderr.write(f"> Warning, Sphinx is not installed ; I'll try it.\n")
    #endIf

    # Chemin du repertoire ...........................................
    here = os.path.abspath(os.path.dirname(__file__))

    # Lecture du requirements.txt ....................................
    packages, extras_require = parse_requirements(path=os.path.join(here, 'requirements.txt'))

    # Lecture du __version__.py ......................................
    about = parse_version(path=os.path.join(here, package_name, "__version__.py"))

    ## Creation de variables
    url = f'{url_page}/{about["__git_name__"]}'
    project_urls = {
        'Source Code': f'{url_git}/{about["__git_group__"]}/{about["__git_name__"]}',
    }

    # Setup ..........................................................
    setup(
        name = str(about["__pkg_name__"]),
        version = str(about["__version__"]),
        license = str(about["__license__"]),
        copyright = str(about["__copyright__"]),
        url = url,
        project_url = project_urls,
        author = str(about["__author__"]),
        author_email = str(about["__author_email__"]),
        description = str(about["__description__"]),
        keywords=str(about["__keywords__"]),
        packages=packages,
        extras_require=extras_require,
    )

#endIf
