#!/bin/bash

# clones and updates a dist-git repo
# $1: branch to be used
# $2: local pristine clone of dist-git
# $3: alternate tmp directory (if you have faster storage)
# $4: alternate dist-git server
# $5: iproute source tarball

rhdistgit_branch=$1;
rhdistgit_cache=$2;
rhdistgit_tmp=$3;
rhdistgit_server=$4;
rhdistgit_tarball=$5;

redhat=$(dirname $0)/..;
topdir=$redhat/..;

function die
{
	echo "Error: $1" >&2;
	exit 1;
}

if [ -z "$rhdistgit_branch" ]; then
	echo "$0 <branch> [local clone] [alternate tmp] [alternate dist-git server]" >&2;
	exit 1;
fi

echo "Cloning the repository"
# clone the dist-git, considering cache
tmpdir=$(clone_tree.sh "$rhdistgit_server" "$rhdistgit_cache" "$rhdistgit_tmp")

echo "Switching the branch"
# change in the correct branch
cd $tmpdir/iproute
rhpkg switch-branch $rhdistgit_branch || die "switching to branch $rhdistgit_branch";

echo "Copying updated files"
(
	cd "$tmpdir"/iproute
	for file in avpkt cbq-0000.example iproute.spec README; do
		cp "$topdir"/redhat/rpm/SOURCES/$file .
		git add $file
	done
	cp "$topdir"/redhat/rpm/SOURCES/*.patch .
	git add *.patch
)

# compare tarball with name and md5sum in sources file
tarball_changed() { # (tarball, sources)
	local sum=$(md5sum $1)
	sum=${sum%% *}		# cut off filename
	grep -q "$sum ${1##*/}" $2
}

if ! tarball_changed $rhdistgit_tarball $tmpdir/iproute/sources; then
	echo "Tarball not new, so not uploading"
else
	echo "Uploading new tarballs"
	# upload tarballs
	sed -i "/iproute-3.*.el7.tar.xz/d" $tmpdir/iproute/sources;
	sed -i "/iproute-3.*.el7.tar.xz/d" $tmpdir/iproute/.gitignore;
	rhpkg upload $rhdistgit_tarball >/dev/null || die "uploading iproute tarball";
fi

echo "Creating diff for review ($tmpdir/diff) and changelog"
# diff the result (redhat/git/dontdiff). note: diff reuturns 1 if
# differences were found
diff -X $redhat/git/dontdiff -upr $tmpdir/iproute $redhat/rpm/SOURCES/ > $tmpdir/diff;
# creating the changelog file
create_distgit_changelog.sh $redhat/rpm/SOURCES/iproute.spec >$tmpdir/changelog

# all done
echo "$tmpdir"
