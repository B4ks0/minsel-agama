import os
from pathlib import Path
from collections import Counter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kemenag_minsel.settings")

import django
django.setup()

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

from main.analytics import run_spk_gereja
from main.models import Gereja, Kecamatan


OUT_DIR = Path("visual_akademik_spk_gereja")
OUT_DIR.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "#D6DEE8",
    "axes.labelcolor": "#1E293B",
    "xtick.color": "#475569",
    "ytick.color": "#475569",
    "text.color": "#1E293B",
    "axes.titleweight": "bold",
    "axes.titlesize": 15,
})

COLORS = {
    "ink": "#0B2545",
    "blue": "#2563EB",
    "teal": "#0F766E",
    "green": "#16A34A",
    "amber": "#D97706",
    "red": "#DC2626",
    "slate": "#64748B",
    "light": "#F8FAFC",
    "border": "#CBD5E1",
    "purple": "#7C3AED",
}


def save(fig, name):
    path = OUT_DIR / name
    fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def add_title(fig, title, subtitle=None):
    fig.text(0.05, 0.965, title, fontsize=18, fontweight="bold", color=COLORS["ink"], va="top")
    if subtitle:
        fig.text(0.05, 0.925, subtitle, fontsize=10.5, color=COLORS["slate"], va="top")


def draw_box(ax, xy, width, height, text, color="#E0F2FE", edge="#2563EB", fontsize=10):
    box = FancyBboxPatch(
        xy, width, height,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        facecolor=color,
        edgecolor=edge,
        linewidth=1.4,
    )
    ax.add_patch(box)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center",
            fontsize=fontsize, wrap=True, fontweight="bold", color=COLORS["ink"])
    return box


def draw_arrow(ax, start, end, color="#475569"):
    arrow = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=14, linewidth=1.4, color=color)
    ax.add_patch(arrow)


def style_barh(ax):
    ax.grid(axis="x", color="#E2E8F0", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)


def get_data():
    result = run_spk_gereja(Gereja.objects.all().order_by("kecamatan", "nama_gereja"))
    rows = []
    for index, row in enumerate(result["ranked"], 1):
        c = row["criteria"]
        rows.append({
            "rank": index,
            "nama": row["nama"],
            "kecamatan": row["wilayah"],
            "desa": row["detail"],
            "skor": row["score"],
            "skor_persen": row["score_percent"],
            "prioritas": row["priority"],
            "cluster": row["cluster"],
            "jumlah_umat": c["jumlah_umat"],
            "risiko_bangunan": c["risiko_bangunan"],
            "kesenjangan_pelayan": c["kesenjangan_pelayan"],
            "tekanan_wilayah": c["tekanan_wilayah"],
        })
    df = pd.DataFrame(rows)
    return result, df


def visual_01_pipeline():
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    add_title(fig, "Flowchart Penelitian SPK Gereja", "Alur end-to-end dari data MySQL sampai rekomendasi prioritas pembinaan")
    steps = [
        ("Data MySQL\nGereja + Kecamatan", 0.05, 0.66, "#DBEAFE", "#2563EB"),
        ("Pra-pemrosesan\nkriteria dan risiko", 0.25, 0.66, "#CCFBF1", "#0F766E"),
        ("AHP\nBobot kriteria", 0.45, 0.78, "#FEF3C7", "#D97706"),
        ("TOPSIS\nSkor prioritas", 0.45, 0.54, "#FDE68A", "#D97706"),
        ("DBSCAN\nSegmentasi gereja", 0.65, 0.66, "#EDE9FE", "#7C3AED"),
        ("Pemetaan administratif\nper kecamatan", 0.82, 0.78, "#DCFCE7", "#16A34A"),
        ("Ranking dan laporan\nakademik", 0.82, 0.54, "#FFE4E6", "#DC2626"),
    ]
    for text, x, y, face, edge in steps:
        draw_box(ax, (x, y), 0.14, 0.12, text, face, edge, fontsize=9.5)
    arrows = [
        ((0.19, 0.72), (0.25, 0.72)),
        ((0.39, 0.72), (0.45, 0.84)),
        ((0.39, 0.72), (0.45, 0.60)),
        ((0.59, 0.84), (0.65, 0.72)),
        ((0.59, 0.60), (0.65, 0.72)),
        ((0.79, 0.72), (0.82, 0.84)),
        ((0.79, 0.72), (0.82, 0.60)),
    ]
    for start, end in arrows:
        draw_arrow(ax, start, end)
    ax.text(0.05, 0.22, "Output utama:", fontsize=12, fontweight="bold", color=COLORS["ink"])
    outputs = [
        "Ranking prioritas gereja",
        "Kategori prioritas tinggi/sedang/rendah",
        "Cluster karakteristik gereja",
        "Skor evaluasi DBSCAN",
        "Rekap prioritas kecamatan",
    ]
    for i, item in enumerate(outputs):
        ax.text(0.08, 0.18 - i * 0.045, f"- {item}", fontsize=10.5, color=COLORS["ink"])
    return save(fig, "01_flowchart_penelitian_spk_gereja.png")


