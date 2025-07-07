from fastapi import APIRouter, HTTPException
from app.services.algorithm import bfs, dfs, dijkstra, floyd_warshall
from app.core.database import gpi_df, cpi_df
from typing import List, Tuple
import random

router = APIRouter()


def generate_flight_network(gpi_df, cpi_df):
    countries = set(gpi_df['iso3c'].tolist()).intersection(cpi_df['country_code'].tolist())
    flight_network = {country: [] for country in countries}

    print(f"Países en flight_network (antes de conexiones): {list(countries)}")

    for i, origin in enumerate(countries):
        for j, dest in enumerate(countries):
            if i != j and len(flight_network[origin]) < 4:  # Máximo 4 conexiones por país
                gpi = gpi_df[gpi_df['iso3c'] == dest]['overall_score'].iloc[0]
                cpi = cpi_df[cpi_df['country_code'] == dest]['cpi_score'].iloc[0]
                if gpi < 2.0 and cpi > 60:  # Aplicar filtros aquí
                    distance = random.randint(5000, 15000)
                    flight_network[origin].append((dest, distance))
                    flight_network[dest].append((origin, distance))  # Bidireccional

    print(f"Conexiones en flight_network: {dict(flight_network)}")
    return flight_network


flight_network = generate_flight_network(gpi_df, cpi_df)


@router.get("/route/{origin}/{destination}")
async def get_route(origin: str, destination: str, algorithm: str = "dijkstra", gpi_threshold: float = 2.0,
                    cpi_threshold: int = 60):
    origin = origin.upper()
    destination = destination.upper()

    print(f"Procesando solicitud: origin={origin}, destination={destination}")
    print(f"Claves en flight_network: {list(flight_network.keys())}")

    if algorithm not in ["bfs", "dfs", "dijkstra", "floyd_warshall"]:
        raise HTTPException(status_code=400, detail="Algoritmo no soportado")
    if origin not in flight_network or destination not in flight_network:
        raise HTTPException(status_code=404, detail="País no encontradoooooooooooooooooooooo")

    if algorithm == "bfs":
        route = bfs(origin, destination, flight_network, gpi_df, cpi_df, gpi_threshold, cpi_threshold)
    elif algorithm == "dfs":
        route = dfs(origin, destination, flight_network, gpi_df, cpi_df, gpi_threshold, cpi_threshold)
    elif algorithm == "dijkstra":
        route, _ = dijkstra(origin, destination, flight_network, gpi_df, cpi_df, gpi_threshold, cpi_threshold)
    else:  # floyd_warshall
        dist = floyd_warshall(flight_network, gpi_df, cpi_df)
        route = [origin]
        current = origin
        while current != destination and dist[(current, destination)] != float('inf'):
            found = False
            for next_dest, _ in flight_network.get(current, []):  # Desempaquetar (dest, distance)
                if dist[(current, next_dest)] != float('inf') and dist[(next_dest, destination)] != float('inf'):
                    if dist[(current, next_dest)] + dist[(next_dest, destination)] == dist[(current, destination)]:
                        route.append(next_dest)
                        current = next_dest
                        found = True
                        break
            if not found:
                break  # Salir si no se encuentra un nodo válido
        if current != destination:
            route = []

        if not route:
            raise HTTPException(status_code=404, detail="No se encontró ruta")

    return {"route": route, "algorithm": algorithm}