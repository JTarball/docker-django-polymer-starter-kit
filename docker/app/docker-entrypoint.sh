#!/bin/bash
set -e

# Add app as command if needed
if [ "${1:0:1}" = '-' ]; then
	set -- app "$@"
fi

function checkLastCommand 
{
	if [ $? == 0 ]; then
		echo $(printf "%s ok" "$1")
	else
		echo $(printf "%s failed" "$1")
		exit 1
	fi
}  

if [ "$1" = 'app' ]; then
	# Change ownership
	#sudo chown -R app $APP_DIR
	#sudo chown -R app:app /usr/local/bin/gosu

	STRLOG="basic check of required environment variables ... "

	if [ -z "$APP_DIR" ]; then
		echo $(printf "%s failed" "$STRLOG")
		echo >&2 'error: you have not set required environment variables: APP_DIR'
		exit 1
	fi

	if [ -z "$SUPERUSER_NAME" -o -z "$SUPERUSER_EMAIL" -o -z "$SUPERUSER_PASSWORD" ]; then
		echo $(printf "%s failed" "$STRLOG")
		echo >&2 'error: you have not set required environment variables: SUPERUSER_NAME, SUPERUSER_EMAIL and SUPERUSER_PASSWORD'
		exit 1
	fi

	echo $(printf "%s ok" "$STRLOG")
	echo "$1"

	case "$1" in
		--create)
			# First Time - Create SuperUser, install polymer & make migrations
			echo "creating superuser $SUPERUSER_NAME"
			echo "from django.contrib.auth.models import User; User.objects.create_superuser('$SUPERUSER_NAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')" | python manage.py shell

			echo 'installing polymer components'
			cd $APP_DIR &&  which yes > /dev/null; if [ $? -eq 0 ]; then yes | npm install -g gulp bower && npm install && bower install; fi

			echo "make first-time migrations for apps: blog, accounts"
			python $APP_DIR/backend/manage.py makemigrations blog accounts
			;;
		# --dev)
		# 	ENV_FLAG="dev"
		# ;;
		# --dev)
		# 	ENV_FLAG="prod"
		# ;;
		# --interactive)
		# 	ENV_FLAG="interactive"
		# ;;
	esac

	# Future: add some basic checks that 'backend/' and 'manage.py' exist etc.
	python $APP_DIR/backend/manage.py migrate
	checkLastCommand "running migrate django ... "

	python $APP_DIR/backend/manage.py collectstatic --noinput
	checkLastCommand "collecting static files ... "

	if [ "$ENV_TYPE" = 'dev' ]; then
		cd $APP_DIR/backend
		python manage.py runserver_plus 0.0.0.0:8000 &
		checkLastCommand "running django development server ... "
		gulp serve
		checkLastCommand "running frontend polymer server ... "

	elif [ "$ENV_TYPE" = 'prod' ]; then
		echo "Running Production Django Server Script"
		python $APP_DIR/backend/bin/run.py &
		echo "Running FrontEnd Polymer"
		gulp

	else
		echo "Neither production or development environment selected - do Nothing"
	fi

	echo
	echo 'App init process done. Ready for start up.'
	echo

	#exec "$@"
fi

exec "$@"
