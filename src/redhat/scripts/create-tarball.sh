#!/bin/sh

GITID=$2
TARBALL=$1
DIR=$2

if [ -f ${TARBALL} ]; then
	TARID=`( xzcat -qq ${TARBALL} | git get-tar-commit-id ) 2>/dev/null`
	if [ "${GITID}" = "${TARID}" ]; then
		echo "`basename ${TARBALL}` unchanged..."
		exit 0
	fi
	rm -f ${TARBALL}
fi

echo "Creating `basename ${TARBALL}`..."
trap 'rm -vf ${TARBALL}' INT
cd ../ &&
  git archive --prefix=${DIR}/ --format=tar ${GITID} | xz --threads 0 > ${TARBALL}
