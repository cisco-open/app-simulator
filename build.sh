#!/bin/bash

# Default values for parameters
PUSH=
#MacOSX M architecture: linux/arm64/v8
PLATFORM="linux/amd64"
IMAGE_PREFIX="app-simulator"
VERSION=$(./bumpversion.sh)

# Function to display help
show_help() {
    echo "Usage: $(basename "$0") [OPTIONS]"
    echo "Options:"
    echo "  --push                   Specify whether to push the built images"
    echo "  --platform=<platform>    Specify the build platform (default: linux/amd64), can be multiple platforms comma separated"
    echo "  --repoprefix=<prefix>    Specify the image prefix (default: app-simulator)"
    echo "  --help                   Display this help message"
}

# Parse command line options
for ARG in "$@"; do
    case $ARG in
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
            IMAGE_PREFIX="${ARG#*=}"
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $ARG"
            show_help
            exit 1
            ;;
    esac
done

for DIR in services/*;
do
  if [ -d $DIR ] ; then
    IMAGE_TAG="${IMAGE_PREFIX}/services-$(basename "$DIR"):$VERSION"
    echo "Building $IMAGE_TAG..."
    echo "Running 'docker buildx build --platform $PLATFORM -t $IMAGE_TAG $DIR $PUSH'"
    docker buildx build --platform $PLATFORM -t $IMAGE_TAG $PUSH $DIR 
  fi
done;

for DIR in loaders/*;
do
  if [ -d $DIR ] ; then
    IMAGE_TAG="${IMAGE_PREFIX}/loaders-$(basename "$DIR"):$VERSION"
    echo "Building $IMAGE_TAG..."
    echo "Building $IMAGE_TAG..."
    echo "Running 'docker buildx build --platform $PLATFORM -t $IMAGE_TAG $DIR $PUSH'"
    docker buildx build --platform $PLATFORM -t $IMAGE_TAG $PUSH $DIR $PUSH
  fi
done;

