"""

:author: Jonathan Decker
"""

import logging
import os
import pathlib

import yaml

from ironik.config_file_handler.deploy_template import OpenStackConfig
from ironik.util import exceptions

logger = logging.getLogger("logger")

cloud_controller_manager_roles_manifest = "cloud-controller-manager-roles.yaml"

cloud_controller_manager_role_bindings_manifest = "cloud-controller-manager-role-bindings.yaml"

openstack_cloud_controller_manager_ds_manifest = "openstack-cloud-controller-manager-ds.yaml"

csi_plugin_manifest = "cinder-csi-plugin.yaml"

path_to_self = pathlib.Path(os.path.abspath(__file__))
path_to_manifests = path_to_self.parent.parent / "manifests"


def get_manifest_path(manifest: str) -> pathlib.Path:
    path = pathlib.Path(path_to_manifests / manifest)
    if path.is_file():
        return path
    else:
        raise exceptions.IronikPassingError(f"Could not find manifest {manifest} in {path}")


def get_openstack_controller_manager_manifest(openstack_config: OpenStackConfig) -> list[dict]:
    path = get_manifest_path(openstack_cloud_controller_manager_ds_manifest)
    with open(path, "r") as f:
        yaml_dicts = [x for x in yaml.safe_load_all(f)]
    target_dict = yaml_dicts[1]
    target_entry_list = target_dict["spec"]["template"]["spec"]["containers"][0]["args"]
    target_entry_list.pop()
    value_to_insert = f"--cluster-cidr={openstack_config.remote_ip_prefix}"
    target_entry_list.append(value_to_insert)

    return yaml_dicts


def get_cloud_controller_roles_manifest() -> dict:
    path = get_manifest_path(cloud_controller_manager_roles_manifest)
    with open(path, "r") as f:
        yaml_dict = yaml.safe_load(f)
    return yaml_dict


def get_cloud_controller_role_bindings_manifest() -> dict:
    path = get_manifest_path(cloud_controller_manager_role_bindings_manifest)
    with open(path, "r") as f:
        yaml_dict = yaml.safe_load(f)
    return yaml_dict


def get_csi_plugin_manifest() -> list[dict]:
    path = get_manifest_path(csi_plugin_manifest)
    with open(path, "r") as f:
        yaml_dicts = [x for x in yaml.safe_load_all(f)]
    return yaml_dicts
