METRIC = [3, 4, 5, 6, 8, 10, 12]   # candidate diameters [mm]
N_LIST = (2, 3, 4)                 # fastener counts to try


def fill_designs(w, n_list=N_LIST, diameters=METRIC, edge_factor=2.0):
    designs = []
    for n in n_list:
        for D2 in diameters:
            e = edge_factor * D2
            s = (w - 2 * e) / (n - 1)
            if 2 * D2 - 1e-9 <= s <= 3 * D2 + 1e-9:
                designs.append({"n": n, "D2": D2, "s": s, "s_over_D2": s / D2,
                                "e": e, "score": n * D2 ** 2})
    return designs


def show(w):
    designs = fill_designs(w)
    print(f"\nWidth w = {w:g} mm  (e1 = e2 = 2*D2)")
    if not designs:
        print("  No feasible pattern for 2/3/4 fasteners at this width.")
        print("  Try a different width or add diameters to METRIC.")
        return
    print(f"{'n':>2} {'D2':>5} {'s':>7} {'s/D2':>6} {'e':>5} {'score':>7}")
    for d in sorted(designs, key=lambda d: (d["n"], -d["score"])):
        print(f"{d['n']:>2} {d['D2']:>5.1f} {d['s']:>7.2f} "
              f"{d['s_over_D2']:>6.2f} {d['e']:>5.1f} {d['score']:>7.0f}")
    best = max(designs, key=lambda d: d["score"])
    print(f"Highest score: n = {best['n']}, D2 = {best['D2']} mm, "
          f"s = {best['s']:.2f} mm, e = {best['e']:.1f} mm")


if __name__ == "__main__":
    print("Back-up plate fastener pattern. Type 'q' to quit.")
    while True:
        raw = input("\nEnter lug width in mm: ").strip().lower()
        if raw in ("q", "quit", "exit"):
            break
        try:
            w = float(raw)
            if w <= 0:
                raise ValueError
        except ValueError:
            print("Please enter a positive number.")
            continue
        show(w)
