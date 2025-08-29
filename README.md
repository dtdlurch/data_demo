
# Data Engineering Demo (BigQuery + dbt + Airflow + CI)


## Contents

- `dbt/`: dbt project with staging + marts models and tests, targeting BigQuery.
- `airflow/`: Dockerized Airflow running a DAG that triggers `dbt build`.
- `.github/workflows/ci.yml`: CI pipeline to run dbt on PR and main.
- `scripts/posthog_event.py`: optional telemetry example. (not yet fully implemented)

---

*Successful dbt run on main on 8/29/25
