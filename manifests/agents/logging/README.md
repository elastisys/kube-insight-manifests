# Fluentbit daemonset

This directory contains Kubernetes manifests for deploying a
[fluentbit](https://fluentbit.io/) daemonset into a Kubernetes cluster that
reads Kubernetes pod logs (via the [tail input
plugin](https://fluentbit.io/documentation/current/input/tail.html) and writes
metrics to an Elastisys [kube-insight-logserver](https://github.com/elastisys/kube-insight-logserver) via the [HTTP output
plugin](https://fluentbit.io/documentation/current/output/http.html))

For more details, refer to the [fluentbit
documentation](https://fluentbit.io/documentation/current/).

## Deploying

Note: you need to set up a
[kube-insight-logserver](https://github.com/elastisys/kube-insight-logserver)
somewhere to receive the logs collected by fluent-bit. For this, follow the
instructions in [../../servers/logging](../../servers/logging/README.md).

The module is installed as a helm chart and to configure the deployment for your
needs the values in [values.yaml](values.yaml) must be edited.

First, [set up helm](https://docs.helm.sh/using_helm/#quickstart-guide) and then run:

    # edit values.yaml
    ${EDITOR} values.yaml

    # create namespace (if it doesn't already exist)
    kubectl create ns logging
    # install chart
    helm install `pwd` --name kube-insight-log-agent
