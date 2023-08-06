"""
Definition and functions for spawning deployment templates.

:author: Jonathan Decker
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from rich import print

from ironik.util.exceptions import IronikFatalError

logger = logging.getLogger("logger")


@dataclass
class RancherCredentials(yaml.YAMLObject):
    rancher_access_key: str
    rancher_secret_key: str
    yaml_tag = "!RancherCredentials"
    yaml_loader = yaml.SafeLoader


@dataclass
class OpenStackCredentials(yaml.YAMLObject):
    username: str
    password: str
    project_id: str
    yaml_tag = "!OpenStackCredentials"
    yaml_loader = yaml.SafeLoader


@dataclass
class RancherConfig(yaml.YAMLObject):
    rancher_api_base_url: str
    ssh_user: str
    new_cluster_admin_user_name: str
    new_cluster_admin_user_password: str = ""
    engine_install_url: str = "https://releases.rancher.com/install-docker/20.10.sh"
    yaml_tag = "!RancherConfig"
    yaml_loader = yaml.SafeLoader


@dataclass
class OpenStackConfig(yaml.YAMLObject):
    openstack_auth_url: str
    user_domain_name: str
    project_domain_name: str
    lb_provider: str
    default_flavor_name: str
    default_image_name: str
    remote_ip_prefix: str
    private_network_id: str
    region_name: str = "RegionOne"
    use_octavia: bool = True
    security_group_name: str = "ironik-k8s-node"
    volume_size: int = 10
    volume_type: str = "ssd"
    yaml_tag = "!OpenStackConfig"
    yaml_loader = yaml.SafeLoader


@dataclass
class NetworkConfig(yaml.YAMLObject):
    required_TCP_ports: list[int] = field(default_factory=list)
    required_UDP_ports: list[int] = field(default_factory=list)
    worker_port_range_min: int = 30000
    worker_port_range_max: int = 32767
    yaml_tag = "!NetworkConfig"
    yaml_loader = yaml.SafeLoader


@dataclass
class KubernetesConfig(yaml.YAMLObject):
    master_node_roles: str = "master, etcd, worker"
    worker_node_roles: str = "worker"
    version: str = "v1.22.9-rancher1-1"
    number_master_nodes: int = 1
    number_worker_nodes: int = 1
    yaml_tag = "!KubernetesConfig"
    yaml_loader = yaml.SafeLoader


@dataclass
class DeploymentOptions(yaml.YAMLObject):
    deploy_example_workload: bool = False
    example_workload_image: str = "rancher/hello-world"
    example_workload_name: str = "hello-world-example"
    deploy_nginx_workload: bool = False
    nginx_ingress_version: str = "4.1.0"
    nginx_ingress_repo: str = "https://kubernetes.github.io/ingress-nginx"
    nginx_ingress_app_name: str = "nginx-ingress-lb"
    install_cinder_driver: bool = False
    deploy_example_volume: bool = False
    cleanup_example_workload: bool = True
    cleanup_nginx_ingress: bool = True
    cleanup_example_volume: bool = True
    yaml_tag = "!DeploymentOptions"
    yaml_loader = yaml.SafeLoader


@dataclass
class DeployConfig(yaml.YAMLObject):
    rancher_credentials: RancherCredentials = RancherCredentials("", "")
    openstack_credentials: OpenStackCredentials = OpenStackCredentials("", "", "")
    rancher_config: RancherConfig = RancherConfig("", "", "", "")
    openstack_config: OpenStackConfig = OpenStackConfig("", "", "", "", "", "", "", "", "")
    network_config: NetworkConfig = NetworkConfig(
        [22, 80, 443, 2376, 2379, 2380, 6443, 8443, 8472, 9913, 10250, 10254], [8443, 8472]
    )
    kubernetes_config: KubernetesConfig = KubernetesConfig()
    deployment_options: DeploymentOptions = DeploymentOptions()
    yaml_tag = "!DeployConfig"
    yaml_loader = yaml.SafeLoader


def write_deploy_template(path: Path, overwrite: bool) -> None:
    """

    :param path:
    :param overwrite:
    :return:
    """
    logger.debug("Preparing to write deploy template.")

    exists = path.exists()
    if exists:
        if path.is_dir():
            logger.debug("Path is dir, adding 'ironik_template.yaml' as file name.")
            path = path / "ironik_template.yaml"

    exists = path.exists()
    if exists:
        logger.info(f"File {path} already exists.")
        print(f"File {path} already exists.")
        if overwrite:
            logger.info("Replacing existing file with template.")
            print("Replacing existing file with template.")
        else:
            logger.info("Overwrite is not enabled, cannot proceed, stopping.")
            print("Overwrite is not enabled, cannot proceed, stopping.")
            return

    template = DeployConfig()

    logger.debug(f"Opening {path}...")
    with open(path, "w+") as f:
        logger.debug("Attempting to dump template into file...")
        yaml.dump(template, f)
    logger.debug("Closed file.")

    logger.info(f"Template has been written to {path.absolute()}")
    print(f"Template has been written to {path.absolute()}")


def load_deploy_template(path: Path) -> DeployConfig:
    """

    :param path:
    :return:
    """

    exists = path.exists()
    if not exists:
        logger.info(f"Given path does not exist: {path.absolute()}")
        print(f"Given path does not exist: {path.absolute()}")
        raise IronikFatalError(f"Given path does not exist: {path.absolute()}")

    is_file = path.is_file()
    if not is_file:
        logger.info(f"Given path is not a file: {path.absolute()}")
        print(f"Given path is not a file: {path.absolute()}")
        raise IronikFatalError(f"Given path is not a file: {path.absolute()}")

    logger.debug(f"Attempting to open {path.absolute()}")
    with open(path, "r") as f:
        logger.debug(f"Attempting to parse file as yaml.")
        try:
            deploy_config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.info(f"Parsing of yaml file failed with error: {e}")
            print("Parsing of template failed with the following error:")
            print(e)
            raise IronikFatalError(f"Parsing of yaml file failed with error: {e}")
        if not type(deploy_config) == DeployConfig:
            logger.info("Could not parse yaml file as Deployment Configuration. Make sure to use the template.")
            print("Could not parse yaml file as Deployment Configuration. Make sure to use the template.")
            logger.debug(f"Type of loaded yaml should be DeployConfig but is {type(DeployConfig)}")
            raise IronikFatalError(
                "Could not parse yaml file as Deployment Configuration. Make sure to use the " "template."
            )

    # TODO: Instead of printing this should validate the config by checking if all attrs are not None and len > 0
    print("Loaded template.")
    # print(deploy_config)
    # TODO: Validate that their is at least one master and one etcd and one worker

    return deploy_config


def validate_deploy_template():
    pass
