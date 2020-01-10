#!/bin/sh

SOURCES=$1
SPECFILE=$2
PKGRELEASE=$3
RPMVERSION=$4
SPECRELEASE=$5
BASERELEASE=$6
clogf="$SOURCES/changelog"
# hide [redhat] entries from changelog
HIDE_REDHAT=1;
# override LC_TIME to avoid date conflicts when building the srpm
LC_TIME=
STAMP=$(echo $MARKER | cut -f 1 -d '-' | sed -e "s/v//");
RPM_VERSION="$RPMVERSION-$PKGRELEASE";

echo >$clogf

lasttag=$(git describe --match="iproute-${RPMVERSION}-*" --abbrev=0)
echo "Gathering new log entries since $lasttag"
git format-patch --first-parent --no-renames -k --stdout ${lasttag}.. | awk '
BEGIN{TYPE="PATCHJUNK"; }
	# add an entry to changelog
	function changelog(subjectline, nameline, zstream)
	{
		subj = substr(subjectline, 10);
		gsub(/%/, "", subj)
		name = substr(nameline, 7);
		pos=match(name, /</);
		name=substr(name,1,pos-2);
		zbz=substr(ZBZ,13);
		meta = "";
		if (zstream == "no") {
			if (BZ != "") {
				meta = " [" BZ "]";
			}
		} else {
			if (zbz != "") {
				if (bz != "") {
					meta = " [" zbz " " bz "]";
				} else {
					meta = " [" zbz "]";
				}
			}
		}
		cve = substr(CVE, 6);
		if (cve != "") {
			if (meta != "") {
				meta = meta " {" cve "}";
			} else {
				meta = " {" cve "}";
			}
		}

		print "- " subj " (" name ")" meta >> CLOGF;
	}

	#special separator, close previous patch
	/^From / { if (TYPE=="PATCHJUNK") {
			COMMIT=substr($0, 6, 40);
			TYPE="HEADER";
			LASTHDR="NEW";
			next;
		} }

	#interesting header stuff
	/^From: / { if (TYPE=="HEADER") {
			namestr=$0;
			#check for mime encoding on the email headers
			#git uses utf-8 q encoding
			if ( $0 ~ /=\?utf-8\?q/ ) {
				#get rid of the meta utf-8 junk
				gsub(/=\?utf-8\?q\?/, "");
				gsub(/\?=/, "");

				#translate each char
				n=split($0, a, "=");
				namestr = sprintf("%s", a[1]);
				for (i = 2; i <= n; ++i) {
					utf = substr(a[i], 0, 2);
					c = strtonum("0x" utf);
					namestr = sprintf("%s%c%s", namestr, c, substr(a[i],3));
				}
			}
			NAMELINE=namestr; next;
		    }
	    }
	/^Date: / {if (TYPE=="HEADER") {DATELINE=$0; next; } }
	/^Subject: / { if (TYPE=="HEADER") {SUBJECTLINE=$0; LASTHDR="SUBJ"; next; } }
	# partially attempt to deal with RFC2822 continuation lines in headers
	/^\ / { if (TYPE=="HEADER") { if (LASTHDR=="SUBJ") { SUBJECTLINE=(SUBJECTLINE $0); } next; } }
	/^Bugzilla: / { if (TYPE=="META") {
		bz=substr($0,11);
		sub(/.*id=/, "", bz);
		if (BZ != "") { BZ = BZ " "; }
		BZ = BZ bz;
	} }
	/^Z-Bugzilla: / { if (TYPE=="META") {ZBZ=$0; } }
	/^CVE: / { if (TYPE=="META") {CVE=$0; } }

	#blank line triggers end of header and to begin processing
	/^$/ { 
	    if (TYPE=="META") {
		#create the dynamic changelog entry
		changelog(SUBJECTLINE, NAMELINE, ZSTREAM);
		#reset cve values because they do not always exist
		CVE="";
		BZ="";
		ZBZ="";
		TYPE="BODY";
	    }
	    if (TYPE=="HEADER") {
		TYPE="META"; next;
	    }
	}

	#in order to handle overlapping keywords, we keep track of each
	#section of the patchfile and only process keywords in the correct section
	/^---$/ {
		if (TYPE=="META") {
			# no meta data found, just use the subject line to fill
			# the changelog
			changelog(SUBJECTLINE, NAMELINE, ZSTREAM);
			#reset cve values because they do not always exist
			CVE="";
			BZ="";
			ZBZ="";
			TYPE="BODY";
		}
		if (TYPE=="BODY") {
			TYPE="PATCHSEP";
		}
	}
	/^diff --git/ { if (TYPE=="PATCHSEP") { TYPE="PATCH"; } }
	/^-- $/ { if (TYPE=="PATCH") { TYPE="PATCHJUNK"; } }

	#filter out stuff we do not care about
	{ if (TYPE == "PATCHSEP") { next; } }
	{ if (TYPE == "PATCHJUNK") { next; } }
	{ if (TYPE == "HEADER") { next; } }

' SOURCES=$SOURCES SPECFILE=$SPECFILE CLOGF=$clogf ZSTREAM=no

cat $clogf | grep -v "tagging $RPM_VERSION" > $clogf.stripped
cp $clogf.stripped $clogf

if [ "x$HIDE_REDHAT" == "x1" ]; then
	cat $clogf | grep -v -e "^- \[redhat\]" |
		sed -e 's!\[Fedora\]!!g' > $clogf.stripped
	cp $clogf.stripped $clogf
fi

LENGTH=$(wc -l $clogf | awk '{print $1}')

#the changelog was created in reverse order
#also remove the blank on top, if it exists
#left by the 'print version\n' logic above
cname="$(git var GIT_COMMITTER_IDENT |sed 's/>.*/>/')"
cdate="$(date +"%a %b %d %Y")"
cversion="[$RPM_VERSION]";
tac $clogf | sed "1{/^$/d; /^- /i\
* $cdate $cname $cversion
	}" > $clogf.rev

if [ "$LENGTH" = 0 ]; then
	rm -f $clogf.rev; touch $clogf.rev
fi

patchdefs="$SOURCES/patchdefs"
patchact="$SOURCES/patchact"
rm -f $patchdefs $patchact
i=0
for patch in $(ls $SOURCES/*.patch 2>/dev/null); do
	printf "%-20s%s\n" "Patch${i}:" $(basename $patch) >>$patchdefs
	echo "%patch${i} -p1" >>$patchact
	i="$[i + 1]"
done

test -n "$SPECFILE" &&
        sed -i -e "
	/%%CHANGELOG%%/r $clogf.rev
	/%%CHANGELOG%%/d
	/%%PATCHDEFS%%/r $patchdefs
	/%%PATCHDEFS%%/d
	/%%PATCHACT%%/r $patchact
	/%%PATCHACT%%/d
	s/%%RPMVERSION%%/$RPMVERSION/
	s/%%BASERELEASE%%/$BASERELEASE/
	s/%%SPECRELEASE%%/$SPECRELEASE/" $SPECFILE

rm -f $clogf{,.rev,.stripped};
rm -f $patchdefs $patchact
