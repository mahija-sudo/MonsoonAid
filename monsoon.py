"""MonsoonAid - priority- and vehicle-aware relief delivery routing on a flood grid.
BFS vs UCS vs A*. All numbers in the deck come from running this file."""
import heapq, random, time, json, itertools, statistics as st

N = 10
DEPOT = (0, 0)
DESTS = {"D1": ((9, 9), 1), "D2": ((9, 3), 2), "D3": ((4, 9), 3)}   # name: (cell, priority)
DELAY = {0: 0.0, 1: 1.0, 2: 3.0, 3: 6.0}                             # extra minutes per cell, level 4 = blocked
VEH = {"Van": (1.0, 1), "Truck": (1.25, 2), "4x4": (1.5, 3)}         # name: (base min/move, max passable depth)
SCEN = {"Low": (.55, .77, .90, .97), "Moderate": (.40, .58, .76, .90), "Severe": (.28, .45, .62, .78)}
MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def make_base(seed):
    r = random.Random(seed)
    z = [[r.random() for _ in range(N)] for _ in range(N)]
    for _ in range(2):  # smooth into flood "blobs"
        z = [[sum(z[a][b] for a, b in [(i, j)] + [(i+di, j+dj) for di, dj in MOVES
              if 0 <= i+di < N and 0 <= j+dj < N]) / (1 + sum(1 for di, dj in MOVES if 0 <= i+di < N and 0 <= j+dj < N))
              for j in range(N)] for i in range(N)]
    flat = sorted(v for row in z for v in row)
    return [[flat.index(z[i][j]) / (N*N - 1) for j in range(N)] for i in range(N)]  # percentile in [0,1]

def depth_grid(base, scen):
    t = SCEN[scen]
    g = [[sum(base[i][j] >= th for th in t) for j in range(N)] for i in range(N)]
    for c in [DEPOT] + [v[0] for v in DESTS.values()]:
        g[c[0]][c[1]] = 0          # depot and affected locations are reachable cells
    return g

def nbrs(g, c, veh):
    base, maxd = VEH[veh]
    for di, dj in MOVES:
        i, j = c[0]+di, c[1]+dj
        if 0 <= i < N and 0 <= j < N and g[i][j] <= maxd:       # g==4 never <= maxd (max 3)
            yield (i, j), base + DELAY[g[i][j]]

def path_cost(g, p, veh):
    return sum(VEH[veh][0] + DELAY[g[c[0]][c[1]]] for c in p[1:])

def bfs(g, s, t, veh):
    t0 = time.perf_counter(); q = [s]; par = {s: None}; k = 0; h = 0
    while h < len(q):
        c = q[h]; h += 1; k += 1
        if c == t: break
        for n, _ in nbrs(g, c, veh):
            if n not in par: par[n] = c; q.append(n)
    else: return None, k, time.perf_counter()-t0
    return rebuild(par, t), k, time.perf_counter()-t0

def best_first(g, s, t, veh, use_h):
    t0 = time.perf_counter(); cmin = VEH[veh][0]
    hf = (lambda c: cmin*(abs(c[0]-t[0])+abs(c[1]-t[1]))) if use_h else (lambda c: 0.0)
    gs = {s: 0.0}; par = {s: None}; pq = [(hf(s), 0, s)]; cnt = 1; done = set(); k = 0
    while pq:
        f, _, c = heapq.heappop(pq)
        if c in done: continue
        done.add(c); k += 1
        if c == t: return rebuild(par, t), k, time.perf_counter()-t0
        for n, w in nbrs(g, c, veh):
            ng = gs[c] + w
            if ng < gs.get(n, 1e18) - 1e-12:
                gs[n] = ng; par[n] = c; heapq.heappush(pq, (ng + hf(n), cnt, n)); cnt += 1
    return None, k, time.perf_counter()-t0

def rebuild(par, t):
    p = []
    while t is not None: p.append(t); t = par[t]
    return p[::-1]

