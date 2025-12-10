# Importación de librerías necesarias
import bluetooth          # Para funcionalidad Bluetooth del ESP32
from BLE import BLEUART   # Para comunicación BLE en modo UART (serial virtual)
from machine import Pin   # Para control de pines GPIO del ESP32
import time              # Para retardos y temporización

# --- MOTOR IZQUIERDO ---
ENA = Pin(32, Pin.OUT)  # Pin Enable/PWM - Controla velocidad motor izquierdo
IN1 = Pin(23, Pin.OUT)  # Control de dirección 1 del puente H
IN2 = Pin(33, Pin.OUT)  # Control de dirección 2 del puente H

# --- MOTOR DERECHO ---  
ENB = Pin(15, Pin.OUT)  # Pin Enable/PWM - Controla velocidad motor derecho
IN3 = Pin(22, Pin.OUT)  # Control de dirección 3 del puente H
IN4 = Pin(21, Pin.OUT)  # Control de dirección 4 del puente H

# Todos los pines se inicializan en 0 para asegurar
# que los motores comiencen en estado de reposo
ENA.value(0)  # Motor izquierdo deshabilitado inicialmente
IN1.value(0)  # Dirección 1 en estado bajo
IN2.value(0)  # Dirección 2 en estado bajo
ENB.value(0)  # Motor derecho deshabilitado inicialmente
IN3.value(0)  # Dirección 3 en estado bajo
IN4.value(0)  # Dirección 4 en estado bajo

def activar_motores():
    """Activa ambos motores habilitando los pines ENA y ENB"""
    ENA.value(1)  # Habilita el puente H del motor izquierdo
    ENB.value(1)  # Habilita el puente H del motor derecho

def desactivar_motores():
    """Desactiva ambos motores deshabilitando ENA y ENB"""
    ENA.value(0)  # Deshabilita el puente H del motor izquierdo
    ENB.value(0)  # Deshabilita el puente H del motor derecho

def adelante():
    """Mueve ambos motores hacia adelante - el vehículo avanza"""
    print("MOVIMIENTO: Adelante")
    activar_motores()  # Asegura que los motores estén habilitados
    # Motor izquierdo adelante: IN1=1, IN2=0
    IN1.value(1)
    IN2.value(0)
    # Motor derecho adelante: IN3=1, IN4=0
    IN3.value(1)
    IN4.value(0)

def atras():
    """Mueve ambos motores hacia atrás - el vehículo retrocede"""
    print("MOVIMIENTO: Atrás")
    activar_motores()  # Asegura que los motores estén habilitados
    # Motor izquierdo atrás: IN1=0, IN2=1
    IN1.value(0)
    IN2.value(1)
    # Motor derecho atrás: IN3=0, IN4=1
    IN3.value(0)
    IN4.value(1)

def izquierda():
    """Gira el vehículo a la izquierda - giro sobre su eje"""
    print("MOVIMIENTO: Izquierda")
    activar_motores()  # Asegura que los motores estén habilitados
    # Motor izquierdo atrás: IN1=0, IN2=1 (gira en reversa)
    IN1.value(0)
    IN2.value(1)
    # Motor derecho adelante: IN3=1, IN4=0 (gira hacia adelante)
    IN3.value(1)
    IN4.value(0)
    # Diferencial de giro: motores en direcciones opuestas

def derecha():
    """Gira el vehículo a la derecha - giro sobre su eje"""
    print("MOVIMIENTO: Derecha")
    activar_motores()  # Asegura que los motores estén habilitados
    # Motor izquierdo adelante: IN1=1, IN2=0 (gira hacia adelante)
    IN1.value(1)
    IN2.value(0)
    # Motor derecho atrás: IN3=0, IN4=1 (gira en reversa)
    IN3.value(0)
    IN4.value(1)
    # Diferencial de giro: motores en direcciones opuestas

def detener():
    """Detiene inmediatamente ambos motores"""
    print("MOVIMIENTO: Detener")
    # Primero detiene las señales de dirección
    IN1.value(0)  # Dirección 1 en bajo
    IN2.value(0)  # Dirección 2 en bajo
    IN3.value(0)  # Dirección 3 en bajo
    IN4.value(0)  # Dirección 4 en bajo
    # Luego desactiva los enables para ahorrar energía
    desactivar_motores()

