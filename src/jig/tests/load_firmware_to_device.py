import os
import shutil
import psutil
import subprocess

import variables
from base_logger import get_logger_for_file


logger = get_logger_for_file(__name__)


firmware_file = None
def get_firmware_file():
    global firmware_file
    if firmware_file and firmware_file.is_file():
        logger.info(f"Use old firmware file {firmware_file}")
        return firmware_file

    firmware_file = None

    files = [f for f in os.listdir(variables.FIRMWARE_PATH) if os.path.isfile(os.path.join(variables.FIRMWARE_PATH, f))]
    if not files:
        logger.warn("Don't see any firmware files")
        return None

    files.sort()
    file = files[-1]
    if not file.endswith(".uf2"):
        logger.warn(f"File from firmware dir is not firmware. {file}")
        return None

    firmware_file = variables.FIRMWARE_PATH / file
    logger.info(f"Firmware file has been found. {file}")
    return firmware_file


def list_unmounted_drives():
    lsblk_output = subprocess.check_output(['lsblk', '-o', 'NAME,TYPE,MOUNTPOINT'], text=True)

    for line in lsblk_output.splitlines()[1:]:
        parts = line.split()
        if len(parts) == 2 and parts[1] == 'part':
            return parts[0][2:]

    return None

def mount_usb_drive(drive_name):
    os.makedirs(variables.MOUNT_POINT, exist_ok=True)
    try:
        subprocess.run(['sudo', 'mount', f'/dev/{drive_name}', variables.MOUNT_POINT], check=True)
        logger.info(f"Mounted /dev/{drive_name} at {variables.MOUNT_POINT}")
    except subprocess.CalledProcessError as e:
        logger.warn(f"Failed to mount /dev/{drive_name}: {e}")


def unmount_usb_drive():
    try:
        subprocess.run(['sudo', 'umount', variables.MOUNT_POINT], check=True)
        logger.info(f"Umounted {variables.MOUNT_POINT}")
    except subprocess.CalledProcessError as e:
        logger.warn(f"Failed to unmount {variables.MOUNT_POINT}: {e}")


def check_mounted_drives():
    for partition in psutil.disk_partitions(all=False):
        if partition.mountpoint == variables.MOUNT_POINT:
            return True
    return False


def copy_firmware_to_usb_drive(source_file):
    destination = os.path.join(variables.MOUNT_POINT, os.path.basename(source_file))
    try:
        shutil.copy2(source_file, destination)  # Copy the file
        logger.info(f"File '{source_file}' has been copied to device.")
        return True
    except Exception as e:
        logger.warn(f"Failed to copy to device: {e}")
        return False


def load_firmware_to_device():
    source_file = get_firmware_file()
    if not source_file:
        logger.warn("Some problem with loading firmware file")
        return None

    if check_mounted_drives():
        logger.info("Mounted drive has been detected")
    else:
        logger.info("Mounted drive has not been detected.")

        unmounted_drive = list_unmounted_drives()

        if unmounted_drive:
            logger.info("Unmounted USB drives detected")
            mount_usb_drive(unmounted_drive)
        else:
            logger.warn("No unmounted USB drives found.")
            return None

    resp = copy_firmware_to_usb_drive(source_file)
    if not resp:
        logger.warn("Failed to copy firmware file")
        return None

    unmount_usb_drive()


if __name__ == "__main__":
    load_firmware_to_device()