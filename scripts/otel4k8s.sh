#!/bin/bash
# This script assumes that you are using a k8s environment and have deployed an application simulation already.
#
# It has been tested with the following setup instructions for the cluster:
# minikube start --cpus 6 --memory 10g --network-plugin=cni --cni=false && cilium install && cilium status --wait
#
# With the simulation deployed into the k8s namespace "my-simulation", run it as follows:
#
# ./otel4k8s.sh "my-simulation"
#
# This will deploy cert manager, otel operater, a LGTM-stack in a single container and the instrumentation instructions
# for your applications. The last step will restart all pods that belong to the simulation.
#
# For a more detailed configuration run
#
# ./otel4k8s.sh --help
# 
# NOTE: Currently only java will be auto instrumented, other languages will be added soon

CERT_MANAGER_VERSION=1.16.3
O11Y_NAMESPACE=o11y
APP_NAMESPACE=""

WITH_CERT_MANAGER=1
WITH_OTEL_OPERATOR=1
WITH_LGTM_CONTAINER=1

KUBECTL="kubectl"

# Function to display help
show_help() {
	echo "Usage: otel4k8s.sh [OPTION]"
	echo "Deploy cert manager, OpenTelemetry operator, a LGTM-stack in a single container and automatic instrumentation for a running app simulation"
	echo
	echo "Options:"
	echo "  --patch   Increase the patch number by 1."
	echo "  (no option) Display the current version."
}

if [[ $# -eq 1 && ${1} != --* ]]; then
    APP_NAMESPACE=${1}
else

for ARG in "$@"; do
	case "$ARG" in
	--help)
		show_help
		exit 0
		;;
	--app-namespace=*)
		APP_NAMESPACE="${ARG#*=}"
		shift
		;;
  --o11y-namespace=*)
    O11Y_NAMESPACE="${ARG#*=}"
		shift
		;;
  --no-cert-manager)
    WITH_CERT_MANAGER=0
    shift
    ;;
  --no-lgtm)
    WITH_LGTM_CONTAINER=0
    shift
    ;;
  --no-otel-operator)
    WITH_OTEL_OPERATOR=0
    shift
    ;;
  --dry-run)
    KUBECTL="echo kubectl"
    shift
    ;;
  *)
		echo "Unknown option: $ARG"
		show_help
		exit 1
		;;
	esac
done

fi

# helper function that will rerun commands until they are successful
retry_until_success() {
    local delay=5         # Seconds to wait between retries
    local max_attempts=0   # 0 means unlimited retries
    local attempt=0

    while true; do
        "$@" && return 0   # Run the command; if it succeeds, return success
        
        attempt=$((attempt + 1))
        echo "Attempt $attempt failed. Retrying in $delay seconds..."

        if [[ $max_attempts -gt 0 && $attempt -ge $max_attempts ]]; then
            echo "Maximum retry attempts reached. Giving up."
            return 1
        fi

        sleep "$delay"
    done
}

# Install Cert Manager
if [[ ${WITH_CERT_MANAGER} -eq 1 ]]; then
  retry_until_success ${KUBECTL} apply -f "https://github.com/cert-manager/cert-manager/releases/download/v${CERT_MANAGER_VERSION}/cert-manager.yaml"
fi

# Install the OTel operator
if [[ ${WITH_OTEL_OPERATOR} -eq 1 ]]; then
  retry_until_success ${KUBECTL} apply -f https://github.com/open-telemetry/opentelemetry-operator/releases/latest/download/opentelemetry-operator.yaml
fi

# Install LGTM in one container
  if [[ ${WITH_LGTM_CONTAINER} -eq 1 ]]; then
  ${KUBECTL} create namespace ${O11Y_NAMESPACE}
  retry_until_success ${KUBECTL} apply -f https://raw.githubusercontent.com/grafana/docker-otel-lgtm/refs/heads/main/k8s/lgtm.yaml --namespace "${O11Y_NAMESPACE}"
fi

add_otel_instrumentation() {
  ${KUBECTL} apply --namespace "${APP_NAMESPACE}" -f - <<EOF
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata:
  name: my-instrumentation
spec:
  exporter:
    endpoint: http://lgtm.${O11Y_NAMESPACE}.svc.cluster.local:4317
  sampler:
    type: parentbased_traceidratio
    argument: "0.25"
EOF
}

retry_until_success add_otel_instrumentation

for deployment in $(kubectl get deployments -n "${APP_NAMESPACE}" -o jsonpath='{.items[*].metadata.name}'); do
    ${KUBECTL} patch deployment ${deployment} -n "${APP_NAMESPACE}" -p '{"spec": {"template":{"metadata":{"annotations":{"instrumentation.opentelemetry.io/inject-java":"true"}}}} }'
done

${KUBECTL} rollout restart deployment -n cue-example

${KUBECTL} port-forward service/lgtm 3000:3000 4317:4317 4318:4318 --namespace ${O11Y_NAMESPACE} &