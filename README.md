# 📦 Prueba_Tec

Un sistema de **e-commerce moderno** que combina un backend en **Python Flask** con un frontend en **React + TypeScript**.  
El proyecto gestiona usuarios, productos y transacciones de compra, soportando múltiples tipos de documentos y operaciones omnicanal.

---

## 🚀 Características principales
- **Arquitectura en tres capas**: presentación, lógica de negocio y persistencia.
- **Backend REST API** con Flask y SQLAlchemy.
- **Frontend SPA** con React, TypeScript y Vite.
- **Gestión de base de datos** con SQLite y migraciones controladas por Alembic.
- **Exportación de datos** a Excel (xlsx + file-saver).
- **Separación de frontend y backend** con soporte CORS.

---

## 🏗️ Arquitectura del sistema

| Capa              | Ubicación              | Componentes clave | Responsabilidades |
|-------------------|------------------------|------------------|------------------|
| **Presentación**  | `frontend/`            | React, TS, Vite  | UI, lógica cliente, exportación Excel |
| **Lógica negocio**| `backend/main.py`      | Flask routes     | Endpoints, validación, formato de respuesta |
| **Acceso datos**  | `backend/models.py`    | SQLAlchemy ORM   | Modelos, relaciones, queries |
| **Persistencia**  | `backend/instance/`    | SQLite DB        | Almacenamiento |
| **Esquema**       | `backend/migrations/`  | Alembic          | Versionado y evolución del esquema |

---

## 🛠️ Tecnologías

### Backend
- **Flask** (Python 3.13+) – servidor REST API
- **SQLAlchemy** – ORM
- **SQLite** – base de datos (`falabella.db`)
- **Alembic + Flask-Migrate** – migraciones
- **Middleware CORS** – soporte cross-origin

### Frontend
- **React 18.3.1** – librería UI
- **TypeScript 5.9.3** – tipado estático
- **Vite 7.2.4** – bundler rápido
- **Tailwind CSS 4.1.17** – estilos utilitarios
- **xlsx + file-saver** – exportación a Excel
- **ESLint 9.39.1** – calidad de código

---

## 🔑 Endpoints principales

- `GET /users` → listado paginado de usuarios  
- `GET /document-types` → tipos de documento disponibles  
- `GET /users/<user_id>/purchases` → historial de compras con filtros de fecha  
- `GET /users/dni/<dniNumber>` → búsqueda de usuario por número de documento  

---

## 🗄️ Modelos de datos

- **User** – identidad del cliente  
- **DocumentType** – catálogo de tipos de documento (CC, TI, NIT, PASAPORTE, etc.)  
- **Product** – catálogo de productos  
- **Purchase** – transacciones de compra  
- **PurchaseProduct** – ítems de compra (tabla de unión)

---

## ⚙️ Configuración y desarrollo

### Backend
1. Instalar dependencias: `pip install -r requirements.txt`
2. Ejecutar migraciones: `flask db upgrade`
3. (Opcional) Sembrar datos de prueba
4. Iniciar servidor: `flask run`

### Frontend
1. Instalar dependencias: `npm install`
2. Iniciar servidor dev: `npm run dev`
3. Compilar producción: `npm run build`

---

## 📊 Funcionalidades destacadas
- API RESTful con respuestas estandarizadas.
- Modelado relacional con claves foráneas.
- Migraciones versionadas con Alembic.
- Exportación de reportes de compras en Excel.
- Flujo de trabajo moderno con React + Vite.

