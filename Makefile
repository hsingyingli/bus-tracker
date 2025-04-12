migrate_up: 
	dbmate -u "postgres://test:testsecret@localhost:5432/bus?sslmode=disable" up

migrate_down: 
	dbmate -u "postgres://test:testsecret@localhost:5432/bus?sslmode=disable" rollback

new_migration:
	@read -p "Enter migration name: " name; \
		dbmate new $$name

