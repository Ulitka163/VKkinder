create table if not exists user_vk (
	id serial primary key,
	vk_id varchar(40) not null unique
);

create table if not exists user_search (
	user_id integer references user_vk(id), 
	vk_id_search varchar(40) not null
);

create table if not exists user_info (
	id integer  primary key references user_vk(id),
	name varchar(40) not null,
	sex integer,
	city varchar(40),
	birth_year varchar(40)
);