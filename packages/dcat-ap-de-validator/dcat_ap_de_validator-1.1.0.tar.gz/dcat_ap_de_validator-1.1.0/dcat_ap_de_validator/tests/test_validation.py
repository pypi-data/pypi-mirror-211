import pytest
from dcat_ap_de_validator.metadata.validate import validate


pytestmark = [pytest.mark.vcr("heilbronn.yaml")]


@pytest.mark.block_network
def test_dkan_validation():
    url = "https://opendata.heilbronn.de/straftaten-im-stadtgebiet-heilbronn"
    result = validate(url)
    assert "results" in result
    assert "valid" in result
    assert "warning" in result
    assert "error" in result
    assert len(result["results"]) == 9
    assert result["valid"] is False
    assert result["warning"] == 4
    assert result["error"] == 5
    assert result["info"] == 0
