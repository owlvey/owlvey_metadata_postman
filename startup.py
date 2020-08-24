import os
import json
from OwlveyGateway import OwlveyGateway


def find_content_type(node):
    if "headers" in node["request"]:
        for item in node["request"]["headers"]:
            if (item["key"] == "Content-Type" or item["key"] == "Accept") and item["value"]:
                return item["value"].replace("application/", "")
        else:
            return "json"
    else:
        return "json"


def build_url(target: str):
    if "?" in target:
        return target[0: target.index("?")]
    else:
        return target


def build_feature(gateway, product, node, feature_root, sources):
    if "_postman_isSubFolder" not in node:
        feature = gateway.create_feature(product["id"], feature_root.lstrip(" "))
        key_method = node["request"]["method"]
        key_url = build_url(node["request"]["url"]["raw"])
        key_media = find_content_type(node)
        key = "{}:{}:{}".format(key_method, key_url, key_media)
        if key not in sources:
            sources[key] = gateway.create_source(product["id"], key)

        gateway.create_sli(feature["id"], sources[key]["id"])
        return
    else:
        for item in node["item"]:
            build_feature(gateway,product, item, feature_root + " " + node["name"], sources)


if __name__ == "__main__":
    metadata = None
    with open('./data/metadata.json', 'r') as f:
        data = f.read()
        metadata = json.loads(data)

    gateway = OwlveyGateway("http://localhost:50001",
                            'http://localhost:47002',
                            "CF4A9ED44148438A99919FF285D8B48D",
                            "0da45603-282a-4fa6-a20b-2d4c3f2a2127")

    organization = gateway.create_organization(metadata["info"]["name"])

    for item in metadata["item"]:
        product = gateway.create_product(organization["id"], item["name"])
        sources = dict()
        for fitem in item["item"]:
            build_feature(gateway, product, fitem, "", sources)







