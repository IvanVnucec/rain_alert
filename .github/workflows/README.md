# Instructions for Github Actions setup

## Idea
We can schedule to run a script on the GitHub Actions servers. 

## Instructions
1. Create GitHub Actions secrets below:
    - CREDENTIALS - See the README.md in the project root directory for more info about the contents.
    - RECEIVERS - Same as above.
    - FAIL_MAIL_USERNAME - Gmail alert address for the workflow fails alerts.
    - FAIL_MAIL_PASSWORD - Gmail password for the above. User is advised to check 
    [Sign in with App Passwords](https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor&visit_id=637593941018469305-643690772&rd=1)

2. Manually run Github Action workflow. It is normal if the Download artifacts from the last workflow 
step fails because there is no workflows beforehand.

3. Thats it. The Github Action workflow should run as scheduled and the Python script should be 
executed once per day.
