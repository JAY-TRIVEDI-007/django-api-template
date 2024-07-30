-- Create database
CREATE DATABASE {{cookiecutter.project_slug}};

-- Create User and assign permissions
CREATE USER '{{cookiecutter.project_slug}}_app'@'%' IDENTIFIED BY '<APP_PASSWORD>';
REVOKE ALL PRIVILEGES ON *.* FROM '{{cookiecutter.project_slug}}_app'@'%';
GRANT ALL PRIVILEGES ON {{cookiecutter.project_slug}}.* TO '{{cookiecutter.project_slug}}_app'@'%';
