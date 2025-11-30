from datetime import datetime
from pytest_bdd import scenarios, given, when, then, parsers
from src.hamster import Hamster, HamsterState
import pytest


scenarios('../features/hamster.feature')


class ConcreteHamster(Hamster):
    def squeak(self):
        return "squeak"

@given(parsers.parse('a hamster with energy={energy} weight={weight}'), target_fixture="hamster")
def hamster_energy_weight(energy, weight):
    h = ConcreteHamster(epoch_seconds=0)
    h.energy = float(energy)
    h._initial_energy = float(energy)
    h.weight = float(weight)
    h.last_update = 0
    return h

@given(parsers.parse('the time is {hours}:{minutes}'))
def the_time_is(hamster, hours, minutes):
    today = datetime.today()
    dt = datetime(today.year, today.month, today.day, int(hours), int(minutes), 0)
    hamster.last_update = int(dt.timestamp())

@given(parsers.parse('hamster is {state}'))
def given_hamster_is(hamster, state):
    hamster.state = HamsterState[state]

@when(parsers.parse('{hours} hours pass'))
def seconds_pass(hamster, hours):
    epoch_seconds = int(getattr(hamster, "last_update", 0) + int(hours) * 3600)
    hamster.on_time(epoch_seconds)

@then(parsers.parse('hamster has energy={energy} weight={weight}'))
def hamster_has_values(hamster, energy, weight):
    assert hamster.energy == pytest.approx(float(energy), rel=0.5)
    assert hamster.weight == pytest.approx(float(weight), rel=0.5)

@then(parsers.parse('hamster is {state}'))
def then_hamster_is(hamster, state):
    assert hamster.state == HamsterState[state]
