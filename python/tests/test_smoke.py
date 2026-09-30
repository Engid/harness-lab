import os

import pytest


def test_package_imports() -> None:
    import harness_lab  # noqa: F401


def test_typesafe_sdk_imports() -> None:
    from typesafe_sdk import Choice, Noul, Score, TypeSafeClient  # noqa: F401


@pytest.mark.skipif(not os.environ.get("TYPESAFE_API_KEY"), reason="TYPESAFE_API_KEY not set")
def test_api_key_is_available() -> None:
    assert os.environ["TYPESAFE_API_KEY"].strip()
