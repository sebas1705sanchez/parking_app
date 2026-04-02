# Controlador de Parking

Sistema web desarrollado en **Python con Flask** para simular el control de un parqueadero de **16 plazas**.

La aplicación permite visualizar en pantalla el estado de cada plaza mediante colores:

- **Verde**: plaza libre
- **Rojo**: plaza ocupada

Además, incluye acciones para simular la **entrada** y **salida** de vehículos, así como reiniciar el estado del parqueadero.

---

## Características principales

- Visualización de las **16 plazas** en pantalla
- Estado visual por colores:
  - Verde = libre
  - Rojo = ocupada
- Contador de:
  - plazas ocupadas
  - plazas disponibles
- Estado general del parqueadero:
  - **LIBRE**
  - **LLENO**
- Botón para **simular entrada**
- Botón para **simular salida**
- Botón para **reiniciar** el sistema
- Posibilidad de cambiar manualmente el estado de una plaza haciendo clic sobre ella

---

## Tecnologías utilizadas

- **Python 3**
- **Flask**
- **HTML**
- **CSS**
- **JavaScript**

---

## Estructura del proyecto

```bash
parking_app/
│
├── app.py
├── requirements.txt
└── templates/
    └── index.html



## Correr el proyecto

```bash
pip install -r requirements.txt
python app.py
