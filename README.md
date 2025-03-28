# 📌 Flask Backend con Arquitectura Hexagonal

Este proyecto es una aplicación backend desarrollada con **Flask**, basada en la **arquitectura hexagonal** (*Ports and Adapters*). La estructura permite un código **modular, mantenible y desacoplado**, facilitando la escalabilidad y la integración con múltiples tecnologías.

## 🚀 Características
- 🔹 **Arquitectura hexagonal**: Desacopla la lógica de negocio de la infraestructura.
- 🔹 **Modularidad**: Fácil de extender y mantener.
- 🔹 **Base de datos flexible**: Se puede cambiar la implementación de la BD sin afectar la lógica de negocio.
- 🔹 **Testabilidad**: Permite probar cada componente de forma independiente.

---

## 📂 Estructura del Proyecto

```
my_project/
│── app/
│   ├── domain/                 # 🟢 Capa de Dominio (Negocio)
│   │   ├── entities/           # 📌 Entidades de negocio
│   │   ├── repositories/       # 📌 Interfaces de repositorios
│   │   ├── services/           # 📌 Casos de uso y lógica de negocio
│
│   ├── application/            # 🔵 Capa de Aplicación
│   │   ├── dtos/               # 📌 DTOs para transferencia de datos
│   │   ├── commands/           # 📌 Comandos para casos de uso
│   │   ├── queries/            # 📌 Consultas
│
│   ├── infrastructure/         # 🟠 Capa de Infraestructura
│   │   ├── config.py           # 📌 Configuración
│   │   ├── database.py         # 📌 Conexión a la BD
│   │   ├── repositories/       # 📌 Implementaciones concretas de los repositorios
│   │   ├── external_services/  # 📌 Conexión con APIs externas
│
│   ├── adapters/               # 🟣 Capa de Adaptadores
│   │   ├── controllers/        # 📌 Endpoints Flask (API REST)
│   │   ├── cli/                # 📌 Comandos de consola
│
│   ├── main.py                 # 📌 Punto de entrada de la aplicación
│   ├── routes.py               # 📌 Registro de rutas
│
├── tests/                      # 📌 Pruebas unitarias
├── requirements.txt            # 📌 Dependencias
├── .env                        # 📌 Variables de entorno
├── README.md                   # 📌 Documentación del proyecto
```

---

## 🛠 Instalación y Configuración

### 1️⃣ **Clonar el repositorio**
```bash
$ git clone https://github.com/tu_usuario/tu_repositorio.git
$ cd tu_repositorio
```

### 2️⃣ **Crear un entorno virtual y activarlo**
```bash
$ python -m venv venv
$ source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3️⃣ **Instalar dependencias**
```bash
$ pip install -r requirements.txt
```

### 4️⃣ **Configurar variables de entorno**
Crear un archivo `.env` con la configuración necesaria, por ejemplo:
```ini
DATABASE_URL=mongodb://localhost:27017/my_database
SECRET_KEY=supersecreto
```

### 5️⃣ **Ejecutar la aplicación**
```bash
$ python main.py
```
La API estará disponible en: `http://127.0.0.1:5000/`

---

## 🔥 Uso de la API

### 📌 **Usuarios**
#### 🔹 Crear un usuario
```http
POST /users
```
**Body:**
```json
{
  "user_id": 1,
  "name": "Juan Pérez",
  "email": "juan@example.com"
}
```

#### 🔹 Obtener usuario por ID
```http
GET /users/1
```

---

## ✅ Pruebas
Para ejecutar las pruebas unitarias:
```bash
$ pytest tests/
```

---

## 🏗️ Tecnologías Utilizadas
- **Flask** - Framework web ligero en Python
- **DynamoDB** - Base de datos
- **Dotenv** - Manejo de variables de entorno
- **Pytest** - Framework de pruebas
- **Docker (opcional)** - Para contenedores
