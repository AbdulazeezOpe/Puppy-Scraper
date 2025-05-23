#!/usr/bin/env bash

mkdir -p ~/.chrome

# Download Chrome
curl -O https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/linux64/chrome-linux64.zip
unzip chrome-linux64.zip

# ✅ Move to Render's project root
mkdir -p $RENDER_PROJECT_ROOT/.chrome
mv chrome-linux64 $RENDER_PROJECT_ROOT/.chrome/chrome

# ✅ Expose path for later
echo "GOOGLE_CHROME_BIN=$RENDER_PROJECT_ROOT/.chrome/chrome/chrome" >> $RENDER_ENV_FILE
