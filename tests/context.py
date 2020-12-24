"""Manipulates the sys.path variable so that the Tests and main.py can be run.
Inspired from the project organization described here:
https://docs.python-guide.org/writing/structure/#test-suite
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../jodeln')))

import jodeln