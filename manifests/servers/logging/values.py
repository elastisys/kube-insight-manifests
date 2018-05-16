values = {
    "namespace": "logging",

    "image": "elastisys/kube-insight-logserver",
    "version": "1.0.0",
    "pullPolicy": "Always",
    "cpuRequestMilliCores": 5,
    "memRequestMB": 20,
    "cpuLimitMilliCores": 50,
    "memLimitMB": 60,

    "cassandraHosts": ["cassandra"],
    "cassandraKeyspace": "insight_logs",
    "cassandraReplicationStrategy": "SimpleStrategy",
    "cassandraReplicationFactors": "{\"cluster\":1}",
    "cassandraWriteConcurrency": 16,
    "logLevel": 3
}
