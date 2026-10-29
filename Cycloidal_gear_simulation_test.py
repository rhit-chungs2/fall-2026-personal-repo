"""
Two-stage cycloidal gearbox simulation (top-down 2D view, default 1:9 x 1:9 = 1:81).

Python port of the Onshape FeatureScript "Cycloidal Gearbox 1:81"
(cycloidal_gearbox_1_81.fs). It uses the same sizing formulas, the same disc
profile equation, and the same phase law linking the input shaft, eccentric
cams, discs and output carriers, so what moves here is what the feature builds.

Run:
    python Cycloidal_gear_simulation_test.py
    python Cycloidal_gear_simulation_test.py --lobes1 11 --lobes2 7 --mode nested
    python Cycloidal_gear_simulation_test.py --check        # interference check only

Controls (animation window):
    space       pause / resume
    up / down   double / halve the input shaft speed
    b           show / hide the balancing B discs
    r           reset the input angle to 0
"""
import argparse
import os
import sys

# Python 3.13.0 venvs on Windows can't find Tcl/Tk (matplotlib's window toolkit).
# Point them at the base Python install before matplotlib loads.
for _var, _lib in (("TCL_LIBRARY", "tcl8.6"), ("TK_LIBRARY", "tk8.6")):
    _path = os.path.join(sys.base_prefix, "tcl", _lib)
    if _var not in os.environ and os.path.isdir(_path):
        os.environ[_var] = _path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, PathPatch
from matplotlib.path import Path


# =====================================================================
# 1. GEOMETRY (same formulas as sections 1-2 of the FeatureScript, in mm)
# =====================================================================
def compute_geometry(R=42.0, n_lobes1=9, n_lobes2=9, n_out_pins=6,
                     mfg="FDM", sleeves=True, pts_per_lobe=40):
    c_prof = {"CNC": 0.05, "FDM": 0.10}[mfg]
    c_press = 0.01 if mfg == "CNC" else 0.04

    e_max = 0.038 * R
    t_cam_brg = 0.058 * R

    r_dd_shaft = 0.155 * R
    w_dd_flat = 0.78 * r_dd_shaft
    r_pilot = (w_dd_flat - 0.35) if sleeves else 0.13 * R

    step_margin = 0.8
    r_cam_b = (0.32 * R - t_cam_brg) if sleeves else (r_pilot + e_max + step_margin)
    r_cam_a = r_cam_b if sleeves else (r_cam_b + 2.0 * e_max + step_margin)
    r_disc_bore_a = r_cam_a + t_cam_brg
    r_disc_bore_b = r_cam_b + t_cam_brg
    max_disc_bore = max(r_disc_bore_a, r_disc_bore_b)

    min_rrp = 0.038 * R
    max_rrp = 0.085 * R
    r_root_ref = R - (max_rrp + c_prof) - e_max
    r_out_pitch = 0.5 * (max_disc_bore + r_root_ref)
    r_bushing_od = 0.086 * R
    r_pin_shank = 0.058 * R
    r_carrier_flange = r_out_pitch + r_pin_shank + 2.5

    stages = []
    for n_lobes in (n_lobes1, n_lobes2):
        n_pins = n_lobes + 1
        E = min(0.42 * (R / n_pins), e_max)
        rrp = float(np.clip(0.27 * (np.pi * R / n_pins), min_rrp, max_rrp))
        stages.append({
            "n_lobes": n_lobes,
            "n_pins": n_pins,
            "E": E,
            "Rrp": rrp,
            "Rrp_eff": rrp + c_prof,
            "r_out_hole": r_bushing_od + E + c_prof,
            "profile": disc_profile_local(n_lobes, R, rrp + c_prof, E, pts_per_lobe),
        })

    return {
        "R": R,
        "n_out_pins": n_out_pins,
        "c_prof": c_prof,
        "sleeves": sleeves,
        "r_dd_shaft": r_dd_shaft,
        "r_pilot": r_pilot,
        "r_cam_a": r_cam_a,
        "r_cam_b": r_cam_b,
        "r_disc_bore_a": r_disc_bore_a + c_press,
        "r_disc_bore_b": r_disc_bore_b + c_press,
        "r_out_pitch": r_out_pitch,
        "r_bushing_od": r_bushing_od,
        "r_pin_shank": r_pin_shank,
        "r_carrier_flange": r_carrier_flange,
        "stages": stages,
    }


