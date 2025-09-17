#!/bin/bash

# Esperar a que PostgreSQL esté listo
echo "Esperando a PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 1
done

echo "PostgreSQL está listo"

# Inicializar la base de datos de Airflow
airflow db init

# Crear usuario administrador
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Crear usuario regular
airflow users create \
    --username user \
    --password user \
    --firstname Regular \
    --lastname User \
    --role User \
    --email user@example.com

echo "Usuarios creados:"
echo "Admin: admin/admin"
echo "User: user/user"