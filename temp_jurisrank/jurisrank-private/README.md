# JurisRank - Sistema Automático de Recolección de Fallos CSJN

## Descripción
JurisRank es un sistema completo y autónomo para la recolección automática, análisis y ranking de fallos de la Corte Suprema de Justicia de la Nación Argentina.

## Características Principales

### ✅ Funcionalidades Implementadas
- **Recolección Automática**: Sistema de scraping con búsqueda por fechas
- **Base de Datos SQLite**: Almacenamiento local con estructura optimizada
- **Algoritmo JurisRank**: Cálculo de importancia basado en múltiples factores
- **Scheduler Automático**: Recolección diaria a las 08:00 y 20:00
- **Monitoreo de Salud**: Verificaciones automáticas cada 6 horas
- **Recuperación de Errores**: Sistema de reintentos con backoff exponencial
- **Reportes Completos**: Análisis estadístico y visualizaciones
- **Logging Avanzado**: Registro detallado de todas las operaciones

### 📊 Estado Actual
- **Total de Fallos**: 72 fallos históricos (Agosto-Septiembre 2025)
- **Algoritmo JurisRank**: Activo y funcionando
- **Conectividad CSJN**: ✅ Verificada
- **Base de Datos**: ✅ Operativa
- **Sistema de Monitoreo**: ✅ Activo

## Estructura del Sistema

```
/home/user/output/
├── jurisrank.db              # Base de datos principal
├── jurisrank_config.json     # Configuración del sistema
├── start_jurisrank.py        # Script de inicialización
├── logs/
│   └── error_recovery.log    # Logs de recuperación de errores
└── data/                     # Datos temporales
```

## Comandos Principales

### Inicialización
```python
from jurisrank_system import JurisRankSystem
sistema = JurisRankSystem()
```

### Operaciones Manuales
```python
# Verificar salud del sistema
sistema.scheduler.health_check_job()

# Recolección manual de fechas específicas
sistema.scheduler.run_immediate_collection(fecha_inicio, fecha_fin)

# Calcular JurisRank para todos los fallos
sistema.jurisrank_algo.calculate_jurisrank_scores()

# Recuperar fechas con errores
sistema.error_recovery.recover_failed_dates()

# Generar reporte completo
sistema.report_generator.generate_complete_report()
```

### Scheduler Automático
```python
# Iniciar recolección automática
sistema.scheduler.start_scheduler()

# Detener scheduler
sistema.scheduler.stop_scheduler()
```

## Algoritmo JurisRank

El algoritmo calcula la importancia de cada fallo basándose en:

1. **Similitud Textual**: PageRank sobre grafo de similitud de documentos
2. **Factor Temporal**: Fallos más recientes tienen mayor peso
3. **Longitud del Documento**: Textos más extensos indican mayor complejidad
4. **Palabras Clave**: Número y relevancia de keywords
5. **Tema Jurídico**: Ponderación especial para temas importantes

## Configuración Automática

El sistema está configurado para:
- Recolección diaria a las **08:00** y **20:00**
- Monitoreo de salud cada **6 horas**
- Reintentos automáticos con backoff exponencial
- Recuperación automática de fechas fallidas
- Logging detallado de todas las operaciones

## Próximos Pasos Recomendados

1. **Activar Scheduler**: Iniciar recolección automática diaria
2. **Interfaz Web**: Desarrollar frontend para consultas
3. **Alertas**: Configurar notificaciones por email
4. **Expansión**: Incluir otros tribunales federales
5. **ML Avanzado**: Mejorar algoritmo con machine learning
6. **API REST**: Exponer funcionalidades vía API

## Soporte y Mantenimiento

- **Logs**: Revisar `/logs/error_recovery.log` para errores
- **Base de Datos**: Backup automático recomendado
- **Monitoreo**: Health checks cada 6 horas automáticamente
- **Updates**: Sistema modular permite actualizaciones incrementales

---

**Versión**: 1.0.0  
**Estado**: ✅ Completamente Operativo  
**Última Actualización**: 2025-09-10 02:38:59
