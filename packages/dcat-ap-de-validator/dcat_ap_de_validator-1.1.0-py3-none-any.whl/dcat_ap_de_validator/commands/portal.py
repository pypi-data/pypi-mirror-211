import json

from rich.console import Console
from rich.progress import track

from dcat_ap_de_validator.portals import Portal, CKAN, DKAN
from dcat_ap_de_validator.metadata.validate import validate


def execute(args):
    console = Console()
    portal_type = str(args.portal_type)
    portal = Portal(args.url)
    if portal_type.lower() == "dkan":
        portal = DKAN(args.url)
    else:
        portal = CKAN(args.url)
    package_list = portal.packages()
    portal_title = portal.get_title()
    validation_result = {"portal": portal_title, "warnings": 0, "errors": 0, "infos": 0, "valid_datasets": 0, "results": []}
    results = []

    console.rule("[bold red]Metadaten download")
    console.print(f"Wir haben {len(package_list)} Daten gefunden.", style="bold gold3")
    for package_name in track(package_list, description="Metadaten validieren..."):
        result = validate(portal.package_metadata_url(package_name))
        # count errors and warnings, successes
        validation_result["warnings"] += result["warning"]
        validation_result["errors"] += result["error"]
        validation_result["infos"] += result["info"]
        if result.get("valid", False):
            validation_result["valid_datasets"] += 1
        results.append({"package": package_name, "url": portal.package_url(package_name), "result": result})

    console.rule("[bold red]Validierungsergebnisse")
    console.print("Valid Datasets:", validation_result["valid_datasets"], style="bold green4")
    console.print("Infos:", validation_result["infos"], style="bold grey39")
    console.print("Warnings:", validation_result["warnings"], style="bold gold3")
    console.print("Errors:", validation_result["errors"], style="bold red")
    validation_result["results"] = results
    with open(f"{portal_title}.json", "w") as f:
        json.dump(validation_result, f)

    return validation_result
