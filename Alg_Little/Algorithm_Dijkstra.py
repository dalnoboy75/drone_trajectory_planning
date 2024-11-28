import sys
import heapq


def dijkstra(n, m, s, t: int, edges: list):
    gr = [[] for _ in range(n + 1)]

    for i in range(m):
        u = edges[i][0]
        v = edges[i][1]
        w = edges[i][2]
        gr[u].append((v, w))
        gr[v].append((u, w))

    put = [-1] * (n + 1)
    dist = []
    visited = [0] * (n + 1)
    ans = [float("inf")] * (n + 1)

    heapq.heappush(dist, (0, s))
    ans[s] = 0

    while dist:
        d, u = heapq.heappop(dist)
        visited[u] = 1
        ans[u] = d

        if u == t:
            break

        for v, d1 in gr[u]:
            if visited[v]:
                continue

            new_d = d + d1
            if new_d < ans[v]:
                if ans[v] < float("inf"):
                    dist.remove((ans[v], v))
                    heapq.heapify(dist)

                ans[v] = new_d
                put[v] = u
                heapq.heappush(dist, (new_d, v))

    if ans[t] == float("inf"):
        return -1, []

    way = []
    tu = t
    while put[t] != -1:
        way.append(t)
        t = put[t]
    way.append(s)
    way.reverse()

    return ans[tu], way
