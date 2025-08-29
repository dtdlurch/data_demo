
-- Take the top name by state/gender
with ranked as (
  select
    state, gender, name, total,
    row_number() over (partition by state, gender order by total desc) as rn
  from {{ ref('stg_popular_names') }}
)
select state, gender, name, total
from ranked
where rn = 1
