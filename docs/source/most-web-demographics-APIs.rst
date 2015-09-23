========
API Docs
========

.. py:module:: demographics


REST API reference
==================

API Methods
-----------

Identifier
``````````

   .. http:method:: POST /demographics/identifier/new/

      Create new identifier.

      :parameter json data: identifier data:

         {
            'type': String or None,
            'domain': String or None,
            'identifier': String
         }

      :responseheader Content-Type: application/json
         :parameter boolean `success`: True if the identifier is successfully created. False otherwise
         :parameter str `message`: a feedback string that would be displayed to the user
         :parameter str `errors`: an error string that explains the raised problems
         :parameter json `data`: if success is True, it contains the created identifier data in json format

   .. http:method:: GET /demographics/identifier/get/

      Get the information of an identifier

      :parameter str query_string: the query string to search.

      :responseheader Content-Type: application/json
         :parameter boolean `success`: True if identifiers are successfully found. False otherwise
         :parameter str `message`: a feedback string that would be displayed to the user
         :parameter str `errors`: an error string that explains the raised problems
         :parameter json `data`: if success is True, it contains the found identifiers data in json format

   .. http:method:: POST /demographics/identifier/(identifier_id)/edit/

      Edit the information of an identifier identified by `identifier_id`

      :parameter json data: identifier data:

         {
            'id': String,
            'type': String or None,
            'domain': String or None,
            'identifier': String
         }

      :responseheader Content-Type: application/json
         :parameter boolean `success`: True if identifier is successfully edited. False otherwise
         :parameter str `message`: a feedback string that would be displayed to the user
         :parameter str `errors`: an error string that explains the raised problems
         :parameter json `data`: if success is True, it contains the edited identifier data in json format

City
````

   .. http:method:: POST /demographics/city/new/

      Create new city.

      :parameter json data: city data:

         {
            'name': String,
            'province': String or None,
            'state': String,
            'code': String or None
         }

      :responseheader Content-Type: application/json
         :parameter boolean `success`: True if the city is successfully created. False otherwise
         :parameter str `message`: a feedback string that would be displayed to the user
         :parameter str `errors`: an error string that explains the raised problems
         :parameter json `data`: if success is True, it contains the created city data in json format

   .. http:method:: GET /demographics/city/get/

      Get the information of a city

      :parameter str query_string: the query string to search.

      :responseheader Content-Type: application/json
         :parameter boolean `success`: True if cities are successfully found. False otherwise
         :parameter str `message`: a feedback string that would be displayed to the user
         :parameter str `errors`: an error string that explains the raised problems
         :parameter json `data`: if success is True, it contains the found cities data in json format

   .. http:method:: POST /demographics/city/(city_id)/edit/

      Edit the information of a city identified by `city_id`

      :parameter json data: city data:

         {
            'id': String,
            'name': String,
            'province': String or None,
            'state': String,
            'code': String or None
         }

      :responseheader Content-Type: application/json
         :parameter boolean `success`: True if city is successfully edited. False otherwise
         :parameter str `message`: a feedback string that would be displayed to the user
         :parameter str `errors`: an error string that explains the raised problems
         :parameter json `data`: if success is True, it contains the edited city data in json format

Patient module
``````````````

   .. http:method:: POST /demographics/patient/new/

      Create new patient.

      :parameter json data: patient data:

         {
            'account_number': String or None,
            'first_name': String,
            'last_name': String,
            'other_ids': Array of Int or None,
            'gender': 'M' | 'F',
            'birth_date': Date,
            'birth_place': Int,
            'address': String or None,
            'city': Int or None,
            'phone': String or None,
            'mobile': String or None,
            'email': String or None,
            'certified_email': String or None,
            'active': True | False
         }

      :responseheader Content-Type: application/json
         :parameter boolean `success`: True if the patient is successfully created. False otherwise
         :parameter str `message`: a feedback string that would be displayed to the user
         :parameter str `errors`: an error string that explains the raised problems
         :parameter json `data`: if success is True, it contains the created patient data in json format

    .. http:method:: GET /demographics/patient/get/

      Get the information of a patient querying an external PDQ supplier service using HL7 as protocol

      :parameter str query_string: the query string to search.

      :responseheader Content-Type: application/json
         :parameter boolean `success`: True if patients are successfully found. False otherwise
         :parameter str `message`: a feedback string that would be displayed to the user
         :parameter str `errors`: an error string that explains the raised problems
         :parameter json `data`: if success is True, it contains the found patients data in json format

   .. http:method:: GET /demographics/patient/filter/

      Get the information of a patient from the local database

      :parameter str query_string: the query string to search.

      :responseheader Content-Type: application/json
         :parameter boolean `success`: True if patients are successfully found. False otherwise
         :parameter str `message`: a feedback string that would be displayed to the user
         :parameter str `errors`: an error string that explains the raised problems
         :parameter json `data`: if success is True, it contains the found patients data in json format


   .. http:method:: POST /demographics/patient/(patient_id)/edit/

      Edit the information of a patient identified by `patient_id`

      :parameter json data: patient data:

         {
            'id': String,
            'account_number': String or None,
            'first_name': String,
            'last_name': String,
            'other_ids': Array of Int or None,
            'gender': 'M' | 'F',
            'birth_date': Date,
            'birth_place': Int,
            'address': String or None,
            'city': Int or None,
            'phone': String or None,
            'mobile': String or None,
            'email': String or None,
            'certified_email': String or None,
            'active': True | False
         }

      :responseheader Content-Type: application/json
         :parameter boolean `success`: True if patient is successfully edited. False otherwise
         :parameter str `message`: a feedback string that would be displayed to the user
         :parameter str `errors`: an error string that explains the raised problems
         :parameter json `data`: if success is True, it contains the edited patient data in json format

      
   .. http:method:: POST /demographics/patient/(patient_id)/deactivate/

      Deactivate a patient identified by `patient_id`

      :responseheader Content-Type: application/json
         :parameter boolean `success`: True if patient is successfully deactivated. False otherwise
         :parameter str `message`: a feedback string that would be displayed to the user
         :parameter str `errors`: an error string that explains the raised problems
         :parameter json `data`: if success is True, it contains the deactivated patient data in json format

      
   .. http:method:: POST /demographics/patient/(patient_id)/activate/

      Activate a patient identified by `patient_id`

      :responseheader Content-Type: application/json
         :parameter boolean `success`: True if patient is successfully activated. False otherwise
         :parameter str `message`: a feedback string that would be displayed to the user
         :parameter str `errors`: an error string that explains the raised problems
         :parameter json `data`: if success is True, it contains the activated patient data in json format
