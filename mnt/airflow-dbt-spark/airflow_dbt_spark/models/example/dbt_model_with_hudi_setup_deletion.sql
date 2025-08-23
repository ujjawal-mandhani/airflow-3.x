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
    select 1 as id, current_timestamp() as updated_at, 'active' as status_col
    union all
    select 2 as id, current_timestamp() as updated_at, 'active' as status_col
),
delete_data as (
    select max(id) as id, current_timestamp() as updated_at, null as status_col
    from source_data
)


select *
from source_data
UNION ALL 
select * 
from delete_data