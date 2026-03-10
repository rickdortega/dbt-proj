FROM postgres:latest

ENV POSTGRES_DB=warehouse
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

COPY sql/init.sql /docker-entrypoint-initdb.d/init.sql