import os
import xml.etree.ElementTree as ET
from typing import Any

import yaml


def load_config(path: str = "config.yml") -> Any:
    """
    Load and parse a YAML configuration file.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"YAML file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML syntax in file '{path}': {e}") from e

    except OSError as e:
        raise RuntimeError(f"Error reading file '{path}': {e}") from e

    return data


def update_value(root: ET.Element, id: str, new_value: str, prefix_char: str = "."):
    """
    Update the text content of an SVG element with a given ID and adjust its prefix length.
    """
    value = root.find(f".//*[@id='{id}']")

    prefix = root.find(f".//*[@id='prefix_{id}']")

    if value is None:
        raise ValueError(f"Element with id '{id}' not found in SVG.")
    if prefix is None:
        raise ValueError(f"Element with id 'prefix_{id}' not found in SVG.")

    old_value = value.text if value.text else ""
    old_prefix = prefix.text if prefix.text else ""

    total_len = len(old_prefix) + len(old_value)

    new_prefix = " " + prefix_char * (total_len - len(new_value) - 2) + " "

    value.text = new_value
    prefix.text = new_prefix


def update_svg(filename: str, config: Any):
    """
    Update the SVG file with values from the configuration."""
    tree = ET.parse(filename)

    root = tree.getroot()

    update_value(root, "os", config["OS"])
    update_value(root, "host", config["Host"])
    update_value(root, "kernel", config["Kernel"])
    update_value(root, "ide", ", ".join(config["IDE"]))

    update_value(root, "lang_prog", ", ".join(config["Languages"]["Programming"]))
    update_value(root, "lang_spk", ", ".join(config["Languages"]["Speaking"]))

    update_value(root, "hobbies", ", ".join(config["Hobbies"]))

    update_value(root, "email_personal", config["Contacts"]["Emails"]["Personal"])
    update_value(root, "linkedin", config["Contacts"]["LinkedIn"])
    update_value(root, "discord", config["Contacts"]["Discord"])

    tree.write(filename, encoding="utf-8", xml_declaration=True)


def main():
    config = load_config()

    update_svg("dark_mode.svg", config)
    update_svg("light_mode.svg", config)


if __name__ == "__main__":
    main()
