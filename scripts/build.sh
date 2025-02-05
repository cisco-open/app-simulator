#!/bin/bash

# Default values for parameters
PUSH=
REPO_DIR=$(dirname "$0")/..
#MacOSX M architecture: linux/arm64/v8
PLATFORM="linux/amd64"
IMAGE_PREFIX="app-simulator"
REPO_PREFIX="cisco-open"
VERSION=$("$REPO_DIR"/scripts/bumpversion.sh)

DOCKER_CMD="docker"

# Function to display help
show_help() {
	echo "Usage: $(basename "$0") [OPTIONS]"
	echo "Options:"
	echo "  --dry-run                Do not build or push images, just print the commands that would be run"
	echo "  --include=<list>         Specify in a comma separated list which components (services, databases, loaders, generators) to include in the build, default is all"
	echo "  --push                   Specify whether to push the built images"
	echo "  --platform=<platform>    Specify the build platform (default: linux/amd64), can be multiple platforms comma separated"
	echo "  --repoprefix=<prefix>    Specify the image prefix (default: app-simulator)"
	echo "  --help                   Display this help message"
}

# Parse command line options
for ARG in "$@"; do
	case $ARG in
	--dry-run)
		DOCKER_CMD="echo docker"
		shift
		;;
	--push)
		PUSH="--push"
		VERSION=$(./bumpversion.sh)
		shift
		;;
	--platform=*)
		PLATFORM="${ARG#*=}"
		shift
		;;
	--repoprefix=*)
		REPO_PREFIX="${ARG#*=}"
		shift
		;;
	--help)
		show_help
		exit 0
		;;
	--include=*)
		INCLUDE_LIST="${ARG#*=}"
		shift
		;;
	*)
		echo "Unknown option: $ARG"
		show_help
		exit 1
		;;
	esac
done

if [[ $INCLUDE_LIST == *"services"* ]] || [ -z "${INCLUDE_LIST}" ]; then
	for DIR in "${REPO_DIR}/src/services"/nodejs; do
		if [ -d "$DIR" ]; then
			IMAGE_TAG="${REPO_PREFIX}/${IMAGE_PREFIX}-services-$(basename "$DIR"):$VERSION"
			echo "Building $IMAGE_TAG..."
			echo "Running 'docker buildx build --platform $PLATFORM -t $IMAGE_TAG $DIR $PUSH'"
			${DOCKER_CMD} buildx build --platform "$PLATFORM" -t "$IMAGE_TAG" $PUSH "$DIR"
		fi
	done
fi

if [[ $INCLUDE_LIST == *"databases"* ]] || [ -z "${INCLUDE_LIST}" ]; then
	for DIR in "${REPO_DIR}/src/databases"/*; do
		if [ -d "$DIR" ]; then
			IMAGE_TAG="${REPO_PREFIX}/${IMAGE_PREFIX}-databases-$(basename "$DIR"):$VERSION"
			echo "Building $IMAGE_TAG..."
			echo "Running 'docker buildx build --platform $PLATFORM -t $IMAGE_TAG $DIR $PUSH'"
			${DOCKER_CMD} buildx build --platform "$PLATFORM" -t "$IMAGE_TAG" $PUSH "$DIR" $PUSH
		fi
	done
fi

if [[ $INCLUDE_LIST == *"loaders"* ]] || [ -z "${INCLUDE_LIST}" ]; then
	for DIR in "${REPO_DIR}/src/loaders"/*; do
		if [ -d "$DIR" ]; then
			IMAGE_TAG="${REPO_PREFIX}/${IMAGE_PREFIX}-loaders-$(basename "$DIR"):$VERSION"
			echo "Building $IMAGE_TAG..."
			echo "Running 'docker buildx build --platform $PLATFORM -t $IMAGE_TAG $DIR $PUSH'"
			${DOCKER_CMD} buildx build --platform "$PLATFORM" -t "$IMAGE_TAG" $PUSH "$DIR" $PUSH
		fi
	done
fi

if [[ $INCLUDE_LIST == *"generators"* ]] || [ -z "${INCLUDE_LIST}" ]; then
	for DIR in "${REPO_DIR}/scripts/generators"/*; do
		if [ -d "$DIR" ]; then
			IMAGE_TAG="${REPO_PREFIX}/${IMAGE_PREFIX}-generators-$(basename "$DIR"):$VERSION"
			echo "Building $IMAGE_TAG..."
			echo "Running 'docker buildx build --platform $PLATFORM -t $IMAGE_TAG $DIR $PUSH'"
			${DOCKER_CMD} buildx build --platform "$PLATFORM" -t "$IMAGE_TAG" $PUSH "$DIR" $PUSH
		fi
	done
fi
