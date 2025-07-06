import heapq
from typing import List, Tuple, Dict

def bfs(start:str, end:str, network: Dict[str, List[Tuple[str, int]]], gpi_df, cpi_df, threshold_gpi:float = 2.0, threshold_cpi:int =60) -> List[str]:
    visited = set()
    queue = [(start, [start])]

    while queue:
        node, path = queue.pop(0)
        if node not in visited:
            visited.add(node)
            if node == end:
                return path
            for next_node, _ in network.get(node, []):
                gpi = gpi_df[gpi_df['iso3c']==next_node]['overall_score'].iloc[0]
                cpi = cpi_df[cpi_df['country_code']==next_node]['cpi_score'].iloc[0]
                if gpi < threshold_gpi and cpi > threshold_cpi and next_node not in visited:
                    queue.append((next_node, path + [next_node]))
    return []

def dfs(start: str, end: str, network: Dict[str, List[Tuple[str, int]]], gpi_df, cpi_df, threshold_gpi: float = 2.0, threshold_cpi: int = 60, path: List[str] = None) -> List[str]:
    if path is None:
        path = [start]
    if start == end:
        return path
    for next_node, _ in network.get(start, []):
        if next_node not in path:
            gpi = gpi_df[gpi_df['iso3c'] == next_node]['overall_score'].iloc[0]
            cpi = cpi_df[cpi_df['country_code'] == next_node]['cpi_score'].iloc[0]
            if gpi < threshold_gpi and cpi > threshold_cpi:
                new_path = dfs(next_node, end, network, gpi_df, cpi_df, threshold_gpi, threshold_cpi, path + [next_node])
                if new_path:
                    return new_path
    return []

def dijkstra(start: str, end: str, network: Dict[str, List[Tuple[str, int]]], gpi_df, cpi_df, threshold_gpi: float = 2.0, threshold_cpi: int = 60) -> Tuple[List[str], float]:
    scores = {node: float('inf') for node in set(network.keys()).union({x[0] for x in sum(network.values(), [])})}
    scores[start] = 0
    paths = {start: [start]}
    pq = List[Tuple[float, str]] = [(0, start)]
    while pq:
        current_score, current = heapq.heappop(pq)
        if current == end:
            return paths[current], current_score
        for next_node, dist in network.get(current, []):
            gpi = gpi_df[gpi_df['iso3c'] == next_node]['overall_score'].iloc[0]
            cpi = cpi_df[cpi_df['country_code'] == next_node]['cpi_score'].iloc[0]
            if gpi < threshold_gpi and cpi > threshold_cpi and current_score + dist < scores[next_node]:
                scores[next_node] = current_score + dist
                paths[next_node] = paths[current] + [next_node]
                heapq.heappush(pq, (scores[next_node], next_node))
    return [], float('inf')

def floyd_warshall(network: Dict[str, List[Tuple[str, int]]], gpi_df, cpi_df) -> Dict[Tuple[str, str], float]:
    nodes = list(set(network.keys()).union({x[0] for x in sum(network.values(), [])}))
    dist = {(u, v): float('inf') for u in nodes for v in nodes}
    for u in nodes:
        dist[(u, u)] = 0
    for u in network:
        for v, d in network[u]:
            gpi = gpi_df[gpi_df['iso3c'] == v]['overall_score'].iloc[0]
            cpi = cpi_df[cpi_df['country_code'] == v]['cpi_score'].iloc[0]
            if gpi < 2.0 and cpi > 60:
                dist[(u, v)] = d
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[(i, k)] != float('inf') and dist[(k, j)] != float('inf'):
                    dist[(i, j)] = min(dist[(i, j)], dist[(i, k)] + dist[(k, j)])
    return dist