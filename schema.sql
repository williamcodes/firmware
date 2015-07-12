
create table readings (cell_id, time, temperature);

create table transmitted as select 0 as reading_id;

create table xbee_id as select null as high, null as low;
