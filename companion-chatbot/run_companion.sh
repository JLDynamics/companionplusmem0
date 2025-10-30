#!/bin/bash
# Wrapper script to run companion chatbot with proper readline support

cd "$(dirname "$0")"

# Set PYTHONSTARTUP to load gnureadline before any other module
export PYTHONSTARTUP="$(pwd)/readline_init.py"

# Run the companion chatbot
python3 companion.py
