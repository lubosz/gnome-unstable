=GNOME 3.12 Beta=

Since the GNOME 3.11.90 is beta and will not be packaged in Arch,
maybe not even completetly in gnome-unstable, I added the missing packages.

These packages were updated

http://artfiles.org/gnome.org/core/3.11/3.11.90/NEWS
http://artfiles.org/gnome.org/apps/3.11/3.11.90/NEWS

=SOURCES=

==Unmodified from gnome-unstable==

atk           dconf            gnome-online-accounts      gtk3       libsoup
at-spi2-atk   glib2            gobject-introspection      json-glib
at-spi2-core  glib-networking  gsettings-desktop-schemas  libgdata   vala

==Unmodified from AUR==

* gnome-logs
* libmediaart

==Modified from AUR or added by myself==

* gnome-boxes
* gnome-software (not in AUR)
* gnome-sound-recorder

Following non GNOME packages were added as a dependency:

* packagekit 0.8.12

All other packages were taken from the extra repo and updated


