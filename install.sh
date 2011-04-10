#!/bin/bash
cnijfilter-ip2700series-3.30-1-i386-deb/install.sh

sudo apt-get -f install
sudo apt-get install m4 autoconf autotools-dev automake libtool

sudo libtool   --mode=install /usr/bin/install -c cnijusb '/usr/lib/cups/backend'
