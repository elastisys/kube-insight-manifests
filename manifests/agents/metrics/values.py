values = {
    "namespace": "metrics",
    "metricsServer": {
        "image": "gcr.io/google_containers/metrics-server-amd64",
        "version": "v0.2.1",
        "pullPolicy": "IfNotPresent",
        "cpuRequestMilliCores": 40,
        "memRequestMB": 40,
        "cpuLimitMilliCores": 80,
        "memLimitMB": 200
    },
    "kubeStateMetrics": {
        "image": "quay.io/coreos/kube-state-metrics",
        "version": "v1.3.1",
        "pullPolicy": "IfNotPresent",
        "cpuRequestMilliCores": 40,
        "memRequestMB": 40,
        "cpuLimitMilliCores": 100,
        "memLimitMB": 200
    },
    "nodeExporter": {
        "image": "quay.io/prometheus/node-exporter",
        "version": "v0.15.2",
        "pullPolicy": "IfNotPresent",
        "cpuRequestMilliCores": 100,
        "memRequestMB": 30,
        "cpuLimitMilliCores": 200,
        "memLimitMB": 50
    },
    "prometheus": {
        "image": "prom/prometheus",
        "version": "v2.1.0",
        "pullPolicy": "IfNotPresent",
        "cpuRequestMilliCores": 100,
        "memRequestMB": 600,
        "cpuLimitMilliCores": 200,
        "memLimitMB": 800,
        "scrapeInterval": "20s",
        "retention": "12h",
        "remoteWriteURL": "http://kube-insight-prometheus-kairosdb-adapter.metrics.svc.cluster.local:9201/write"
    }
}
