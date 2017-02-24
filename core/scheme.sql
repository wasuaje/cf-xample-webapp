drop table if exists entries;
drop table if exists config;
create table entries (
  id integer primary key autoincrement,
  lob text not null,
  app text not null,
  version text not null,
  env text not null,
  last_update text not null
);

create table config (
  id integer primary key autoincrement,
  last_update datetime not null
);



