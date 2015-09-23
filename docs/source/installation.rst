===============
Getting started
===============

Installation
~~~~~~~~~~~~

**Demographics** is a Django application, indipendent from any Django
project.

To use **Demographics** in your project, add it to ``INSTALLED_APPS`` in
your settings.py file.

.. code:: python

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # ...
        # your apps go here
        # ...
        'demographics',The following **HowTo** makes use of `requests` and `json` module.
    
    The sample blocks of code illustrate how to use them making use of the **[helper shown in this module](http://localhost:8888/notebooks/DemographicsHelper.ipynb)**
    )

If you want to connect to an external PDQ supplier to get the patients data, specify in the settings.py file of your project the parameters of the MLLP server.
For example:

.. code:: python

    MLLP_HOST = "localhost"
    MLLP_PORT = 2575
