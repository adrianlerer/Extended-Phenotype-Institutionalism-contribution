#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
JurisRank - Sistema Automático de Recolección de Fallos CSJN
Script de inicialización automática
'''

import os
import sys
import json
from datetime import datetime, timedelta

def main():
    print("🚀 Iniciando JurisRank System...")

    # Importar el sistema (requiere que esté en el path)
    try:
        from jurisrank_system import JurisRankSystem
        print("✅ Módulos importados correctamente")
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        return False

    # Inicializar sistema
    sistema = JurisRankSystem()
    print("✅ Sistema JurisRank inicializado")

    # Verificar configuración
    config_file = os.path.join(sistema.base_dir, "jurisrank_config.json")
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        print(f"✅ Configuración cargada: {config['sistema']['nombre']} v{config['sistema']['version']}")

    # Verificar salud del sistema
    sistema.scheduler.health_check_job()

    # Iniciar scheduler automático
    respuesta = input("¿Iniciar scheduler automático? (y/N): ")
    if respuesta.lower() in ['y', 'yes', 's', 'si']:
        sistema.scheduler.start_scheduler()
        print("✅ Scheduler automático iniciado")
        print("📅 El sistema recolectará fallos automáticamente a las 08:00 y 20:00")
        print("🏥 Verificaciones de salud cada 6 horas")

        # Mantener el programa corriendo
        try:
            print("🔄 Sistema corriendo... (Ctrl+C para detener)")
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo sistema...")
            sistema.scheduler.stop_scheduler()
            print("✅ Sistema detenido correctamente")

    return True

if __name__ == "__main__":
    main()
