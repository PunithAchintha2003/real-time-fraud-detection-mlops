from src.training.retrain_business_model import (
    should_promote_candidate,
)


def make_metrics(
    f1_score: float,
    roc_auc: float,
) -> dict[str, float]:
    return {
        "precision": 0.80,
        "recall": 0.80,
        "f1_score": f1_score,
        "roc_auc": roc_auc,
    }


def test_promotes_when_no_champion_exists():
    candidate = make_metrics(
        f1_score=0.80,
        roc_auc=0.90,
    )

    promoted, reason = should_promote_candidate(
        candidate,
        None,
    )

    assert promoted is True
    assert "No existing champion" in reason


def test_promotes_better_candidate():
    candidate = make_metrics(
        f1_score=0.82,
        roc_auc=0.91,
    )

    champion = make_metrics(
        f1_score=0.80,
        roc_auc=0.90,
    )

    promoted, reason = should_promote_candidate(
        candidate,
        champion,
    )

    assert promoted is True
    assert "passed" in reason


def test_rejects_equal_candidate():
    candidate = make_metrics(
        f1_score=0.80,
        roc_auc=0.90,
    )

    champion = make_metrics(
        f1_score=0.80,
        roc_auc=0.90,
    )

    promoted, reason = should_promote_candidate(
        candidate,
        champion,
    )

    assert promoted is False
    assert "rejected" in reason


def test_rejects_lower_f1():
    candidate = make_metrics(
        f1_score=0.79,
        roc_auc=0.92,
    )

    champion = make_metrics(
        f1_score=0.80,
        roc_auc=0.90,
    )

    promoted, _ = should_promote_candidate(
        candidate,
        champion,
    )

    assert promoted is False


def test_rejects_lower_roc_auc():
    candidate = make_metrics(
        f1_score=0.82,
        roc_auc=0.89,
    )

    champion = make_metrics(
        f1_score=0.80,
        roc_auc=0.90,
    )

    promoted, _ = should_promote_candidate(
        candidate,
        champion,
    )

    assert promoted is False
