create_table_raw_turnstile = """
create table if not exists turnstile(
    c_a varchar,
    unit varchar,
    scp varchar,
    station varchar,
    linename varchar,
    division varchar,
    recorded_date date,
    recorded_time time,
    des varchar,
    entries integer,
    exits integer
);
"""


drop_table_raw_turnstile = """
drop table if exists turnstile;
"""


populate_table_raw_turnstile = """
COPY turnstile
FROM STDIN
DELIMITER ',' CSV HEADER;
"""

create_table_queries = [create_table_raw_turnstile]
drop_table_queries = [drop_table_raw_turnstile]