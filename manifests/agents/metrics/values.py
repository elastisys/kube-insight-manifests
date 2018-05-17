values = {
    "namespace": "monitoring",
    "metricsServer": {
        "image": "gcr.io/google_containers/metrics-server-amd64",
        "version": "0.2.1",
        "pullPolicy": "IfNotPresent",
        "cpuRequestMilliCores": 40,
        "memRequestMB": 40,
        "cpuLimitMilliCores": 80,
        "memLimitMB": 200
    },
    "kubeStateMetrics": {
        "image": "quay.io/coreos/kube-state-metrics",
        "version": "1.3.1",
        "pullPolicy": "IfNotPresent",
        "cpuRequestMilliCores": 40,
        "memRequestMB": 40,
        "cpuLimitMilliCores": 100,
        "memLimitMB": 200
    },
    "nodeExporter": {
        "image": "quay.io/prometheus/node-exporter",
        "version": "0.15.2",
        "pullPolicy": "IfNotPresent",
        "cpuRequestMilliCores": 100,
        "memRequestMB": 30,
        "cpuLimitMilliCores": 200,
        "memLimitMB": 50
    }
}
