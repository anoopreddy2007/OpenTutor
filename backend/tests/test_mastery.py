from app.services.mastery import classify_mastery


def test_beginner_mastery():
    assert classify_mastery(0.20) == "beginner"


def test_developing_mastery():
    assert classify_mastery(0.50) == "developing"


def test_proficient_mastery():
    assert classify_mastery(0.80) == "proficient"


def test_mastery_boundaries():
    assert classify_mastery(0.0) == "beginner"
    assert classify_mastery(0.30) == "developing"
    assert classify_mastery(0.70) == "proficient"