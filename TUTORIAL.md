# Tutorial: Análisis de Redes Cliente-Servicio

## Introducción

Este tutorial muestra cómo usar el módulo `network_analysis` para analizar redes cliente-servicio y comparar diferentes períodos temporales (pre vs. post evento).

## Tabla de Contenidos

1. [Instalación](#instalación)
2. [Conceptos Básicos](#conceptos-básicos)
3. [Caso de Uso 1: Red Simple](#caso-de-uso-1-red-simple)
4. [Caso de Uso 2: Comparación de Períodos](#caso-de-uso-2-comparación-de-períodos)
5. [Caso de Uso 3: Cargar Datos desde Archivos](#caso-de-uso-3-cargar-datos-desde-archivos)
6. [Análisis Avanzado](#análisis-avanzado)
7. [Interpretación de Resultados](#interpretación-de-resultados)

## Instalación

```bash
pip install -r requirements.txt
```

## Conceptos Básicos

### Red Cliente-Servicio

Una red cliente-servicio es un grafo bipartito donde:
- **Clientes**: Nodos que consumen servicios
- **Servicios**: Nodos que proveen funcionalidades
- **Enlaces**: Conexiones entre clientes y servicios (pueden ser ponderadas)

### Metadatos de Servicios

Cada servicio puede tener información adicional:
- Nombre
- Capacidad
- Tipo
- Cualquier otro atributo relevante

## Caso de Uso 1: Red Simple

### Crear una red básica

```python
from network_analysis import ClientServiceNetwork

# Crear red ponderada
network = ClientServiceNetwork(weighted=True)

# Agregar un servicio con metadatos
network.add_service('S1', {
    'name': 'Servidor Web',
    'capacity': 100,
    'type': 'web'
})

# Agregar un cliente
network.add_client('C1')

# Crear conexión entre cliente y servicio
network.add_connection('C1', 'S1', weight=5.0)

print(f"Red: {network.number_of_nodes()} nodos, {network.number_of_edges()} enlaces")
```

### Calcular métricas básicas

```python
from network_analysis import NetworkMetrics

# Calcular centralidad
centrality = NetworkMetrics.calculate_centrality(network)
print("Centralidad de grado:", centrality['degree'])

# Calcular conectividad
connectivity = NetworkMetrics.calculate_connectivity(network)
print("Densidad:", connectivity['density'])

# Detectar comunidades
communities = NetworkMetrics.detect_communities(network)
print("Comunidades:", communities)
```

### Visualizar la red

```python
from network_analysis import NetworkVisualization
import matplotlib.pyplot as plt

NetworkVisualization.plot_network(network, "Mi Red")
plt.show()
```

## Caso de Uso 2: Comparación de Períodos

Este es el caso principal: comparar una red antes y después de un evento.

### Paso 1: Crear red pre-evento

```python
from network_analysis import ClientServiceNetwork

network_pre = ClientServiceNetwork(weighted=True)

# Agregar servicios iniciales
network_pre.add_service('S1', {'name': 'Web Server', 'capacity': 100})
network_pre.add_service('S2', {'name': 'Database', 'capacity': 80})

# Agregar clientes
network_pre.add_client('C1')
network_pre.add_client('C2')
network_pre.add_client('C3')

# Agregar conexiones
network_pre.add_connection('C1', 'S1', 5.0)
network_pre.add_connection('C2', 'S1', 3.0)
network_pre.add_connection('C3', 'S2', 4.0)
```

### Paso 2: Crear red post-evento

```python
network_post = ClientServiceNetwork(weighted=True)

# Servicios con capacidades actualizadas
network_post.add_service('S1', {'name': 'Web Server', 'capacity': 120})
network_post.add_service('S2', {'name': 'Database', 'capacity': 100})
network_post.add_service('S3', {'name': 'Cache', 'capacity': 80})  # Nuevo servicio

# Clientes (algunos nuevos)
network_post.add_client('C1')
network_post.add_client('C2')
network_post.add_client('C3')
network_post.add_client('C4')  # Nuevo cliente

# Conexiones actualizadas
network_post.add_connection('C1', 'S1', 6.0)  # Peso aumentado
network_post.add_connection('C2', 'S1', 4.0)
network_post.add_connection('C3', 'S2', 5.0)
network_post.add_connection('C4', 'S3', 7.0)  # Nueva conexión
network_post.add_connection('C1', 'S3', 3.0)  # Nueva conexión
```

### Paso 3: Realizar comparación

```python
from network_analysis import comprehensive_period_comparison

results = comprehensive_period_comparison(
    network_pre, 
    network_post, 
    output_prefix="mi_analisis"
)
```

Esto generará:
- `mi_analisis_centrality.csv`: Tabla con cambios de centralidad
- Análisis impreso en consola

### Paso 4: Analizar resultados específicos

```python
# Cambios en centralidad
centrality_df = results['centrality']
top_changes = centrality_df.nlargest(5, 'degree_change')
print("Nodos con mayor aumento de centralidad:")
print(top_changes[['node', 'degree_change']])

# Cambios en conectividad
conn = results['connectivity']
print(f"Cambio en densidad: {conn['changes']['density']:.4f}")
print(f"Cambio en diámetro: {conn['changes'].get('diameter', 'N/A')}")

# Cambios en comunidades
comm = results['communities']
print(f"Comunidades antes: {comm['num_communities_pre']}")
print(f"Comunidades después: {comm['num_communities_post']}")

# Transformaciones estructurales
struct = results['structural_changes']
print(f"Nodos agregados: {struct['nodes_added']}")
print(f"Enlaces agregados: {struct['edges_added']}")
```

## Caso de Uso 3: Cargar Datos desde Archivos

### Cargar desde edge list

Crear archivo `red_pre.txt`:
```
C1 S1 5.0
C2 S1 3.0
C3 S2 4.0
```

```python
network_pre = ClientServiceNetwork(weighted=True)
network_pre.load_from_edgelist('red_pre.txt', weighted=True)
```

### Cargar metadatos desde CSV

Crear archivo `servicios.csv`:
```csv
service_id,name,capacity,type
S1,Web Server,100,web
S2,Database,80,database
```

```python
network_pre.load_metadata('servicios.csv')

# Acceder a metadatos
metadata = network_pre.get_service_metadata('S1')
print(metadata)  # {'name': 'Web Server', 'capacity': 100, 'type': 'web'}
```

## Análisis Avanzado

### Comparación de centralidad específica

```python
from network_analysis import NetworkComparison

centrality_df = NetworkComparison.compare_centrality(network_pre, network_post)

# Filtrar solo servicios
services = [node for node in centrality_df['node'] if node.startswith('S')]
service_df = centrality_df[centrality_df['node'].isin(services)]

print("Cambios en centralidad de servicios:")
print(service_df[['node', 'betweenness_change', 'closeness_change']])
```

### Análisis de comunidades detallado

```python
from network_analysis import NetworkMetrics

# Detectar con diferentes métodos
communities_louvain = NetworkMetrics.detect_communities(network_post, method='louvain')
communities_label = NetworkMetrics.detect_communities(network_post, method='label_propagation')

print("Comunidades (Louvain):", communities_louvain)
print("Comunidades (Label Propagation):", communities_label)
```

### Visualizaciones personalizadas

```python
from network_analysis import NetworkVisualization
import matplotlib.pyplot as plt

# Graficar centralidad para múltiples métricas
centrality_df = results['centrality']

for metric in ['degree', 'betweenness', 'closeness']:
    fig = NetworkVisualization.plot_centrality_comparison(
        centrality_df, 
        metric=metric, 
        top_n=10
    )
    fig.savefig(f'centrality_{metric}.png', dpi=150, bbox_inches='tight')
    plt.close()
```

### Identificar nodos críticos

```python
# Nodos con mayor cambio porcentual en centralidad
critical_nodes = centrality_df.nlargest(5, 'betweenness_change_pct')
print("Nodos críticos (mayor cambio % en betweenness):")
for _, row in critical_nodes.iterrows():
    print(f"  {row['node']}: {row['betweenness_change_pct']:.2f}%")
```

## Interpretación de Resultados

### Centralidad

- **Degree Centrality**: Mide el número de conexiones directas
  - Aumento → Nodo más conectado (más clientes o servicios vinculados)
  - Disminución → Nodo menos activo

- **Betweenness Centrality**: Mide cuántos caminos pasan por el nodo
  - Aumento → Nodo más importante como intermediario
  - Disminución → Nodo menos crítico para conectividad

- **Closeness Centrality**: Mide cercanía promedio a otros nodos
  - Aumento → Nodo más accesible desde otros nodos
  - Disminución → Nodo más aislado

- **Eigenvector Centrality**: Mide importancia basada en vecinos importantes
  - Aumento → Conectado a nodos más influyentes
  - Disminución → Conectado a nodos menos influyentes

### Conectividad

- **Densidad**: Proporción de enlaces existentes vs. posibles
  - Aumento → Red más interconectada
  - Disminución → Red más dispersa

- **Diámetro**: Camino más largo entre dos nodos
  - Aumento → Red más extendida
  - Disminución → Red más compacta

- **Average Shortest Path**: Distancia promedio entre nodos
  - Aumento → Nodos más alejados en promedio
  - Disminución → Mejor conectividad general

- **Clustering Coefficient**: Tendencia a formar grupos
  - Aumento → Más agrupamiento local
  - Disminución → Estructura más plana

### Comunidades

- **Aumento en número de comunidades**: Mayor fragmentación/especialización
- **Disminución en número de comunidades**: Mayor integración
- **Nodos cambiando de comunidad**: Reestructuración de relaciones

### Transformaciones Estructurales

- **Nodos agregados**: Crecimiento de la red (nuevos clientes o servicios)
- **Nodos removidos**: Contracción o eliminación
- **Enlaces agregados**: Nuevas relaciones cliente-servicio
- **Enlaces removidos**: Relaciones terminadas

## Ejemplos de Interpretación

### Escenario 1: Migración a la Nube

**Observaciones:**
- Nuevo servicio S6 (Load Balancer) con alta centralidad
- Aumento en betweenness de S6
- Reducción en diámetro de la red

**Interpretación:**
La introducción del balanceador de carga mejoró la conectividad general. La red es ahora más eficiente con caminos más cortos entre nodos.

### Escenario 2: Evento de Falla

**Observaciones:**
- Servicio S2 con reducción drástica en degree centrality
- Aumento en enlaces a S1 y S3
- Aumento en número de comunidades

**Interpretación:**
Después de la falla de S2, los clientes se redistribuyeron a otros servicios, creando una estructura más fragmentada pero con mayor redundancia.

### Escenario 3: Crecimiento Orgánico

**Observaciones:**
- Incremento constante en nodos (clientes nuevos)
- Density se mantiene constante
- Aumento moderado en todas las centralidades

**Interpretación:**
La red está creciendo de manera balanceada, manteniendo su estructura mientras escala.

## Mejores Prácticas

1. **Siempre limpiar datos**: Verificar que los archivos de entrada no tengan duplicados
2. **Normalizar identificadores**: Usar nombres consistentes para nodos
3. **Documentar eventos**: Registrar qué evento se está analizando
4. **Comparar múltiples métricas**: No confiar solo en una métrica
5. **Visualizar resultados**: Las visualizaciones ayudan a identificar patrones
6. **Guardar resultados**: Exportar análisis para referencias futuras

## Solución de Problemas

### Error: "Graph is not connected"

Si la red no está conectada, algunas métricas (como diámetro) se calcularán solo para el componente más grande.

```python
connectivity = NetworkMetrics.calculate_connectivity(network)
if not connectivity['is_connected']:
    print("Red desconectada. Métricas calculadas para componente mayor.")
```

### Error: "Eigenvector centrality did not converge"

Para algunas redes, eigenvector centrality puede no converger. El módulo maneja esto automáticamente asignando valores de 0.

### Warnings sobre comunidades

Si no tiene `python-louvain` instalado, el método cambia automáticamente a 'greedy'. Instale para mejores resultados:

```bash
pip install python-louvain
```

## Recursos Adicionales

- NetworkX Documentation: https://networkx.org/
- Ejemplo completo: Ver `example_usage.py`
- Jupyter Notebook: Ver `example_notebook.ipynb`
- Repositorio: https://github.com/RPAldair/TF_ComplexNetworks_14091_grupo_6