def visual_02_dbscan_flow():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    add_title(fig, "Flowchart Algoritma DBSCAN", "Segmentasi gereja berdasarkan vektor kriteria ternormalisasi")
    boxes = [
        ("Input vektor kriteria\n[jumlah umat, risiko,\ngap pelayan, tekanan wilayah]", 0.04, 0.50),
        ("Normalisasi\nMin-Max", 0.25, 0.50),
        ("Tentukan parameter\neps dan min_samples", 0.43, 0.50),
        ("Cari tetangga\ndalam radius eps", 0.62, 0.50),
        ("Label cluster\natau outlier", 0.80, 0.50),
    ]
    for text, x, y in boxes:
        draw_box(ax, (x, y), 0.15, 0.16, text, "#EDE9FE", "#7C3AED", fontsize=9)
    for x in [0.19, 0.37, 0.56, 0.75]:
        draw_arrow(ax, (x, 0.58), (x + 0.05, 0.58), COLORS["purple"])
    ax.text(0.08, 0.23, "Parameter final pada laporan:", fontsize=12, fontweight="bold")
    ax.text(0.08, 0.17, "eps = 0.45, min_samples = 4, jumlah cluster = 2, silhouette = 0.551", fontsize=11)
    return save(fig, "02_flowchart_algoritma_dbscan.png")


