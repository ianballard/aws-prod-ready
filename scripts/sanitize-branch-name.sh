#!/bin/sh
branch_name=$1

test -z branch_name && echo "branch name is required." 1>&2 && exit 1

# Convert the branch name to lowercase
branch_name="$(echo "$branch_name" | tr '[:upper:]' '[:lower:]')"

# Remove all characters leading up to and including a forward slash
branch_name="${branch_name#*/}"

# Remove all special characters
branch_name="$(echo "$branch_name" | tr -cd '[:alnum:]')"

# Limit the output to no more than 30 characters
branch_name="${branch_name:0:30}"

# Output the sanitized branch name
echo "$branch_name"
