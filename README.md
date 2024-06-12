# Menu Service
An API to understand where and what your employees like to eat.

## Installation
```bash
git clone https://github.com/sashabryl/menu-service.git
cd menu-service
cp .env.sample .env
```
Fill the .env file accordingly.
```bash
docker-compose build
docker-compose up
```

## Documentation
To see the documentation, visit /api/schema/swagger-ui/

## Tests
```bash
docker exec -it <id of the docker container with the app> pytest
```

## How it works
Before you can do anything, a superuser must be created:
```bash
docker exec -it <id of the docker container with the app> python manage.py createsuperuser
```
Then, login into that superuser at /api/users/auth/login. Now you can create employees at 
/api/users/employees/ and restaurants at /api/users/auth/restaurants/. The restaurants then can login and
 upload their menus at /api/menus/upload/ (one a day). The employees then see the menus at /api/menus/ and vote for their
favorites at /api/menus/<menu_id>/vote. Each employee may have only one favorite a day and once the choice is made it's for good.
An admin can also visit /api/menus/, and he will see such additional information as number of votes for each menu and its publication date, 
since admins can also see menus from the past like that: /api/menus?date=2015-03-21.