def visual_03_topsis_flow():
    fig, ax = plt.subplots(figsize=(13, 6.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    add_title(fig, "Flowchart AHP-TOPSIS", "Perhitungan skor prioritas pembinaan gereja")
    boxes = [
        ("Matriks keputusan\n594 gereja x 4 kriteria", 0.04, 0.58),
        ("Normalisasi\nMin-Max", 0.22, 0.58),
        ("Bobot AHP\n0.30, 0.25, 0.25, 0.20", 0.40, 0.58),
        ("Solusi ideal\npositif dan negatif", 0.58, 0.58),
        ("Jarak ke ideal\nD+ dan D-", 0.75, 0.58),
        ("Skor preferensi\nCi = D-/(D+ + D-)", 0.40, 0.30),
        ("Ranking dan kategori\nprioritas", 0.62, 0.30),
    ]
    for text, x, y in boxes:
        draw_box(ax, (x, y), 0.14, 0.14, text, "#FEF3C7", "#D97706", fontsize=8.8)
    for x in [0.18, 0.36, 0.54, 0.72]:
        draw_arrow(ax, (x, 0.65), (x + 0.04, 0.65), COLORS["amber"])
    draw_arrow(ax, (0.82, 0.58), (0.53, 0.44), COLORS["amber"])
    draw_arrow(ax, (0.54, 0.37), (0.62, 0.37), COLORS["amber"])
    return save(fig, "03_flowchart_ahp_topsis.png")


def visual_04_dataset_overview(result, df):
    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.axis("off")
    add_title(fig, "Ringkasan Dataset Penelitian", "Data gereja Kabupaten Minahasa Selatan yang dianalisis dari MySQL")
    metrics = [
        ("Total Gereja", f"{len(df):,}", COLORS["blue"]),
        ("Kecamatan", f"{df['kecamatan'].nunique()}", COLORS["teal"]),
        ("Prioritas Tinggi", f"{result['priority_summary']['Tinggi']}", COLORS["red"]),
        ("Prioritas Sedang", f"{result['priority_summary']['Sedang']}", COLORS["amber"]),
        ("Prioritas Rendah", f"{result['priority_summary']['Rendah']}", COLORS["green"]),
        ("Cluster DBSCAN", f"{result['evaluation']['cluster_count']}", COLORS["purple"]),
    ]
    for i, (label, value, color) in enumerate(metrics):
        x = 0.06 + (i % 3) * 0.30
        y = 0.60 - (i // 3) * 0.28
        rect = FancyBboxPatch((x, y), 0.24, 0.18, boxstyle="round,pad=0.02,rounding_size=0.025",
                              facecolor="#F8FAFC", edgecolor=color, linewidth=1.6)
        ax.add_patch(rect)
        ax.text(x + 0.02, y + 0.115, value, fontsize=24, fontweight="bold", color=color)
        ax.text(x + 0.02, y + 0.055, label, fontsize=11, color=COLORS["ink"])
    ax.text(0.06, 0.12, "Catatan: pemetaan GIS pada laporan bersifat administratif per kecamatan karena database belum memuat koordinat titik gereja.", fontsize=10.5, color=COLORS["slate"])
    return save(fig, "04_ringkasan_dataset.png")


def visual_05_status_distribution():
    counts = Counter(Gereja.objects.values_list("status_bangunan", flat=True))
    labels = list(counts.keys())
    values = [counts[x] for x in labels]
    colors = ["#16A34A" if x == "Permanen" else "#D97706" if x == "Semi Permanen" else "#DC2626" if x == "Darurat" else "#64748B" for x in labels]
    fig, ax = plt.subplots(figsize=(11, 6.5))
    bars = ax.bar(labels, values, color=colors, edgecolor="white", linewidth=1.2)
    ax.set_title("Distribusi Status Bangunan Gereja")
    ax.set_ylabel("Jumlah gereja")
    ax.grid(axis="y", color="#E2E8F0")
    ax.spines[["top", "right"]].set_visible(False)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 6, f"{int(bar.get_height())}", ha="center", fontweight="bold")
    return save(fig, "05_distribusi_status_bangunan.png")


def visual_06_weights(result):
    labels = [x.replace("_", " ").title() for x in result["weights"].keys()]
    values = list(result["weights"].values())
    fig, ax = plt.subplots(figsize=(11, 6.5))
    bars = ax.barh(labels[::-1], values[::-1], color=[COLORS["blue"], COLORS["teal"], COLORS["amber"], COLORS["purple"]][::-1])
    ax.set_title("Bobot Kriteria AHP")
    ax.set_xlabel("Bobot")
    style_barh(ax)
    for bar in bars:
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height() / 2, f"{bar.get_width():.2f}", va="center", fontweight="bold")
    ax.set_xlim(0, max(values) + 0.08)
    return save(fig, "06_bobot_kriteria_ahp.png")


def visual_07_priority_distribution(result):
    labels = ["Tinggi", "Sedang", "Rendah"]
    values = [result["priority_summary"][x] for x in labels]
    colors = [COLORS["red"], COLORS["amber"], COLORS["green"]]
    fig, ax = plt.subplots(figsize=(10, 7))
    wedges, _, autotexts = ax.pie(values, labels=labels, autopct=lambda p: f"{p:.1f}%\n({int(round(p*sum(values)/100))})",
                                  startangle=90, colors=colors, wedgeprops={"linewidth": 1.2, "edgecolor": "white"})
    for text in autotexts:
        text.set_fontweight("bold")
        text.set_color("white")
    ax.set_title("Distribusi Kategori Prioritas TOPSIS")
    return save(fig, "07_distribusi_prioritas_topsis.png")


def visual_08_cluster_profile(result):
    profiles = result["cluster_profiles"]
    labels = [p["label"] for p in profiles]
    data = pd.DataFrame({
        "Skor rata-rata": [p["avg_score"] for p in profiles],
        "Umat rata-rata / 1000": [p["averages"]["jumlah_umat"] / 1000 for p in profiles],
        "Risiko bangunan": [p["averages"]["risiko_bangunan"] for p in profiles],
        "Gap pelayan / 1000": [p["averages"]["kesenjangan_pelayan"] / 1000 for p in profiles],
    }, index=labels)
    fig, ax = plt.subplots(figsize=(12, 7))
    x = np.arange(len(labels))
    width = 0.18
    for i, col in enumerate(data.columns):
        ax.bar(x + (i - 1.5) * width, data[col], width, label=col)
    ax.set_xticks(x, labels)
    ax.set_title("Profil Cluster DBSCAN")
    ax.set_ylabel("Nilai profil terskala")
    ax.legend(frameon=False, ncols=2)
    ax.grid(axis="y", color="#E2E8F0")
    ax.spines[["top", "right"]].set_visible(False)
    for p in profiles:
        ax.text(labels.index(p["label"]), max(data.loc[p["label"]]) + 0.03, f"n={p['total']}", ha="center", fontweight="bold")
    return save(fig, "08_profil_cluster_dbscan.png")


def visual_09_cluster_scatter(df):
    fig, ax = plt.subplots(figsize=(11.5, 7))
    color_map = {"Cluster 1": COLORS["blue"], "Cluster 2": COLORS["red"], "Outlier": COLORS["slate"]}
    for cluster, group in df.groupby("cluster"):
        ax.scatter(group["jumlah_umat"], group["risiko_bangunan"], s=45, alpha=0.75,
                   label=f"{cluster} (n={len(group)})", color=color_map.get(cluster, COLORS["purple"]),
                   edgecolor="white", linewidth=0.4)
    ax.set_title("Sebaran Cluster: Jumlah Umat vs Risiko Bangunan")
    ax.set_xlabel("Jumlah umat")
    ax.set_ylabel("Risiko bangunan")
    ax.grid(color="#E2E8F0")
    ax.legend(frameon=True, facecolor="white", edgecolor="#E2E8F0")
    ax.spines[["top", "right"]].set_visible(False)
    return save(fig, "09_scatter_cluster_umat_risiko.png")


def visual_10_top20(df):
    top = df.head(20).iloc[::-1]
    colors = [COLORS["red"] if p == "Tinggi" else COLORS["amber"] if p == "Sedang" else COLORS["green"] for p in top["prioritas"]]
    fig, ax = plt.subplots(figsize=(12, 9))
    labels = [f"{r.rank}. {r.nama[:32]}" for r in top.itertuples()]
    bars = ax.barh(labels, top["skor"], color=colors)
    ax.set_title("Top 20 Ranking Prioritas Pembinaan Gereja")
    ax.set_xlabel("Skor TOPSIS")
    style_barh(ax)
    for bar, score in zip(bars, top["skor"]):
        ax.text(bar.get_width() + 0.006, bar.get_y() + bar.get_height() / 2, f"{score:.4f}", va="center", fontsize=8.5)
    ax.set_xlim(0, top["skor"].max() + 0.08)
    return save(fig, "10_top20_ranking_prioritas_gereja.png")


def visual_11_kecamatan(df, result):
    wilayah = pd.DataFrame(result["wilayah"])
    wilayah = wilayah.sort_values("score")
    colors = [COLORS["red"] if p == "Tinggi" else COLORS["amber"] if p == "Sedang" else COLORS["green"] for p in wilayah["priority"]]
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(wilayah["nama"], wilayah["score"], color=colors)
    ax.set_title("Pemetaan Administratif Prioritas Kecamatan")
    ax.set_xlabel("Skor rata-rata prioritas wilayah")
    style_barh(ax)
    for bar, total, priority in zip(bars, wilayah["total"], wilayah["priority"]):
        ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height() / 2,
                f"{bar.get_width():.3f} | n={total} | {priority}", va="center", fontsize=8.3)
    ax.set_xlim(0, wilayah["score"].max() + 0.09)
    return save(fig, "11_pemetaan_administratif_kecamatan.png")


