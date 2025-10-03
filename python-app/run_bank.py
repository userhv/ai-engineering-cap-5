#!/usr/bin/env python3
"""
Banking System - Main entry point
Run this script to start the banking application.
"""

import sys
import os

# Add the bank package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bank.main import main

if __name__ == "__main__":
    main()