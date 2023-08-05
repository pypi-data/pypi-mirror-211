import base64
from .types import UULE_A
import urllib


def pad(uule):
    """
    For base64 decoding, padding bytes need to be added. These are stripped out
    for UULE transmission.
    """
    return uule + "=" * (4 - len(uule) % 4)


def clean(uule):
    """
    Remove HTTP escape characters, etc.
    """
    return urllib.parse.unquote(uule).replace("-", "+").replace("_", "/")


def decode_a(uule) -> UULE_A:
    """
    Decodes UULE's of type "a+......"
    """
    uule = pad(clean(uule[2:]))
    lines = base64.urlsafe_b64decode(uule).decode().split("\n")
    data = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":")
            data[key.strip()] = value.strip()
    # Rescale to true lat/long
    print(lines, data)
    data["latitude"] = float(data.pop("latitude_e7")) / 10e7
    data["longitude"] = float(data.pop("longitude_e7")) / 10e7
    # Convert to appropriate data types
    data["radius"] = float(data["radius"])
    data["role"] = int(data["role"])
    data["producer"] = int(data["producer"])
    data["provenance"] = int(data["provenance"])
    data["radius"] = int(data["radius"])
    data["timestamp"] = int(data["timestamp"])
    return data


def decode_w(uule) -> str:
    """
    Decodes UULE's of type "w+...."
    """
    uule = pad(clean(uule[10:]))
    return base64.urlsafe_b64decode(uule).decode().lstrip()


def encode_w(canonical_location) -> str:
    """
    Canonical location must be from the list at
    """
    ascii_map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    len_bytes = ascii_map[len(canonical_location)]
    location = (
        base64.urlsafe_b64encode(bytes(canonical_location, "ascii")).decode().strip("=")
    )
    return f"w+CAIQICI{len_bytes}{location}"
