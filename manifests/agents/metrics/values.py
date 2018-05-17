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
    }
}
