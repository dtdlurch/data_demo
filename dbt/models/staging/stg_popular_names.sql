
-- Aggregate counts by state, gender, name from public dataset
select
  state,
  gender,
  name,
  sum(number) as total
from `bigquery-public-data.usa_names.usa_1910_2013`
group by 1,2,3
