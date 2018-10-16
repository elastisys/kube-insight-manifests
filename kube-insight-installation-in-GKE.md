# kube-insight installation in Google Kubernetes Engine

kube-insight repository:  https://github.com/elastisys/kube-insight-manifests
## 1.Setup two clusters in GKE
According to the kube-insight recommendation, Creating two clusters: one named monitored(agent) and the other named insight(server)

Follow the official doc:  https://cloud.google.com/kubernetes-engine/docs/how-to/creating-a-cluster
### 1.1. Set zone and region
```
$ gcloud config set compute/zone europe-north1-a
Updated property [compute/zone].
$ gcloud config set compute/region europe-north1-a
Updated property [compute/region].
```
### 1.2. Create Two clusters
```
$ gcloud container clusters create monitored --zone europe-north1-a
$ gcloud container clusters create insight --zone europe-north1-a
```
### 1.3. List the cluster information
```
$ gcloud container clusters list
NAME       LOCATION         MASTER_VERSION  MASTER_IP      MACHINE_TYPE   NODE_VERSION  NUM_NODES  STATUS
insight    europe-north1-a  1.9.7-gke.6     35.228.164.55  n1-standard-1  1.9.7-gke.6   3          RUNNING
monitored  europe-north1-a  1.9.7-gke.6     35.228.38.59   n1-standard-1  1.9.7-gke.6   3          RUNNINGli_wu@cloudshell:~ (test1012-219213)$
```
### 1.4. Enable kubectl and get cluster-info with --cluster specified
Get the cluster info in config
```
$ kubectl config view
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: REDACTED
    server: https://35.228.164.55
  name: gke_test1012-219213_europe-north1-a_insight
- cluster:
    certificate-authority-data: REDACTED
    server: https://35.228.38.59
  name: gke_test1012-219213_europe-north1-a_monitored
```
The name in each cluster is the cluster name. Show the cluster info with --cluster specified
```
$ kubectl cluster-info --cluster gke_test1012-219213_europe-north1-a_insight
$ kubectl cluster-info --cluster gke_test1012-219213_europe-north1-a_monitored
```
## 2. Set up a virtual environment for manifestr
### 2.1  install pipenv
```
$ sudo pip install pipenv
```
### 2.2 setup manifestr
```
$ pipenv install --three
$ pipenv shell
```
## 3. Setup monitored cluster

### 3.1 Deploy metrics
cd to folder `/kube-insight-manifests/manifests/agents/metrics`
#### 3.1.1 Render j2 files
```
$ manifestr --values `pwd`/values.py --template-root-dir `pwd`/templates --output-dir `pwd`/output
overwrite /home/li_wu/kube-insight-manifests/manifests/agents/metrics/output (y/n)?y
```
#### 3.1.2 Create namespace metrics
```
$ kubectl create ns metrics --cluster gke_test1012-219213_europe-north1-a_monitored
namespace "metrics" created
```
#### 3.1.3. Set user with cluster-admin for deploy RBAC
```
$ kubectl create clusterrolebinding cluster-admin-binding   --clusterrole cluster-admin   --user $(gcloud config get-value account) --cluster gke_test1012-219213_europe-north1-a_monitored
```

Note: if this step is missing, you will get following error during step 3.1.4
```
Error from server (Forbidden): error when creating "output/node-exporter/node-exporter-rbac.yaml": clusterroles.rbac.authorization.k8s.io "node-exporter" is forbidden: attempt to grant extra privileges: [PolicyRule{Resources:["tokenreviews"], APIGroups:["authentication.k8s.io"], Verbs:["create"]} PolicyRule{Resources:["subjectaccessreviews"], APIGroups:["authorization.k8s.io"], Verbs:["create"]}] user=&{li.wu@elastisys.com  [system:authenticated] map[user-assertion.cloud.google.com:[AGKDXmrmxR4ldy6MKeKjP/yU11f3oYRk8PD+N0PgGAq22xLez1St1GzcuML16US1LpSUuGhBOnxyxwZsHp7SCQjDpznRqruCdKWr/VWWNPbAwug79cP3/aWm082ChAydsV4O9mpVKPNRdUeQGWHrVs1nNYADq9+a39CgHjH6lHF0hGtRHFdZ+21irqPHQYoc3/FkERUC2ax9wRdypoU/lgYoRVj9o4siTnwHcmU=]]} ownerrules=[PolicyRule{Resources:["selfsubjectaccessreviews" "selfsubjectrulesreviews"], APIGroups:["authorization.k8s.io"], Verbs:["create"]} PolicyRule{NonResourceURLs:["/api" "/api/*" "/apis" "/apis/*" "/healthz" "/swagger-2.0.0.pb-v1" "/swagger.json" "/swaggerapi" "/swaggerapi/*" "/version"], Verbs:["get"]}] ruleResolutionErrors=[]
```
#### 3.1.4 Deployment
```
$ kubectl apply -R -f output/ --cluster gke_test1012-219213_europe-north1-a_monitored
```

