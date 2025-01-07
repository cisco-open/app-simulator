#!/bin/bash

# Function to display help
show_help() {
	echo "Usage: bumpversion.sh [OPTION]"
	echo "Modify or display the version string in the form of 'v{major}.{minor}.{patch}'."
	echo "Version information is managed using Git tags."
	echo
	echo "Options:"
	echo "  --patch   Increase the patch number by 1."
	echo "  --minor   Increase the minor number by 1 and reset patch to 0."
	echo "  --major   Increase the major number by 1, reset minor to 0, reset patch to 0."
	echo "  --push    Push the latest or newly created tag to the remote repository."
	echo "  --help    Display this help message."
	echo "  (no option) Display the current version."
}

# Function to get the latest version from Git tags
get_version() {
	# Get the latest tag matching the version pattern, fallback to v0.0.0
	git tag --list 'v[0-9]*.[0-9]*.[0-9]*' --sort=-v:refname | head -n 1 || echo "v0.0.0"
}

# Function to set a new Git tag with the updated version
set_version() {
	git tag "$1"
}

# Function to push a tag to the remote repository
push_version() {
	git push origin "$1"
}

# Parse command-line arguments
push_to_remote=false
operation=""

for arg in "$@"; do
	case "$arg" in
	--patch | --minor | --major)
		operation="$arg"
		;;
	--push)
		push_to_remote=true
		;;
	--help)
		show_help
		exit 0
		;;
	*)
		echo "Unknown option: $arg"
		show_help
		exit 1
		;;
	esac
done

# Get the current version
current_version=$(get_version)

# If --push is used without --patch, --minor, or --major
if $push_to_remote && [ -z "$operation" ]; then
	push_version "$current_version"
	echo "Pushed existing tag $current_version to the remote repository."
	exit 0
fi

# Extract major, minor, and patch numbers
version_pattern='^v([0-9]+)\.([0-9]+)\.([0-9]+)$'
if [[ $current_version =~ $version_pattern ]]; then
	major=${BASH_REMATCH[1]}
	minor=${BASH_REMATCH[2]}
	patch=${BASH_REMATCH[3]}
else
	echo "Invalid version format: $current_version"
	exit 1
fi

# Handle version increment based on the operation
case "$operation" in
--patch)
	((patch++))
	;;
--minor)
	((minor++))
	patch=0
	;;
--major)
	((major++))
	minor=0
	patch=0
	;;
"")
	# No operation provided, just display the current version
	echo "$current_version"
	exit 0
	;;
esac

# Construct the new version string
new_version="v${major}.${minor}.${patch}"

# Update the Git tag
set_version "$new_version"

# Push the tag if the --push flag is provided
if $push_to_remote; then
	push_version "$new_version"
	echo "Pushed tag $new_version to the remote repository."
else
	echo "Created tag $new_version locally. Use '--push' to push it to the remote repository."
fi

# Output the new version
echo "$new_version"
