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
    }
}
