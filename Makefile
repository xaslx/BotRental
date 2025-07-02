DC = docker compose
STORAGES_FILE = docker_compose/storages.yaml
EXEC = docker exec -it
DB_CONTAINER = postgresdb
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
APP_CONTAINER = bot-rental
BROKER_FILE = docker_compose/broker.yaml
TELEGRAM_BOT_FILE = docker_compose/tg_bot.yaml
LOGS_MONITORING = docker_compose/logs_monitoring.yaml
TASKIQ_FILE = docker_compose/taskiq_worker.yaml


.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${BROKER_FILE} -f ${TASKIQ_FILE} -f ${LOGS_MONITORING} -f ${TELEGRAM_BOT_FILE} ${ENV} up --build -d


.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f


.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} -f ${BROKER_FILE} -f ${TASKIQ_FILE} -f ${LOGS_MONITORING} -f ${TELEGRAM_BOT_FILE} down


.PHONY: alembic-revision
alembic-revision:
	${EXEC} ${APP_CONTAINER} alembic revision --autogenerate


.PHONY: alembic-upgrade
alembic-upgrade:
	${EXEC} ${APP_CONTAINER} alembic upgrade head

.PHONY: alembic-generate
alembic-generate:
	${EXEC} ${APP_CONTAINER} alembic revision --autogenerate -m "initial"


.PHONY: run-test
run-test:
	${EXEC} ${APP_CONTAINER} env PYTHONPATH=/app pytest -s -v