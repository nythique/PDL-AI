@echo off
:loop
python main.py
timeout /t 2 
goto loop