# 💻 Simulador de Ahorro Programado

Herramienta financiera construida para la asignatura **Lenguajes de Programación y Código Limpio**. Este sistema está diseñado aplicando principios de separación de responsabilidades, manejo preventivo de errores y un entorno riguroso de pruebas unitarias automatizadas.

Su función principal es calcular la cuota mensual requerida para cumplir un objetivo de ahorro en un tiempo definido, tomando en cuenta el rendimiento de una tasa de interés mensual y el impacto de inyecciones de capital (abonos extra).

---

## 🚀 Propósito del Proyecto

El objetivo central es automatizar el cálculo de la **cuota mensual fija** que un usuario debe depositar para alcanzar una meta económica. Para esto, el algoritmo se apoya en el modelo matemático de **anualidades de valor futuro con interés compuesto**, evaluando cómo un aporte extraordinario disminuye la carga mensual del ahorrador.

---

## 📊 Bases Matemáticas y Fórmulas

El motor de cálculo financiero del programa se rige por las siguientes premisas:

- 📌 **Tasa de rendimiento mensual ($i$):** Fijada en `0.75%` (0.0075) para las proyecciones.

- 📌 **Valor Futuro del Abono Extra:** Este aporte ($Extra$) genera rendimientos desde el mes en que se deposita ($k$) hasta el vencimiento del plan ($n$). 
$$VF_{extra} = Extra \times (1 + i)^{(n - k)}$$

- 📌 **Valor Futuro de Anualidad Ordinaria:** Calcula cómo el dinero aportado mes a mes ($C$) va sumando valor con los intereses para alcanzar una Meta ($VF$).
$$VF = C \times \frac{(1 + i)^n - 1}{i}$$

- 📌 **Cálculo de la Cuota Mensual ($C$):** Al total de la meta original se le descuenta el valor futuro generado por el abono extra. Sobre ese nuevo total, se despeja $C$ para hallar el pago exacto:
$$C = \frac{(Meta - VF_{extra}) \times i}{(1 + i)^n - 1}$$

Todos los valores monetarios de salida se redondean a **2 decimales** para garantizar precisión contable.

---

## 🗄️ Base de Datos y Persistencia (PostgreSQL)

Para cumplir con la persistencia de datos solicitada en la rúbrica, el sistema se integra con una base de datos PostgreSQL alojada en **Render**. 

### 1. Creación de Tablas (SQL)
Ejecute el siguiente script en su gestor de base de datos para habilitar la estructura necesaria:

