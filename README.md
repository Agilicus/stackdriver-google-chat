# stackdriver-google-chat

Convert from a Stackdriver webhook into a Google Chat format

Set two env vars:
- TOKEN : url will be http[s]://DOMAIN?token=TOKEN
- URL : url to POST to Google chat (the inbound webhook)

An incident will be notified as:
```
{
    "incident": {
        "condition_name": "Uptime Health Check on api-noc-users",
        "ended_at": null,
        "incident_id": "0.ligwyr056k2l",
        "policy_name": "api - noc - users",
        "resource": {
            "labels": {
                "host": "api.agilicus.com"
            },
            "type": "uptime_url"
        },
        "resource_id": "",
        "resource_name": "agilicus Uptime Check URL labels {host=api.agilicus.com}",
        "started_at": 1579559444,
        "state": "open",
        "summary": "An uptime check on agilicus Uptime Check URL labels {host=api.agilicus.com} is failing.",
        "url": "https://app.google.stackdriver.com/incidents/0.ligwyr056k2l?project=agilicus"
    },
    "version": "1.2"
}
```

And return to health:
```
{
    "incident": {
        "condition_name": "Uptime Health Check on api-noc-users",
        "ended_at": 1579559552,
        "incident_id": "0.ligwyr056k2l",
        "policy_name": "api - noc - users",
        "resource": {
            "labels": {
                "host": "api.agilicus.com"
            },
            "type": "uptime_url"
        },
        "resource_id": "",
        "resource_name": "agilicus Uptime Check URL labels {host=api.agilicus.com}",
        "started_at": 1579559444,
        "state": "closed",
        "summary": "The uptime check for agilicus Uptime Check URL labels {host=api.agilicus.com} has returned to a normal state.",
        "url": "https://app.google.stackdriver.com/incidents/0.ligwyr056k2l?project=agilicus"
    },
    "version": "1.2"
}
```

