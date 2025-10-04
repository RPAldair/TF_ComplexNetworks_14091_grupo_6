# TF_ComplexNetworks_14091_grupo_6
Repositorio git trabajo parcial y final Complex Networks

## Análisis de Redes Cliente-Servicio

Este proyecto proporciona un sistema completo para analizar redes cliente-servicio, con énfasis en la comparación entre diferentes períodos temporales (pre y post evento).

### Características Principales

- **Red Cliente-Servicio**: Modelado de redes con nodos (clientes y servicios) y enlaces (ponderados o no ponderados)
- **Metadatos de Servicios**: Cada servicio puede tener metadatos asociados (capacidad, tipo, etc.)
- **Comparación de Períodos**: Análisis comparativo entre redes pre y post evento
- **Métricas de Centralidad**: Cálculo de centralidad de grado, intermediación, cercanía y eigenvector
- **Análisis de Conectividad**: Métricas de conectividad, densidad, diámetro y caminos más cortos
- **Detección de Comunidades**: Identificación de comunidades usando algoritmos de Louvain, propagación de etiquetas o modularidad greedy
- **Transformaciones Estructurales**: Identificación de cambios clave en la estructura de la red
- **Visualizaciones**: Gráficos de redes, comparaciones de centralidad y estructuras comunitarias

### Instalación

1. Clone el repositorio:
```bash
git clone https://github.com/RPAldair/TF_ComplexNetworks_14091_grupo_6.git
cd TF_ComplexNetworks_14091_grupo_6
```

2. Instale las dependencias:
```bash
pip install -r requirements.txt
```

### Uso Básico

#### Ejemplo Simple

```python
from network_analysis import (
    ClientServiceNetwork,
    NetworkMetrics,
    NetworkComparison,
    comprehensive_period_comparison
)

# Crear red pre-evento
network_pre = ClientServiceNetwork(weighted=True)
network_pre.add_service('S1', {'name': 'Web Server', 'capacity': 100})
network_pre.add_client('C1')
network_pre.add_connection('C1', 'S1', weight=5.0)

# Crear red post-evento
network_post = ClientServiceNetwork(weighted=True)
network_post.add_service('S1', {'name': 'Web Server', 'capacity': 120})
network_post.add_client('C1')
network_post.add_connection('C1', 'S1', weight=7.0)

# Comparar redes
results = comprehensive_period_comparison(network_pre, network_post)
```

#### Ejecutar Ejemplo Completo

El proyecto incluye un ejemplo completo que demuestra todas las funcionalidades:

```bash
python example_usage.py
```

Este script:
1. Crea dos redes de ejemplo (pre y post evento)
2. Realiza un análisis comparativo completo
3. Genera archivos CSV con resultados detallados
4. Crea visualizaciones de las redes y métricas

### Estructura del Proyecto

- `network_analysis.py`: Módulo principal con todas las clases y funciones
  - `ClientServiceNetwork`: Clase para representar redes cliente-servicio
  - `NetworkMetrics`: Cálculo de métricas de red
  - `NetworkComparison`: Comparación entre redes de diferentes períodos
  - `NetworkVisualization`: Herramientas de visualización
  - `comprehensive_period_comparison()`: Función de análisis completo

- `example_usage.py`: Script de ejemplo que demuestra el uso del módulo
- `requirements.txt`: Dependencias del proyecto

### Resultados Potenciales

El análisis de comparación entre períodos proporciona:

1. **Cambios en Centralidad**:
   - Identificación de nodos con mayor/menor centralidad
   - Métricas de cambio absoluto y porcentual
   - Top nodos por cambio en centralidad

2. **Cambios en Conectividad**:
   - Número de componentes conectados
   - Densidad de la red
   - Diámetro y caminos más cortos promedio
   - Coeficiente de clustering

3. **Cambios en Comunidades**:
   - Número de comunidades detectadas
   - Nodos que cambiaron de comunidad
   - Estructura comunitaria antes y después

4. **Transformaciones Estructurales**:
   - Nodos y enlaces agregados/removidos
   - Cambios en densidad de la red
   - Identificación de nodos críticos

### Cargar Datos desde Archivos

#### Desde Edge List

```python
network = ClientServiceNetwork(weighted=True)
network.load_from_edgelist('edges.txt', weighted=True)
```

Formato del archivo `edges.txt`:
```
C1 S1 5.0
C2 S1 3.0
C1 S2 4.0
```

#### Metadatos desde CSV

```python
network.load_metadata('service_metadata.csv')
```

Formato del archivo `service_metadata.csv`:
```csv
service_id,name,capacity,type
S1,Web Server,100,web
S2,Database,80,database
```

### API Completa

#### ClientServiceNetwork

- `add_service(service_id, metadata)`: Agregar un servicio
- `add_client(client_id)`: Agregar un cliente
- `add_connection(client_id, service_id, weight)`: Agregar conexión
- `load_from_edgelist(filepath, weighted)`: Cargar desde archivo
- `load_metadata(filepath)`: Cargar metadatos
- `get_service_metadata(service_id)`: Obtener metadatos de servicio

#### NetworkMetrics

- `calculate_centrality(network)`: Calcular métricas de centralidad
- `calculate_connectivity(network)`: Calcular métricas de conectividad
- `detect_communities(network, method)`: Detectar comunidades

#### NetworkComparison

- `compare_centrality(network_pre, network_post)`: Comparar centralidad
- `compare_connectivity(network_pre, network_post)`: Comparar conectividad
- `compare_communities(network_pre, network_post)`: Comparar comunidades
- `identify_structural_changes(network_pre, network_post)`: Identificar cambios estructurales

#### NetworkVisualization

- `plot_network(network, title)`: Graficar red
- `plot_centrality_comparison(centrality_df, metric)`: Graficar comparación de centralidad
- `plot_community_structure(network, communities)`: Graficar estructura comunitaria

### Dependencias

- NetworkX: Análisis de redes
- Pandas: Manipulación de datos
- NumPy: Operaciones numéricas
- Matplotlib: Visualizaciones
- Python-Louvain: Detección de comunidades (opcional)

### Contribuciones

Este proyecto fue desarrollado como parte del trabajo final del curso Complex Networks 14091, Grupo 6.

### Licencia

MIT License
