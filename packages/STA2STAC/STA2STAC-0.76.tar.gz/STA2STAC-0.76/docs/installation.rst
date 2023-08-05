.. highlight:: shell

============
Installation
============


Stable release
--------------

To install STA2STAC, run this command in your terminal:

.. code-block:: console

    pip install sta2stac

This is the preferred method to install STA2STAC, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for STA2STAC can be downloaded from the `Gitlab repo`_.

You can either clone the public repository:

.. code-block:: console

    git clone git://codebase.helmholtz.cloud/CAT4KIT/sta2stac
    cd sta2stac
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements_dev.txt

Or download the `tarball`_:

.. code-block:: console

    curl -OJL https://codebase.helmholtz.cloud/CAT4KIT/sta2stac/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    python setup.py install


.. _Gitlab repo: https://codebase.helmholtz.cloud/CAT4KIT/sta2stac
.. _tarball: https://codebase.helmholtz.cloud/CAT4KIT/sta2stac/tarball/master
