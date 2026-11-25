-- Databases for the discovery of the template PostgreSQL Custom. Without
-- template1: the plugin keeps its connections open, and CREATE DATABASE
-- fails while template1 has a connection. The role updates the extensions
-- of template1 itself.
SELECT datname FROM pg_database WHERE datallowconn AND NOT datistemplate ORDER BY datname
