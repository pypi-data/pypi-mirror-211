import requests
import json


VALIDATION_API_URL = "https://www.itb.ec.europa.eu/shacl/dcat-ap.de/api/validate"


def severity_key(severity):
    if severity == "sh:Warning":
        return "warning"
    elif severity == "sh:Violation":
        return "error"
    elif severity == "sh:Info":
        return "info"


def extract_validation_results(json_ld):
    result = { "valid": False, "results": [] , "warning": 0, "error": 0, "info": 0}

    for graph_item in json_ld.get("@graph", []):
        result_type =graph_item.get("@type", "")
        if result_type == "sh:ValidationReport":
            result["valid"] = graph_item["sh:conforms"]
        if result_type == "sh:ValidationResult":
            result_message = graph_item["resultMessage"]["@value"]
            result_path = graph_item["resultPath"]
            severity = graph_item["resultSeverity"]
            result[severity_key(severity)] += 1
            result["results"].append({"message": result_message, "path": result_path, "type": severity})

    return result


def validate(url, verbose=False):
    payload = {
        "contentToValidate": url,
        "validationType": "v20_de_spec_implr"
    }

    headers = {
        "Content-Type": "application/json",
        "accept": "application/ld+json"
    }

    response = requests.post(VALIDATION_API_URL, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        data = json.loads(response.content)

        validation_results = extract_validation_results(data)

        if validation_results["valid"]:
            if verbose:
                print(f"Package validated successfully: {url}")
        else:
            if verbose:
                print(f"Validation failed for package {url}:")
    else:
        if verbose:
            print(f"Error validating package at {url}. Status code: {response.status_code}")

    return validation_results
