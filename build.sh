#!/usr/bin/env bash

mkdir -p ~/.chrome

# Retry download up to 3 times
curl --retry 3 -O https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/linux64/chrome-linux64.zip

# Extract
unzip chrome-linux64.zip
mv chrome-linux64 ~/.chrome/chrome

# Expose for app
echo "GOOGLE_CHROME_BIN=$HOME/.chrome/chrome/chrome" >> $RENDER_ENV_FILE
