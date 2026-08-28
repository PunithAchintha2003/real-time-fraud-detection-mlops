import os

import joblib

import api.main as api_main


def test_business_model_hot_reload(
    tmp_path,
    monkeypatch,
):
    model_path = (
        tmp_path
        / "business_fraud_model.joblib"
    )

    first_artifact = {
        "model_version": "1",
    }

    joblib.dump(
        first_artifact,
        model_path,
    )

    monkeypatch.setattr(
        api_main,
        "BUSINESS_MODEL_PATH",
        model_path,
    )

    monkeypatch.setattr(
        api_main,
        "business_artifact",
        None,
    )

    monkeypatch.setattr(
        api_main,
        "business_model_mtime_ns",
        None,
    )

    assert (
        api_main.ensure_business_model_loaded()
        is True
    )

    assert (
        api_main.business_artifact["model_version"]
        == "1"
    )

    first_mtime_ns = (
        model_path.stat().st_mtime_ns
    )

    second_artifact = {
        "model_version": "2",
    }

    joblib.dump(
        second_artifact,
        model_path,
    )

    newer_mtime_ns = (
        first_mtime_ns
        + 1_000_000_000
    )

    os.utime(
        model_path,
        ns=(
            newer_mtime_ns,
            newer_mtime_ns,
        ),
    )

    assert (
        api_main.ensure_business_model_loaded()
        is True
    )

    assert (
        api_main.business_artifact["model_version"]
        == "2"
    )
