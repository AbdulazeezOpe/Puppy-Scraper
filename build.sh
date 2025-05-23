#!/usr/bin/env bash
# install chrome
mkdir -p ~/.chrome
wget https://storage.googleapis.com/chrome-for-testing-public/116.0.5845.188/linux64/chrome-linux64.zip
unzip chrome-linux64.zip
mv chrome-linux64 ~/.chrome/chrome

# expose binary location for Render
echo "GOOGLE_CHROME_BIN=$HOME/.chrome/chrome/chrome" >> $RENDER_ENV_FILE
