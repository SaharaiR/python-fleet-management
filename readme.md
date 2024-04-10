Tutorial crear BD en Vercel:
https://vercel.com/docs/storage/vercel-postgres/quickstart

CREAR TABLA DE taxis:
CREATE TABLE taxis (
   id INT PRIMARY KEY,
   plate VARCHAR(10) NOT NULL
);

CREAR TABLA DE trajectories:
CREATE TABLE trajectories(
    id SERIAL PRIMARY KEY,
    taxi_id INT NOT NULL,
    date TIMESTAMP NOT NULL,
    latitude NUMERIC(9,6) NOT NULL,
    longitude NUMERIC(9,6) NOT NULL,
    FOREIGN KEY (taxi_id) REFERENCES taxis(id)
);