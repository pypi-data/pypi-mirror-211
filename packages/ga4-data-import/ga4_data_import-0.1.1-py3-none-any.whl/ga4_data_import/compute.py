# This file contains functions for creating a Compute Engine instance and static address.

from google.cloud.compute_v1.services.instances.client import InstancesClient
from google.cloud.compute_v1.services.addresses.client import AddressesClient
from google.cloud.compute_v1.types import (
    Address,
    AccessConfig,
    AttachedDisk,
    AttachedDiskInitializeParams,
    InsertAddressRequest,
    InsertInstanceRequest,
    Instance,
    Items,
    GetAddressRequest,
    Metadata,
    NetworkInterface,
    Scheduling,
    ServiceAccount,
    ShieldedInstanceConfig,
    ShieldedInstanceIntegrityPolicy,
    SetMetadataInstanceRequest,
    Tags,
)
from ga4_data_import.common import (
    get_region_from_zone,
    get_project_number,
)


def create_static_address(project_id, zone, instance_name):
    """
    Create a static address with the provided name, project id, and region.
    Args:
        project_id: The project id.
        zone: The zone to create the static address in.
        instance_name: The name of the instance.
    Returns:
        str, The static address.
    """
    region = get_region_from_zone(zone)
    address_name = f"{instance_name}-static"
    address_request = GetAddressRequest(
        project=project_id, region=region, address=address_name
    )
    address_client = AddressesClient()

    try:
        # Check if the address already exists
        existing_address_response = address_client.get(address_request)
        return existing_address_response.address
    except:
        # Address does not exist, create a new one
        insert_address_request = InsertAddressRequest(
            project=project_id,
            region=region,
            address_resource=Address(name=address_name, network_tier="STANDARD"),
        )
        address_client.insert(insert_address_request).result()
        new_address_response = address_client.get(address_request)
        return new_address_response.address


def create_instance(
    instance_name, project_id, zone, static_address, sftp_username, bucket_name
):
    """
    Create a Compute Engine instance with the provided name, project id, zone, and bucket name.
    Args:
        instance_name: The name of the instance.
        project_id: The project id.
        zone: The zone to create the instance in.
        static_address: The static address to assign to the instance.
        sftp_username: The username to create on the instance.
        bucket_name: The name of the bucket to mount on the instance.
    """

    # Create the instance request
    disk = AttachedDisk(
        auto_delete=True,
        boot=True,
        initialize_params=AttachedDiskInitializeParams(
            disk_size_gb=10,
            source_image="projects/debian-cloud/global/images/debian-11-bullseye-v20230509",
            disk_type=f"projects/{project_id}/zones/{zone}/diskTypes/pd-balanced",
        ),
    )
    project_number = get_project_number(project_id)
    metadata = [
        Items(
            key="startup-script",
            value=f"""#!/bin/bash

sftp_username={sftp_username}
bucket_name={bucket_name}

# Install SFTP server
apt-get update -y
apt-get install -y openssh-server

# Install gcloud
# https://cloud.google.com/sdk/docs/install#installation_instructions
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | tee /usr/share/keyrings/cloud.google.gpg
apt-get update -y
apt-get install google-cloud-sdk -y

# Install gcsfuse
# https://cloud.google.com/storage/docs/gcsfuse-quickstart-mount-bucket#install
export GCSFUSE_REPO=gcsfuse-$(lsb_release -c -s)
echo "deb https://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update -y
sudo apt-get install -y fuse gcsfuse
rm -rf /var/lib/apt/lists/*

# Create user
adduser $sftp_username
mkdir /home/$sftp_username
chown root:root /home/sftp_user
sed -i "s/^Subsystem\tsftp.*/Subsystem\tsftp internal-sftp/" /etc/ssh/sshd_config
tee -a /etc/ssh/sshd_config << EOM
Match User $sftp_username
\tForceCommand internal-sftp -d /sftp
\tChrootDirectory /home/%u
\tAllowTcpForwarding no
\tX11Forwarding no
\tPasswordAuthentication no
\tAuthenticationMethods publickeyEOM
systemctl restart ssh

# Mount bucket
sudo -u $sftp_username mkdir /home/$sftp_username/sftp
sudo -u $sftp_username gcsfuse $bucket_name /home/$sftp_username/sftp""",
        )
    ]
    network_interface = NetworkInterface(
        name=f"{instance_name}-nic0",
        access_configs=[
            AccessConfig(
                nat_i_p=static_address,
                network_tier="STANDARD",
            )
        ],
    )
    service_account = ServiceAccount(
        email=f"{project_number}-compute@developer.gserviceaccount.com",
        scopes=[
            "https://www.googleapis.com/auth/devstorage.read_only",
            "https://www.googleapis.com/auth/logging.write",
            "https://www.googleapis.com/auth/monitoring.write",
            "https://www.googleapis.com/auth/servicecontrol",
            "https://www.googleapis.com/auth/service.management.readonly",
            "https://www.googleapis.com/auth/trace.append",
        ],
    )
    insert_instance_request = InsertInstanceRequest(
        project=project_id,
        zone=zone,
        instance_resource=Instance(
            disks=[disk],
            machine_type=f"projects/{project_id}/zones/{zone}/machineTypes/f1-micro",
            name=instance_name,
            network_interfaces=[network_interface],
            metadata=Metadata(items=metadata),
            scheduling=Scheduling(
                automatic_restart=True,
                on_host_maintenance="MIGRATE",
                preemptible=False,
                provisioning_model="STANDARD",
            ),
            service_accounts=[service_account],
            shielded_instance_config=ShieldedInstanceConfig(
                enable_secure_boot=False,
                enable_vtpm=True,
                enable_integrity_monitoring=True,
            ),
            tags=Tags(items=["default-allow-ssh"]),
            shielded_instance_integrity_policy=ShieldedInstanceIntegrityPolicy(
                update_auto_learn_policy=True
            ),
            ignore_unknown_fields=True,
        ),
        ignore_unknown_fields=True,
    )

    # Create the instance
    InstancesClient().insert(request=insert_instance_request).result()


def add_shh_pub_key(project_id, zone, instance_name, sftp_username, key):
    """
    Add the provided SSH public key to the instance metadata.

    Args:
        project_id: The project id.
        zone: The zone to create the instance in.
        instance_name: The name of the instance.
        sftp_username: The username to create on the instance.
        key: SSH public key value
    Returns:
        None
    """
    instance_client = InstancesClient()
    instance_response = instance_client.get(
        project=project_id, zone=zone, instance=instance_name
    )

    existing_ssh_keys = ""
    for item in instance_response.metadata.items:
        if item.key == "ssh-keys":
            existing_ssh_keys = item.value
            break

    new_key = sftp_username.strip() + ":" + key.strip()
    need_append = True
    if existing_ssh_keys:
        existing_ssh_keys = existing_ssh_keys.split("\n")
        keys = []
        for key in existing_ssh_keys:
            keys.append(key.strip())
            if new_key == key.strip():
                need_append = False
                break
        existing_ssh_keys = "\n".join(keys)

    # Update the instance metadata with the new SSH key
    if need_append:
        request = SetMetadataInstanceRequest(
            project=project_id,
            zone=zone,
            instance=instance_name,
            metadata_resource=Metadata(
                fingerprint=instance_response.metadata.fingerprint,
                items=[
                    Items(
                        key="ssh-keys",
                        value=(existing_ssh_keys + "\n" + new_key)
                        if existing_ssh_keys
                        else new_key,
                    )
                ],
            ),
        )

        InstancesClient().set_metadata(request).result()
