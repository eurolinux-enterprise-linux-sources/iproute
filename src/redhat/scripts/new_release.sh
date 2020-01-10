#!/bin/bash
if [ -z "$1" ]; then
	echo "$(basename $0) <redhat path>" >&2;
	exit 1;
fi

RHPATH="$1";

RELEASE=$(sed -n -e 's/^BUILD:=\(.*\)/\1/p' $RHPATH/rules.mk);
NEW_RELEASE="$[RELEASE + 1]";
sed -i -e "s/BUILD:=$RELEASE/BUILD:=$NEW_RELEASE/" $RHPATH/rules.mk
