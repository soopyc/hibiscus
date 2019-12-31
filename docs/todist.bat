@echo off
echo Removing old asset directory
rm assets -vfr
echo Copying files...
cp build/* ./ -vr
echo Removing useless files...
rm host.bat
echo Done.
rem pause