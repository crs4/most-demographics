Examples
========

REST APIs
~~~~~~~~~

The following **HowTo** makes use of ``requests`` and ``json`` module.

The sample blocks of code illustrate how to use them making use of the
**`helper shown in this
module <http://localhost:8888/notebooks/DemographicsHelper.ipynb>`__**

Identifier module
^^^^^^^^^^^^^^^^^

Identifier module provides the following web API:

-  ``/demographics/identifier/new/``

-  ``/demographics/identifier/get/``

-  ``/demographics/identifier/edit/``

.. code:: python

    # -*- coding: utf-8 -*-
    from helper import *
    
    
    HOST_ADDRESS = 'http://127.0.0.1:8000'
    IDENTIFIER_DATA = {
        'type': 'business',
        'domain': 'hospital_1',
        'identifier': '0123456789'
    }
    
    
    identifier = compose_post_request(HOST_ADDRESS, '/demographics/identifier/new/', IDENTIFIER_DATA)
    print_response_data('identifier', identifier)
.. code:: python

    # -*- coding: utf-8 -*-
    from helper import *
    
    
    HOST_ADDRESS = 'http://127.0.0.1:8000'
    
    
    identifier = compose_get_request(HOST_ADDRESS, '/demographics/identifier/get/', '01234')
    print_response_data('identifier', identifier)
.. code:: python

    # -*- coding: utf-8 -*-
    from helper import *
    
    
    HOST_ADDRESS = 'http://127.0.0.1:8000'
    IDENTIFIER_DATA = {
        'type': 'business',
        'domain': 'hospital_X',
        'identifier': 'ZZZZZZZZZZ'
    }
    
    
    identifier = compose_get_request(HOST_ADDRESS, '/demographics/identifier/get/', '01234')
    print_response_data('identifier', identifier)
    identifier_id = identifier['data'][0]['id']
    edited_identifier = compose_post_request(HOST_ADDRESS, '/demographics/identifier/%s/edit/' % identifier_id, IDENTIFIER_DATA)
    print_response_data('identifier', edited_identifier)
    

City module
^^^^^^^^^^^

City module provides the following web API:

-  ``/demographics/city/new/``

-  ``/demographics/city/get/``

-  ``/demographics/city/edit/``

.. code:: python

    # -*- coding: utf-8 -*-
    from helper import *
    
    
    HOST_ADDRESS = 'http://127.0.0.1:8000'
    CITY_DATA = {
        'name': 'Milano',
        'province': 'MI',
        'state': 'Italia',
        'code': '20100'
    }
    
    
    city = compose_post_request(HOST_ADDRESS, '/demographics/city/new/', CITY_DATA)
    print_response_data('city', city)
.. code:: python

    # -*- coding: utf-8 -*-
    from helper import *
    
    
    HOST_ADDRESS = 'http://127.0.0.1:8000'
    
    city = compose_get_request(HOST_ADDRESS, '/demographics/city/get/', 'Mi')
    print_response_data('city', city)
.. code:: python

    # -*- coding: utf-8 -*-
    from helper import *
    
    
    HOST_ADDRESS = 'http://127.0.0.1:8000'
    CITY_DATA = {
        'name': 'Milano',
        'province': 'MI',
        'state': 'Italia',
        'code': '20128'
    }
    
    
    city = compose_get_request(HOST_ADDRESS, '/demographics/city/get/', 'Milano 20100')
    print_response_data('city', city)
    city_id = city['data'][0]['id']
    edited_city = compose_post_request(HOST_ADDRESS, '/demographics/city/%s/edit/' % city_id, CITY_DATA)
    print_response_data('city', edited_city)
    
    
Patient module
^^^^^^^^^^^^^^

Patient module provides the following web API:

-  ``/demographics/patient/new/``

-  ``/demographics/patient/get/``

-  ``/demographics/patient/edit/``

-  ``/demographics/patient/deactivate/``

-  ``/demographics/patient/activate/``

-  ``# /demographics/patient/add_id/``

-  ``# /demographics/patient/remove_id/``

-  ``# /demographics/patient/edit/``

-  ``# /demographics/patient/set_birth_place/``

-  ``# /demographics/patient/set_city/``

.. code:: python

    # -*- coding: utf-8 -*-
    from helper import *
    
    
    HOST_ADDRESS = 'http://127.0.0.1:8000'
    PATIENT_DATA = {
        'account_number': 'RSSMRA80H51B354M',
        'first_name': 'Maria',
        'last_name': 'Rossi',
        'other_ids': [1],
        'gender': 'F',
        'birth_date': '1980-06-11',
        'birth_place': 1,
        'address': 'Via Cagliari 4',
        'city': 4,
        'active': True
    }
    
    
    patient = compose_post_request(HOST_ADDRESS, '/demographics/patient/new/', PATIENT_DATA)
    print_response_data('patient', patient)
.. code:: python

    # -*- coding: utf-8 -*-
    from helper import *
    
    
    HOST_ADDRESS = 'http://127.0.0.1:8000'
    
    
    patient = compose_get_request(HOST_ADDRESS, '/demographics/patient/get/', 'RSS')
    print_response_data('patient', patient)
.. code:: python

    # -*- coding: utf-8 -*-
    from helper import *
    
    
    HOST_ADDRESS = 'http://127.0.0.1:8000'
    PATIENT_DATA = {
        'account_number': 'RSSMRA80H51B354M',
        'first_name': 'Marianna',
        'last_name': 'Rossi',
        'other_ids': [1],
        'gender': 'F',
        'birth_date': '1980-06-11',
        'birth_place': 1,
        'address': 'Via Cagliari 4',
        'city': 4,
        'active': True
    }
    
    
    patient = compose_get_request(HOST_ADDRESS, '/demographics/patient/get/', 'RSS')
    print_response_data('patient', patient)
    patient_id = patient['data'][0]['id']
    edited_patient = compose_post_request(HOST_ADDRESS, '/demographics/patient/%s/edit/' % patient_id, PATIENT_DATA)
    print_response_data('patient', edited_patient)