def run(g, t, veh):
    out = {}
    for name, fn in [("BFS", lambda: bfs(g, DEPOT, t, veh)),
                     ("UCS", lambda: best_first(g, DEPOT, t, veh, False)),
                     ("A*",  lambda: best_first(g, DEPOT, t, veh, True))]:
        p, k, dt = fn()
        out[name] = dict(path=p, cost=None if p is None else path_cost(g, p, veh), exp=k, ms=dt*1000)
    return out

def check_consistency(g, veh, t):
    cmin = VEH[veh][0]; h = lambda c: cmin*(abs(c[0]-t[0])+abs(c[1]-t[1]))
    bad = 0; edges = 0
    for i in range(N):
        for j in range(N):
            for n, w in nbrs(g, (i, j), veh):
                edges += 1
                if h((i, j)) > w + h(n) + 1e-9: bad += 1
    return edges, bad

if __name__ == "__main__":
    SEEDS = range(50)
    agg = {}; mism = 0; unreach = 0; total = 0; edges_total = 0; bad_total = 0; bfs_subopt = 0; bfs_cmp = 0
    for seed in SEEDS:
        base = make_base(seed)
        for sc in SCEN:
            g = depth_grid(base, sc)
            for veh in VEH:
                for dn, (t, pr) in DESTS.items():
                    e, b = check_consistency(g, veh, t); edges_total += e; bad_total += b
                    r = run(g, t, veh); total += 1
                    if r["UCS"]["cost"] is None:
                        unreach += 1; assert r["BFS"]["cost"] is None and r["A*"]["cost"] is None; continue
                    if abs(r["UCS"]["cost"] - r["A*"]["cost"]) > 1e-9: mism += 1
                    bfs_cmp += 1; bfs_subopt += r["BFS"]["cost"] > r["UCS"]["cost"] + 1e-9
                    for a in r:
                        d = agg.setdefault((sc, veh, a), dict(cost=[], exp=[], ms=[]))
                        d["cost"].append(r[a]["cost"]); d["exp"].append(r[a]["exp"]); d["ms"].append(r[a]["ms"])
    summary = {}
    for (sc, veh, a), d in agg.items():
        summary.setdefault(sc, {}).setdefault(veh, {})[a] = dict(n=len(d["cost"]), cost=st.mean(d["cost"]), exp=st.mean(d["exp"]), ms=st.mean(d["ms"]))
    # per-scenario, all vehicles pooled (solved instances only)
    pooled = {}
    for sc in SCEN:
        for a in ["BFS", "UCS", "A*"]:
            cs = [x for veh in VEH for x in agg.get((sc, veh, a), {"cost": []})["cost"]]
            es = [x for veh in VEH for x in agg.get((sc, veh, a), {"exp": []})["exp"]]
            ms = [x for veh in VEH for x in agg.get((sc, veh, a), {"ms": []})["ms"]]
            pooled.setdefault(sc, {})[a] = dict(n=len(cs), cost=st.mean(cs), exp=st.mean(es), ms=st.mean(ms))
    unreach_sc = {sc: 0 for sc in SCEN}; tot_sc = {sc: 0 for sc in SCEN}
    for seed in SEEDS:
        base = make_base(seed)
        for sc in SCEN:
            g = depth_grid(base, sc)
            for veh in VEH:
                for dn, (t, pr) in DESTS.items():
                    tot_sc[sc] += 1
                    if best_first(g, DEPOT, t, veh, False)[0] is None: unreach_sc[sc] += 1
    json.dump(dict(pooled=pooled, unreach=unreach_sc, tot=tot_sc, mism=mism, total=total, unreach_total=unreach,
                   bfs_subopt=bfs_subopt, bfs_cmp=bfs_cmp, edges=edges_total, bad_edges=bad_total), open("batch.json", "w"), indent=1)
    print(json.dumps(dict(pooled=pooled, unreach=unreach_sc, mism=mism, total=total, bfs_subopt=bfs_subopt, bfs_cmp=bfs_cmp, edges=edges_total, bad=bad_total), indent=1))
