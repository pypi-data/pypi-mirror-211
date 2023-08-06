import argparse
from dcat_ap_de_validator.commands import portal


def main():
    parser = argparse.ArgumentParser(description="Validate Open Data Metadata")
    subparsers = parser.add_subparsers()

    # Portal Parse
    parser_portal = subparsers.add_parser("portal", help="Portal Validation help")
    parser_portal.add_argument("url", help="Portal URL")
    parser_portal.add_argument("-p", "--portal_type", help="Type of Portal, either ckan or dkan")
    parser_portal.set_defaults(func=portal.execute)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