```sql
-- Tabla de usuarios
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL
);

-- Tabla de metas de ahorro
CREATE TABLE metas_ahorro (
    id_meta SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    meta DECIMAL(18,2) NOT NULL,
    plazo INT NOT NULL,
    extra DECIMAL(18,2) DEFAULT 0,
    mes_extra INT DEFAULT 0,
    cuota_mensual DECIMAL(18,2)
);

-- Tabla de historial de cálculos
CREATE TABLE historial_calculos (
    id_historial SERIAL PRIMARY KEY,
    id_usuario INT REFERENCES usuarios(id_usuario),
    meta DECIMAL(18,2),
    plazo INT,
    extra DECIMAL(18,2),
    mes_extra INT,
    cuota_mensual DECIMAL(18,2),
    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Conexión Segura con `secret_config.py`
El sistema utiliza un archivo de configuración externa para proteger las credenciales y cumplir con el requisito de no exponer datos privados:
1. Cree un archivo llamado `secret_config.py` en la raíz del proyecto.
2. Agregue este archivo a su `.gitignore`.
3. Utilice la siguiente plantilla para establecer la conexión:

```python
# Instrucciones: Reemplace los valores con sus credenciales reales de Render
PGDATABASE = "nombre_de_tu_db"
PGUSER = "tu_usuario"
PGPASSWORD = "tu_password_secreto"
PGHOST = "tu_host_de_render"
PGPORT = "5432"
```

---

## 🔄 Flujo de Ejecución del Algoritmo

1. Recepción de los parámetros de configuración del ahorro por parte del usuario.
2. Filtro de seguridad (evaluación estricta de las reglas de negocio y validación de datos).
3. Determinación de los intereses ganados por el abono extraordinario a lo largo del tiempo restante.
4. Estimación del factor matemático de acumulación de la anualidad.
5. Cálculo y despeje de la cuota mensual requerida para cubrir la diferencia exacta.
6. Guardado en la base de datos (Render).
7. Retorno del valor a pagar o impresión del respectivo código de error si las reglas se incumplen.

---

## 🏗️ Arquitectura del Proyecto y Responsabilidades

El sistema sigue el principio de **separación de responsabilidades (SRP)**, dividiendo el proyecto en tres capas principales: Core/Model (Lógica), UI (Interfaz) y Tests (Pruebas).

```text
CALCULADORA_AHORRO_PROGRAMADO/
│
├── src/
│   ├── controller/
│   │   ├── usuario_controller.py  # Persistencia de usuarios en BD
│   │   └── ahorro_controller.py   # Guardado de metas en BD
│   ├── model/
│   │   ├── usuario.py             # Objeto Usuario
│   │   └── ahorro.py              # Lógica financiera (Core)
│   └── ui/
│       ├── console.py             # Interfaz de comandos
│       └── gui/                   # Interfaz gráfica (Kivy)
│
├── tests/
│   ├── __init__.py                
│   └── test_db.py                 # 9 Pruebas integrales requeridas
│
├── secret_config.py               # Credenciales (Ignorado en Git)
└── README.md
```

---

## 📥 Entradas del Sistema

El programa solicita y procesa cuatro variables clave:

| Variable | Tipo | Descripción |
|----------|--------|--------------|
| `meta` | `float` | Capital final que el usuario desea acumular. |
| `plazo` | `int` | Cantidad total de meses contemplados para el ahorro. |
| `abono_extra` | `float` | Inyección de capital adicional (0 si no aplica). |
| `mes_abono_extra` | `int` | Mes exacto en el cual se efectuará el depósito. |

---

## 🛡️ Reglas de Negocio y Validaciones

El programa evalúa de forma estricta que:

- La **meta** sea mayor que 0.
- El **plazo** sea mayor que 0.
- El **abono extra** no sea un número negativo.
- El **abono extra** no supere la meta total.
- El **mes del abono** ocurra dentro de la vigencia del plazo de ahorro.

Si alguna condición falla, el sistema lanza **excepciones personalizadas** (Ej: `ErrorMetaInvalida`, `ErrorAbonoSuperaMeta`).

---

## ▶️ Ejecución de la Aplicación

### Prerrequisitos
Asegúrate de tener Python 3.x instalado. Para la interfaz gráfica y la base de datos, instala las dependencias:

```bash
pip install kivy psycopg2
```

### Interfaz gráfica (GUI)
El GUI está construido con Kivy. Para ejecutarlo, corre el siguiente comando **desde la raíz del proyecto**:

```bash
python src/ui/gui/gui_calculadora.py
```

Una vez abierta la aplicación, encontrarás los campos necesarios para ingresar tu meta de ahorro. Al presionar **"Calcular Ahorro"**, la aplicación mostrará el monto que debes ahorrar cada mes y gestionará el guardado en la base de datos.

### Consola
Si prefieres usar la versión de línea de comandos, ejecuta:

```bash
python src/ui/console.py
```

El programa te pedirá los mismos datos de forma interactiva.

---

## 🧪 Ejecución de Pruebas Unitarias

**Ejecución Estándar**  
Este comando ejecuta las 9 pruebas (3 de insertar, 3 de buscar y 3 de modificar) de forma silenciosa, mostrándote los puntos de éxito:
```powershell
python -m unittest tests.test_db
```

**Ejecución Detallada (Recomendada para la entrega)**  
Usa la bandera `-v` (verbose) para que el sistema liste cada prueba individualmente y confirme que tanto los casos normales como los de error están pasando:
```powershell
python -m unittest -v tests.test_db
```

**Descubrimiento Automático**  
Si decides agregar más archivos de prueba en la carpeta `tests`, este comando encontrará y ejecutará todos automáticamente:
```powershell
python -m unittest discover -s tests -p "test*.py"
```

> **Nota Técnica:** Asegúrate de que tu entorno virtual (`.venv`) esté activado y que te encuentres en la raíz de la carpeta `Calculadora-de-Ahorro-Programado` para que las importaciones de `src` y `secret_config` funcionen correctamente. Si usas PowerShell y tienes problemas de importación, puedes usar: `$env:PYTHONPATH = "."; python -m unittest tests.test_db`

---

## 🧼 Principios de Código Limpio Aplicados

- ✔️ Programación Orientada a Objetos (POO) y Arquitectura MVC.
- ✔️ Separación de responsabilidades.
- ✔️ Validaciones robustas y tipado estricto (Type Hints).
- ✔️ Excepciones personalizadas con contexto.
- ✔️ Eliminación de "Números Mágicos" usando constantes.
- ✔️ Protección de credenciales usando `secret_config.py` y `.gitignore`.
- ✔️ Fixtures en pruebas (`setUp`) para limpieza automática de datos.

---

## 👨‍💻 Autores

**Equipo de Desarrollo:**
- **Jose Angel Sanchez**
- **Miguel Angel Salazar**
- **Sebastian Aristizabal Aristizabal**
- **Isabella Quintero Gutierrez**

Proyecto académico desarrollado como práctica de modelado financiero aplicado al ahorro programado y buenas prácticas de programación en Python.
