# CEC Medical — Sistema de Gestión de Inventario

Sistema web desarrollado para **CEC Medical** con el objetivo de centralizar y facilitar la administración de equipos médicos, repuestos, herramientas, órdenes de trabajo y movimientos de inventario.

La aplicación permite llevar un control de las existencias, registrar entradas y salidas de repuestos, controlar los componentes utilizados durante las reparaciones y mantener un historial mediante un Kardex de movimientos.

---

## 1. Descripción del proyecto

El sistema permite digitalizar los procesos relacionados con la gestión del inventario y mantenimiento de equipos médicos de CEC Medical.

Entre las principales funcionalidades se encuentran:

* Gestión de usuarios.
* Gestión de equipos médicos.
* Gestión de marcas.
* Gestión de repuestos e insumos.
* Gestión de herramientas.
* Gestión de órdenes de trabajo.
* Registro de repuestos utilizados en reparaciones.
* Devolución de repuestos al inventario.
* Registro de entradas de inventario.
* Registro de egresos de inventario.
* Registro de devoluciones.
* Kardex de movimientos.
* Control de stock.
* Control de stock mínimo.
* Validación de stock disponible.
* Asociación de repuestos con órdenes de trabajo.
* Registro del usuario que realiza cada movimiento.
* Control de acceso mediante autenticación de Django.

---

# 2. Tecnologías utilizadas

## Backend

* Python 3.10+
* Django
* PostgreSQL
* psycopg2-binary

## Frontend

* HTML5
* Django Templates
* Tailwind CSS mediante CDN
* JavaScript

## Base de datos

* PostgreSQL

## Control de versiones

* Git
* GitHub

---

# 3. Requisitos previos

Antes de instalar el proyecto se debe disponer de:

### Python

Se recomienda utilizar:

```text
Python 3.10 o superior
```

Para verificar la versión:

```bash
python --version
```

En Windows también puede utilizarse:

```bash
py --version
```

---

### PostgreSQL

Instalar PostgreSQL y asegurarse de que el servidor se encuentre ejecutándose.

Durante la instalación se debe recordar:

* Usuario de PostgreSQL.
* Contraseña.
* Puerto.
* Nombre de la base de datos.

El puerto utilizado normalmente es:

```text
5432
```

Para este proyecto se utiliza PostgreSQL como motor de base de datos.

---

### Git

Verificar la instalación:

```bash
git --version
```

---

# 4. Clonar el proyecto

Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
```

Entrar al directorio:

```bash
cd nombre-del-proyecto
```

Ejemplo:

```bash
cd repoPrueba
```

---

# 5. Crear entorno virtual

Se recomienda utilizar un entorno virtual para evitar conflictos entre las dependencias del proyecto y las instaladas globalmente.

En Windows:

```bash
python -m venv venv
```

Activar el entorno:

```bash
venv\Scripts\activate
```

Si se utiliza PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Una vez activado debería aparecer algo similar a:

```text
(venv) C:\proyecto>
```

---

# 6. Instalar dependencias

Actualizar pip:

```bash
python -m pip install --upgrade pip
```

Instalar Django:

```bash
pip install django
```

Instalar el controlador de PostgreSQL:

```bash
pip install psycopg2-binary
```

Si el proyecto contiene un archivo `requirements.txt`, se recomienda utilizar:

```bash
pip install -r requirements.txt
```

---

# 7. Crear la base de datos PostgreSQL

Abrir PostgreSQL mediante **pgAdmin** o `psql`.

Crear la base de datos:

```sql
CREATE DATABASE cec_medical_db;
```

La configuración utilizada por el proyecto debe coincidir con la configuración de `settings.py`.

Ejemplo:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cec_medical_db',
        'USER': 'postgres',
        'PASSWORD': 'TU_CONTRASEÑA',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

> No se debe subir la contraseña real de PostgreSQL al repositorio.

---

# 8. Configuración de Django

Abrir:

```text
cec_medical/settings.py
```

Verificar principalmente:

```python
INSTALLED_APPS
```

Debe incluir la aplicación:

```python
'inventario',
```

También verificar la configuración de PostgreSQL:

```python
DATABASES
```

Ejemplo:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cec_medical_db',
        'USER': 'postgres',
        'PASSWORD': 'TU_CONTRASEÑA',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

# 9. Aplicar migraciones

Después de configurar la base de datos ejecutar:

```bash
python manage.py makemigrations
```

Luego:

```bash
python manage.py migrate
```

Las migraciones crean las tablas necesarias para:

* Usuarios.
* Equipos médicos.
* Marcas.
* Repuestos.
* Herramientas.
* Órdenes de trabajo.
* Movimientos de inventario.
* Sesiones de Django.
* Administración de Django.

---

# 10. Crear usuario administrador

Para crear un usuario administrador:

```bash
python manage.py createsuperuser
```

Django solicitará:

```text
Username:
Email:
Password:
Password (again):
```

Después se podrá ingresar al panel administrativo:

```text
http://127.0.0.1:8000/admin/
```

---

# 11. Ejecutar el sistema

Ejecutar:

```bash
python manage.py runserver
```

La aplicación estará disponible normalmente en:

```text
http://127.0.0.1:8000/
```

Para acceder desde otro dispositivo dentro de la misma red:

```bash
python manage.py runserver 0.0.0.0:8000
```
---

# 12. Autor

**Braulio Castillo**
