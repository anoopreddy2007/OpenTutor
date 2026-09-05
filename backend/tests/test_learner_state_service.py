def test_mastery_increases_after_correct_answer():
    old_mastery = 0.4
    learning_rate = 0.10

    new_mastery = old_mastery + learning_rate * (1.0 - old_mastery)

    assert new_mastery > old_mastery
    assert 0.0 <= new_mastery <= 1.0


def test_mastery_decreases_after_incorrect_answer():
    old_mastery = 0.7
    learning_rate = 0.10

    new_mastery = old_mastery - learning_rate * old_mastery

    assert new_mastery < old_mastery
    assert 0.0 <= new_mastery <= 1.0