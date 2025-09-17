# 🚀 Airflow Local con Docker

Este proyecto proporciona una instalación completa de Apache Airflow con Docker para desarrollo local, incluyendo autenticación de usuarios y un DAG de ejemplo.

## 📋 Características

- ✅ Apache Airflow 2.7.0
- ✅ PostgreSQL como base de datos
- ✅ Docker Compose para orquestación
- ✅ Usuarios preconfigurados (admin/user)
- ✅ DAG ejemplo "Hola Mundo"
- ✅ Volúmenes persistentes para DAGs y logs
- ✅ Entorno listo para desarrollo Python

## 🛠 Prerrequisitos

- **Docker Desktop** instalado y ejecutándose
- **Docker Compose** (viene incluido con Docker Desktop)
- **Git** (opcional)

## 🚀 Instalación y Ejecución

### 1. Clonar/Descargar el proyecto

```bash
mkdir airflow-project
cd airflow-project
```

### 2. Crear la estructura de directorios

```bash
mkdir -p dags logs plugins scripts
```

### 3. Crear los archivos necesarios

Crea los archivos `docker-compose.yaml`, `Dockerfile`, `requirements.txt`, y `dags/hola_mundo.py` con el contenido proporcionado.

### 4. Iniciar los contenedores

```bash
docker-compose up -d --build
```

### 5. Verificar el estado

```bash
docker-compose ps
```

## 👤 Acceso a la Interfaz Web

- **URL:** http://localhost:8080
- **Usuario admin:** `admin` / `admin`
- **Usuario regular:** `user` / `user`

## 📊 DAG de Ejemplo: Hola Mundo

El proyecto incluye un DAG demostrativo (`hola_mundo_dag`) que:

1. Imprime un mensaje "¡Hola Mundo desde Airflow!"
2. Crea y procesa un DataFrame de pandas con datos de ejemplo
3. Muestra el poder de los PythonOperator en Airflow

### Para ejecutar el DAG:

1. Accede a http://localhost:8080
2. Encuentra `hola_mundo_dag` en la lista
3. Haz clic en el toggle para activarlo (si no está activo)
4. Haz clic en ▶ **Trigger DAG** para ejecutarlo manualmente
5. Ve a la pestaña "Graph" para ver el progreso

## 📁 Estructura del Proyecto

```
airflow-project/
├── docker-compose.yaml    # Configuración de contenedores
├── Dockerfile            # Personalización de la imagen
├── requirements.txt      # Dependencias de Python
├── dags/
│   └── hola_mundo.py    # DAG ejemplo "Hola Mundo"
├── logs/                # Logs de ejecución (persistentes)
├── plugins/             # Plugins personalizados
└── scripts/
    └── init.sh          # Script de inicialización
```

## 🐛 Troubleshooting

### Ver logs de los contenedores:

```bash
# Todos los servicios
docker-compose logs

# Servicio específico
docker-compose logs airflow-webserver
docker-compose logs airflow-scheduler
docker-compose logs postgres
```

### Reiniciar servicios:

```bash
docker-compose restart
```

### Detener y eliminar contenedores:

```bash
docker-compose down
```

### Si los DAGs no aparecen:

```bash
# Reiniciar el scheduler
docker-compose restart airflow-scheduler
```

## 🎯 Comandos Útiles

```bash
# Ejecutar comandos de Airflow directamente
docker-compose exec airflow-webserver airflow version
docker-compose exec airflow-webserver airflow dags list

# Ver task instances
docker-compose exec airflow-webserver airflow tasks list hola_mundo_dag

# Ver variables de configuración
docker-compose exec airflow-webserver airflow config list
```

## 🔧 Personalización

### Agregar nuevos DAGs:
Coloca tus archivos `.py` en la carpeta `dags/` y se cargarán automáticamente.

### Agregar dependencias Python:
Edita `requirements.txt` y reconstruye:

```bash
docker-compose up -d --build
```

### Configuración personalizada:
Modifica las variables de entorno en `docker-compose.yaml` o crea un archivo `config/airflow.cfg`.

## 📝 Próximos Pasos

1. Explorar la UI de Airflow y sus funcionalidades
2. Crear tus propios DAGs en la carpeta `dags/`
3. Agregar conexiones a bases de datos externas
4. Configurar variables de Airflow para parámetros
5. Explorar operadores adicionales (Python, Bash, SQL, etc.)

## 📚 Recursos Útiles

- [Documentación oficial de Airflow](https://airflow.apache.org/docs/)
- [Guía de conceptos de Airflow](https://airflow.apache.org/docs/apache-airflow/stable/concepts/)
- [Ejemplos de DAGs](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)

## 🆘 Soporte

Si encuentras problemas:

1. Verifica que Docker Desktop esté ejecutándose
2. Revisa los logs con `docker-compose logs`
3. Asegúrate de que los puertos 8080 y 5432 no estén en uso

---

¡Listo para comenzar a trabajar con Apache Airflow! 🎉