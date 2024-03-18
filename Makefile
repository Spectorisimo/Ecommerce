DC = docker compose
EXEC = docker exec -it
DB_CONTAINER = ninja-postgres
LOGS = docker logs
APP_FILE = deploy/local/app.compose.yml
APP_CONTAINER = ninja-backend
MANAGE_PY = python manage.py
MONITORING_FILE = deploy/local/monitoring.compose.yml



.PHONY: postgres
postgres:
	${EXEC} ${DB_CONTAINER} psql

.PHONY: app
app:
	${DC} -f ${APP_FILE}  up --build -d
.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down



.PHONY: monitoring
monitoring:
	${DC} -f ${MONITORING_FILE} up --build -d

.PHONY: monitoring-logs
monitoring-logs:
	${DC} -f ${MONITORING_FILE} logs -f




.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} migrate

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} makemigrations

.PHONY: superuser
superuser:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} createsuperuser

.PHONY: collectstatic
collectstatic:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} collectstatic

.PHONY: run-test
run-test:
	${EXEC} ${APP_CONTAINER} pytest
