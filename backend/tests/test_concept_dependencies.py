import pytest

from app.services.concept_dependencies import (
    ConceptDependency,
    all_prerequisites_ready,
    calculate_dependency_gap,
    evaluate_dependency,
    is_prerequisite_ready,
)


def test_prerequisite_is_ready():
    assert is_prerequisite_ready(0.70) is True
    assert is_prerequisite_ready(0.90) is True


def test_prerequisite_is_not_ready():
    assert is_prerequisite_ready(0.69) is False
    assert is_prerequisite_ready(0.30) is False


def test_mastery_is_clamped():
    assert is_prerequisite_ready(1.5) is True
    assert is_prerequisite_ready(-1.0) is False


def test_invalid_threshold_is_rejected():
    with pytest.raises(ValueError):
        is_prerequisite_ready(0.5, threshold=-0.1)

    with pytest.raises(ValueError):
        is_prerequisite_ready(0.5, threshold=1.1)


def test_evaluate_dependency():
    dependency = ConceptDependency(
        concept_id=10,
        prerequisite_id=5,
    )

    status = evaluate_dependency(
        dependency=dependency,
        prerequisite_mastery=0.80,
    )

    assert status.concept_id == 10
    assert status.prerequisite_id == 5
    assert status.mastery == 0.80
    assert status.ready is True


def test_evaluate_dependency_not_ready():
    dependency = ConceptDependency(
        concept_id=10,
        prerequisite_id=5,
    )

    status = evaluate_dependency(
        dependency=dependency,
        prerequisite_mastery=0.40,
    )

    assert status.mastery == 0.40
    assert status.ready is False


def test_dependency_gap():
    assert calculate_dependency_gap(
        [0.50, 0.60],
        threshold=0.70,
    ) == pytest.approx(0.15)


def test_dependency_gap_is_zero_when_ready():
    assert calculate_dependency_gap(
        [0.80, 0.90],
        threshold=0.70,
    ) == 0.0


def test_dependency_gap_empty_list():
    assert calculate_dependency_gap([]) == 0.0


def test_all_prerequisites_ready():
    assert all_prerequisites_ready(
        [0.70, 0.80, 0.90]
    ) is True


def test_all_prerequisites_not_ready():
    assert all_prerequisites_ready(
        [0.70, 0.50, 0.90]
    ) is False


def test_empty_prerequisites_are_ready():
    assert all_prerequisites_ready([]) is True