After deployment, below services are available
```
$ kubectl get svc --cluster gke_test1012-219213_europe-north1-a_monitored -n metrics
NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kube-state-metrics    ClusterIP   10.35.248.48    <none>        8080/TCP         23m
node-exporter         ClusterIP   None            <none>        9100/TCP         23m
prometheus            ClusterIP   10.35.251.102   <none>        9090/TCP         23m
prometheus-nodeport   NodePort    10.35.243.209   <none>        9090:30090/TCP   23m
```
### 3.2 Deploy logging
cd to folder `/kube-insight-manifests/manifests/agents/logging`
#### 3.2.1 Render j2 files
```
$ manifestr --values `pwd`/values.py --template-root-dir `pwd`/templates --output-dir `pwd`/output
```
#### 3.2.2.  Create namespace logging
```
$ kubectl create ns logging  --cluster gke_test1012-219213_europe-north1-a_monitored
```

#### 3.2.3. Deployment
```
$ kubectl apply -R -f output/ --cluster gke_test1012-219213_europe-north1-a_monitored

```
After deployment,  pods are:
```
$ kubectl get pods -n logging --cluster gke_test1012-219213_europe-north1-a_monitored
NAME               READY     STATUS    RESTARTS   AGE
fluent-bit-c48nq   1/1       Running   0          25s
fluent-bit-f8wlh   1/1       Running   0          25s
fluent-bit-xj99g   1/1       Running   0          25s
```
## 4. Setup insight cluster
### 4.1 Deploy metrics
cd to folder `/kube-insight-manifests/manifests/servers/metrics`
#### 4.1.1 Render j2
```
$ manifestr --values `pwd`/values.py --template-root-dir `pwd`/templates --output-dir `pwd`/output
```
#### 4.1.2. Create namespace metrics
```
$ kubectl create ns metrics --cluster gke_test1012-219213_europe-north1-a_insight
```
#### 4.1.3. Deployment
```
$ kubectl apply -R -f output/ --cluster gke_test1012-219213_europe-north1-a_insight
```
After deployment, services are:
```
$ kubectl get svc -n metrics --cluster gke_test1012-219213_europe-north1-a_insight
NAME                                       TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                               AGE
kube-insight-cassandra                     ClusterIP   10.19.248.71    <none>        9042/TCP,7000/TCP,7001/TCP,7199/TCP   22s
kube-insight-grafana                       ClusterIP   10.19.252.71    <none>        3000/TCP                              21s
kube-insight-grafana-nodeport              NodePort    10.19.250.219   <none>        3000:30300/TCP                        21s
kube-insight-kairosdb                      ClusterIP   10.19.243.230   <none>        8080/TCP                              21s
kube-insight-prometheus-kairosdb-adapter   ClusterIP   10.19.240.136   <none>        9201/TCP
```

### 4.2 Deploy logging
cd to folder `/kube-insight-manifests/manifests/servers/logging`
#### 4.2.1 Render j2
```
$ manifestr --values `pwd`/values.py --template-root-dir `pwd`/templates --output-dir `pwd`/output
```

#### 4.2.2 Create namespace
```
$ kubectl create ns logging --cluster gke_test1012-219213_europe-north1-a_insight
namespace "logging" created
```
#### 4.2.3. Deployment
```
$  kubectl apply -R -f output/ --cluster gke_test1012-219213_europe-north1-a_insight
```

