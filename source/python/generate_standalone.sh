#!/bin/bash
pyinstaller --onefile --hidden-import=PIL --hidden-import=PIL._imagingtk --hidden-import=PIL._tkinter_finder main.py
