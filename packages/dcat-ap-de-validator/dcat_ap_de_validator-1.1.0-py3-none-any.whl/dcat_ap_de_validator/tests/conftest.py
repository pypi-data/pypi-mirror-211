import os
import pytest


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    module = request.node.fspath
    return os.path.join(module.dirname, "cassettes")
