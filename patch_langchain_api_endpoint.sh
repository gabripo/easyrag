#!/bin/bash

# Usage: ./script.sh old_keyword new_keyword filename

# Check if exactly 3 arguments are provided
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 old_keyword new_keyword filename"
  exit 1
fi

# Assign arguments to variables
OLD_KEYWORD=$1
NEW_KEYWORD=$2
FILENAME=$3

# Check if the file exists
if [ ! -f "$FILENAME" ]; then
  echo "File not found!"
  exit 1
fi

# Escape the keywords to handle any special characters
ESCAPED_OLD_KEYWORD=$(printf '%s\n' "$OLD_KEYWORD" | sed 's/[]\/$*.^[]/\\&/g')
ESCAPED_NEW_KEYWORD=$(printf '%s\n' "$NEW_KEYWORD" | sed 's/[&/\]/\\&/g')

# Use sed to replace the old keyword with the new keyword
sed -i "s/$ESCAPED_OLD_KEYWORD/$ESCAPED_NEW_KEYWORD/g" "$FILENAME"

echo "Keyword '$OLD_KEYWORD' replaced with '$NEW_KEYWORD' in file '$FILENAME'."