def disc_profile_local(n_lobes, R, rrp_eff, E, pts_per_lobe):
    """Epitrochoid disc outline centered at the origin (buildOptimizedCycloidalDisc)."""
    n_pins = n_lobes + 1
    t = np.linspace(0.0, 2.0 * np.pi, n_lobes * pts_per_lobe, endpoint=False)
    psi = np.arctan2(np.sin((1 - n_pins) * t), R / (E * n_pins) - np.cos((1 - n_pins) * t))
    x = R * np.cos(t) - rrp_eff * np.cos(t + psi) - E * np.cos(n_pins * t)
    y = -R * np.sin(t) + rrp_eff * np.sin(t + psi) + E * np.sin(n_pins * t)
    return np.column_stack([x, y])


# =====================================================================
# 2. KINEMATICS (same phase law as section 4 of the FeatureScript)
# =====================================================================
def gearbox_angles(theta_in, n_lobes1, n_lobes2):
    """All angles in radians. Stage 2's cams are driven by carrier 1."""
    carrier1 = -theta_in / n_lobes1
    carrier2 = -carrier1 / n_lobes2
    return {
        "cam1a": theta_in,
        "cam1b": theta_in + np.pi,
        "carrier1": carrier1,
        "cam2a": carrier1,
        "cam2b": carrier1 + np.pi,
        "carrier2": carrier2,
    }


def disc_pose(stage, theta_cam, theta_carrier, geo):
    """World-space outline, center, and output-hole centers for one disc."""
    E = stage["E"]
    center = np.array([E * np.cos(theta_cam), E * np.sin(theta_cam)])
    phi = -theta_cam / stage["n_lobes"]
    rot = np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])
    outline = stage["profile"] @ rot.T + center

    hole_angles = 2.0 * np.pi * np.arange(geo["n_out_pins"]) / geo["n_out_pins"] + theta_carrier
    holes = center + geo["r_out_pitch"] * np.column_stack([np.cos(hole_angles), np.sin(hole_angles)])
    return outline, center, holes


def output_pin_centers(geo, theta_carrier):
    a = 2.0 * np.pi * np.arange(geo["n_out_pins"]) / geo["n_out_pins"] + theta_carrier
    return geo["r_out_pitch"] * np.column_stack([np.cos(a), np.sin(a)])


def ring_pin_centers(geo, stage):
    a = 2.0 * np.pi * np.arange(stage["n_pins"]) / stage["n_pins"]
    return geo["R"] * np.column_stack([np.cos(a), np.sin(a)])


# =====================================================================
# 3. INTERFERENCE CHECK (disc outline vs. stationary ring pins)
# =====================================================================
def min_ring_pin_clearance(geo, stage_idx, n_samples=90):
    """Smallest gap (mm) between a disc and the ring pins over a full cam turn.

    Should come out close to the radial clearance (c_prof); negative means the
    disc would cut into a pin."""
    stage = geo["stages"][stage_idx]
    dense = dict(stage, profile=disc_profile_local(
        stage["n_lobes"], geo["R"], stage["Rrp_eff"], stage["E"], 400))
    pins = ring_pin_centers(geo, stage)
    worst = np.inf
    for theta_cam in np.linspace(0.0, 2.0 * np.pi, n_samples, endpoint=False):
        for offset in (0.0, np.pi):  # disc A and disc B
            outline, _, _ = disc_pose(dense, theta_cam + offset, 0.0, geo)
            d = np.linalg.norm(outline[None, :, :] - pins[:, None, :], axis=2)
            worst = min(worst, d.min() - stage["Rrp"])
    return worst


# =====================================================================
# 4. DRAWING HELPERS
# =====================================================================
def _ring(points, ccw):
    """Closed polygon ring with the requested winding (for holes in a PathPatch)."""
    x, y = points[:, 0], points[:, 1]
    signed_area = 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)
    if (signed_area > 0) != ccw:
        points = points[::-1]
    verts = np.vstack([points, points[:1]])
    codes = [Path.MOVETO] + [Path.LINETO] * (len(points) - 1) + [Path.CLOSEPOLY]
    return verts, codes


def _circle_points(center, r, n=48):
    a = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    return center + r * np.column_stack([np.cos(a), np.sin(a)])


def disc_path(outline, center, bore_r, holes, hole_r):
    rings = [_ring(outline, ccw=True), _ring(_circle_points(center, bore_r), ccw=False)]
    rings += [_ring(_circle_points(h, hole_r), ccw=False) for h in holes]
    verts = np.vstack([v for v, _ in rings])
    codes = [c for _, cs in rings for c in cs]
    return Path(verts, codes)


