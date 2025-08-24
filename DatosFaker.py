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
