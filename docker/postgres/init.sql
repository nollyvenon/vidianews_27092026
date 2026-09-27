-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Set statement timeout to 30 seconds
SET statement_timeout TO '30s';

-- Create schema
CREATE SCHEMA IF NOT EXISTS public;
GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;

-- Log initial setup
SELECT 'PostgreSQL initialized' as status;
