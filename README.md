# Generador de **tareas.xlsx** con Faker → insumo para Power Automate

> **Propósito:** Crear un archivo Excel con tareas realistas para practicar flujos de **alertas de vencimiento** en **Power Automate** (Teams/Correo). Pensado para clases y demos.

---

## ✅ Resultado
Al ejecutar el script se genera **`tareas.xlsx`** con estas columnas:

| Columna            | Ejemplo                        | Uso en el flujo |
|--------------------|--------------------------------|-----------------|
| `ID`               | `T-001`                        | Identificador legible |
| `Titulo`           | `Revisar inventario mensual`   | Texto principal |
| `Descripcion`      | Frase corta                    | Opcional |
| `Responsable`      | `Ana Torres`                   | Mostrar en tabla |
| `Email`            | `ana.torres@acme.com`          | Envío de correo |
| `Equipo`           | `Operaciones`                  | Ruteo por canal |
| `FechaVencimiento` | `YYYY-MM-DD`                   | Filtros por fecha |
| `Estado`           | `Pendiente / En Progreso / Completada` | Reglas del flujo |

> Se incluyen **3 casos de control** para probar: *mañana*, *hoy* y *ayer* (todas en **Pendiente**).

---

## 🧰 Requisitos
- Python 3.8+
- Paquetes: `faker`, `pandas`

Instalación rápida:
```bash
pip install faker pandas
```

---

## ▶️ Cómo ejecutar
1. Guarda el script como `generar_tareas.py` (o el nombre que prefieras).
2. Ejecuta en terminal:
   ```bash
   python generar_tareas.py
   ```
3. Se creará **`tareas.xlsx`** en la misma carpeta.

> Para usar en Power Automate, sube el archivo a **OneDrive** o **SharePoint**. En Excel (opcional pero recomendado), conviértelo en **Tabla** llamada **`Tareas`**: *Insertar → Tabla* y asigna ese nombre.

---

## 🧠 Explicación del código (paso a paso)
```python
from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
```
Importamos librerías: **Faker** para datos realistas, **pandas** para crear/exportar el Excel, **random/datetime** para aleatoriedad y fechas.

```python
fake = Faker('es_CO')    # localización: nombres/correos con sabor colombiano
random.seed(42)          # semilla para resultados reproducibles en clase
hoy = datetime.utcnow()  # base de tiempo (UTC) para calcular vencimientos
```
Configuración básica: locale, semilla y referencia temporal.

```python
estados = ["Pendiente", "En Progreso", "Completada"]
equipos = ["Operaciones", "Finanzas", "Ventas", "Logística", "TI", "Marketing"]

tareas_ejemplos = [
    "Revisar inventario mensual",
    "Actualizar base de datos de clientes", 
    "Preparar informe de ventas",
    "Capacitar nuevo personal",
    "Auditar procesos de calidad",
    "Desarrollar campaña publicitaria",
    "Analizar presupuesto trimestral",
    "Optimizar sistema de pedidos",
    "Planificar reunión de equipo",
    "Evaluar proveedores"
]

descripciones = [
    "Revisar y documentar el proceso según protocolo establecido.",
    "Coordinar con el equipo para completar la actividad.",
    "Analizar datos y preparar reporte para presentación.",
    "Implementar mejoras basadas en feedback recibido.",
    "Seguir procedimientos estándar y documentar resultados.",
    "Evaluar opciones y presentar recomendaciones.",
    "Actualizar información y verificar cumplimiento.",
    "Coordinar con otras áreas para completar objetivos."
]
```
Catálogos básicos para asignar estado, equipo, títulos y descripciones variadas.

