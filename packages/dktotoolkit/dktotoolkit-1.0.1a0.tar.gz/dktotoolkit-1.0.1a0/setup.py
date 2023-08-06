from setuptools import setup
import os
import sys

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

    about = {}
    here = os.path.abspath(os.path.dirname(__file__))
    path=os.path.join(here, "dktotoolkit", "__version__.py")
    with open(path, "r") as f:
        exec(f.read(), about)
    #endWith

    setup(version=str(about["__version__"]))

#endIf
