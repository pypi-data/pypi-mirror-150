# pylint: disable=duplicate-code

""" R1Z2 Platform Definition """

from typing import List

from kubernetes import client

from mcli.models import MCLIPlatform
from mcli.serverside.job.mcli_k8s_job import MCLIVolume
from mcli.serverside.platforms.gpu_type import GPUType
from mcli.serverside.platforms.platform import GenericK8sPlatform, PlatformSetupError
from mcli.serverside.platforms.platform_instances import (LocalPlatformInstances, PlatformInstanceGPUConfiguration,
                                                          PlatformInstances)
from mcli.utils.utils_kube import kube_call_idem
from mcli.utils.utils_kube_labels import label

USER_WORKDISK_SERVER = '10.100.1.241'
USER_WORKDISK_PATH = '/mnt/tank0/r1z2'
USER_WORKDISK_STORAGE_CAPACITY = '10Gi'

a100_config = PlatformInstanceGPUConfiguration(
    gpu_type=GPUType.A100_40GB,
    gpu_nums=[1, 2, 4],
    gpu_selectors={label.mosaic.cloud.INSTANCE_SIZE: label.mosaic.instance_size_types.A100_40G_1},
    cpus=64,
    cpus_per_gpu=8,
    memory=512,
    memory_per_gpu=64,
    storage=1600,
    storage_per_gpu=200,
)
R1Z2_INSTANCES = LocalPlatformInstances(
    # Enable CPU Interactive
    available_instances={GPUType.NONE: [0]},
    gpu_configurations=[a100_config],
)


class R1Z2Platform(GenericK8sPlatform):
    """ R1Z2 Platform Overrides """

    allowed_instances: PlatformInstances = R1Z2_INSTANCES

    def __init__(self, mcli_platform: MCLIPlatform) -> None:
        super().__init__(mcli_platform)
        self.interactive = True

    @property
    def workdisk_name(self) -> str:
        return f'workdisk-{self.namespace}'

    def setup(self) -> bool:
        """See the docs for `create_user_volume`
        """
        return self.create_user_volume()

    def create_user_volume(self) -> bool:
        """Creates the user's PVC and PV for their personal workdisk

        Returns:
            True if PV and PVC were successfully created

        Raises:
            PlatformSetupError: Raised if pv or pvc creation failed
        """
        shared_metadata = client.V1ObjectMeta(name=self.workdisk_name)

        # Create PV
        pv_spec = client.V1PersistentVolumeSpec(
            capacity={'storage': USER_WORKDISK_STORAGE_CAPACITY},
            access_modes=['ReadWriteMany'],
            nfs={
                'path': USER_WORKDISK_PATH,
                'server': USER_WORKDISK_SERVER,
            },
        )
        volume = client.V1PersistentVolume(
            api_version='v1',
            kind='PersistentVolume',
            spec=pv_spec,
            metadata=shared_metadata,
        )

        # Create PVC
        pvc_spec = client.V1PersistentVolumeClaimSpec(
            access_modes=['ReadWriteMany'],
            resources={'requests': {
                'storage': USER_WORKDISK_STORAGE_CAPACITY
            }},
        )
        claim = client.V1PersistentVolumeClaim(
            api_version='v1',
            kind='PersistentVolumeClaim',
            spec=pvc_spec,
            metadata=shared_metadata,
        )

        # Deploy to Kubernetes
        with MCLIPlatform.use(self.mcli_platform):
            api = client.CoreV1Api()
            try:
                kube_call_idem(api.create_persistent_volume, body=volume)
                kube_call_idem(api.create_namespaced_persistent_volume_claim, namespace=self.namespace, body=claim)
            except client.ApiException as e:
                raise PlatformSetupError(e) from e

        return True

    def get_volumes(self) -> List[MCLIVolume]:
        """Get the volumes for the R1Z2 platform, including the user's workdisk volume
        """
        volumes = super().get_volumes()

        # Get workdisk mount
        volume = client.V1Volume(
            name='workdisk',
            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                claim_name=self.workdisk_name,
                read_only=False,
            ),
        )
        mount = client.V1VolumeMount(name='workdisk', mount_path='/workdisk')
        volumes.append(MCLIVolume(volume=volume, volume_mount=mount))

        return volumes
