# kube-insight-logserver

This directory contains Kubernetes manifests for deploying
[kube-insight-logserver](https://github.com/elastisys/kube-insight-logserver).

It is intended to be set up as a server that receives Kubernetes pod logs
collected by a fluentbit daemonset installed on the _monitored cluster_. The
fluentbit agents can be isntalled via [these manifests](../../agents/logging).


## Deploying
The manifests are written as templates with some configurable placeholders,
whose values are substituded for the values in [values.py](values.py) when
the [manifestr](../../../manifestr) manifest rendering script is run. The
rendered manifests can then be applied with `kubectl`.

First, [set up manifestr](../../../manifestr/README.md) and then run:

    # edit values.py
    ${EDITOR} values.py
    # render k8s manifests
    manifestr --values-dict values.py --template-root-dir templates/

    # create namespace (if it doesn't already exist)
    kubectl create ns <name>
    # apply manifests
    kubectl apply -f output/
