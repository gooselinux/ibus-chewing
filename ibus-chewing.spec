Name:       ibus-chewing
Version:    1.3.5.20100714
Release:    1%{?dist}
Summary:    The Chewing engine for IBus input platform
Summary(zh_TW): IBus新酷音輸入法
License:    GPLv2+
Group:      System Environment/Libraries
URL:        http://code.google.com/p/ibus/
Source0:    http://ibus.googlecode.com/files/%{name}-%{version}-Source.tar.gz

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gettext-devel
BuildRequires:  gtk2-devel
BuildRequires:  ibus-devel >= 1.1
BuildRequires:  cmake >= 2.4

# Make sure gob2 is patched against https://bugzilla.redhat.com/show_bug.cgi?id=519108
%if 0%{?fedora} == 11
BuildRequires:  gob2 >= 2.0.15-5
%else
BuildRequires:  gob2 >= 2.0.16-4
%endif
BuildRequires:  libchewing-devel >= 0.3.2-16
BuildRequires:  pkgconfig
BuildRequires:  GConf2-devel
BuildRequires:  libXtst-devel
Requires:   ibus >= 1.1
Requires:  libchewing >= 0.3.2-16
Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2

%description
IBus-chewing is an IBus front-end of Chewing, an intelligent Chinese input
method for Zhuyin (BoPoMoFo) users.
It supports various Zhuyin keyboard layout, such as standard (DaChen),
IBM, Gin-Yeah, Eten, Eten 26, Hsu, Dvorak, Dvorak-Hsu, and DaChen26.

Chewing also support toned Hanyu pinyin input.

%description -l zh_TW
IBus-chewing 是新酷音輸入法的IBus前端。
新酷音輸入法是個智慧型注音輸入法，支援多種鍵盤布局，諸如：
標準注音鍵盤、IBM、精業、倚天、倚天26鍵、許氏、Dvorak、Dvorak許氏
及大千26鍵。

本輸入法也同時支援帶調漢語拼音輸入。

%prep
%setup -q -n %{name}-%{version}-Source

%build
# $RPM_OPT_FLAGS should be  loaded from cmake macro.
%cmake -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo .
%__make VERBOSE=1  %{?_smp_mflags}

%install
%__rm -rf $RPM_BUILD_ROOT
%__make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}

