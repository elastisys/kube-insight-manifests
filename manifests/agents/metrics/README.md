# metric collection agents
This directory contains Kubernetes manifests for deploying metric collection
agents in a monitored cluster.

The key metric collection component is a Prometheus server, which is configured
to scrape metrics from several sources in the monitored cluster, some of which
are built-into Kubernetes (such as apiserver, kubelet/cadvisor metrics), some
which are provided via these [manifests](templates), and other
application-specific can be collected automatically for deployed applications
with the right scraping annotations (`prometheus.io/scrape: true`).

*NOTE: This Prometheus server is intended to be a "metric shipper", collecting
metrics and then passing them on to a remote metrics server in the "insight
cluster". It should NOT not relied upon for long-term storage, as it uses an
`emptyDir` pod-local data directory that is wiped whenever its pod is killed.
It should be considered a temporary metric store and nothing else.*

**TODO**: manifests for a [server-side metric receiver](../../servers/metrics) needs
to be set up and be configured as a [remote
write](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#%3Cremote_write%3E)
in Prometheus. This would allow the scraping prometheus server in the monitored
cluster to forward scraped data to remote server (in insight cluster), for
remote, long-term storage. Prometheus itself may not be the best solution in
this regard (see
[this](https://prometheus.io/docs/prometheus/latest/storage/#remote-storage-integrations).


The metric collection agents deployed via manifests in this repository include:

- [node-exporter](https://github.com/prometheus/node_exporter): a daemon set
  that collects machine-level metrics.
- [metrics-server](https://github.com/kubernetes-incubator/metrics-server):
  exposes cluster-wide Kubernetes resource usage metrics via the
  [metrics API](https://kubernetes.io/docs/tasks/debug-application-cluster/core-metrics-pipeline/). It
  can be thought of as a [replacement for
  Heapster](https://coreos.com/blog/autoscaling-with-prometheus-and-kubernetes-metrics-apis)
  and is needed to back the `kubectl top` command. You can, for example, play
  with the API via 

        kubectl get --raw https://kubernetes:443/apis/metrics.k8s.io/v1beta1/
- [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics):
  collects and publishes state metrics for various API objects (pods,
  deployments, etc) from the Kubernetes API.


Besides these sources, the Prometheus server is configured to also scrape these
targets:

- [kubelet metrics](https://godoc.org/k8s.io/kubernetes/pkg/kubelet/metrics):
  publishes stats about the operation of each nodes' kubelet.
- [cadvisor](https://github.com/google/cadvisor) metrics: publishes per-container
  metrics such as CPU/memory usage, disk I/O, and network I/O.
- apiserver metrics: publishes stats about the operation of each apiserver.
- scrape-enabled services: all endpoints backing a given service annotated with
  `prometheus.io/scrape` will have each of its ports scraped. The following
  annotations can be used to be more specific about how to scrape an endpoint:

    - `prometheus.io/path`: to use a metrics path different than `/metrics`.
    - `prometheus.io/port`: If the metrics are exposed on a different port to the
       service then set this appropriately.

- scrape-enabled pods: `prometheus.io/scrape`: applications running in the
  Kubernetes may choose to have their (application-specific) metrics scraped by
  Prometheus. As in the service case, this is enabled by the
  `prometheus.io/scrape` annotation (and the path and port annotations). The
  scrape endpoint needs to expose metrics in a [Prometheus-compatible
  format](https://prometheus.io/docs/instrumenting/writing_exporters/)).






## Deploy
The manifests are written as templates with some configurable placeholders,
whose values are substituded for the values in [values.py](values.py) when
the [manifestr](../../../manifestr) manifest rendering script is run. The
rendered manifests can then be applied with `kubectl`.

First, [set up manifestr](../../../manifestr/README.md) and then run:

    # edit values.py
    ${EDITOR} values.py
    # render k8s manifests
    manifestr

	# create namespace (if it doesn't already exist)
	kubectl create ns <name>
    # apply manifests
    kubectl apply -f output/


## Verify
A nodeport service (port `30090`) is set up for Prometheus. You can visit its
web GUI via:

    http://<cluster-node>:30090/
	
or by running `kubectl proxy -p 8001` followed by:

    http://localhost:8001/api/v1/namespaces/monitoring/services/prometheus:9090/proxy/targets
