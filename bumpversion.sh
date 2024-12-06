#!/bin/bash

# File that stores the version string
VERSION_FILE=".version"

# Function to display help
show_help() {
    echo "Usage: bumpversion.sh [OPTION]"
    echo "Modify or display the version string in the form of 'v{major}.{minor}.{build}'."
    echo "Stores the version in the file '$VERSION_FILE', defaults to v0.0.0 if it does not exist"
    echo
    echo "Options:"
    echo "  --build   Increase the build number by 1."
    echo "  --minor   Increase the minor number by 1 and the build number by 1."
    echo "  --major   Increase the major number by 1, reset minor to 0, and increase build by 1."
    echo "  --help    Display this help message."
    echo "  (no option) Display the current version."
}

# Function to read the current version from the file
get_version() {
    if [ -f "$VERSION_FILE" ]; then
        cat "$VERSION_FILE"
    else
        echo "v0.0.0"  # Default version if the file does not exist
    fi
}

# Function to update the version in the file
set_version() {
    echo "$1" > "$VERSION_FILE"
}

# Get the current version
current_version=$(get_version)

# Extract major, minor, and build numbers
version_pattern='^v([0-9]+)\.([0-9]+)\.([0-9]+)$'
if [[ $current_version =~ $version_pattern ]]; then
    major=${BASH_REMATCH[1]}
    minor=${BASH_REMATCH[2]}
    build=${BASH_REMATCH[3]}
else
    echo "Invalid version format"
    exit 1
fi

# Handle command-line arguments
case "$1" in
    --build)
        ((build++))
        ;;
    --minor)
        ((minor++))
        ((build++))
        ;;
    --major)
        ((major++))
        minor=0
        ((build++))
        ;;
    --help)
        show_help
        exit 0
        ;;
    *)
        # No argument, just return the current version
        echo "$current_version"
        exit 0
        ;;
esac

# Construct the new version string
new_version="v${major}.${minor}.${build}"

# Update the version file
set_version "$new_version"

# Output the new version
echo "$new_version"