#!/bin/bash

# Set server as current directory
cd './server'

# Setup virtual env
DIR='./venv'
if [ -d "$DIR" ]; then
    rm -rf "$DIR"
fi

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
. venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Create .env file
cp .env-example .env

# Deactivate virtual environment
deactivate

# Set client as current directory
cd '../client'

# Delete if node modules is present
DIR_NODE='./node_modules'
if [ -d "$DIR_NODE" ]; then
    rm -rf "$DIR_NODE"
fi

# Delete if node package.lock.json is present
FILE_PACKAGE_LOCK='./package-lock.json'
if [ -d "$FILE_PACKAGE_LOCK" ]; then
    rm -rf "$FILE_PACKAGE_LOCK"
fi

# Install all npm dependencies
npm i -y

echo "Setup done. Happy Development! :)"