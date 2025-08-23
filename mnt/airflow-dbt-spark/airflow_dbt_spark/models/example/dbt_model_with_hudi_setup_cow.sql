
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml
    materialized='table',
    Try changing "table" to "view" below
    'hoodie.keep.min.commits': '1',
    'hoodie.keep.max.commits': '1',
    'hoodie.cleaner.policy': 'KEEP_LATEST_COMMITS'
*/

{{ config(
    materialized='incremental',
    file_format='hudi',
    unique_key='id',
    options={
      'type': 'COPY_ON_WRITE',
      'primaryKey': 'id',
      'preCombineField': 'updated_at',
      'hoodie.parquet.compression.codec': 'snappy',
      'parquet.compression': 'SNAPPY'
    },
    tags=["hudi"]
) }}

with source_data as (

    select 1 as id, current_timestamp() as updated_at
    union all
    select 2 as id, current_timestamp() as updated_at

)

select *
from source_data

/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null