```python
tareas = []
for i in range(120):
    # Distribución: 60% fechas futuras (1–15 días), 40% pasadas (1–7 días)
    if random.random() < 0.6:
        dias = random.randint(1, 15)
        vence = hoy + timedelta(days=dias)
    else:
        dias = random.randint(1, 7)
        vence = hoy - timedelta(days=dias)
    
    tarea = {
        "ID": f"T-{i+1:03d}",
        "Titulo": random.choice(tareas_ejemplos),
        "Descripcion": random.choice(descripciones),
        "Responsable": fake.name(),
        "Email": fake.email(),
        "Equipo": random.choice(equipos),
        "FechaVencimiento": vence.strftime("%Y-%m-%d"),
        "Estado": random.choices(estados, weights=[0.6, 0.25, 0.15])[0]
    }
    tareas.append(tarea)
```
Generamos **120** tareas con mezcla de fechas futuras/pasadas y estados con pesos realistas (*Pendiente 60%*, *En Progreso 25%*, *Completada 15%*). La fecha va en formato **`YYYY-MM-DD`** (fácil de filtrar en Power Automate).

```python
# Casos especiales para pruebas (los primeros 3)
tareas[0]["FechaVencimiento"] = (hoy + timedelta(days=1)).strftime("%Y-%m-%d")  # Mañana
tareas[0]["Estado"] = "Pendiente"

tareas[1]["FechaVencimiento"] = hoy.strftime("%Y-%m-%d")  # Hoy
tareas[1]["Estado"] = "Pendiente"

tareas[2]["FechaVencimiento"] = (hoy - timedelta(days=1)).strftime("%Y-%m-%d")  # Ayer
tareas[2]["Estado"] = "Pendiente"
```
Insertamos **3 casos de control** para validar fácilmente los filtros del flujo (*mañana*, *hoy*, *ayer*).

```python
df = pd.DataFrame(tareas)
df.to_excel("tareas.xlsx", index=False)
print(" Archivo 'tareas.xlsx' creado")
```
Exportamos a Excel y confirmamos por consola.

---

## 🛠️ Personalización rápida
- Cantidad de tareas → cambia `range(120)`.
- Rangos de días → ajusta `randint(1, 15)` (futuro) y `randint(1, 7)` (pasado).
- Pesos de estado → modifica `weights=[0.6, 0.25, 0.15]`.
- Locale de Faker → `Faker('es_MX')`, `Faker('es_ES')`, etc.
- Fecha local (en vez de UTC) → `hoy = datetime.now()`.

---



## 🔗 Uso en Power Automate (resumen)

