Feature: Hamster behavior
  Verify hamster energy/weight and state changes

  Scenario: Fat hamsters die
    Given a hamster with energy=150 weight=250
    When 1 hours pass
    Then hamster has energy=100 weight=200
    Then hamster is DEAD

  Scenario: Starving hamsters die
    Given a hamster with energy=50 weight=0
    When 1 hours pass
    Then hamster is DEAD

  Scenario: Hamster is running when it can
    Given a hamster with energy=80 weight=100
    And the time is 23:00
    When 1 hours pass
    Then hamster is RUNNING

  Scenario: Hamster falls asleep when tired
    Given a hamster with energy=10 weight=100
    When 1 hours pass
    Then hamster is SLEEPING

  Scenario: Hamster gets tired while running
    Given a hamster with energy=80 weight=100
    And hamster is RUNNING
    And the time is 23:00
    When 1 hours pass
    Then hamster has energy=63 weight=100
