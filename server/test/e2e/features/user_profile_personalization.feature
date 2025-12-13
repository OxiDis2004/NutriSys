Feature: User profile personalization

  Scenario: Change user language settings
    Given system has user with telegram id "telegram_123" and language "ua"
    And system has language "en"
    When user with telegram id "telegram_123" updates profile language to "en"
    Then response status 200
    And user profile language should be "en"

  Scenario: Persist user profile settings
    Given system has user with telegram id "telegram_123" and language "ua"
    When user update profile information
    Then response status 202
