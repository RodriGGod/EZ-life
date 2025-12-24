"""
Test script to display tooltip directly
"""
import sys
sys.path.insert(0, 'd:/DEVELOPER/Aplicaciones/EZ-life/src')

from utils.tooltip import show_tooltip
import time

print("Mostrando tooltip de prueba...")
show_tooltip("🌍 Cambiado a: Brave")
print("Tooltip mostrado. Debería aparecer cerca del cursor con fondo NEGRO y texto BLANCO")
time.sleep(3)
print("Test finalizado")
