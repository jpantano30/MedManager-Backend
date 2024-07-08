<!-- markdownlint-disable -->
# MedMangager API

#### Description 

The MedManager API is designed to facilitate medication management by allowing users to track their medications, including details such as dosage, frequency, and refill dates. This API is built using Django and Django REST Framework and supports user authentication.

#

###
<a href="https://medmanager.netlify.app/login"> MedMangager</a>

Heroku URl:
<a href="https://medmanager-b797ac84ca9c.herokuapp.com">Backend URL</a>

Frontend Repository:
<a href="https://github.com/jpantano30/MedManager">Frontend Repository</a>


#### Accessing the API

The API is hosted on Heroku:
<a href="https://medmanager-b797ac84ca9c.herokuapp.com">Backend URL</a>

To access the API, clients must first register and authenticate to receive a JWT (JSON Web Token). This token must be included in the header of subsequent requests to access protected endpoints.

**Base URL:** https://medmanager-b797ac84ca9c.herokuapp.com


#

#### Endpoints 

- User Management
  - Register a User
    - POST `/users/`
    - Body: `username`, `email`, `password`
    - Returns: User details excluding password
  - User Login (Obtain JWT)
    - POST `/token/`
    - Body: `username`, `password`
    - Returns: `access` and `refresh` tokens
  - Refresh Token
    - POST `/token/refresh/`
    - Body: `refresh`
    - Returns: New `access` token
  - User Profile
    - GET, PUT `/users/profile/`
    - Headers: `Authorization: Bearer <token>`
    - GET Returns: Current user details
    - PUT Body: User details to update
    - PUT Returns: Updated user details

- Medication Management
  - List All Medications
    - GET `/medications/`
    - Headers: `Authorization: Bearer <token>`
    - Returns: List of medications associated with the user
  - Add a Medication
    - POST `/medications/`
    - Headers: `Authorization: Bearer <token>`
    - Body: `name`, `dosage`, `frequency`, `start_date`, `end_date (optional)`, `refill_due_date (optional)`
    - Returns: Created medication details
  - Update a Medication
    - PUT `/medications/{id}/`
    - Headers: `Authorization: Bearer <token>`
    - Body: Medication details to update
    - Returns: Updated medication details
  - Delete a Medication
    - DELETE `/medications/{id}/`
    - Headers: `Authorization: Bearer <token>`
    - Returns: Status code `204 No Content`
- Medication Log
  - List Medication Logs
    - GET `/medication_logs/`
    - Headers: `Authorization: Bearer <token>`
    - Returns: List of medication logs for the user
  - Create a Medication Log
    - POST `/medication_logs/`
    - Headers: `Authorization: Bearer <token>`
    - Body: `medication_id`, `date` (auto-set to current date), `taken`
    - Returns: Created log details


#

#### Running the API Locally

1. Clone the repository.
2. Set up a virtual environment and install dependencies from `requirements.txt`.
3. Configure environment variables.
4. Run migrations using `python manage.py migrate`.
5. Start the server with `python manage.py runserver`.


#


#### Technologies Used 

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
