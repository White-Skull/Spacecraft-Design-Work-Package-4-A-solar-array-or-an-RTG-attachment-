DIA = [3, 4, 5, 6, 8, 10, 12]   # Candidate diameters [mm]
N_LIST = (2, 3, 4)               # Fastener counts

W = 46.5                         # Fixed lug width [mm]
EDGE_FACTOR = 2.0                # Minimum edge distance factor


def fill_designs(w, n_list=N_LIST, diameters=DIA,
                 edge_factor=EDGE_FACTOR):

    designs = []

    for n in n_list:
        for D2 in diameters:

            if n == 2:
                # Two-fastener pattern
                # w = 2e + s
                # Choose maximum spacing: s = 3D2

                s = 3 * D2
                e = (w - s) / 2

                if e >= edge_factor * D2 - 1e-9:
                    designs.append({
                        "n": n,
                        "D2": D2,
                        "s": s,
                        "s_over_D2": s / D2,
                        "e": e,
                        "score": D2 ** 2 / n
                    })

            else:
                # Three- or four-fastener pattern
                # e = 2D2

                e = edge_factor * D2
                s = (w - 2 * e) / (n - 1)

                if 2 * D2 - 1e-9 <= s <= 3 * D2 + 1e-9:
                    designs.append({
                        "n": n,
                        "D2": D2,
                        "s": s,
                        "s_over_D2": s / D2,
                        "e": e,
                        "score": D2 ** 2 / n
                    })

    return designs


def show(w):

    designs = fill_designs(w)

    print(f"\nLug width w = {w:.2f} mm")

    if not designs:
        print("No feasible fastener pattern found.")
        return

    print(
        f"{'n':>3} {'D2':>6} {'s':>8} "
        f"{'s/D2':>8} {'e':>8} {'score':>9}"
    )

    print("-" * 48)

    for d in sorted(designs, key=lambda d: (d["n"], -d["score"])):

        print(
            f"{d['n']:>3} "
            f"{d['D2']:>6.1f} "
            f"{d['s']:>8.2f} "
            f"{d['s_over_D2']:>8.2f} "
            f"{d['e']:>8.2f} "
            f"{d['score']:>9.2f}"
        )

    best = max(designs, key=lambda d: d["score"])

    print("\nBEST DESIGN")
    print(f"Number of fasteners: {best['n']}")
    print(f"Fastener diameter:   {best['D2']} mm")
    print(f"Spacing:             {best['s']:.2f} mm")
    print(f"Spacing ratio:       {best['s_over_D2']:.2f}")
    print(f"Edge distance:       {best['e']:.2f} mm")
    print(f"Score:               {best['score']:.2f}")


if __name__ == "__main__":

    show(W)
