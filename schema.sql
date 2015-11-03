
create table temperatures (
       cell_id not null,
       temperature not null,
       sleep_period not null,
       time not null default (strftime('%s', 'now')),
