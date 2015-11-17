#!/bin/bash

#
# Copy of config.sh from official library + custom tests
# Can't seem to get two config files working
# Will need to update this periodically

set -e

globalTests+=(
	gmt
	#django
)

testAlias+=(

)

imageTests+=(
	[jtarball/docker-generator-app-test:latest]='
		python-imports
		python-pip-requests-ssl
		python-sqlite3
	'
)

globalExcludeTests+=(
	# single-binary images
	[jtarball/docker-generator-app-test:latest_utc]=1
)