## 5. Set firewall-rules to open ports
### 5.1 open port for  prometheus-nodeport
```
$ gcloud compute firewall-rules create monitored --allow tcp:30090
Creating firewall...⠧Created [https://www.googleapis.com/compute/v1/projects/test1012-219213/global/firewalls/monitored].
Creating firewall...done.
NAME       NETWORK  DIRECTION  PRIORITY  ALLOW      DENY  DISABLED
monitored  default  INGRESS    1000      tcp:30090        False
```
### 5.2 Open port for kube-insight-grafana-nodeport
```
$ gcloud compute firewall-rules create insight --allow tcp:30300
Creating firewall...⠧Created [https://www.googleapis.com/compute/v1/projects/test1012-219213/global/firewalls/insight].
Creating firewall...done.
NAME     NETWORK  DIRECTION  PRIORITY  ALLOW      DENY  DISABLED
insight  default  INGRESS    1000      tcp:30300        False
```

### 5.3 Check firewall-rules list
```
$ gcloud compute firewall-rules list
NAME                        NETWORK  DIRECTION  PRIORITY  ALLOW                         DENY  DISABLED
default-allow-icmp          default  INGRESS    65534     icmp                                False
default-allow-internal      default  INGRESS    65534     tcp:0-65535,udp:0-65535,icmp        False
default-allow-rdp           default  INGRESS    65534     tcp:3389                            False
default-allow-ssh           default  INGRESS    65534     tcp:22                              False
gke-insight-8ac4f2cc-all    default  INGRESS    1000      icmp,esp,ah,sctp,tcp,udp            False
gke-insight-8ac4f2cc-ssh    default  INGRESS    1000      tcp:22                              False
gke-insight-8ac4f2cc-vms    default  INGRESS    1000      icmp,tcp:1-65535,udp:1-65535        False
gke-monitored-09d5aa05-all  default  INGRESS    1000      sctp,tcp,udp,icmp,esp,ah            False
gke-monitored-09d5aa05-ssh  default  INGRESS    1000      tcp:22                              False
gke-monitored-09d5aa05-vms  default  INGRESS    1000      icmp,tcp:1-65535,udp:1-65535        False
insight                     default  INGRESS    1000      tcp:30300                           False
monitored                   default  INGRESS    1000      tcp:30090                           False
```

## 6. Verify prometheus and grafana dashboard
### 6.1 Get the node IP address of monitored cluster
```
$ kubectl get nodes -o wide  --cluster gke_test1012-219213_europe-north1-a_monitored
NAME                                       STATUS    ROLES     AGE       VERSION        EXTERNAL-IP      OS-IMAGE                             KERNEL-VERSION   CONTAINER-RUNTIME
gke-monitored-default-pool-e2adbe60-dtwq   Ready     <none>    1h        v1.9.7-gke.6   35.228.102.123   Container-Optimized OS from Google   4.4.111+         docker://17.3.2
gke-monitored-default-pool-e2adbe60-fsmb   Ready     <none>    1h        v1.9.7-gke.6   35.228.18.194    Container-Optimized OS from Google   4.4.111+         docker://17.3.2
gke-monitored-default-pool-e2adbe60-mpkn   Ready     <none>    1h        v1.9.7-gke.6   35.228.1.126     Container-Optimized OS from Google   4.4.111+         docker://17.3.2
```
### 6.2 Verification prometheus
Pick and external-ip and visit from browser directly, eg: http://35.228.102.123:30090/

### 6.3 Get the node IP address of insight cluster
```
$ kubectl get nodes -o wide  --cluster gke_test1012-219213_europe-north1-a_insight
NAME                                     STATUS    ROLES     AGE       VERSION        EXTERNAL-IP      OS-IMAGE                             KERNEL-VERSION   CONTAINER-RUNTIME
gke-insight-default-pool-21ca5d99-1rqd   Ready     <none>    1h        v1.9.7-gke.6   35.228.41.4      Container-Optimized OS from Google   4.4.111+         docker://17.3.2
gke-insight-default-pool-21ca5d99-2rfx   Ready     <none>    1h        v1.9.7-gke.6   35.228.142.189   Container-Optimized OS from Google   4.4.111+         docker://17.3.2
gke-insight-default-pool-21ca5d99-9mr2   Ready     <none>    1h        v1.9.7-gke.6   35.228.243.25    Container-Optimized OS from Google   4.4.111+         docker://17.3.2
```
### 6.4 Verification grafana
Pick and external-ip and visit from browser directly, eg: http://35.228.41.4:30300/
Username: admin
Password: [please check configuration](https://github.com/elastisys/kube-insight-manifests/blob/master/manifests/servers/metrics/values.py#L49)

