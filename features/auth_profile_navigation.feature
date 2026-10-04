Feature: User Authentication, Profile Management, and Navigation
  As a customer of Toolshop
  I want to register, authenticate, manage my personal profile, and browse product categories
  So that I can securely manage my account and find tools easily

  Background:
    Given the customer is on the Toolshop application home page

  # ---------------------------------------------------------------------------
  # 1. USER REGISTRATION
  # ---------------------------------------------------------------------------
  @auth @register @smoke @positive
  Scenario: Successful customer registration with valid personal details
    Given the customer navigates to the registration page
    When the customer submits the registration form with valid and complete personal information
    Then the system should register the new account successfully
    And the customer should be redirected to the login page with a success confirmation

  @auth @register @negative
  Scenario: Registration rejected when applicant is under legal age (under 18 years old)
    Given the customer navigates to the registration page
    When the customer attempts to register with a date of birth indicating age younger than 18 years
    Then the system should reject the registration submission
    And an age validation error stating that the customer must be at least 18 years old should be displayed

  # ---------------------------------------------------------------------------
  # 2. USER LOGIN (SCENARIO OUTLINE)
  # ---------------------------------------------------------------------------
  @auth @login @data-driven
  Scenario Outline: Customer login attempts with various credential states
    Given the customer navigates to the login page
    When the customer attempts to sign in with email "<email>" and password "<password>"
    Then the authentication outcome should be "<status>"
    And the customer should receive the expected message "<expected_message>"

    Examples:
      | email                                | password         | status  | expected_message             |
      | customer@practicesoftwaretesting.com | welcome01        | SUCCESS | User dashboard displayed     |
      | customer@practicesoftwaretesting.com | WrongPassword99! | FAILED  | Invalid email or password    |
      | unregistered.user.2026@test.com      | ValidPass#2026   | FAILED  | Invalid email or password    |
      |                                      | ValidPass#2026   | FAILED  | E-mail is required           |
      | customer@practicesoftwaretesting.com |                  | FAILED  | Password is required         |

  # ---------------------------------------------------------------------------
  # 3. EDIT PROFILE
  # ---------------------------------------------------------------------------
  @profile @positive
  Scenario: Successful update of customer profile details
    Given the customer is authenticated with an active account
    And the customer accesses the account profile settings
    When the customer updates the phone number and residential address with new details
    Then the updated profile should be saved successfully
    And the new information should persist upon reloading the profile page

  # ---------------------------------------------------------------------------
  # 4. CHANGE PASSWORD
  # ---------------------------------------------------------------------------
  @profile @password @negative
  Scenario: Password change rejected when new password does not satisfy security complexity
    Given the customer is authenticated with an active account
    And the customer accesses the change password page
    When the customer attempts to set a weak new password lacking numbers or special characters
    Then the system should reject the password update request
    And a password complexity warning should prompt the customer to fulfill security requirements

  @profile @password @positive
  Scenario: Successful password change and re-authentication with new password
    Given the customer is authenticated with an active account
    And the customer accesses the change password page
    When the customer submits the correct current password and a valid new compliant password
    Then the account password should be updated successfully
    And the customer should be able to log in with the new password in a new session

  # ---------------------------------------------------------------------------
  # 5. MENU NAVIGATION
  # ---------------------------------------------------------------------------
  @navigation @catalog @positive
  Scenario: Targeted product catalog filtering through header category menu
    When the customer navigates to "Power Tools" via the top categories navigation menu
    Then the product catalog view should display only products classified under "Power Tools"
    And the page header and breadcrumb should display "Power Tools"