> **Acceso directo:** [Abrir Power Automate](https://make.powerautomate.com/environments/Default-f57a5949-3738-41ef-a86e-00490c08ccb5/home)

> **IMPORTANTE**
> - En **Excel**, convierte el rango a **Tabla** y nómbrala **`Tareas`** (*Insertar → Tabla → Nombre de tabla: `Tareas`*).
> - Sube `tareas.xlsx` **preferiblemente a SharePoint** (biblioteca del equipo). Evita OneDrive personal para ambientes colaborativos.

1. **Enumerar las filas de una tabla** (Excel Online (Business) → archivo `tareas.xlsx`, **Tabla `Tareas`**).  
2. **Filtrar matriz** (reglas típicas):
   - **Vencidas:** `FechaVencimiento < startOfDay(utcNow())` **y** `Estado = Pendiente`.
   - **Vence hoy:** `startOfDay(FechaVencimiento) = startOfDay(utcNow())` **y** `Estado ≠ Completada`.
   - **Próximas (1–3 días):** `FechaVencimiento ∈ [mañana, +3 días]` **y** `Estado ≠ Completada`.
3. **Crear tabla HTML** (Columnas personalizadas): `Titulo`, `Vence (dd/MM/yyyy)`, `Responsable`, `Estado`, `Acción (Abrir)`.  
4. **Enviar** a **Teams** (Publicar mensaje en un canal) o **Correo (V2)**, marcando **Es HTML = Sí**.

> **Ruta sugerida en SharePoint**  
> `https://<tu-tenant>.sharepoint.com/sites/<TuSitio>/Documentos compartidos/Automatizaciones/tareas.xlsx`

---

## ✅ Checklist antes de correr el flujo

- [ ] **`tareas.xlsx` está en SharePoint** (recomendado) en una carpeta con permisos para el equipo.  
- [ ] El rango de datos está en **formato Tabla** y el **nombre de la Tabla es `Tareas`**.  
- [ ] Los **nombres de columnas** coinciden con los usados por el flujo (`Titulo`, `Responsable`, `FechaVencimiento`, `Estado`, etc.).  
- [ ] Existen **casos de control** (mañana, hoy, ayer) para prueba rápida.  
- [ ] En **Enumerar las filas de una tabla** está **habilitada la paginación** (umbral ≥ 5000).  
- [ ] Nadie tiene el archivo abierto en edición cuando corra el flujo (evita bloqueos del conector).  

> **Por qué SharePoint > OneDrive:** mejor colaboración (permisos por sitio/canal), menos bloqueos por edición y referencia más estable desde Power Automate.


---

## 🧩 Script completo (copiar/pegar)
```python
from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

# Configuración básica
fake = Faker('es_CO')
random.seed(42)
hoy = datetime.utcnow()

# Listas simples de datos
estados = ["Pendiente", "En Progreso", "Completada"]
equipos = ["Operaciones", "Finanzas", "Ventas", "Logística", "TI", "Marketing"]

tareas_ejemplos = [
    "Revisar inventario mensual",
    "Actualizar base de datos de clientes", 
    "Preparar informe de ventas",
    "Capacitar nuevo personal",
    "Auditar procesos de calidad",
    "Desarrollar campaña publicitaria",
    "Analizar presupuesto trimestral",
    "Optimizar sistema de pedidos",
    "Planificar reunión de equipo",
    "Evaluar proveedores"
]

descripciones = [
    "Revisar y documentar el proceso según protocolo establecido.",
    "Coordinar con el equipo para completar la actividad.",
    "Analizar datos y preparar reporte para presentación.",
    "Implementar mejoras basadas en feedback recibido.",
    "Seguir procedimientos estándar y documentar resultados.",
    "Evaluar opciones y presentar recomendaciones.",
    "Actualizar información y verificar cumplimiento.",
    "Coordinar con otras áreas para completar objetivos."
]

# Generar 120 tareas
tareas = []
for i in range(120):
    # Fecha de vencimiento: 60% futuras, 40% pasadas
    if random.random() < 0.6:
        dias = random.randint(1, 15)  # 1-15 días en el futuro
        vence = hoy + timedelta(days=dias)
    else:
        dias = random.randint(1, 7)   # 1-7 días en el pasado
        vence = hoy - timedelta(days=dias)
    
    tarea = {
        "ID": f"T-{i+1:03d}",  # T-001, T-002, etc.
        "Titulo": random.choice(tareas_ejemplos),
        "Descripcion": random.choice(descripciones),
        "Responsable": fake.name(),
        "Email": fake.email(),
        "Equipo": random.choice(equipos),
        "FechaVencimiento": vence.strftime("%Y-%m-%d"),
        "Estado": random.choices(estados, weights=[0.6, 0.25, 0.15])[0]
    }
    
    tareas.append(tarea)

# Casos especiales para pruebas (los primeros 3)
tareas[0]["FechaVencimiento"] = (hoy + timedelta(days=1)).strftime("%Y-%m-%d")  # Mañana
tareas[0]["Estado"] = "Pendiente"

tareas[1]["FechaVencimiento"] = hoy.strftime("%Y-%m-%d")  # Hoy
tareas[1]["Estado"] = "Pendiente"

tareas[2]["FechaVencimiento"] = (hoy - timedelta(days=1)).strftime("%Y-%m-%d")  # Ayer
tareas[2]["Estado"] = "Pendiente"

# Crear Excel
df = pd.DataFrame(tareas)
df.to_excel("tareas.xlsx", index=False)

print(" Archivo 'tareas.xlsx' creado")
```

---


