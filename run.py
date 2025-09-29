#!/usr/bin/env python3
"""
Script principal para ejecutar el Sistema de Riego Automatizado
IPC2 - Proyecto 2
Universidad de San Carlos de Guatemala
"""

import os
import sys

if __name__ == '__main__':
    print("=" * 60)
    print("Sistema de Riego Automatizado - GuateRiegos 2.0")
    print("IPC2 - Proyecto 2")
    print("Universidad de San Carlos de Guatemala")
    print("=" * 60)
    print("Servidor iniciando en http://0.0.0.0:5000")
    print("Presione Ctrl+C para detener el servidor")
    print("=" * 60)
    
    # Ejecutar directamente el archivo app.py
    os.system("python app.py")
