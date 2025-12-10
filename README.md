# Control de Carro Robótico con ESP32 mediante Bluetooth Low Energy (BLE)

## Integrantes del equipo
- Mascorro Barraza Jorge Ubaldo (2530311)
- Sifuentes Guevara Oscar Isaí (2530336)
- Vargas Cepeda Santiago (2530298)
- Escobedo Contreras Omar Oswaldo (2430238)
- Rodríguez Cuéllar Gerardo (2530125)

## 1. Introducción
Este proyecto implementa el control inalámbrico de un vehículo robótico utilizando un microcontrolador **ESP32** programado en **MicroPython**. El robot puede recibir comandos mediante **Bluetooth Low Energy (BLE)** usando un servicio tipo UART, lo que permite manejar sus motores desde una aplicación móvil compatible.

El sistema combina electrónica, control de motores con puente H y comunicación inalámbrica, resultando en un vehículo capaz de avanzar, retroceder, girar y detenerse según los comandos recibidos.

---

## 2. Objetivos

### **Objetivo general**
Desarrollar un sistema robótico controlado por BLE utilizando un ESP32 para controlar motores DC mediante comandos inalámbricos enviados desde un dispositivo móvil.

### **Objetivos específicos**
- Configurar el ESP32 como dispositivo BLE tipo UART.
- Implementar funciones de movimiento controlando motores a través de un puente H.
- Procesar comandos BLE en tiempo real.
- Crear una secuencia de arranque segura y pruebas automáticas.
- Garantizar la detención segura del robot ante cualquier error o desconexión.

---

## 3. Materiales

- Microcontrolador **ESP32**
- Puente H **L298N** o **TB6612FNG**
- 2 Motores DC
- Chasis de robot
- Batería o fuente externa
- Cables Dupont
- Aplicaciones BLE recomendadas:  
  - **BLE Scanner**  
  - **Serial Bluetooth Terminal**

---

## 4. Descripción general del sistema
El ESP32 actúa como servidor BLE exponiendo un servicio UART. Cuando un dispositivo móvil se conecta y envía comandos, el microcontrolador interpreta la información y ejecuta movimientos mediante señales digitales hacia el puente H.

Los pines configurados en el sistema son:

| Pin | Función |
|-----|---------|
| 23  | IN1 (Motor Izquierdo) |
| 33  | IN2 (Motor Izquierdo) |
| 32  | ENA (Enable Motor Izquierdo) |
| 22  | IN3 (Motor Derecho) |
| 21  | IN4 (Motor Derecho) |
| 15  | ENB (Enable Motor Derecho) |

Todos los pines se inicializan en estado bajo para evitar movimientos inesperados al encender el ESP32.

---

## 5. Funcionamiento del software

### 5.1 Configuración BLE
Se crea un objeto BLE con nombre:

- ESP32-Motores

El método `uart.irq(handler=on_rx)` permite ejecutar automáticamente la función `on_rx()` cuando se reciben datos BLE.

### 5.2 Control de motores
Se implementan funciones específicas para cada movimiento:

- `adelante()`
- `atras()`
- `izquierda()`
- `derecha()`
- `detener()`
- `activar_motores()`
- `desactivar_motores()`

Cada función activa o desactiva los pines correspondientes del puente H para generar el movimiento deseado.

### 5.3 Comandos compatibles

#### **Comandos tipo botón**
Relevantes para apps como Bluefruit:

| Acción | Código BLE |
|--------|------------|
| Adelante | `!B516` |
| Atrás | `!B615` |
| Izquierda | `!B714` |
| Derecha | `!B813` |
| Detener | `!B507`, `!B606`, `!B705`, `!B804` |

#### **Comandos de texto**
- `ACTIVAR`
- `DESACTIVAR`
- `ESTADO`
- `AYUDA`

El código también contiene un contador de comandos recibidos para depuración.

### 5.4 Secuencia de arranque
Al iniciar:
- Se imprime información en consola.
- Se envía un mensaje por BLE.
- Se activa brevemente el sistema de motores como prueba rápida.
- Después, el ESP32 queda en espera de comandos.

---

## 6. Resultados
El sistema obtuvo resultados satisfactorios:

- Conexión BLE estable y rápida.
- Interpretación correcta de comandos en tiempo real.
- Movimientos precisos y diferenciados.
- Seguridad en la activación y detención de motores.
- Alta compatibilidad con múltiples aplicaciones BLE.

La latencia en la comunicación fue mínima, permitiendo un control fluido del robot.

---

## 7. Conclusiones
El proyecto demostró la capacidad del ESP32 para controlar sistemas robóticos mediante BLE sin necesidad de módulos Bluetooth externos. La estructura modular del código facilita la ampliación del proyecto con nuevas funciones como PWM, sensores o navegación autónoma.

El sistema es estable, seguro y perfectamente útil para prácticas de robótica, control de motores, electrónica y comunicaciones inalámbricas.

---

## 8. Trabajo futuro
- Implementar control de velocidad usando PWM.
- Añadir sensor ultrasónico para evitar colisiones.
- Integrar sensor seguidor de línea.
- Crear una aplicación móvil personalizada.
- Añadir telemetría BLE (voltaje, estados de motores, alertas).

---

## 9. Código fuente
El código principal se encuentra en `main.py`, incluyendo:

- Configuración BLE  
- Control de motores  
- Manejo de comandos  
- Secuencia de inicialización  

---

## 10. Referencias
- MicroPython Official Documentation  
- Espressif ESP32 Technical Reference  
- Documentación BLE UART  
- Datasheets L298N / TB6612FNG  
