#!/usr/bin/env bash

mkdir -p ~/.chrome

# Download Chrome
curl --retry 3 -O https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.86/linux64/chrome-linux64.zip

# Extract and move it
unzip -o chrome-linux64.zip
rm -rf ~/.chrome/chrome
mv chrome-linux64 ~/.chrome/chrome

# Just to verify it worked
echo "✅ Chrome binary installed at:"
ls -la ~/.chrome/chrome/chrome
