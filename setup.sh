#!/bin/bash

# Set server as current directory
cd './server'

# Setup virtual env
DIR='./venv'
if [ -d "$DIR" ]; then
    rm -rf "$DIR"
fi

find . -type d -name __pycache__ -exec rm -r {} \+

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
. venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Create .env file
cp .env-example .env

echo "Start server?"
read answer

if [ answer='y' ]
then

    gunicorn --bind 0.0.0.0:5000 app:app

else

    # Deactivate virtual environment
    deactivate

    echo "Setup done. Happy Development! :)"

fi