# debsaws
# AWS Account Admin for SRE

## Tools Included
- ListDefault
- ListAll
- ListAccount
- AddNewAccount
- DeleteAccount
- UpdateAccount

## How to Use

### DEPLOYED VERSION

- List Default AWS Account
  - https://ic5jbzort7.execute-api.eu-west-1.amazonaws.com/api/

- Get default AWS Account
  - http https://ic5jbzort7.execute-api.eu-west-1.amazonaws.com/api/awsacc

- Get all AWS Accounts
  - http https://ic5jbzort7.execute-api.eu-west-1.amazonaws.com/api/awsacc/all

- Get one numbered AWS Accounts
  - http https://ic5jbzort7.execute-api.eu-west-1.amazonaws.com/api/awsacc/178611996779
  - http https://ic5jbzort7.execute-api.eu-west-1.amazonaws.com/api/awsacc/058700374591

- Add an AWS Account
  - echo '{ "AccountNumber": "01234567890", "AccountName": "DebsTestAccount", "Active": "N", "Description": "Debs Test Account", "RealUsers": "N", "AccOwners": {"Deborah Balm", "Chris Allison"} "OwnerTeam": "SRE", "PreviousName": "Debs", "SecOpsEmail": "secadmin-prod.awsnotifications@hivehome.dev", "SecOpsSlackChannel": "#debs_backoffice", "TeamEmail": "sre@bgch.co.uk" }' | http POST https://ic5jbzort7.execute-api.eu-west-1.amazonaws.com/api/awsacc

  - echo '{ "AccountNumber": "01234567810", "AccountName": "DebsTestAccount2", "Active": "N", "Description": "Debs Test Account 2", "RealUsers": "N", "AccOwners": "Deborah Balm", "OwnerTeam": "SRE", "PreviousName": "Debs", "SecOpsEmail": "secadmin-prod.awsnotifications@hivehome.dev", "SecOpsSlackChannel": "#debs_backoffice", "TeamEmail": "sre@bgch.co.uk" }' | http POST http POST https://ic5jbzort7.execute-api.eu-west-1.amazonaws.com/api/awsacc


- Delete an Account
  - http DELETE https://ic5jbzort7.execute-api.eu-west-1.amazonaws.com/api/awsacc/01234567810

- Update Details in an account
  - echo '{"Active": "Y", "Description": "Debs purple Test Account 2"}' | http PUT https://ic5jbzort7.execute-api.eu-west-1.amazonaws.com/api/awsacc/01234567810
  - echo '{"AccOwners": "Deborah Balm, Chris Allison" }' | http PUT https://ic5jbzort7.execute-api.eu-west-1.amazonaws.com/api/awsacc/01234567810

###LOCAL SERVER


- List Default AWS Account
  - http localhost:8000/awsacc

- Get default AWS Account
  - http localhost:8000/awsacc

- Get all AWS Accounts
  - http localhost:8000/awsacc/all

- Get one numbered AWS Accounts
  - http localhost:8000/awsacc/178611996779
  - http localhost:8000/awsaccc/058700374591

- Add an AWS Account
  - echo '{ "AccountNumber": "01234567890", "AccountName": "DebsTestAccount", "Active": "N", "Description": "Debs Test Account", "RealUsers": "N", "AccOwners": {"Deborah Balm", "Chris Allison"} "OwnerTeam": "SRE", "PreviousName": "Debs", "SecOpsEmail": "secadmin-prod.awsnotifications@hivehome.dev", "SecOpsSlackChannel": "#debs_backoffice", "TeamEmail": "sre@bgch.co.uk" }' | http POST localhost:8000/awsacc

  - echo '{ "AccountNumber": "01234567810", "AccountName": "DebsTestAccount2", "Active": "N", "Description": "Debs Test Account 2", "RealUsers": "N", "AccOwners": "Deborah Balm", "OwnerTeam": "SRE", "PreviousName": "Debs", "SecOpsEmail": "secadmin-prod.awsnotifications@hivehome.dev", "SecOpsSlackChannel": "#debs_backoffice", "TeamEmail": "sre@bgch.co.uk" }' | http POST http://127.0.0.1:8000/awsacc


- Delete an Account
  - http DELETE localhost:8000/awsacc/01234567810

- Update Details in an account
  - echo '{"Active": "Y"}' | http PUT localhost:8000/awsacc/01234567810
  - echo '{"Active": "Y", "Description": "Debs purple Test Account 2"}' | http PUT localhost:8000/awsacc/01234567810
  - echo '{"AccOwners": "Deborah Balm, Chris Allison" }' | http PUT localhost:8000/awsacc/01234567810