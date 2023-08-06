from .node import KubernetesNode
from .namespace import KubernetesNamespace
from .deployment import KubernetesDeployment
from .replica_set import KubernetesReplicaSet
from .stateful_set import KubernetesStatefulSet
from .daemon_set import KubernetesDaemonSet
from .controller_revision import KubernetesControllerRevision
from .pod import KubernetesPod
from .horizontal_pod_autoscaler import KubernetesHorizontalPodAutoscaler

mandatory_collectors = {
    "nodes": KubernetesNode.collect,
    "namespaces": KubernetesNamespace.collect,
}

global_collectors = {
    "deployments": KubernetesDeployment.collect,
    "stateful_set": KubernetesStatefulSet.collect,
    "replica_set": KubernetesReplicaSet.collect,
    "controller_revision": KubernetesControllerRevision.collect,
    "daemon_set": KubernetesDaemonSet.collect,
    "pods": KubernetesPod.collect,
    "horizontal_pod_autoscaler": KubernetesHorizontalPodAutoscaler.collect,
}

all_collectors = dict(mandatory_collectors)
all_collectors.update(global_collectors)