%pre
if [ "$1" -gt 1 ] ; then
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
[ -r %{_sysconfdir}/gconf/schemas/%{name}.schemas ] &&
gconftool-2 --makefile-uninstall-rule \
%{_sysconfdir}/gconf/schemas/%{name}.schemas >/dev/null || :
# Upgrading 1.0.2.20090302-1.fc11 or older?
[ -r %{_sysconfdir}/gconf/schemas/%{name}.schema ] &&
gconftool-2 --makefile-uninstall-rule \
%{_sysconfdir}/gconf/schemas/%{name}.schema >/dev/null || :
fi

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
%{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :

%preun
if [ "$1" -eq 0 ] ; then
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-uninstall-rule \
%{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :
fi

%clean
%__rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS README ChangeLog NEWS COPYING
%{_libexecdir}/ibus-engine-chewing
%{_datadir}/%{name}
%{_datadir}/ibus/component/chewing.xml
%config(noreplace) %{_sysconfdir}/gconf/schemas/%{name}.schemas

%changelog
* Wed Jul 14 2010 Ding-Yi Chen <dchen at redhat.com> - 1.3.5.20100714-1
- Resolves: #608991
- Removes Ctrl-v/V Hotkey

* Wed Jul 07 2010 Ding-Yi Chen <dchen at redhat.com> - 1.3.5.20100706-1
- Fixed google issue 965:
  Candidate missing if both "Plain Zhuyin" and "Space As selection" are enabled.
- Revised Basic.macro
- Resolved: #608991

* Tue Jun 08 2010 Ding-Yi Chen <dchen at redhat.com> - 1.3.4.20100608-1
- ibus-chewing can now use mouse to click on mouse. Thus
  Fix Issue 951: Chewing does not support selection of candidates via mouseclick
  Thanks zork@chromium.org for the patch.

* Fri Jun 04 2010 Ding-Yi Chen <dchen at redhat.com> - 1.3.4.20100605-1
- Fix Issue 942: Fix unsunk references in ibus-chewing
  Applied the patch provided by zork@chromium.org.
- Rename CVS_DIST_TAGS to FEDORA_DIST_TAGS, and move its
  definition to cmake_modules/
- Gob2 generated file is now removed, because
  Bug 519108 is fixed from Fedora 11.

* Wed Apr 07 2010 Peng Huang <shawn.p.huang@gmail.com> - 1.2.99.20100317-2
- Rebuild with ibus-1.3.0

* Wed Mar 17 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.99.20100317-1
- Fix google 796: English input for dvorak
- Fix google 797: Zhuyin input for dvorak
- Fix google 807: ibus-chewing shows the over-the-spot panel
  even when not necessary

* Fri Feb 19 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.99.20100217-1
- Fixed the CMake description that leads summary incorrect.

* Tue Feb 16 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.99.20100216-1
- Fixed when typing English immediately after incomplete Chinese character.
- Add zh_TW summary.
- Revised description and write its zh_TW translation.

* Mon Feb 15 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.99.20100215-1
- "Macroize" rpm spec.
- Resolves: #565388

* Fri Feb 12 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.99.20100212-1
- Fixed Google issue 505.
- Google issue 755 is fixed in libchewing-0.3.2-22,
  See Chewing Google issue 10
- Fixed behavior of Del, Backspace,  Home, End
- Revert the change that fix Google issue 758.
- Change the default input style to "in candidate window",
  because not all application handle the on-the-spot mode well.
- Fixed Google issue 776

* Tue Feb 09 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20100210-1
- Revert the change that fix Google issue 758.
- Remove "tag" target, add "commit" which do commit and tag.

* Tue Feb 09 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20100209-1
- Fixed Google issue 754: commit string is missing when inputting
  long English text in the end.
- Fixed Google issue 758: Space is irresponsive in Temporary English mode
  if no Chinese in preedit buffer.
- Fixed Google Issue 763: [ibus-chewing] [qt] Shift-Up/Down does not mark
  text area properly.
- Change the String "on the spot" to "in application window",
  Chinese translation change to "在輸入處組詞"
- Change the "over the spot" to "in candidate window",
  Chinese translation remain the same
- Fixed bodhi submission.

* Mon Feb 08 2010 Adam Jackson <ajax@redhat.com> - 1.2.0.20100125-2
- Rebuild for new libibus.so.2 ABI.

* Mon Jan 25 2010 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20100125-1
- Add over-the-spot editing mode.
- Possible fixed of Google issue 505: ibus acts strange in Qt programs.
- Implemented Google issue 738:  Add a mode that allow editing in candidate window
  (thus over-the-spot mode).

* Fri Dec 11 2009 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20091211-1
- Fix Google issue 608: ibus-chewing does not show cursor in xim mode.
- Fix Google issue 611: ibus-chewing keyboard setting reverts to default unexpectlly.
- Fix Google issue 660: failed to build with binutils-gold.
- Remove make target commit.
- Add make target tag

* Fri Oct 09 2009 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20091002-1
- Bug 518901 - ibus-chewing would not work with locale zh_TW.Big
- Fix Google issue 501: ibus-chewing buffer doesn't get cleared when
toggling ibus on/off
- Fix Google issue 502: ibus-chewing: character selection window stays
behind when toggling ibus off- Use WM's revised ibus-chewing icon.
- Debug output now marked with levels.

* Wed Sep 30 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.2.0.20090917-2
- Rebuild with ibus-1.2.0

* Thu Sep 17 2009 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20090917-1
- Addressed Upstream (IBUS Google code) issue 484:
  + Find the source that why the / and . are not working.
- Pack the gob2 generation source to avoid the [Bug 519108]:
  [gob2] class and enum names convert incorrectly in mock / koji.

* Wed Sep 09 2009 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20090831-1
- IBusProperty and IBusPropList are free upon destruction.
- Fixed Red Hat Bugzilla [Bug 519328] [ibus-chewing] inconsistent between normal mode and plain Zhuyin mode.
- Addressed Upstream (IBUS Google code) issue 484:
  Arithmetic symbols (+-*/) on number pad does not input properly.

* Wed Aug 26 2009 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20090818-1
- Merged 1.2 and 1.1 source code.
- Addressed Upstream (IBUS Google code) issue 471.
- Remove libX11 dependency.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0.20090624-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Ding-Yi Chen <dchen at redhat.com> - 1.2.0.20090624-1
- Lookup table now shows the selection key.

* Mon Jun 22 2009 Peng Huang <shawn.p.huang@gmail.com> - 1.2.0.20090622-1
- Update to 1.2.0.20090622.

* Fri May 22 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.10.20090523-2
- Add back the export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`

* Fri May 22 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.10.20090523-1
- Applied Lubomir Rintel's patch

* Fri May 22 2009 - Ding-Yi Chen <dchen at redhat.com> - 1.0.10.20090522-1
- Now the 1st down key brings the longest possible phrases.
  The 2nd down key brings the 2nd longest possible phrases from the back,
  unlike the previous versions where the cursor stays in the head of longest phrase.
- Add force lowercase in English mode option.
- Fix double free issue when destroy ibus-chewing.
- Hide ibus-chewing-panel when ibus-chewing is focus-out

* Mon May 11 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.9.20090508-1
  Now commit is forced when switch of ibus-chewing or current application loses focus.
- New ibus-chewing.png is contribute by WM.
- input-keyboard.png is no longer needed and removed.
- ibus-engine-chewing -v option now need an integer as verbose level.
- ibus-chewing.schemas is now generated.
- Fix some CMake modules bugs.

* Tue Apr 28 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.8.20090428-1
Fix the errors which Funda Wang as pointing out:
- Move src/chewing.xml.in to data/
- Fixed some typo in next_version targets.
- Remove GConf2 package requirement, while add gconftool-2 requirement.

* Mon Mar 30 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.5.20090330-1
- Added tooltips.
- Revealed the sync caps lock setting.
- Fixed Right key bug.
- Added CMake policy 0011 as OLD.

* Mon Mar 23 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.4.20090323-2
- Fix koji build issues.

* Mon Mar 23 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.4.20090323-1
- Various Settings are now in dialog.
- Integer settings are now revealed.
- MakerDialog.gob is now available.
- Work around of easy symbol input.
- Fix iBus Google issue 310.

* Sun Mar 22 2009 Lubomir Rintel <lkundrak@v3.sk> - 1.0.3.20090311-2
- Properly reinstall the schema when updating from 1.0.2.20090303-1 or older

* Wed Mar 11 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.3.20090311-1
- IBus Google issue 305:  ibus-chewing.schema -> ibus-chewing.schemas
- IBus Google issue 307:  hardcoded chewing datadir
    - Sync chewing candPerPage and IBusTable->page_size
- Sync between IM and keyboard (Experimental)
    - ibus-chewing.schema -> ibus-chewing.schemas

* Tue Mar 03 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.2.20090303-1
- Required gconf2 -> GConf2.
- Fix RPM install issues.

* Fri Feb 27 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.1.20090227-1
- Setting shows/hides KBType, selKeys, and various settings.
- Add gconf schema.
- Fix some memory leaking checked.
- Move some function to cmake_modules.
- Fix Google code issue 281

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1.20081023-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.0.20090220-1
- First working version for IBus C

* Wed Jan 28 2009 Ding-Yi Chen <dchen at redhat.com> - 1.0.0.20090128-1
- Fix the binding with libchewing 0.3.2.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1.1.20081023-2
- Rebuild for Python 2.6

* Thu Oct 23 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080923-1
- Update to 0.1.1.20080923.

* Wed Sep 17 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080917-1
- Update to 0.1.1.20080917.

* Tue Sep 16 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080916-1
- Update to 0.1.1.20080916.

* Mon Sep 09 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20080901-1
- Update to 0.1.1.20080901.

* Fri Aug 15 2008 Huang Peng <shawn.p.huang@gmail.com> - 0.1.1.20081023-1
- The first version.







