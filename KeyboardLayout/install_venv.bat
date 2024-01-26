@echo off
@echo 'Creation of Python Virtual Environment for Keyboard Layout'

python -m venv layout_venv

@echo Python Virtual Environments created successfully, next step: installing dependencies
@echo Next step: installing dependencies

call .\layout_venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r requirements.txt

@echo Python Virtual Environments succesfully installed and updated
@pause
call .\layout_venv\Scripts\deactivate.bat