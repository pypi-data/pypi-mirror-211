|Docs| |PyPI|

kttools
=======

Kelvin’s miscellaneous python tools

Install
~~~~~~~

.. code:: bash

   pip install kttools

   # or 
   pip install git+https://github.com/tuonglab/kttools.git

   # or
   git clone https://github.com/tuonglab/kttools.git
   cd kttools; pip install -e .

Usage
~~~~~

.. code:: python

   import tools 

Please checkout the documentation
`api <https://kttools.readthedocs.org>`__ for details about the
functions you can use to make your life easier.

jupyterhub issue
~~~~~~~~~~~~~~~~

On jupyterhub, If you find yourself trying to import from local
directory, i.e. ``git clone``, and finding that you can’t import it, you
will need to edit your your ``kernel.json`` file like so:

.. code:: bash

   vi /home/jovyan/.local/share/jupyter/kernels/<condaenvironmentname>/kernel.json 

add in the ``$PATH`` and ``$PYTHONPATH`` bits:

.. code:: bash

   {
    "argv": [
     "/home/jovyan/my-conda-envs/<condaenvironmentname>/bin/python",
     "-m",
     "ipykernel_launcher",
     "-f",
     "{connection_file}"
    ],
    "env": {
        "PATH": "/home/jovyan/scripts/kttools:$PATH",
        "PYTHONPATH": "/home/jovyan/scripts/kttools:$PYTHONPATH"
    },
    "display_name": "Python (<condaenvironmentname>)",
    "language": "python"
   }

.. |Docs| image:: https://readthedocs.org/projects/kttools/badge/?version=latest
   :target: https://kttools.readthedocs.io/en/latest/?badge=latest
.. |PyPI| image:: https://img.shields.io/pypi/v/kttools?logo=PyPI
   :target: https://pypi.org/project/kttools/
