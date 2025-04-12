postgres:
	docker run --name bus -p 5432:5432 -e POSTGRES_USER=test -e POSTGRES_PASSWORD=testsecret -e POSTGRES_DB=bus -d postgres:14-alpine 

migrate_up: 
	dbmate -u "postgres://test:testsecret@localhost:5432/bus?sslmode=disable" up

migrate_down: 
	dbmate -u "postgres://test:testsecret@localhost:5432/bus?sslmode=disable" rollback

new_migration:
	@read -p "Enter migration name: " name; \
		dbmate new $$name

