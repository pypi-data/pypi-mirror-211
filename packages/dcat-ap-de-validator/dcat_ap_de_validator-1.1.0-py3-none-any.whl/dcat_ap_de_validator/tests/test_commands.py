import pytest
import argparse

from dcat_ap_de_validator.commands.portal import execute


pytestmark = [pytest.mark.vcr("heilbronn.yaml")]


@pytest.fixture
def args():
    namespace = argparse.Namespace()
    namespace.portal_type = 'dkan'
    namespace.url = 'https://opendata.heilbronn.de'
    return namespace


@pytest.mark.block_network
def test_portal_command_success(args):
    result = execute(args)

    assert "warnings" in result
    assert "portal" in result
    assert "errors" in result
    assert "infos" in result
    assert "valid_datasets" in result
    assert result["portal"] == "OffeneDatenHeilbronn"
    assert result["warnings"] == 4
    assert result["errors"] == 5
    assert result["valid_datasets"] == 0
