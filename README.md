# CTF Manager

A manager for your CTFs. Manage teams, flags and their validation.

## Work In Progress

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
