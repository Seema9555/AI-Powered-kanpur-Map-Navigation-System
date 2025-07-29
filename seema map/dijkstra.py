import heapq

def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()

    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue

        visited.add(node)
        path = path + [node]

        if node == end:
            return path

        for adj, weight in graph.get(node, {}).items():
            if adj not in visited:
                heapq.heappush(queue, (cost + weight, adj, path))

    return None