def visual_12_sensitivity():
    eps_values = [0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.60, 0.70]
    clusters, outliers, silhouettes = [], [], []
    for eps in eps_values:
        item = run_spk_gereja(Gereja.objects.all(), eps=eps, min_samples=4)
        ev = item["evaluation"]
        clusters.append(ev["cluster_count"])
        outliers.append(ev["outlier_count"])
        silhouettes.append(np.nan if ev["silhouette"] is None else ev["silhouette"])
    fig, ax1 = plt.subplots(figsize=(11.5, 7))
    ax1.plot(eps_values, clusters, marker="o", color=COLORS["blue"], linewidth=2.2, label="Jumlah cluster")
    ax1.plot(eps_values, outliers, marker="s", color=COLORS["red"], linewidth=2.2, label="Outlier")
    ax1.set_xlabel("Eps DBSCAN")
    ax1.set_ylabel("Jumlah")
    ax1.grid(color="#E2E8F0")
    ax2 = ax1.twinx()
    ax2.plot(eps_values, silhouettes, marker="^", color=COLORS["teal"], linewidth=2.2, label="Silhouette")
    ax2.set_ylabel("Silhouette score")
    ax1.set_title("Uji Sensitivitas Parameter DBSCAN")
    lines = ax1.get_lines() + ax2.get_lines()
    ax1.legend(lines, [l.get_label() for l in lines], frameon=False, loc="upper right")
    ax1.axvspan(0.40, 0.50, color="#DCFCE7", alpha=0.5)
    ax1.text(0.405, max(clusters) - 0.25, "zona stabil", fontsize=10, color=COLORS["teal"], fontweight="bold")
    return save(fig, "12_sensitivitas_parameter_dbscan.png")


