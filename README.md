# CTF Manager

![pipeline](https://github.com/tanguynicolas/CTF-Manager/actions/workflows/container.yml/badge.svg)
[![PR's Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)
[![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/)

A manager for your CTFs. Manage teams, flags and their validation.

  Team dasboard               |  API docs
:----------------------------:|:----------------------:
 ![](docs/team_dashboard.png) | ![](docs/api_docs.png)

## Configuration

Set environment variable.

| Variable         | Default                      |
| ---------------- | ---------------------------- |
| `MONGODB_URL`    | mongodb://localhost/ (`str`) |
| `KAFKA_ENABLE`   | false (`bool`)               |
| `KAFKA_HOSTNAME` | localhost (`str`)            |
| `KAFKA_PORT`     | 9092 (`str`)                 |
| `KAFKA_TOPIC`    | ctfmanager (`str`)           |

Use `MONGODB_URL` to pass username and password: like `MONGODB_URL=mongodb://manager:password@1.2.3.4:27017`. Be careful at password format.

You **can** use Kafka to send information in JSON to a topic that a team has found a flag. You can then use another application like [this one](https://github.com/tanguynicolas/Audio-Playback-from-Kafka) to play a sound based on the tags associated with the flag.

## My full setup

### Docker Compose

If you use my full setup, with Docker Compose, you need to create `.env` file (to accessing variable from `docker-compose.yml`) with:

```shell
MONGODB_USERNAME=""
MONGODB_PASSWORD=""
MONGODB_URL=""

EXTERNAL_IP=""

GCLOUD_PDC_SIGNING_TOKEN=""
GCLOUD_HOSTED_GRAFANA_ID=""
GCLOUD_PDC_CLUSTER=""
```

### Data vizualisation

1. You have to create Grafana Cloud account.
2. Then add Private Datasource Connector
3. Then add MongoDB datasource
4. Then add dashboards (see `dashboards/`)