ble = bluetooth.BLE()  # Crea una instancia del controlador Bluetooth
# Configura el servicio UART sobre BLE con nombre visible
uart = BLEUART(ble, name="ESP32-Motores")

# Contador para llevar registro de comandos recibidos
comandos_recibidos = 0

def on_rx():
    """
    Función callback que se ejecuta automáticamente
    cuando se reciben datos por Bluetooth
    """
    global comandos_recibidos  # Permite modificar la variable global
    try:
        # Lee y decodifica los datos recibidos por BLE
        data = uart.read().decode().strip()
        print(f"Comando {comandos_recibidos}: {data}")
        comandos_recibidos += 1  # Incrementa el contador
        
        # --- COMANDOS DE MOVIMIENTO ---
        # Los códigos !Bxxx corresponden a una app específica
        if data == "!B516":  # Botón 1 presionado (Adelante)
            adelante()
            
        elif data == "!B615":  # Botón 2 presionado (Atrás)
            atras()
            
        elif data == "!B714":  # Botón 3 presionado (Izquierda)
            izquierda()
            
        elif data == "!B813":  # Botón 4 presionado (Derecha)
            derecha()
            
        # --- COMANDOS DE DETENCIÓN ---
        # Se ejecutan cuando se sueltan los botones
        elif data in ["!B507", "!B606", "!B705", "!B804"]:
            detener()
            
        # --- COMANDOS ADICIONALES DE TEXTO ---
        elif data == "ACTIVAR":
            activar_motores()
            uart.write("Motores activados\n")
            
        elif data == "DESACTIVAR":
            desactivar_motores()
            uart.write("Motores desactivados\n")
            
        elif data == "ESTADO":
            # Consulta y envía el estado actual de todos los pines
            estado = f"ENA:{ENA.value()},IN1:{IN1.value()},IN2:{IN2.value()},"
            estado += f"ENB:{ENB.value()},IN3:{IN3.value()},IN4:{IN4.value()}"
            uart.write(f"Estado: {estado}\n")
            
        elif data == "AYUDA":
            # Envía lista de comandos disponibles al cliente
            ayuda = "Comandos:\n!B516:Adelante\n!B615:Atrás\n!B714:Izquierda\n"
            ayuda += "!B813:Derecha\n!B5/6/7/807:Detener\nACTIVAR/DESACTIVAR\nESTADO"
            uart.write(ayuda + "\n")
            
        else:
            # Respuesta para comandos no reconocidos
            uart.write(f"Comando desconocido: {data}\n")
            
    except Exception as e:
        # Manejo de errores en la recepción/procesamiento
        print(f"Error procesando comando: {e}")

# Asigna la función on_rx como manejador de interrupciones de recepción BLE
uart.irq(handler=on_rx)

# ================================================
# FUNCIÓN AUXILIAR PARA ENVIAR MENSAJES POR BLE
# ================================================
def enviar_mensaje(mensaje):
    """Envía un mensaje de texto a través de la conexión BLE"""
    try:
        uart.write(mensaje + "\n")
        print(f"Enviado: {mensaje}")
    except:
        print("Error enviando mensaje")

print("=" * 40)
print("Sistema de Control de Motores por BLE")
print("ESP32 listo para conectar")
print("Nombre BLE: ESP32-Motores")
print("=" * 40)

# Envía mensaje de inicio por BLE
print("Prueba inicial de motores...")
enviar_mensaje("Sistema iniciado")

# Pequeña secuencia de prueba automática
time.sleep(1)            # Espera 1 segundo
activar_motores()        # Activa motores
time.sleep(0.5)          # Mantiene activos 0.5 segundos
detener()                # Detiene motores

# Mensajes informativos en consola
print("Esperando comandos BLE...")
print("Usa una app como 'Serial Bluetooth Terminal'")
print("o 'BLE Scanner' para controlar los motores")

try:
    while True:
        # Bucle principal - mantiene el programa en ejecución
        # La recepción de comandos se maneja por interrupciones (irq)
        time.sleep(0.1)  # Pequeña pausa para evitar sobrecarga de CPU
        
except KeyboardInterrupt:
    # Manejo de interrupción por teclado (Ctrl+C)
    print("\nApagando sistema...")
    detener()              # Detiene los motores de forma segura
    desactivar_motores()   # Desactiva completamente los puentes H
    print("Sistema apagado correctamente")
