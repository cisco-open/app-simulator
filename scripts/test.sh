#!/bin/bash

REPO_DIR=$(dirname "$0")/..
IMAGE_PREFIX="app-simulator"
REPO_PREFIX="ghcr.io/cisco-open"
BUILD=0
VERSION=$("$REPO_DIR"/scripts/bumpversion.sh)

# Function to display help
show_help() {
	echo "Usage: $(basename "$0") [OPTIONS]"
	echo "Options:"
	echo "  --build                  Build the service images, test them and delete them"
	echo "  --help                   Display this help message"
}

# Parse command line options
for ARG in "$@"; do
    case $ARG in
    --build)
        BUILD=1
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

# Only build services for testing
if [ $BUILD -eq 1 ]; then
    REPO_PREFIX="app-simulator-test-${RANDOM}"
    "${REPO_DIR}/scripts/build.sh" --include=services --repoprefix="${REPO_PREFIX}" --platform=linux/arm64/v8
fi


for DIR in "${REPO_DIR}/src/services"/nodejs; do
    name=$(basename "${DIR}")
    container_name=app-sim-test-${name}; 
    docker run --name "${container_name}" -d --rm -t -i "${REPO_PREFIX}/${IMAGE_PREFIX}-services-${name}:${VERSION}"
    while [ "$SECONDS" -lt "$MAX_WAIT" ]; do
        status=$(docker inspect --format="{{.State.Health.Status}}" "${container_name}" 2>/dev/null)
        if [ "${status}" = "healthy" ]; then
            echo "Container is healthy"
            exit 0
        fi
        sleep 1
    done
done

if [ $BUILD -eq 1 ]; then
    # Delete all docker images with app-simulator-test prefix
    LIST=$(docker images | grep "${REPO_PREFIX}" | awk '{print $3}')
    docker rmi "${LIST}" -f
fi
