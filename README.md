# kube-insight-manifests

`kube-insight` is a Kubernetes observability stack, intended to integrate
several best-of-breed cluster monitoring products with the intent of creating
a comprehensive observability solution to help administrators track overall
cluster and micro-service health, and to better understand system dynamics.

`kube-insight` is intended to provide the following key functionalities:

- *topology-awareness*: determines a service dependency graph by detecting the
  communication flow between containers.
- *metrics collection*: collects container metrics for all deployed services.
- *log collection*: collects container logs for troubleshooting
- *event collection*: collects Kubernetes events to form a system change history
  to, for example, be able to determine what changes introduced a performance
  degradation.
- *visualization*: provides a single UI for visualizing the system state in a
  topology-centric manner, allowing drill-down to watch details (metrics, logs,
  events) pertaining to a certain deployment/pod/container.
- time-travel: by continusously saving state (topology, metrics, logs, events)
  in a backing Cassandra cluster, the system state is tracked over time to
  produce a system audit trail.

We believe that `kube-insight` can ease the life of Kubernetes cluster operators
by providing contextualized insight into the system. Todays microservice-based
architectures involve a lot of moving parts with complex inter-dependencies. The
service topology should simplify the task of root-cause-analysis, by quickly
allowing the operator to zoom in on the relevant services and then being able to
drill down to troubleshoot individual pods (metrics, logs).

The project is based on modern, cloud-native components, and adds some glue-code
where necessary to integrate third-party software. For more details, refer to
the [architecture](#architecture) section below.


## Project status
This project is very much a work in progress. Additional manifests will be added
as components are added to the stack.

For the time being there isn't a single isntaller script but the
[manifests](manifests) need to be deployed one-by-one. See the [deploy
section](#deploy) for additional details.


## Architecture
The `kube-insight` observability stack is "Kubernetes-native" in that it both
monitors a Kubernetes cluster and runs in a Kubernetes cluster. The monitored
cluster can, and probably, should be a different cluster from the one where
`kube-insight` is deployed (at least for production settings: the times when
your cluster is experiencing problems are the times when you *don't* want your
observabilit solution to fail -- so keep those error domains separate!).


TODO: architecture sketch


## Deploy
The [manifests](manifests) are separated into two categories: manifests intended
to be deployed onto the _monitored cluster_ ("agents") and manifests intended to
be deployed on the _insight cluster_ ("servers"). The server-side components
receive data sent by the agents and stores them in Cassandra.

- [agents](manifests/agents): intended to be deployed on the _monitored cluster_
  to collect data and send to receivers on the _insight cluster_.
- [servers](manifests/servers): intended to be deployed on the _insight cluster_
  to receive (and store) data sent from the agents on the _monitored cluster_.

Note that agents and servers _can_ be deployed onto the same cluster, but are
recommended to run on separate clusters (at least in production).

A single installer script is not available at this time. For more details and
for installation instructions, go to each [manifests](manifests) subfolder. 

A generic Jinja2 manifest renderer is available under [manifestr](manifestr)
("manifest renderer") and can be used when some degree of parameterization is
required in the Kubernetes manifests.
