values = {
    "namespace": "metrics",

    "cassandra": {
        "image": "cassandra",
        "version": "3.11",
        "pullPolicy": "IfNotPresent",
        "replicas": 1,
        "cpuRequestMilliCores": 100,
        "memRequestMB": 1024,
        "cpuLimitMilliCores": 200,
        "memLimitMB": 2048
    },

    "kairosdb": {
        "image": "elastisys/kairosdb",
        "version": "1.2.1",
        "pullPolicy": "IfNotPresent",
        "replicas": 1,
        "cpuRequestMilliCores": 100,
        "memRequestMB": 512,
        "cpuLimitMilliCores": 200,
        "memLimitMB": 1024,
        "cassandraWriteConsistencyLevel": "ONE",
        "cassandraReadConsistencyLevel": "ONE"
    },

    "prometheusKairosDBAdapter": {
        "TODO": "replace image with proofpoint/prom-to-kairosdb as soon as https://github.com/proofpoint/prom-to-kairosdb/issues/3 is resolved",
        "image": "elastisys/prom-to-kairosdb",
        "version": "latest",
        "pullPolicy": "IfNotPresent",
        "replicas": 1,
        "cpuRequestMilliCores": 100,
        "memRequestMB": 20,
        "cpuLimitMilliCores": 200,
        "memLimitMB": 80
    },

    "grafana": {
        "image": "grafana/grafana",
        "version": "5.1.3",
        "pullPolicy": "IfNotPresent",
        "replicas": 1,
        "cpuRequestMilliCores": 100,
        "memRequestMB": 100,
        "cpuLimitMilliCores": 200,
        "memLimitMB": 200,
        "adminPassword": "secret"
    }
}
