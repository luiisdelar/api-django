insert into api_permiso (id, name) values
(1, 'add_user'), (2, 'changue_user'), (3, 'delet_user'),
(4, 'add_rol'), (5, 'changue_rol'), (6, 'delet_rol');

insert into api_rol (id, name) values
(1, 'administrator'), (2, 'create_users');

insert into api_rol_permisos (id, rol_id, permiso_id) values
(1, 1, 1), (2, 1, 2), (3, 1, 3), (4, 1, 4), 
(5, 1, 5), (6, 1, 6), (7, 2, 1), (8, 2, 2);

insert into auth_user (id, password, is_superuser, username, email, is_staff, rol, user_verified) values
(1, 'pbkdf2_sha256$216000$759YSkZsKDmD$PjHr6cj/chYofRwmI1AXfkairJEcdZzXasIQkFMc0T0=', true, 'admin', 'admin@admin.com', true, 'administrator', true);