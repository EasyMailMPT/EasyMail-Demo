#### DELETE DOCKER CONTAINERS
dockerdelete:
	docker-compose down -v

#### BUILD PRODUCTION 
dockerprod:
	docker-compose -f docker-compose.prod.yml up -d --build

##### BUILD PRODUCTION WITH NEW DATABASE - !!!!!! CLEARING DATABASE
dockerprodfull:
	docker-compose -f docker-compose.prod.yml up -d --build
	docker-compose -f docker-compose.prod.yml exec web python manage.py create_db
	docker-compose -f docker-compose.prod.yml exec web python manage.py create_days
	docker-compose -f docker-compose.prod.yml exec web python manage.py create_admin

##### BUILD DOCKER WHEN CHANGE IN BACKEND
	
#### ADD ADMIN TO DATABASE
dockeradmin:
	docker-compose -f docker-compose.prod.yml exec web python manage.py create_admin

##### ADD DAYS TO DATABASE
dockerdays:
	docker-compose -f docker-compose.prod.yml exec web python manage.py create_days

###### BUILD DOCKER FOR DEVELOPMENT
dockerdev:
	docker-compose down -v
	docker-compose -f docker-compose.yml up -d --build
	docker-compose -f docker-compose.yml exec web python manage.py create_db
