@echo off
cd /d %~dp0\..
pdm run markurl %*
