@echo off

:start
cls

rem Install requirements
pip install -r requirements.txt
cls rem clear the screen existing output

rem start the python script
python image-upload-maker.py

rem remove new-image directory
del images\new-image\*  /f /q /s

rem remove original directory
del images\original\*  /f /q /s

rem remove sql directory
del images\sql\sqlQuery.sql /f /q /s

pause rem stay prompt