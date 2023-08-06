import os
import subprocess

imgcat_path = None
# TODO: Thorough way to find executable path for different environments
if os.path.isfile(os.path.expanduser("~/bin/imgcat")):
    imgcat_path = os.path.expanduser("~/bin/imgcat")


def imgcat(filename, width_chars=None, height_chars=None):
    if not imgcat_path:
        return ""

    options = ["inline=1"]
    if width_chars:
        options.append(f"width={width_chars}")
    if height_chars:
        options.append(f"height={height_chars}")

    img = subprocess.check_output([imgcat_path, filename]).decode("utf-8")
    img = img.replace("inline=1", ";".join(options))

    return img
