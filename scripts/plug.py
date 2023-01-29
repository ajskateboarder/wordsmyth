#!/usr/bin/env python3

"""Plugin to command-line function"""
from importlib.util import spec_from_file_location, module_from_spec


def main(platform: str) -> None:
    """Plugin importer"""
    spec = spec_from_file_location("plugins", f"wordsmyth/plugins/{platform}.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)

    module = {k: getattr(module, k) for k in dir(module) if not k.startswith("_")}
    print(module.keys())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Download a specific number of comments in chunks to a JSON document",
        usage="./scripts/plug.py <platform> --help",
    )
    parser.add_argument(dest="platform", help="Plugin to import")
    args = parser.parse_args()

    main(args.platform)
