# Análisis de Datos Económicos Geolocalizados utilizando Persistencia Homológica

Paulina Leal Mosqueda, A01659576
Samuel López Araiza Cadena, A01026507
Santiago Nava Figueroa, A01174557
Ricardo Villareal Bazán, A01666859


Este repositorio contiene un cuaderno de Jupyter (`RetoTopologia62.ipynb`) que realiza un análisis geoespacial de servicios de salud en la Zona Metropolitana. Se utilizan datos de establecimientos, consultorios y hospitales de la Ciudad de México y el Estado de México para explorar cobertura, conectividad y vacíos en el acceso a servicios médicos mediante técnicas de persistencia homológica y clustering.

## Qué hace el documento

- Carga y limpia datos de establecimientos de salud de INEGI y DENUE.
- Filtra establecimientos del sector salud y selecciona coordenadas geográficas relevantes.
- Genera visualizaciones descriptivas de servicios médicos por alcaldía y municipio.
- Construye complejos simpliciales de Vietoris-Rips para analizar conectividad espacial.
- Usa homología persistente para identificar "huecos" y zonas con posible falta de cobertura a 1 km.
- Compara resultados para hospitales y consultorios externos.
- Aplica K-Means para agrupar servicios y contrastar hallazgos con el análisis topológico.
- Simula la adición de nuevos hospitales o consultorios y evalúa el efecto sobre los huecos persistentes.

## Requisitos de librerías

Las dependencias principales están listadas en `requirements.txt`. Para instalar todas las librerías necesarias, ejecuta:

```bash
pip install -r requirements.txt
```

Dependencias clave:

- numpy==2.4.4
- pandas==3.0.2
- matplotlib==3.10.8
- scipy==1.17.1
- scikit-learn==1.8.0
- ripser==0.6.14
- persim==0.3.8
- gudhi==3.12.0
- pyproj==3.6.1
- shapely==2.0.6

## Archivos principales

- `RetoTopologia62.ipynb`: Notebook con el análisis completo.
- `requirements.txt`: Lista de dependencias del proyecto.
- `denue_inegi_09_.csv`, `denue_inegi_15_1.csv`, `denue_inegi_15_2.csv`: datos de establecimientos.


## Uso rápido

1. Instala dependencias: `pip install -r requirements.txt`
2. Abre el notebook `RetoTopologia62.ipynb` en Jupyter.
3. Ejecuta las celdas en orden para reproducir el análisis.

## Objetivo general

El objetivo del proyecto es usar persistencia homológica y análisis de clustering para identificar áreas con posible falta de acceso a servicios de salud, comparar el comportamiento de hospitales y consultorios, y analizar si la presencia de consultorios ayuda a reducir los vacíos de cobertura.
