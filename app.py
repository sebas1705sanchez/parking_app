from flask import Flask, render_template, jsonify

# -----------------------------------------------------------------------------
# CONFIGURACIÓN GENERAL DE LA APLICACIÓN
# -----------------------------------------------------------------------------
# Se crea la instancia principal de Flask.
app = Flask(__name__)

# Capacidad máxima del parqueadero.
CAPACIDAD_TOTAL = 16

# Lista que representa el estado de las plazas del parqueadero.
# Cada posición de la lista corresponde a una plaza:
# - False = plaza libre
# - True  = plaza ocupada
#
# Ejemplo:
# plazas[0] representa la plaza 1
# plazas[1] representa la plaza 2
# ...
# plazas[15] representa la plaza 16
plazas = [False for _ in range(CAPACIDAD_TOTAL)]


# -----------------------------------------------------------------------------
# FUNCIONES AUXILIARES
# -----------------------------------------------------------------------------
def contar_ocupadas() -> int:
    """
    Cuenta cuántas plazas del parqueadero están ocupadas.

    Returns:
        int: Número total de plazas ocupadas.
    """
    return sum(plazas)


def estado_parqueadero() -> str:
    """
    Determina el estado general del parqueadero.

    Returns:
        str:
            - "LLENO" si todas las plazas están ocupadas.
            - "LIBRE" si aún existe al menos una plaza disponible.
    """
    return "LLENO" if contar_ocupadas() == CAPACIDAD_TOTAL else "LIBRE"


# -----------------------------------------------------------------------------
# RUTAS DE VISTA
# -----------------------------------------------------------------------------
@app.route("/")
def inicio():
    """
    Muestra la vista principal del sistema.

    Esta ruta carga el archivo HTML principal donde se visualizan
    las 16 plazas del parqueadero y los controles del sistema.

    Returns:
        Response: Renderiza la plantilla 'index.html'.
    """
    return render_template("index.html")


# -----------------------------------------------------------------------------
# RUTAS API
# -----------------------------------------------------------------------------
@app.route("/api/plazas", methods=["GET"])
def obtener_plazas():
    """
    Devuelve el estado completo del parqueadero en formato JSON.

    Incluye:
    - capacidad total
    - cantidad de plazas ocupadas
    - cantidad de plazas disponibles
    - estado general del parqueadero
    - listado de plazas con su identificador y estado

    Returns:
        Response: JSON con la información actual del parqueadero.
    """
    # Se construye una lista de diccionarios con el estado de cada plaza.
    data = [
        {
            "id": i + 1,          # Número de plaza visible para el usuario
            "ocupada": plazas[i]  # Estado actual de la plaza
        }
        for i in range(CAPACIDAD_TOTAL)
    ]

    return jsonify({
        "capacidad_total": CAPACIDAD_TOTAL,
        "ocupadas": contar_ocupadas(),
        "disponibles": CAPACIDAD_TOTAL - contar_ocupadas(),
        "estado": estado_parqueadero(),
        "plazas": data
    })


@app.route("/api/entrada", methods=["POST"])
def registrar_entrada():
    """
    Registra la entrada de un vehículo.

    Lógica:
    - Busca la primera plaza libre.
    - Si la encuentra, la marca como ocupada.
    - Si no hay plazas libres, devuelve un error indicando
      que el parqueadero está lleno.

    Returns:
        Response:
            - JSON con éxito si se ocupó una plaza.
            - JSON con error y código 400 si el parqueadero está lleno.
    """
    for i in range(CAPACIDAD_TOTAL):
        if not plazas[i]:
            plazas[i] = True
            return jsonify({
                "ok": True,
                "mensaje": f"Vehículo ingresó a la plaza {i + 1}"
            })

    return jsonify({
        "ok": False,
        "mensaje": "El parqueadero está lleno"
    }), 400


@app.route("/api/salida", methods=["POST"])
def registrar_salida():
    """
    Registra la salida de un vehículo.

    Lógica:
    - Busca una plaza ocupada comenzando desde la última.
    - Si la encuentra, la libera.
    - Si no hay vehículos en el parqueadero, devuelve un error.

    Returns:
        Response:
            - JSON con éxito si se liberó una plaza.
            - JSON con error y código 400 si no hay vehículos para retirar.
    """
    for i in range(CAPACIDAD_TOTAL - 1, -1, -1):
        if plazas[i]:
            plazas[i] = False
            return jsonify({
                "ok": True,
                "mensaje": f"Vehículo salió de la plaza {i + 1}"
            })

    return jsonify({
        "ok": False,
        "mensaje": "No hay vehículos para retirar"
    }), 400


@app.route("/api/plaza/<int:plaza_id>/toggle", methods=["POST"])
def cambiar_estado_plaza(plaza_id: int):
    """
    Cambia manualmente el estado de una plaza específica.

    Si la plaza está libre, la ocupa.
    Si la plaza está ocupada, la libera.

    Args:
        plaza_id (int): Número de la plaza que se desea modificar.

    Returns:
        Response:
            - JSON con éxito si la plaza fue actualizada.
            - JSON con error y código 404 si el número de plaza no es válido.
    """
    # Validar que el número de plaza esté dentro del rango permitido.
    if plaza_id < 1 or plaza_id > CAPACIDAD_TOTAL:
        return jsonify({
            "ok": False,
            "mensaje": "Plaza inválida"
        }), 404

    # Convertir el número de plaza a índice de lista.
    indice = plaza_id - 1

    # Cambiar el estado actual de la plaza.
    plazas[indice] = not plazas[indice]

    return jsonify({
        "ok": True,
        "mensaje": f"Plaza {plaza_id} actualizada",
        "ocupada": plazas[indice]
    })


@app.route("/api/reset", methods=["POST"])
def reiniciar_parqueadero():
    """
    Reinicia el parqueadero completo.

    Todas las plazas vuelven a quedar libres.

    Returns:
        Response: JSON confirmando que el parqueadero fue reiniciado.
    """
    global plazas
    plazas = [False for _ in range(CAPACIDAD_TOTAL)]

    return jsonify({
        "ok": True,
        "mensaje": "Parqueadero reiniciado"
    })


# -----------------------------------------------------------------------------
# PUNTO DE ENTRADA DE LA APLICACIÓN
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    """
    Ejecuta la aplicación Flask en modo desarrollo.

    debug=True permite:
    - recarga automática al guardar cambios
    - ver mensajes de error más detallados durante el desarrollo
    """
    app.run(debug=True)