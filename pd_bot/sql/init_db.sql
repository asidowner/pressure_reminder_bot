create table if not exists Pressure
(
    [chat_id]          bigint   not null,
    [date_]            datetime not null,
    systolic_pressure  int      not null,
    diastolic_pressure int      not null,
    pulse              int      not null
);

