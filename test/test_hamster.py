import pytest
from pytest_bdd import scenarios, when, then
from unittest.mock import patch, MagicMock
from src.hamster import Hamster
from mocks import MockLCD, MockTouch, MockGyro, MockPiezo, MockBattery


scenarios('../features/hamster.feature')


@pytest.fixture
def hamster():
    lcd = MockLCD()
    touch = MockTouch()
    gyro = MockGyro()
    piezo = MockPiezo()
    battery = MockBattery()
    with patch('builtins.open', MagicMock()):
        h = Hamster(lcd, touch, gyro, piezo, battery, now_ms=0, tick_ms=10)
    return h


@when('the hamster is dropped')
def hamster_is_dropped(hamster):
    hamster.gyro._values = [1.0, 1.0, 1.0, 0, 0, 0]  # mag2 = 3.0 >= 1.5
    with patch('builtins.open', MagicMock()):
        hamster.tick(now_ms=1000, tick=0)
        hamster.tick(now_ms=1110, tick=1)  # > 100ms after start


@when('the hamster is shaken')
def hamster_is_shaken(hamster):
    hamster.gyro._values = [0.5, 0.5, 1.5, 300, 0, 0]
    with patch('builtins.open', MagicMock()):
        hamster.tick(now_ms=100, tick=0)


@when('the hamster is swiped up')
def hamster_is_swiped_up(hamster):
    hamster.touch._gesture = MockTouch.UP
    with patch('builtins.open', MagicMock()):
        hamster.tick(now_ms=100, tick=0)


@when('the hamster is swiped down')
def hamster_is_swiped_down(hamster):
    hamster.touch._gesture = MockTouch.DOWN
    with patch('builtins.open', MagicMock()):
        hamster.tick(now_ms=100, tick=0)


@then('hamster face is dead')
def hamster_face_is_dead(hamster):
    assert hamster.face.face_id == "dead"


@then('hamster face is scared')
def hamster_face_is_scared(hamster):
    assert hamster.face.face_id == "scared"


@then('hamster face is eating')
def hamster_face_is_eating(hamster):
    assert hamster.face.face_id == "eating"


@then('hamster face is content')
def hamster_face_is_content(hamster):
    assert hamster.face.face_id == "content"
