
# Data Engineering Mini-Demo (BigQuery + dbt + Airflow + CI)

This is a tiny, interview-ready demo that proves you can:
- Run **dbt** models on **BigQuery** (with tests).
- Orchestrate a run via **Airflow** (Docker).
- Use **CI** (GitHub Actions) to run `dbt build` on pull requests and on main.
- (Optional) Send an event to **PostHog** to show basic instrumentation.

> Goal: small, high-signal repo you can talk through in 5 minutes.

---

## Contents

- `dbt/`: dbt project with staging + marts models and tests, targeting BigQuery.
- `airflow/`: Dockerized Airflow running a DAG that triggers `dbt build`.
- `.github/workflows/ci.yml`: CI pipeline to run dbt on PR and main.
- `scripts/posthog_event.py`: optional telemetry example.

---

## Prereqs

- **GCP project** with BigQuery enabled.
- A **service account** with BigQuery permissions (BigQuery Job User, BigQuery Data Editor is plenty for demo).
- Download the JSON key for this service account.

### Quick GCP Setup (high level)
1) Create a dataset `demo_dbt` in BigQuery (or choose another name).  
2) Create a service account and grant it BigQuery permissions.  
3) Download the key `gcp.json`.

---

## Local dbt (without Airflow)

1) Install `dbt-bigquery` locally (optional if you only use CI):  
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install dbt-bigquery
   ```

2) Create `dbt/profiles/profiles.yml` (or copy from `profiles.yml.example`) and set:
   - `project` = your GCP project id
   - `dataset` = `demo_dbt` (or your dataset)
   - `keyfile` = absolute path to your `gcp.json`

3) Run:
   ```bash
   cd dbt
   dbt deps
   dbt build --profiles-dir ./profiles
   ```

If it works, you’ll see tests pass and two tables/views appear in your dataset.

---

## Airflow (Docker)

1) Put your service account key at `airflow/secrets/gcp.json` (not committed).
2) From repo root:
   ```bash
   export AIRFLOW_UID=$(id -u)  # on mac/linux; on windows set a number like 50000
   docker compose -f airflow/docker-compose.yml up -d
   ```
3) Visit Airflow web UI at http://localhost:8080 (user: `airflow`, pass: `airflow`).
4) Trigger DAG: **dbt_bigquery_demo**.

The DAG has two steps:
- A lightweight "extract" placeholder
- `dbt build` pointing to this repo’s dbt project

---

## CI (GitHub Actions)

In your GitHub repo settings, add secrets:
- `GCP_SA_KEY` – the **entire** JSON of your service account key
- `GCP_PROJECT_ID` – your project id
- `DBT_DATASET` – e.g., `demo_dbt`
- `GCP_LOCATION` – e.g., `US`

CI will:
- On PR: install `dbt-bigquery`, write `gcp.json` + `profiles.yml` dynamically, run `dbt build`.
- On push to `main`: same as PR (you can extend to deploy docs, build images, etc.).

---

## Optional: PostHog event

1) Create a (free) PostHog project and get your API key (Project API Key).  
2) Add secrets (for CI) or env vars (local):
   - `POSTHOG_API_KEY` and optional `POSTHOG_HOST` (defaults to https://app.posthog.com)
3) Run:
   ```bash
   python scripts/posthog_event.py
   ```

This sends a one-off “pipeline_run” event with a timestamp.

---

## Talking points (interview-ready)

- **Data modeling**: staging model aggregates raw public data; marts selects top-N by partition.  
- **Testing**: not-null & unique tests demonstrate quality gates.  
- **Orchestration**: simple Airflow DAG with `BashOperator` to run dbt; easy to extend with sensors/SLAs.  
- **CI**: PR checks run `dbt build`, preventing broken models from merging.  
- **Security**: credentials via secrets; nothing sensitive in repo.  
- **Next steps** (if asked): add freshness checks, sources, slim CI artifacts, and (optionally) Datadog/Stackdriver logging.

---

## Safety

- Do **NOT** commit `gcp.json`. It’s ignored by `.gitignore` and lives only locally or in GitHub Secrets.
- The demo reads from a public dataset: `bigquery-public-data.usa_names.usa_1910_2013`.

Good luck—ship it!
