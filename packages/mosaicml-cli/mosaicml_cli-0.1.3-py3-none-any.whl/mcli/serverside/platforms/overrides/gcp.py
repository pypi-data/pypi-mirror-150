# pylint: disable=duplicate-code

""" The GCP Platform """

from typing import Dict

from mcli.serverside.platforms.gpu_type import GPUType
from mcli.serverside.platforms.instance_type import InstanceType
from mcli.serverside.platforms.overrides.gcp_instances import GCP_ALLOWED_INSTANCES
from mcli.serverside.platforms.platform import GenericK8sPlatform
from mcli.serverside.platforms.platform_instances import PlatformInstances
from mcli.utils.utils_kube_labels import label


class GCPPlatform(GenericK8sPlatform):
    """ The GCP Platform """

    allowed_instances: PlatformInstances = GCP_ALLOWED_INSTANCES

    def get_annotations(self, instance_type: InstanceType) -> Dict[str, str]:
        annotations = super().get_annotations(instance_type)
        if instance_type.gpu_type in (GPUType.TPUv2, GPUType.TPUv3):
            annotations[label.gcp.TPU_ANNOTATION] = label.gcp.TF_VERSION
        return annotations
