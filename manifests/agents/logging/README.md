# fluentbit daemonset

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

The manifests are written as templates with some configurable placeholders,
whose values are substituded for the values in [values.py](values.py) when
the [manifestr](../../../manifestr) manifest rendering script is run. The
rendered manifests can then be applied with `kubectl`.

First, [set up manifestr](../../../manifestr/README.md) and then run:

    # edit values.py
    ${EDITOR} values.py
    # render k8s manifests
    manifestr --values `pwd`/values.py --template-root-dir `pwd`/templates --output-dir `pwd`/output

	# create namespace (if it doesn't already exist)
	kubectl create ns logging
    # apply manifests
    kubectl apply -f output/
