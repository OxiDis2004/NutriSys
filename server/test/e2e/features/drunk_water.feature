# Created by denis at 12.12.2025
Feature: Drunk water from user

  Scenario: Add water without user_id
    Given system has no user with telegram id "telegram_123"
    When I add 500 ml of water
    Then response status 400
    And with message "User id is null"

  Scenario: Add water successfully
    Given system has user with telegram id "telegram_123" and language "ua"
    And remove data in table
    And today user already drank 1000 ml
    When I add 500 ml of water
    Then response status 200
    And total drunk water should be 1500 ml today

  Scenario: Add water successfully 3 times
    Given system has user with telegram id "telegram_123" and language "ua"
    And remove data in table
    When I add 1000 ml of water
    And I add 250 ml of water
    And I add 500 ml of water
    Then response status 200
    And total drunk water should be 1750 ml today
    
  Scenario: Get daily statistic
    Given system has user with telegram id "telegram_123" and language "ua"
    And remove data in table
    And today user already drank 1000 ml
    When get daily statistic
    Then response status 200
    And daily statistic

  Scenario: Get weekly statistic
    Given system has user with telegram id "telegram_123" and language "ua"
    And remove data in table
    And add data in table
    And at this week user drunk
    When get weekly statistic
    Then response status 200
    And weekly statistic

  Scenario: Get monthly statistic
    Given system has user with telegram id "telegram_123" and language "ua"
    And remove data in table
    And user drunk almost days in month
    When get monthly statistic
    Then response status 200
    And monthly statistic

  Scenario: Get yearly statistic
    Given system has user with telegram id "telegram_123" and language "ua"
    And remove data in table
    And user drunk in almost days in year
    When get yearly statistic
    Then response status 200
    And yearly statistic