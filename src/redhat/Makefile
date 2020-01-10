include rules.mk
include rhpkg.mk

all: rh-rtg

rh-clean-sources:
	@rm -f $(RPM)/SPECS/*
	@for i in $(RPM)/SOURCES/*; do \
		rm -f $$i; \
	done

rh-release: rh-clean-sources
	@new_release.sh $(REDHAT)
	@$(MAKE) rh-release-finish

# make sure we don't export redhat directory
format-patches:
	git format-patch -N -o $(SOURCES)/ \
		refs/tags/iproute-$(IPROUTE_VERSION)-$(BASEBUILD)$(DIST) \
		$(filter-out $(TOPDIR)/redhat,$(wildcard $(TOPDIR)/*))
	# Fix up my mess in patch 50
	( cd $(SOURCES); \
	  p=0050-xfrm-revise-man-page-and-document-ip-xfrm-policy-set.patch; \
	  awk 'BEGIN{skip=false} /Bugzilla:/{skip=!skip} {if (!skip) print}' \
		$$p >$${p}.tmp; \
	  mv $${p}.tmp $${p}; \
	)

setup-source: rh-clean-sources format-patches
	@cp $(REDHAT)/$(SPECFILE).template $(SOURCES)/$(SPECFILE)
	@genspec.sh $(SOURCES) $(SOURCES)/$(SPECFILE) $(PKGRELEASE) $(RPMVERSION) $(SPECRELEASE) $(BASERELEASE)
	@cp $(SOURCES)/$(SPECFILE) $(SOURCES)/../SPECS/
	@cp $(REDHAT)/avpkt $(REDHAT)/cbq-0000.example $(REDHAT)/README $(SOURCES)/

$(TARBALL):
	@create-tarball.sh $(TARBALL) iproute-$(IPROUTE_VERSION)-$(PKGRELEASE)

sources-rh: $(TARBALL)
	@cp -l $(TARBALL) $(SOURCES)/ || cp $(TARBALL) $(SOURCES)/

rh-release-finish: setup-source
	@update_changelog.sh $(REDHAT) "$(IPROUTE_VERSION)-$(BUILD)$(DIST)"
	@git commit -s rules.mk $(SPECFILE).template -m "[redhat] iproute-$(IPROUTE_VERSION)-$(BUILD)$(DIST)"
	@$(MAKE) sources-rh

rh-release-tag:
	@git tag -a -m "iproute-$(IPROUTE_VERSION)-$(PKGRELEASE)" iproute-$(IPROUTE_VERSION)-$(PKGRELEASE)

rh-dist-git: $(REDHAT)/rpm/SOURCES/iproute.spec $(TARBALL)
ifeq ("$(RHDISTGIT_BRANCH)", "")
 $(error RHDISTGIT_BRANCH unset)
endif
	rh-dist-git.sh "$(RHDISTGIT_BRANCH)" "$(RHDISTGIT_CACHE)" "$(RHDISTGIT_TMP)" "$(RHDISTGIT)" "$(TARBALL)"

rh-rtg: rh-release
	@$(MAKE) rh-release-tag
	@$(MAKE) rh-dist-git
