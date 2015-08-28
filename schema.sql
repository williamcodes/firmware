
create table temperatures (
       xbee_id,
       cell_id not null,
       temperature not null,
       sleep_period,
       time not null default (strftime('%s', 'now')),
       relayed_time
);

create table status as select
       null as xbee_id_high,
       null as xbee_id_low,
       null as sleep_period;
