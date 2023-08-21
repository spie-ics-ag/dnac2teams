# dnac2teams

## Overview
dnac2teams is a simple webhook receiver for Cisco DNA Center notifications, forwarding all notifications events to a Microsoft Teams incoming webhook.

DNAC notifications will be displayed as Adaptive Cards in MS Teams:
![Adaptive Card](teamsac.png)

## Installation 

##  Prerequisites
- Add an incoming webhook to a MS Teams team/space ([howto](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook))
- If using the preferred AWS/SAM installation method [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) must be installed

##  AWS Serverless Application Model (SAM)
dnac2teams is using the AWS Serverless Application Model (Lambda+API-Gateway) and is best installed via SAM CLI.


- You must be logged in to AWS (via AWS CLI) 
- You need either full admin permissions or sufficient permissions on the following services:
  - Lambda
  - API Gateway
  - S3
  - Cloud Formation
  - IAM

1. Clone the repo:
    ```bash
    git clone https://github.com/maercu/dnac2teams.git
    ```
2. Go to your project folder:
    ```bash
    cd dnac2teams
    ```
3. Edit the `template.yaml` file - Change the global environment variables (line numbers 13/14) for the Teams incoming webhook URL and the authentication token:
    ```yaml
    TEAMS_URL: https://company.webhook.office.com/webhookb2/webhookid
    AUTH_TOKEN: yoursupersecrettoken
    ```
4. Build the SAM app
    ```bash
    sam build --use-container
    ```
5. Deploy the app
    ```bash
    sam deploy --guided
    ```

Once deployed the public endpoint URL is displayed in the SAM output, use this URL and the token (specified in point 3) to create the webhook in DNAC.

## On-prem installation options
For on-prem installations, there is a simple Flask-RESTX based receiver available.

Clone the repo:
```bash
 git clone https://github.com/maercu/dnac2teams.git
```
Go to your project folder:
```bash
cd dnac2teams
```

Deploy the app using docker or in a Python3 virtual environment

### Docker
1. Edit the `Dockerfile` file - Change the environment variables (line numbers 3/4) for the Teams incoming webhook URL and the authentication token:
    ```Dockerfile
    ENV TEAMS_URL=https://company.webhook.office.com/webhookb2/webhookid
    ENV AUTH_TOKEN=yoursupersecrettoken
    ```
2. Build the container image:
    ```bash
    docker build -t dnac2teams .
    ```  
3. Run the container:
    ```bash
    docker run --rm -p 5000:5000 dnac2teams
    ```  

### Python
1. Create a virtual environment:
    ```bash
    python3 -m venv .venv
    ```
2. Activate your venv:
    ```bash
    source .venv/bin/activate
    ```
3. Install dependencies:
    ```bash
    pip install pip --upgrade
    pip install -r requirements.txt
    ```
4. Configure the webhook URL and the authentication token as environment variables:
    ```bash
    export TEAMS_URL=https://company.webhook.office.com/webhookb2/webhookid
    export AUTH_TOKEN=yoursupersecrettoken
    ```
5. Run the app:
    ```bash
    cd dnac_to_teams
    python flaskapp.py
    ```  

### On-prem webhook endpoint
After starting either the Docker container or Python script, the webhook endpoint is available at [http://localhost:5000/prod/dnac2teams](http://localhost:5000/prod/dnac2teams). If you need a public endpoint, use [ngrok](https://ngrok.com/)

## Troubleshooting
### Webhook configuration in DNAC
The secret-token must be used as a bearer token. In DNAC use *Basic* as the authentication method, this will set the authorization header, as the header value enter *Bearer yourToken* (replace "yourToken" with the value of the AUTH-TOKEN variable). 
 
