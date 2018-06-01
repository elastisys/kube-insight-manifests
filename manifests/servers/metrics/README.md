# kube-insight metric services

This directory contains Kubernetes manifests for deploying the server-side
kube-insight components for handling metrics. These components include:

- [Cassandra](http://cassandra.apache.org/): metrics storage
- [KairosDB](https://kairosdb.github.io/): time-series database which writes
  data to Cassandra
- [prom-to-kairosdb](https://github.com/proofpoint/prom-to-kairosdb): a
  Prometheus [remote
  writer](https://prometheus.io/docs/prometheus/latest/storage/#remote-storage-integrations)
  to which the scraping Prometheus server deployed in the monitored cluster
  (agent-side) writes all scraped data. `prom-to-kairosdb` applies a few
  configurable filters on the received datapoints (to clean out irrelevant
  metrics) and then writes datapoints to KairosDB.
- [Grafana](https://grafana.com/): visualization of metrics.

The agent-side metric components are set up with separate manifests under
[../..agents/metrics](../..agents/metrics).


## Status
These manifests definitely need to undergo additional scrutiny. A few
improvements from the top of my head that are still missing:

- TODO: use a statefulset of configurable size for Cassandra
- TODO: use persistent volumes for Cassandra
- TODO: set up more filters in prometheus-kairosdb-adapter configmap to reduce
  the amount of metrics being written to KairosDB.
- TODO: configure time-to-live for KairosDB
- TODO: configure roll-ups for KairosDB



## Deploying
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
    kubectl apply -R -f output/


## Verifying
After deploying, you can visit the services at these locations (after running
`kubectl proxy -p 8001`):

- Grafana: 
    - http://localhost:8001/api/v1/namespaces/metrics/services/kube-insight-grafana:3000/proxy
    - a nodeport service (port `303000`) is also set up for Grafana. You can 
	  visit its web GUI at  http://<cluster-node>:30090/
	  
- KairosDB: http://localhost:8001/api/v1/namespaces/metrics/services/kube-insight-kairosdb:8080/proxy

In Grafana, create a KairosDB datasource for
`http://kube-insight-kairosdb:8080` to start experimenting. 
