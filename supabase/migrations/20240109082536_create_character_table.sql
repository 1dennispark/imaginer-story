create table if not exists character (
  id serial primary key,
  name varchar(128),
  mbti varchar(128),
  gender varchar(128),
  age varchar(128),
  description varchar(256),
  profile_image varchar(256),
  original_images json
);