def visual_13_evaluation_dashboard(result):
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis("off")
    add_title(fig, "Dashboard Evaluasi Model", "Ringkasan angka utama untuk laporan akademik")
    cards = [
        ("Silhouette", result["evaluation"]["silhouette_label"], "Separasi cluster moderat", COLORS["teal"]),
        ("Cluster", str(result["evaluation"]["cluster_count"]), "DBSCAN default", COLORS["purple"]),
        ("Outlier", str(result["evaluation"]["outlier_count"]), f"{result['evaluation']['outlier_percent']}% data", COLORS["red"]),
        ("Prioritas Tinggi", str(result["priority_summary"]["Tinggi"]), "Top 15% ranking", COLORS["red"]),
        ("Prioritas Sedang", str(result["priority_summary"]["Sedang"]), "35% berikutnya", COLORS["amber"]),
        ("Prioritas Rendah", str(result["priority_summary"]["Rendah"]), "Sisa ranking", COLORS["green"]),
    ]
    for i, (title, value, note, color) in enumerate(cards):
        x = 0.06 + (i % 3) * 0.30
        y = 0.62 - (i // 3) * 0.30
        rect = FancyBboxPatch((x, y), 0.25, 0.19, boxstyle="round,pad=0.02,rounding_size=0.025",
                              facecolor="#F8FAFC", edgecolor=color, linewidth=1.6)
        ax.add_patch(rect)
        ax.text(x + 0.02, y + 0.12, value, fontsize=24, fontweight="bold", color=color)
        ax.text(x + 0.02, y + 0.075, title, fontsize=11, fontweight="bold")
        ax.text(x + 0.02, y + 0.035, note, fontsize=9.2, color=COLORS["slate"])
    return save(fig, "13_dashboard_evaluasi_model.png")


def visual_14_contact_sheet(paths):
    images = [plt.imread(path) for path in paths[:13]]
    fig, axes = plt.subplots(5, 3, figsize=(15, 20))
    axes = axes.flatten()
    for ax, img, path in zip(axes, images, paths[:13]):
        ax.imshow(img)
        ax.set_title(path.stem.replace("_", " "), fontsize=9, fontweight="bold")
        ax.axis("off")
    for ax in axes[len(images):]:
        ax.axis("off")
    fig.suptitle("Kumpulan Visual Akademik SPK Gereja", fontsize=20, fontweight="bold", y=0.995)
    fig.tight_layout()
    return save(fig, "14_contact_sheet_semua_visual.png")


def main():
    result, df = get_data()
    paths = [
        visual_01_pipeline(),
        visual_02_dbscan_flow(),
        visual_03_topsis_flow(),
        visual_04_dataset_overview(result, df),
        visual_05_status_distribution(),
        visual_06_weights(result),
        visual_07_priority_distribution(result),
        visual_08_cluster_profile(result),
        visual_09_cluster_scatter(df),
        visual_10_top20(df),
        visual_11_kecamatan(df, result),
        visual_12_sensitivity(),
        visual_13_evaluation_dashboard(result),
    ]
    paths.append(visual_14_contact_sheet(paths))
    print(OUT_DIR.resolve())
    for path in paths:
        print(path.resolve())


if __name__ == "__main__":
    main()
