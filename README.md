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

### 1. Configuración de conexión

El sistema utiliza un archivo de configuración externa para proteger las credenciales y cumplir con el requisito de no exponer datos privados:
1. Copia `secret_config_sample.py` a `secret_config.py`.
2. Asegúrate de que `secret_config.py` esté incluido en tu `.gitignore`.
3. Abre `secret_config.py` y escribe estos datos (reemplazando con tus credenciales reales):

```python
# Instrucciones: Reemplace los valores con sus credenciales reales de Render
PGDATABASE = "calculadora_ahorro"
PGUSER = "salas18"
PGPASSWORD = "OyXLN6OLFMdldi0HA5GKwcA6GWeB7Mg0"
PGHOST = "dpg-d7ln7667r5hc73c2j1pg-a.oregon-postgres.render.com"
PGPORT = "5432"
```

No necesitas usar comandos extra ni variables de entorno. Solo asegúrate de tener Python instalado.

### 2. Crear las tablas

Si la base de datos ya existe, puedes crear las tablas desde Python con este comando en la raíz del proyecto:

```bash
python -c "from src.controller.usuario_controller import UsuarioController; UsuarioController.crear_tablas()"
```

O bien, si prefieres usar los archivos SQL aplicando los principios de Código Limpio, abre la terminal en la carpeta del proyecto y ejecuta en este orden estricto:

```bash
psql -d calculadora_ahorro_programado -f sql/01_usuarios.sql
psql -d calculadora_ahorro_programado -f sql/02_metas_ahorro.sql
psql -d calculadora_ahorro_programado -f sql/03_historial_calculos.sql
```

**Estructura de archivos en la carpeta `sql/`**:

| Script | Propósito |
|--------|-----------|
| `00_borrar_tablas.sql`| Contiene los `DROP TABLE CASCADE`. Es utilizado automáticamente por el entorno de pruebas (**Test Fixtures**) para vaciar la base de datos antes de cada test, garantizando que arranquen desde cero y evitando errores de llaves duplicadas. |
| `01_usuarios.sql` | Crea la tabla principal de `usuarios` que utilizan la calculadora. |
| `02_metas_ahorro.sql` | Crea la tabla `metas_ahorro`, que guarda cada simulación con sus parámetros financieros (meta, plazo, extra, mes_extra) y la cuota mensual resultante. Depende de la tabla usuarios. |
| `03_historial_calculos.sql` | Crea la tabla `historial_calculos`, registrando el detalle completo de cada cálculo (incluyendo factor de anualidad) para auditoría. Depende de la tabla usuarios. |
| `04_inserts_ejemplo.sql` | Archivo opcional que inserta datos de prueba (ej. Miguel Angel, Jose Angel) para verificar que la base de datos funciona correctamente sin tener que teclear desde Python. |

### 3. Diagrama Entidad-Relación

```text
┌─────────────┐       ┌──────────────────┐       ┌──────────────────────┐
│   usuarios  │       │   metas_ahorro   │       │ historial_calculos   │
├─────────────┤       ├──────────────────┤       ├──────────────────────┤
│ id_usuario  │──┐    │ id_meta          │       │ id_historial         │
│ nombre      │  │    │ id_usuario (FK)  │◄──────┤ id_usuario (FK)      │
│ email       │  └────┤ meta             │       │ meta                 │
│ fecha_reg   │       │ plazo            │       │ plazo                │
└─────────────┘       │ extra            │       │ extra                │
                      │ mes_extra        │       │ mes_extra            │
                      │ tasa             │       │ tasa                 │
                      │ cuota_mensual    │       │ valor_futuro_extra   │
                      │ fecha_calculo    │       │ factor_anualidad     │
                      └──────────────────┘       │ cuota_mensual        │
                                                 │ fecha_calculo        │
                                                 └──────────────────────┘
```


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
## 🏗️ Arquitectura del Proyecto y Responsabilidades

El sistema sigue el principio de **separación de responsabilidades (SRP)**, dividiendo el proyecto en capas bien definidas. A continuación, se presenta la estructura real del repositorio:

```text
CALCULADORA-DE-AHORRO-PROGRAMADO/
│
├── docs/                          # Documentación y archivos de apoyo
│   └── Libro de excel (1).xlsx    # Prototipo y cálculos manuales
│
├── sql/                           # Scripts para inicializar y limpiar la base de datos
│   ├── borrar_tablas.sql
│   ├── historial_calculos.sql
│   ├── inserts_ejemplo.sql
│   ├── metas_ahorro.sql
│   └── usuarios.sql
│
├── src/                           # Código fuente principal de la aplicación
│   ├── controller/                # Capa de Control (Persistencia y BD)
│   │   ├── __init__.py
│   │   ├── ahorro_controller.py
│   │   └── usuario_controller.py
│   │
│   ├── core/                      # Reglas de negocio puras
│   │   ├── __init__.py
│   │   └── logica.py
│   │
│   ├── model/                     # Definición de Objetos/Entidades
│   │   ├── __init__.py
│   │   ├── ahorro.py
│   │   ├── historial_calculo.py
│   │   ├── meta_ahorro.py
│   │   └── usuario.py
│   │
│   └── view/                      # Capa de Presentación (UI/Consola)
│       ├── __init__.py
│       ├── console.py             # Script principal de consola
│       ├── error.png              # Recursos gráficos
│       ├── gui_calculadora.py     # Script principal de la interfaz Kivy
│       └── view-console/          # Vistas individuales por consola
│           ├── buscar_ahorro.py
│           ├── crear_meta_ahorro.py
│           ├── crear_usuario.py
│           └── __init__.py
│
├── tests/                         # Entorno riguroso de pruebas unitarias
│   ├── __init__.py
│   ├── test_ahorro_programado.py
│   └── test_db.py
│
├── .gitignore                     # Archivos ignorados por Git (ej. pycache, secretos)
├── buildozer.spec                 # Configuración para compilar APK en Android
├── calculadora_ahorro.spec        # Configuración de PyInstaller
├── main.py                        # Punto de entrada de la aplicación
├── README.md                      # Documentación del proyecto
└── secret_config.py               # Credenciales de Render (NO SUBIR A GITHUB)
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
python src/view/gui_calculadora.py
```

Una vez abierta la aplicación, encontrarás los campos necesarios para ingresar tu meta de ahorro. Al presionar **"Calcular Ahorro"**, la aplicación mostrará el monto que debes ahorrar cada mes y gestionará el guardado en la base de datos.

### Consola
Si prefieres usar la versión de línea de comandos, ejecuta:

```bash
python src/view/console.py
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
python -m unittest discover -s src/tests -p "test*.py"
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
- **Jose Angel Martinez**
- **Miguel Angel Salazar**
- **Sebastian Aristizabal Aristizabal**
- **Isabella Quintero Gutierrez**

Proyecto académico desarrollado como práctica de modelado financiero aplicado al ahorro programado y buenas prácticas de programación en Python.
