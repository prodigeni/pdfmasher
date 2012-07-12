#!/usr/bin/make -f

all:
	dh_prep  
	dh_installdirs
	chmod +x src/run.py
	cp -R src/ $(CURDIR)/debian/pdfmasher/usr/share/pdfmasher
	cp $(CURDIR)/debian/pdfmasher.desktop $(CURDIR)/debian/pdfmasher/usr/share/applications
	ln -s /usr/share/pdfmasher/run.py $(CURDIR)/debian/pdfmasher/usr/bin/pdfmasher
