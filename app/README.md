# Inkarri - Sistema de Gestión con Empresas Indígenas

## Registro y Gestión de Usuarios

Este módulo implementa las reglas de negocio para el registro y gestión de usuarios en la plataforma Inkarri, enfocándose específicamente en la validación y aprobación de clientes y empresas indígenas.

## Reglas de Negocio Implementadas

- **RN01**: Un cliente no podrá acceder al sistema hasta que su cuenta haya sido aprobada por un administrador.
- **RN02**: Una empresa indígena no podrá ofertar productos o servicios hasta que su registro haya sido validado por un administrador.
- **RN03**: Los administradores son los únicos con permisos para aprobar o rechazar registros de clientes y empresas.
- **RN04**: Cada usuario tendrá un tipo de rol que determinará sus permisos: Administrador, Cliente, Empresa Indígena.

## Estructura del Proyecto

El módulo sigue una arquitectura hexagonal (puertos y adaptadores) con las siguientes capas:

```
app/
├── domain/
│   ├── entities/
│   │   └── user.py                 # Entidad de usuario
│   ├── repositories/
│   │   └── user_repository.py      # Interfaz de repositorio
│   └── services/
│       ├── user_service.py         # Servicio de usuarios
│       └── admin_service.py        # Servicio de administración
├── infrastructure/
│   └── repositories/
│       └── user_repository_impl.py # Implementación del repositorio
├── adapters/
│   └── controllers/
│       └── user_controller.py      # Controlador REST
└── tests/
    ├── conftest.py                 # Configuración de pruebas
    ├── domain/
    │   └── services/
    │       ├── test_user_service.py
    │       └── test_admin_service.py
    └── integration/
        └── test_user_workflow.py   # Pruebas de integración
```

## Características Implementadas

### Entidades

- **User**: Modelo de usuario con atributos como nombre, email, contraseña, rol y estado de aprobación.
  - Estados posibles: `pending`, `approved`, `rejected`
  - Roles implementados: `admin`, `client`, `indigenous_company`

### Servicios

- **UserService**:

  - Registro de usuarios con validación de datos
  - Cifrado de contraseñas con Werkzeug Security
  - Estado inicial "pending" para nuevos usuarios
  - Gestión de cambios de estado
- **AdminService**:

  - Validación de permisos de administrador
  - Aprobación de usuarios pendientes
  - Rechazo de usuarios con motivo
  - Verificación de roles y permisos

### Seguridad

- Contraseñas cifradas mediante hash
- Validación de permisos por rol
- Validación de datos de entrada

## Pruebas Implementadas

Las pruebas verifican todas las reglas de negocio y garantizan el correcto funcionamiento del módulo.

### Pruebas Unitarias

- **TestUserService**:

  - Registro de usuarios con datos válidos
  - Validación de datos de entrada
  - Validación de roles
  - Cambio de estado de usuarios
- **TestAdminService**:

  - Aprobación de usuarios por administradores
  - Rechazo de usuarios por administradores
  - Verificación de permisos administrativos
  - Manejo de errores

### Pruebas de Integración

- **TestUserWorkflow**:
  - Flujo completo de registro de cliente y aprobación
  - Flujo completo de registro de empresa indígena y rechazo
  - Verificación de roles y estados en cada paso

## Ejecución de Pruebas

Para ejecutar las pruebas con salida detallada:

```bash
python -m pytest app/tests -v -s
```

### Resultados de las Pruebas

Las pruebas muestran el proceso completo de aplicación de las reglas de negocio:

```
=== Test: Registro de usuario con datos válidos ===
- Creando servicio de usuario con repositorio mock
- Preparando datos de usuario cliente
- Registrando usuario: John Doe, john@example.com, role=client
- Verificando que el usuario fue creado correctamente
- Verificando nombre: John Doe
- Verificando email: john@example.com
- Verificando rol: client
- Verificando estado: pending
- Verificando que la contraseña fue cifrada
- Verificando que se llamó al método save del repositorio
✓ Test completado con éxito

=== Test: Aprobación de usuario por administrador ===
- Creando servicios de admin y usuario con repositorio mock
- Creando un usuario cliente en estado 'pending'
- Usuario creado con ID: 1 y estado: pending
- Usando administrador con ID: admin1
- Administrador aprobando al usuario
- Verificando que el estado cambió a 'approved'
- Verificando que se llamó al método update del repositorio
✓ Test completado con éxito - RN03 verificada

=== Prueba de Integración: Flujo completo de registro y aprobación ===
- Creando servicios de usuario y admin
- Usando administrador con ID: admin1

>> PASO 1: Registro de usuario cliente (RN04)
- Registrando cliente: John Client, john@example.com, role=client
- Cliente creado con ID: 1
- Verificando estado inicial: pending (RN01)

>> PASO 2: Administrador aprueba al cliente (RN03)
- Admin admin1 aprobando al cliente 1
- Verificando nuevo estado: approved

>> PASO 3: Registro de empresa indígena (RN04)
- Registrando empresa: Native Company, company@example.com, role=indigenous_company
- Empresa creada con ID: 2
- Verificando estado inicial: pending (RN02)

>> PASO 4: Administrador rechaza a la empresa (RN03)
- Admin admin1 rechazando a la empresa 2
- Razón: Documentación incompleta
- Verificando nuevo estado: rejected

✓ Prueba de integración completada con éxito
- Reglas verificadas: RN01, RN02, RN03, RN04
```

## Próximos Pasos

- Implementación de autenticación JWT
- Integración con base de datos persistente
- Desarrollo de interfaz de usuario para administración
- Implementación del módulo de Cotizaciones

---

## Instrucciones para Desarrolladores

### Requisitos

- Python 3.8+
- pytest
- werkzeug

### Instalación

```bash
pip install -r requirements.txt
```

### Configuración

1. Configura la conexión a la base de datos en `app/infrastructure/database.py`
2. Asegúrate de crear un usuario administrador inicial

### Ejecución

```bash
python -m app.main
```

Para ejecutar las pruebas:

```bash
python -m pytest app/tests -v
```
