*meik- also *meig-, Proto-Indo-European root meaning "to mix." 

This is my dumping ground for various small scripts in all kind of languages, but mostly bash, python, php, and powershell plus config files. They are useful in Linux and macOS, but occasionally Windows.

I'll try to drop a comment on what they're for as I put them up.

My stuff will be GPL, but I may be editing other's work, so that would retain their appropriate licenses.

Don't trust my code here. I try, but I don't program for a living - I sysadmin for a living.

####syncthing.spec
a rpm spec file for building Syncthing 2 for Fedora(until they make it fancy to get in the official repo building system)
- Assuming 2.0.6 is the previous version installed and in the spec file, this command will build and update the version previously installed:
```
ver=2.0.7 ; old=2.0.6 ; \
sed -i "s/$old/$ver/" ~/rpmbuild/SPECS/syncthing.spec ; \
wget -O ~/rpmbuild/SOURCES/syncthing-source-v$ver.tar.gz \
    https://github.com/syncthing/syncthing/releases/download/v$ver/syncthing-source-v$ver.tar.gz ; \
rpmbuild --bb ~/rpmbuild/SPECS/syncthing.spec ; sudo dnf update ~/rpmbuild/RPMS/x86_64/syncthing-$ver-*.rpm
```
