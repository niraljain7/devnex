# library-management

Steps to deploy - 
  - cd library-management
  - docker-compose up --build

Swagger will be accessible at - /swagger/

Admin will be accessible at - /admin/
admin credentials - username=admin, password=librarian

Docker compose will start django application, celery worker, and redis server.
A postman collection with all requests and samples is added to the repo.
An sqlite db with dummy data is also added to the repo.



