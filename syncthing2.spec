%global basever 2.0.7
%global goipath github.com/syncthing/syncthing
%global tag     v%{basever}%{?rcnum:-rc.%{rcnum}}

Name:           syncthing
Version:        %{basever}
Release:        0KL
Summary:        Continuous File Synchronisation

License:        MPL-2.0
URL:            https://syncthing.net/
Source:         https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-source-v%{version}.tar.gz
# signature can not be validated at the moment, see changelog entry from "Jan 16 11:32:55 UTC 2025" and https://github.com/syncthing/syncthing/issues/9902

BuildRequires:  desktop-file-utils
BuildRequires:  systemd-rpm-macros
BuildRequires:  sqlite-devel
Requires:       hicolor-icon-theme

Provides:       bundled(golang(github.com/syncthing/notify)) = c7027d4

%description
Syncthing replaces other file synchronization services with something
open, trustworthy and decentralized. Your data is your data alone and
you deserve to choose where it is stored, if it is shared with some
third party and how it's transmitted over the Internet. Using syncthing,
that control is returned to you.

This package contains the syncthing client binary and systemd services.

%package        tools
Summary:        Continuous File Synchronization (server tools)

%description    tools
Syncthing replaces other file synchronization services with something
open, trustworthy and decentralized. Your data is your data alone and
you deserve to choose where it is stored, if it is shared with some
third party and how it's transmitted over the Internet. Using syncthing,
that control is returned to you.

This package contains the main syncthing server tools:

* strelaysrv / strelaypoolsrv, the syncthing relay server for indirect
  file transfers between client nodes, and
* stdiscosrv, the syncthing discovery server for discovering nodes
  to connect to indirectly over the internet.

%prep
%autosetup -v -n %{name} -p1

%build
# cd "$PWD/%{name}-%{version}

# set build environment, in particular use "-mod=vendor" to use the Go modules from the source archive's vendor dir
export CGO_CPPFLAGS="${CPPFLAGS}" CGO_CFLAGS="${CFLAGS}" CGO_CXXFLAGS="${CXXFLAGS}" CGO_LDFLAGS="${LDFLAGS}"
#export GOFLAGS="-trimpath -mod=vendor"
export GOFLAGS="-trimpath"

# build and install syncthing without automatic updates
go run build.go -no-upgrade -version v%{version} -tags libsqlite3 install
# build and install strelaysrv without automatic updates
go run build.go -no-upgrade -version v%{version} -tags libsqlite3 install strelaysrv
# build and install strelaypoolsrv  without automatic updates
go run build.go -no-upgrade -version v%{version} -tags libsqlite3 install strelaypoolsrv
# build and install stdiscosrv without automatic updates
go run build.go -no-upgrade -version v%{version} -tags libsqlite3 install stdiscosrv
#popd

#%sysusers_generate_pre %{SOURCE3} %{name}-strelaysrv %{name}-strelaysrv-user.conf

%install
#cd "$PWD/../src/github.com/syncthing/"%{name}
#echo -n "HERE: $PWD"
export GO111MODULE=off

# install binaries
mkdir -p %{buildroot}/%{_bindir}

cp -pav bin/syncthing %{buildroot}/%{_bindir}/
cp -pav bin/stdiscosrv %{buildroot}/%{_bindir}/
cp -pav bin/strelaysrv %{buildroot}/%{_bindir}/
cp -pav bin/strelaypoolsrv %{buildroot}/%{_bindir}/

# install man pages
mkdir -p %{buildroot}/%{_mandir}/man1
mkdir -p %{buildroot}/%{_mandir}/man5
mkdir -p %{buildroot}/%{_mandir}/man7

