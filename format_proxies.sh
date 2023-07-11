#!/bin/bash

echo "["

# Iterate over each line of the input and format it as a Python string
while IFS= read -r line; do
  # Remove lines containing the "=" character
  if ! echo "$line" | grep -q "="; then
    # Remove leading/trailing whitespace and parentheses
    formatted_line=$(echo "$line" | sed -e 's/^[[:space:]([:space:]]*//' -e 's/[[:space:]([:space:]]*$//')

    # Add quotes around the IP address and port
    formatted_line=$(echo "$formatted_line" | sed -E 's/([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:[0-9]+).*/"\1"'/)

    # Only output lines containing a number
    if echo "$formatted_line" | grep -q -E '[0-9]'; then
      # Print the formatted line
      echo "    $formatted_line,"
    fi
  fi

done

echo "]"
