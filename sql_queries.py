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
    exits integer,
    primary key(unit, scp, station, recorded_date, recorded_time, des)
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


transform_table_raw_turnstile = """
DROP TABLE IF EXISTS turnstile_transformed;
SELECT 
    * 
INTO 
    turnstile_transformed
FROM
    (
    SELECT 
        station, 
        unit, 
        scp, 
        linename, 
        recorded_date, 
        recorded_time, 
        entries, 
        abs(entries - FIRST_VALUE(entries) OVER (
            PARTITION BY 
                station, 
                scp, 
                unit
            ORDER BY
                recorded_date DESC,
                recorded_time DESC 
            ROWS BETWEEN 1 FOLLOWING AND UNBOUNDED FOLLOWING
        )) as entry_count
    FROM turnstile
    WHERE division='BMT' or division='IND' or division='IRT'
    ) as f
WHERE entry_count is not null
"""

create_table_queries = [create_table_raw_turnstile]
drop_table_queries = [drop_table_raw_turnstile]