create table IF NOT EXISTS entries (
  id INT AUTO_INCREMENT,
  lob text not null,
  app text not null,
  version text not null,
  env text not null,
  last_update text not null,
    PRIMARY KEY (id) );
create table IF NOT EXISTS config (
  id INT AUTO_INCREMENT,
  last_update datetime not null,
      PRIMARY KEY (id) );