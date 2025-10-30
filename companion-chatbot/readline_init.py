# This file forces gnureadline to be imported before readline
# It's automatically loaded via PYTHONSTARTUP environment variable

import sys
import os

# Force gnureadline to be imported first
try:
    import gnureadline as readline
    sys.modules['readline'] = readline
    
    # Load .inputrc configuration
    inputrc_path = os.path.expanduser("~/.inputrc")
    if os.path.exists(inputrc_path):
        readline.read_init_file(inputrc_path)
except ImportError:
    # Fallback to standard readline if gnureadline not available
    import readline
    print("⚠ Warning: gnureadline not found, using system readline")
