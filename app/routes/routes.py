from fastapi import APIRouter, HTTPException
from app.services.algorithm import bfs, dfs, dijkstra, floyd_warshall
from app.core.database import gpi_df, cpi_df, merged_df
from typing import List, Tuple
import random
router = APIRouter()

def generate_flight_network(gpi_df,cpi_df):
    countries = set(gpi_df['iso3c'].tolist()).intersection(cpi_df['country_code'].tolist())
    flight_network = {country: [] for country in countries}
    for country in countries:
        possible_destination = list(countries - {country})
        num_connections = min(random.randint(2,4), len(possible_destination))
        destinations = random.sample(possible_destination, num_connections)

        for dest in destinations:
            distance = random.randint(5000,15000)
            flight_network[country].append((dest, distance))
    return flight_network


flight_network = generate_flight_network(gpi_df,cpi_df)

@router.get("/route/{origin}/{destination}")
async def get_route(origin: str, destination: str, algorithm: str = "dijkstra", gpi_threshold: float = 2.0, cpi_threshold: int = 60):
    if algorithm not in ["bfs", "dfs", "dijkstra", "floyd_warshall"]:
        raise HTTPException(status_code=400, detail="Invalid algorithm")
    if origin not in flight_network or destination not in flight_network:
        raise HTTPException(status_code=404, detail="Country not found")

    if algorithm == "bfs":
        route = bfs(origin, destination, flight_network, gpi_df, cpi_df, gpi_threshold, cpi_threshold)
    elif algorithm == "dfs":
        route = dfs(origin,destination, flight_network, gpi_df, cpi_df, gpi_threshold, cpi_threshold)
    elif algorithm == "dijkstra":
        route,_=dijkstra(origin,destination,flight_network,gpi_df,cpi_df,gpi_threshold,cpi_threshold)
    else:
        dist = floyd_warshall(flight_network,gpi_df,cpi_df)
        route = [origin]
        current = origin
        while current != destination and dist[(current, destination)]!=float('inf'):
            for next_node,_ in flight_network.get(current,[]):
                if dist[(current, next_node[0])] + dist[(next_node[0],destination)]:
                    route.append(next_node[0])
                    current = next_node[0]
                    break
        if current != destination:
            route = []
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    return {'route': route, 'algorithm': algorithm}