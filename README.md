# *meik- also *meig-

Proto-Indo-European root meaning "to mix."

This is my dumping ground for various small scripts in all kind of languages, but mostly bash, python, php, and powershell plus config files. They are useful in Linux and macOS, but occasionally Windows.

I'll try to drop a comment on what they're for as I put them up.

My stuff will be GPL, but I may be editing other's work, so that would retain their appropriate licenses.

Don't trust my code here. I try, but I don't program for a living - I sysadmin for a living.

## pandora-station-artists.py

This parses the web page for a Pandora station (You can get this in most browsers by opening the station, select Show All, then ctl-s/cmd-s to Save Page As > Web Page, HTML Only). It prints to the console the Seeds for that Station (`> filename` to save it). You'll need the BeautifulSoup module aka "bs4" installed. Using a virtual env:

```
python3 -m venv venv
source ./venv/bin/activate
pip install bs4
./pandora-station-artists.py -s saved-station.html
```

This should run everything that can run a modern browser, but you'll have to searhc how to run Python if you don't know. I tested this on macOS, but nothing fancy is in the code.

## **syncthing2.spec**

an rpm spec file for building Syncthing 2 for Fedora 42+ as it comes up(until they make one to get in the official repo building system)

Assuming 2.0.6 is the previous version installed and in the spec file anbd updating tpo 2.0.7, this command will build and update the version previously installed:

```
ver=2.0.7 ; old=2.0.6 ; \
sed -i "s/$old/$ver/" ~/rpmbuild/SPECS/syncthing.spec ; \
wget -O ~/rpmbuild/SOURCES/syncthing-source-v$ver.tar.gz \
    https://github.com/syncthing/syncthing/releases/download/v$ver/syncthing-source-v$ver.tar.gz ; \
rpmbuild --bb ~/rpmbuild/SPECS/syncthing.spec ; sudo dnf update ~/rpmbuild/RPMS/x86_64/syncthing-$ver-*.rpm
```

If it's a first time, use ```dnf install ~/rpmbuild/RPMS/x86_64/syncthing-$ver-0KL.x86_64.rpm``` and install additional packages if desired
