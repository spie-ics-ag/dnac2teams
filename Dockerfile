FROM python:3.11.4-alpine

ENV TEAMS_URL=https://company.webhook.office.com/webhookb2/webhookid
ENV AUTH_TOKEN=yoursupersecrettoken

EXPOSE 5000

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dnac_to_teams/flaskapp.py .
COPY dnac_to_teams/teamsproxy.py .

CMD [ "python", "./flaskapp.py" ]