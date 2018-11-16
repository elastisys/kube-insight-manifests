# kube-insight-logserver

This directory contains Kubernetes manifests for deploying
[kube-insight-logserver](https://github.com/elastisys/kube-insight-logserver).

It is intended to be set up as a server that receives Kubernetes pod logs
collected by a fluentbit daemonset installed on the _monitored cluster_. The
fluentbit agents can be installed via [these manifests](../../agents/logging).

## Deploying

The module is installed as a helm chart and to configure the deployment for your
needs the values in [values.yaml](values.yaml) must be edited.

First, [set up helm](https://docs.helm.sh/using_helm/#quickstart-guide) and then run:

    # edit values.yaml
    ${EDITOR} values.yaml

    # create namespace (if it doesn't already exist)
    kubectl create ns logging
    # install chart
    helm install `pwd` --name kube-insight-logging-server
