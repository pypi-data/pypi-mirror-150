# PREFIX is environment variable, but if it is not set, then set default value
ifeq ($(PREFIX),)
    PREFIX := /usr/local
endif

install:
	install git-release.sh $(DESTDIR)$(PREFIX)/bin/git-release
.PHONY: install