cp -pav ./man/syncthing.1 %{buildroot}/%{_mandir}/man1/
cp -pav ./man/*.5 %{buildroot}/%{_mandir}/man5/
cp -pav ./man/*.7 %{buildroot}/%{_mandir}/man7/
cp -pav ./man/stdiscosrv.1 %{buildroot}/%{_mandir}/man1/
cp -pav ./man/strelaysrv.1 %{buildroot}/%{_mandir}/man1/

# install desktop files and icons
mkdir -p %{buildroot}/%{_datadir}/applications
cp -pav etc/linux-desktop/syncthing-start.desktop %{buildroot}/%{_datadir}/applications/
cp -pav etc/linux-desktop/syncthing-ui.desktop %{buildroot}/%{_datadir}/applications/

for size in 32 64 128 256 512; do
    mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
    cp -pav assets/logo-${size}.png %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps/syncthing.png
done
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/scalable/apps
cp -pav assets/logo-only.svg %{buildroot}/%{_datadir}/icons/hicolor/scalable/apps/syncthing.svg

# install systemd units
mkdir -p %{buildroot}/%{_unitdir}
mkdir -p %{buildroot}/%{_userunitdir}

cp -pav etc/linux-systemd/system/syncthing@.service %{buildroot}/%{_unitdir}/
cp -pav etc/linux-systemd/user/syncthing.service %{buildroot}/%{_userunitdir}/

# unmark source files as executable
for i in $(find -name "*.go" -type f -executable -print); do
    chmod a-x $i;
done
%pre

%post

%preun

%postun

%files
%license LICENSE
%doc AUTHORS CONDUCT.md CONTRIBUTING.md GOALS.md README.md

%{_bindir}/syncthing
%{_bindir}/stdiscosrv
%{_datadir}/applications/syncthing*.desktop
%{_datadir}/icons/hicolor/*/apps/syncthing.*
%{_mandir}/*/syncthing*
%{_unitdir}/syncthing@.service
%{_userunitdir}/syncthing.service

%files tools
%license LICENSE
%doc README.md AUTHORS

%{_bindir}/strelaysrv
%{_bindir}/strelaypoolsrv
%{_mandir}/*/stdiscosrv*
%{_mandir}/*/strelaysrv*

%changelog
* Fri Sep 05 2025 Kalak Lanar <kalaklanar@gmail.com>
- Update to 2.0.7
* Thu Sep 04 2025 Kalak Lanar <kalaklanar@gmail.com>
- Update to 2.0.5
* Wed Sep 03 2025 Kalak Lanar <kalaklanar@gmail.com>
- Update to 2.0.4
* Wed Sep 03 2025 Kalak Lanar <kalaklanar@gmail.com>
- Update to 2.0.4
* Fri Aug 22 2025 Marius Kittler <marius.kittler@suse.com>
- Update to 2.0.3
  * Fixes
    fix(cmd): restore --version flag for compatibility by @acolomb in #10269
    fix(cmd): make database migration more robust to write errors by @calmh in #10278
    fix(cmd): provide temporary GUI/API server during database migration by @calmh in #10279
    fix(db): clean files for dropped folders at startup by @calmh in #10280
  * Other
    chore(slog): re-enable LOGGER_DISCARD (fixes #10262) by @rasa in #10267
    build: downgrade gopsutil (fixes #10276) by @calmh in #10277
  * Note that 2.0.2 didn't bring anything relevant to GNU/Linux and
    was therefore skipped
* Thu Aug 14 2025 Marius Kittler <marius.kittler@suse.com>
- Update to 2.0.1
  * Fixes
    allow upgrade without config dir (fixes #10240) by @calmh in #10241
    fix various typos by @rasa in #10242
    correct incantation to launch browser in Linux desktop file by @calmh in #10246
    handle path names that include URL special chars (fixes #10245) by @calmh in #10247
    increase default delete retention to 15 months by @calmh in #10252
  * Other
    update (most) dependencies by @calmh in #10243
* Tue Aug 12 2025 Marius Kittler <marius.kittler@suse.com>
- Update to 2.0.0
  This is the first release of the new 2.0 series. Expect some rough edges
  and keep a sense of adventure! Major changes:
  * Database backend switched from LevelDB to SQLite. There is a migration on
    first launch which can be lengthy for larger setups. The new database is
    easier to understand and maintain and, hopefully, less buggy.
  * The logging format has changed to use structured log entries (a message
    plus several key-value pairs). Additionally, we can now control the log
    level per package, and a new log level WARNING has been inserted between
    INFO and ERROR (which was previously known as WARNING...). The INFO level
    has become more verbose, indicating the sync actions taken by Syncthing. A
    new command line flag --log-level sets the default log level for all
    packages, and the STTRACE environment variable and GUI has been updated
    to set log levels per package. The --verbose and --logflags command
    line options have been removed and will be ignored if given.
  * Deleted items are no longer kept forever in the database, instead they are
    forgotten after six months. If your use case require deletes to take
    effect after more than a six month delay, set the
  - -db-delete-retention-interval command line option or corresponding
    environment variable to zero, or a longer time interval of your choosing.
  * Modernised command line options parsing. Old single-dash long options are
    no longer supported, e.g. -home must be given as --home. Some options
    have been renamed, others have become subcommands. All serve options are
    now also accepted as environment variables. See syncthing --help and
    syncthing serve --help for details.
  * Rolling hash detection of shifted data is no longer supported as this
    effectively never helped. Instead, scanning and syncing is faster and more
    efficient without it.
  * A "default folder" is no longer created on first startup.
  * Multiple connections are now used by default between v2 devices. The new
    default value is to use three connections: one for index metadata and two
    for data exchange.
  * The handling of conflict resolution involving deleted files has changed. A
    delete can now be the winning outcome of conflict resolution, resulting in
    the deleted file being moved to a conflict copy.

