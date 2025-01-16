from base_logger import get_logger_child
import variables
import requests

firmware_logger = get_logger_child('firmware_updater')

headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    # "Authorization": f"Bearer {variables.GITHUB_TOKEN}"
}


def __get_last_release(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    release = requests.get(url, headers=headers)

    if release.status_code != 200:
        firmware_logger.error(f"Failed to get latest release for {owner}/{repo}")
        raise Exception(f"Failed to get latest release for {owner}/{repo}")

    firmware_logger.info(f"Success to get latest release for {owner}/{repo}")

    release = release.json()

    data = {
        "id": release["id"],
        "name": release["name"],
        "body": release["body"],
        "assets": []
    }

    assets_url = release["assets_url"]
    assets = requests.get(assets_url, headers=headers).json()

    for asset in assets:
        data["assets"].append({
            "url": asset["url"],
            "name": asset["name"],
        })

    return data


def update_firmware_files(owner, repo):
    assets = __get_last_release(owner, repo)["assets"]

    headers_download = headers.copy()
    headers_download["Accept"] = "application/octet-stream"

    for asset in assets:
        asset_binary = requests.get(asset["url"], headers=headers_download)
        with open(variables.FIRMWARE_PATH / f"{asset['name']}", "wb") as f:
            f.write(asset_binary.content)