class StagePanel:
    """Everything drawn for one stage: ring pins, two discs, cams, output pins."""

    def __init__(self, ax, geo, stage_idx, title):
        self.geo = geo
        self.stage = geo["stages"][stage_idx]
        self.idx = stage_idx
        st = self.stage
        R = geo["R"]

        ax.set_aspect("equal")
        lim = R + st["Rrp"] + 6
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("mm")
        ax.grid(alpha=0.2)

        ax.add_patch(Circle((0, 0), R + 0.15 * st["Rrp"] + st["Rrp"], fill=False,
                            ls="--", lw=0.8, color="0.6"))
        for c in ring_pin_centers(geo, st):
            ax.add_patch(Circle(c, st["Rrp"], color="0.55", zorder=4))

        ax.add_patch(Circle((0, 0), geo["r_carrier_flange"], fill=False, ls=":", lw=1.0,
                            color="tab:orange" if stage_idx == 0 else "tab:red"))

        disc_colors = [("#2e8be0", "#7cc0f5"), ("#23b875", "#6fdca6")][stage_idx]
        self.disc_b = PathPatch(Path(np.zeros((1, 2))), fc=disc_colors[1], ec="k",
                                lw=0.6, alpha=0.45, zorder=2)
        self.disc_a = PathPatch(Path(np.zeros((1, 2))), fc=disc_colors[0], ec="k",
                                lw=0.8, alpha=0.85, zorder=3)
        ax.add_patch(self.disc_b)
        ax.add_patch(self.disc_a)

        self.cam_a = Circle((0, 0), geo["r_cam_a"], fc="#d4ad38", ec="k", lw=0.6, zorder=5)
        self.cam_b = Circle((0, 0), geo["r_cam_b"], fc="#e6c247", ec="k", lw=0.6,
                            alpha=0.6, zorder=5)
        ax.add_patch(self.cam_b)
        ax.add_patch(self.cam_a)
        ax.add_patch(Circle((0, 0), geo["r_dd_shaft"], fc="#e0ad29", ec="k", lw=0.6, zorder=6))
        self.shaft_mark, = ax.plot([], [], color="k", lw=2, zorder=7)

        self.bushings = []
        for _ in range(geo["n_out_pins"]):
            outer = Circle((0, 0), geo["r_bushing_od"], fc="#d39438", ec="k", lw=0.6, zorder=6)
            inner = Circle((0, 0), geo["r_pin_shank"], fc="#c7cbd6", ec="k", lw=0.5, zorder=7)
            ax.add_patch(outer)
            ax.add_patch(inner)
            self.bushings.append((outer, inner))
        self.carrier_mark, = ax.plot([], [], color="tab:red", lw=2.5, zorder=8)
        self.disc_dot, = ax.plot([], [], "o", color="crimson", ms=6, zorder=8)

        self.info = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top",
                            fontsize=9, family="monospace", zorder=20,
                            bbox=dict(fc="white", ec="0.7", alpha=0.85))

    def update(self, angles, show_b):
        geo, st = self.geo, self.stage
        key = "1" if self.idx == 0 else "2"
        cam_a, cam_b = angles["cam" + key + "a"], angles["cam" + key + "b"]
        carrier = angles["carrier" + key]
        shaft = cam_a  # stage 1: input shaft, stage 2: carrier 1

        out_a, cen_a, holes_a = disc_pose(st, cam_a, carrier, geo)
        out_b, cen_b, holes_b = disc_pose(st, cam_b, carrier, geo)
        self.disc_a.set_path(disc_path(out_a, cen_a, geo["r_disc_bore_a"], holes_a, st["r_out_hole"]))
        self.disc_b.set_path(disc_path(out_b, cen_b, geo["r_disc_bore_b"], holes_b, st["r_out_hole"]))
        self.disc_b.set_visible(show_b)
        self.cam_b.set_visible(show_b)

        self.cam_a.center = cen_a
        self.cam_b.center = cen_b
        r = geo["r_dd_shaft"]
        self.shaft_mark.set_data([0, r * np.cos(shaft)], [0, r * np.sin(shaft)])

        for (outer, inner), c in zip(self.bushings, output_pin_centers(geo, carrier)):
            outer.center = c
            inner.center = c
        rc = geo["r_carrier_flange"]
        self.carrier_mark.set_data([0, rc * np.cos(carrier)], [0, rc * np.sin(carrier)])

        # Marks one point on disc A so its slow backwards spin is easy to follow
        phi = -cam_a / st["n_lobes"]
        p = cen_a + 0.8 * geo["r_out_pitch"] * np.array([np.cos(phi + np.pi / geo["n_out_pins"]),
                                                         np.sin(phi + np.pi / geo["n_out_pins"])])
        self.disc_dot.set_data([p[0]], [p[1]])

        in_name = "input" if self.idx == 0 else "carrier1"
        out_name = "carrier1" if self.idx == 0 else "output"
        self.info.set_text(
            f"{st['n_lobes']} lobes / {st['n_pins']} ring pins\n"
            f"E = {st['E']:.2f} mm\n"
            f"{in_name:>8}: {np.degrees(shaft):9.1f} deg\n"
            f"{out_name:>8}: {np.degrees(carrier):9.2f} deg"
        )


