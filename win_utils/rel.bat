@echo off

REM https://thegrid.gtnexus.local/engineering/ant_copyconfig_shows_skipping_folder_is_absent
REM tradiant\release\wlconfig\wlserver10> ant clean setup
REM tradiant\release\> ant copyconfig

REM set relpath=C:\gtsrc\workspaces\kepler_july2013\tradiant_trunk\release
REM set relpath=C:\gtsrc\workspaces\kepler_july2013\tradiant_agile_14_3\release
REM set relpath=C:\gtsrc\workspaces\march_2014\tradiant_staging_14.3.0\release

REM set relpath=C:\code\gtnexus\quickdev\modules\main\tradiant\release

set relpath=C:\code\gtnexus\development\modules\main\tradiant\release


title GTNexus Tradiant Project - %relpath%

cd %relpath%
