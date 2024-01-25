@echo off
set origin_path=%cd%
rem cd ..\

@echo 'Creation of Python Virtual Environment for Keyboard Layout'

python -m venv layout_venv

@echo Python Virtual Environments created successfully, next step: installing dependencies
@echo Next step: installing dependencies

call .\layout_venv\Scripts\activate.bat

python -m pip install --upgrade pip
rem cd %origin_path%
pip install -r requirements.txt

@echo Python Virtual Environments succesfully installed and updated
@pause