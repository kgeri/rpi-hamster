Feature: Hamster reactions
  Verify hamster reacts to physical interactions

  Scenario: When dropped, hamster dies
    When the hamster is dropped
    Then hamster face is dead

  Scenario: When shaken, hamster gets scared
    When the hamster is shaken
    Then hamster face is scared

  Scenario: When swiped up, hamster is eating
    When the hamster is swiped up
    Then hamster face is eating

  Scenario: When swiped down (pet), hamster is content
    When the hamster is swiped down
    Then hamster face is content
