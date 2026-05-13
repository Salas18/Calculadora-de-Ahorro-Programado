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

## 🔄 Flujo de Ejecución del Algoritmo

1. Recepción de los parámetros de configuración del ahorro por parte del usuario.
2. Filtro de seguridad (evaluación estricta de las reglas de negocio y validación de datos).
3. Determinación de los intereses ganados por el abono extraordinario a lo largo del tiempo restante.
4. Estimación del factor matemático de acumulación de la anualidad.
5. Cálculo y despeje de la cuota mensual requerida para cubrir la diferencia exacta.
6. Retorno del valor a pagar en consola o impresión del respectivo código de error si las reglas se incumplen.

---

## 🏗️ Arquitectura del Proyecto y Responsabilidades

El sistema sigue el principio de **separación de responsabilidades (SRP)**, dividiendo el proyecto en tres capas principales: Core (Lógica), UI (Interfaz) y Tests (Pruebas).

```text
CALCULADORA_AHORRO_PROGRAMADO/
│
├── src/
│   ├── core/
│   │   └── logica.py            
│   │
│   └── ui/
│       └── console.py           
│
├── tests/
│   └── test_ahorro_programado.py 
│
└── README.md
```

### 📦 1. Capa Core (`src/core/logica.py`)
Contiene la **lógica de negocio del sistema** y las excepciones personalizadas. 

| Método | Responsabilidad |
|------|------|
| `__init__()` | Inicializa los datos con Type Hints para asegurar los tipos correctos. |
| `_validar_datos()` | Función privada que aísla la lógica de validación (Fail-Fast). |
| `calcular_cuota_mensual()` | Ejecuta el cálculo financiero principal aplicando las fórmulas matemáticas. |

### 🖥️ 2. Capa UI (`src/ui/console.py`)
Contiene la **interfaz de usuario por consola**.
* **Responsabilidades:** Solicitar datos numéricos de forma segura, mostrar el menú interactivo, invocar a la lógica de negocio y atrapar las excepciones personalizadas para mostrar mensajes de error amigables al usuario.

### 🧪 3. Capa Tests (`tests/test_ahorro_programado.py`)
Contiene la **suite de 11 pruebas unitarias automatizadas** usando la librería `unittest`. Cubre casos estándar, inyecciones de capital totales y parciales, diferencias de centavos, y verifica que todos los errores se disparen correctamente.

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

Para ejecutar la calculadora desde la consola, ubícate en la raíz del proyecto y ejecuta:

```bash
python src/ui/console.py
```

**Ejemplo de interacción:**
```text
===================================
   CALCULADORA DE AHORRO PROGRAMADO 
===================================

Ingrese la meta de ahorro ($): 1100000
Ingrese el plazo en meses: 6
Ingrese el abono extra (0 si no hay): 0
Ingrese el mes del abono extra (0 si no hay): 0

✅ Cálculo exitoso
Debes ahorrar mensualmente: $179,925.80
```

---

## 🧪 Ejecución de Pruebas Unitarias

Para ejecutar el entorno de pruebas automatizadas y verificar la salud del código, utiliza:

```bash
python -m unittest discover -s src/tests -v
```

Salida esperada:
```text
.....
----------------------------------------------------------------------
Ran 11 tests in 0.002s

OK
```

---

## 🧼 Principios de Código Limpio Aplicados

- ✔️ Programación Orientada a Objetos (POO).
- ✔️ Separación de responsabilidades.
- ✔️ Validaciones robustas y tipado estricto (Type Hints).
- ✔️ Excepciones personalizadas con contexto.
- ✔️ Eliminación de "Números Mágicos" usando constantes.
- ✔️ Nombres de variables y funciones descriptivos.

---

## 👨‍💻 Autores

**Equipo de Desarrollo:**
- **Jose Angel Sanchez**
- **Miguel Angel Salazar**

Proyecto académico desarrollado como práctica de modelado financiero aplicado al ahorro programado y buenas prácticas de programación en Python.


-------------
## Ejecución

### Prerrequisitos

Asegúrate de tener Python 3.x instalado. Para la interfaz gráfica, también necesitas instalar Kivy:

```bash
pip install kivy
```

### Interfaz gráfica (GUI)

El GUI está construido con Kivy. Para ejecutarlo, corre el siguiente comando **desde la raíz del proyecto**:

```bash
python src/ui/gui/gui_calculadora.py
```

Una vez abierta la aplicación, encontrarás cuatro campos: la meta de ahorro (monto total que deseas alcanzar), el plazo en meses, un abono extra opcional y el mes en que se realizará dicho abono. Si no tienes abono extra, ingresa `0` en los dos últimos campos. Al presionar el botón **"Calcular Ahorro"**, la aplicación mostrará el monto que debes ahorrar cada mes para alcanzar tu meta.

### Consola

Si prefieres usar la versión de línea de comandos, ejecuta:

```bash
python src/ui/console.py
```

El programa te pedirá los mismos datos de forma interactiva: meta de ahorro, plazo en meses, abono extra y el mes del abono extra. Al finalizar, mostrará el ahorro mensual necesario.

> En ambos casos, es importante ejecutar los comandos desde la raíz del proyecto (`Calculadora-de-Ahorro-Programado/`) para que las importaciones funcionen correctamente.

REALIZADO POR: SEBASTIAN ARISTIZABAL ARISTIZABAL E ISABELLA QUINTERO GUTIERREZ