# =====================================================================
# 5. MAIN
# =====================================================================
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--R", type=float, default=42.0, help="ring pin pitch radius, mm (26-200)")
    ap.add_argument("--lobes1", type=int, default=9, help="stage 1 lobes (4-35)")
    ap.add_argument("--lobes2", type=int, default=9, help="stage 2 lobes (4-35)")
    ap.add_argument("--out-pins", type=int, default=6, help="output drive pins per stage (4-10)")
    ap.add_argument("--mfg", choices=["FDM", "CNC"], default="FDM", help="clearance preset")
    ap.add_argument("--mode", choices=["sleeves", "nested"], default="sleeves",
                    help="shaft architecture (changes cam / bore sizes)")
    ap.add_argument("--speed", type=float, default=4.0, help="input shaft speed, deg per frame")
    ap.add_argument("--check", action="store_true", help="print interference check and exit")
    ap.add_argument("--snapshot", metavar="PNG", help="save one frame to a PNG and exit")
    ap.add_argument("--angle", type=float, default=0.0, help="input angle (deg) for --snapshot")
    args = ap.parse_args()

    geo = compute_geometry(args.R, args.lobes1, args.lobes2, args.out_pins,
                           args.mfg, sleeves=(args.mode == "sleeves"))
    n1, n2 = args.lobes1, args.lobes2

    print(f"Total ratio 1:{n1 * n2}  (stage 1 -1:{n1}, stage 2 -1:{n2})")
    for i, st in enumerate(geo["stages"]):
        gap = min_ring_pin_clearance(geo, i)
        status = "OK" if gap >= 0 else "INTERFERENCE"
        print(f"Stage {i + 1}: E = {st['E']:.3f} mm, ring pin r = {st['Rrp']:.3f} mm, "
              f"min disc-to-pin gap = {gap:.3f} mm ({status})")
    if args.check:
        return

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7.2))
    fig.suptitle(f"Two-Stage Cycloidal Gearbox 1:{n1 * n2}   ({args.mode}, {args.mfg} fit)",
                 fontsize=13)
    panels = [
        StagePanel(ax1, geo, 0, f"Stage 1: input shaft -> carrier 1  (-1:{n1})"),
        StagePanel(ax2, geo, 1, f"Stage 2: carrier 1 -> output  (total 1:{n1 * n2})"),
    ]
    fig.text(0.5, 0.02,
             "space: pause   up/down: speed   b: toggle B discs   r: reset      "
             "black line = driving shaft, red line = output carrier",
             ha="center", fontsize=9, color="0.35")

    state = {"theta": np.radians(args.angle), "speed": np.radians(args.speed),
             "paused": False, "show_b": True}

    def draw():
        angles = gearbox_angles(state["theta"], n1, n2)
        for p in panels:
            p.update(angles, state["show_b"])

    if args.snapshot:
        draw()
        fig.savefig(args.snapshot, dpi=110)
        print(f"Saved {args.snapshot}")
        return

    def on_key(event):
        if event.key == " ":
            state["paused"] = not state["paused"]
        elif event.key == "up":
            state["speed"] *= 2.0
        elif event.key == "down":
            state["speed"] /= 2.0
        elif event.key == "b":
            state["show_b"] = not state["show_b"]
        elif event.key == "r":
            state["theta"] = 0.0
        draw()
        fig.canvas.draw_idle()

    def step(_frame):
        if not state["paused"]:
            state["theta"] += state["speed"]
        draw()
        return []

    fig.canvas.mpl_connect("key_press_event", on_key)
    anim = FuncAnimation(fig, step, interval=30, cache_frame_data=False)  # noqa: F841 (keep alive)
    plt.show()


if __name__ == "__main__":
    main()
