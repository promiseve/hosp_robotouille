#!/bin/bash

# Path to your requirements file
REQUIREMENTS_FILE="requirements.txt"

# Loop through each line in the requirements file
while IFS= read -r package; do
  # Install the package with --no-binary option
  pip install --no-binary :all: $package
done < "$REQUIREMENTS_FILE"
