#!/usr/bin/env bash

mkdir -p ~/.chrome

# Download & extract Chrome
curl --retry 3 -O https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/linux64/chrome-linux64.zip
unzip -o chrome-linux64.zip  # overwrite if already exists
rm -rf ~/.chrome/chrome
mv chrome-linux64 ~/.chrome/chrome

# Write binary path to profile
echo 'export GOOGLE_CHROME_BIN=$HOME/.chrome/chrome/chrome' >> ~/.profile
