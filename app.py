# app.py
# ------------------------------------------
# Streamlit Web Version – Two generator styles (A/B)
# Adjustable parameters, random seed, and PNG download.
# Run with: streamlit run app.py
# ------------------------------------------

import io
import random
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ========== Shared Function ==========
def make_heart(n_points=400, scale=1.0, offset=(0, 0)):
    t = np.linspace(0, 2*np.pi, n_points)
    x = 16 * np.sin(t)**3
    y = 13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t)
    x, y = scale * x, scale * y
    x += offset[0]
    y += offset[1]
    return x, y

# ========== Version A (your first script) ==========
def fixed_palette(n_colors=8):
    base_colors = [
        (0.6, 1.0, 0.6, 1.0),  # green
        (0.6, 0.8, 1.0, 1.0),  # blue
        (1.0, 0.6, 0.8, 1.0),  # pink
        (1.0, 1.0, 0.6, 1.0),  # yellow
        (1.0, 1.0, 1.0, 1.0),  # white
    ]
    colors = [base_colors[i % len(base_colors)] for i in range(n_colors)]
    random.shuffle(colors)
    return colors

def make_blob_A(n_points=200, radius=1.0, wobble=0.3, seed=None, harmonic=3):
    if seed is not None:
        np.random.seed(seed)
    angles = np.linspace(0, 2*np.pi, n_points, endpoint=False)
    r = radius * (
        1
        + wobble * np.sin(harmonic * angles + np.random.rand() * 2*np.pi)
        + 0.2 * np.random.randn(n_points)
    )
    x = r * np.cos(angles)
    y = r * np.sin(angles)
    return x, y

def draw_poster_A(
    n_blobs=8,
    n_points=300,
    min_radius=0.5,
    max_radius=2.5,
    wobble=0.3,
    n_hearts=10,
    seed=None,
    figsize=(8, 8)
):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    colors = fixed_palette(n_colors=n_blobs)
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_facecolor((0.05, 0.05, 0.07))

    # Blobs
    for i in range(n_blobs):
        r = np.linspace(min_radius, max_radius, n_blobs)[i]
        harmonic = random.choice([2, 3, 5, 7])
        wob = wobble * random.uniform(0.5, 1.5)
        x, y = make_blob_A(
            n_points=n_points,
            radius=r,
            wobble=wob,
            harmonic=harmonic
        )
        ax.fill(x, y, color=colors[i], alpha=random.uniform(0.5, 0.8), zorder=i)
        ax.plot(x, y, color=(0, 0, 0, 0.2), lw=1, zorder=i + 0.5)

    # Hearts
    heart_colors = [
        (1.0, 0.4, 0.7, 1.0),  # bright pink
        (1.0, 0.2, 0.5, 1.0),  # hot pink
        (0.9, 0.3, 0.9, 1.0),  # magenta-pink
        (1.0, 0.8, 0.3, 1.0),  # golden yellow
        (0.6, 0.9, 1.0, 1.0),  # sky blue
        (0.6, 1.0, 0.6, 1.0),  # soft green
        (1.0, 1.0, 1.0, 1.0),  # white
    ]
    for _ in range(n_hearts):
        scale = random.uniform(0.05, 0.15)
        offset = (random.uniform(-3.5, 3.5), random.uniform(-3.5, 3.5))
        hx, hy = make_heart(scale=scale, offset=offset)
        ax.fill(hx, hy, color=random.choice(heart_colors),
                alpha=random.uniform(0.6, 0.9), zorder=20)

    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    return fig

# ========== Version B (your second script) ==========
def palette_B():
    return [
        (0.60, 1.00, 0.60, 1.0),  # green
        (0.60, 0.80, 1.00, 1.0),  # blue
        (1.00, 0.60, 0.80, 1.0),  # pink
        (1.00, 1.00, 0.60, 1.0),  # yellow
        (1.00, 1.00, 1.00, 1.0),  # white
    ]

def make_blob_B(n_points=150, radius=1.0, wobble=0.35, irregularity=0.25):
    angles = np.linspace(0, 2*np.pi, n_points, endpoint=False)
    ripple = wobble * np.sin(random.randint(2, 7) * angles + random.random() * 2 * np.pi)
    jitter = irregularity * np.random.randn(n_points)
    r = radius * (1 + ripple + jitter)
    x = r * np.cos(angles)
    y = r * np.sin(angles)
    return x, y

def draw_poster_B(
    n_blobs=8,
    n_hearts=12,
    min_radius=0.7,
    max_radius=2.5,
    seed=None,
    figsize=(8, 8),
    wobble_low=0.25,
    wobble_high=0.5,
    irregularity=0.15
):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    colors = palette_B()
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_facecolor((0.07, 0.06, 0.08))  # dark background

    # Blobs
    for i in range(n_blobs):
        r = np.linspace(min_radius, max_radius, n_blobs)[i]
        x, y = make_blob_B(radius=r,
                           wobble=random.uniform(wobble_low, wobble_high),
                           irregularity=irregularity)
        ax.fill(x, y, color=random.choice(colors), alpha=random.uniform(0.5, 0.8), zorder=i)

    # Hearts
    heart_colors = [
        (1.0, 0.4, 0.7, 1.0), (1.0, 0.2, 0.5, 1.0),
        (0.9, 0.3, 0.9, 1.0), (1.0, 0.85, 0.3, 1.0),
        (0.6, 0.9, 1.0, 1.0), (0.6, 1.0, 0.6, 1.0),
        (1.0, 1.0, 1.0, 1.0),
    ]
    for _ in range(n_hearts):
        scale = random.uniform(0.05, 0.15)
        offset = (random.uniform(-3.2, 3.2), random.uniform(-3.2, 3.2))
        hx, hy = make_heart(scale=scale, offset=offset)
        ax.fill(hx, hy, color=random.choice(heart_colors),
                alpha=random.uniform(0.6, 0.9), zorder=20)

    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    return fig

# ========== Streamlit UI ==========
st.set_page_config(page_title="Blob & Heart Poster", page_icon="💖", layout="wide")
st.title("🎨 Blob & Heart Poster (Web Generator)")
st.caption("Switch between generator versions A/B, adjust parameters, fix random seed, and export as PNG.")

with st.sidebar:
    st.header("Parameters")
    version = st.radio("Generator Version", ["A (harmonic blobs)", "B (ripple blobs)"])

    col_fs1, col_fs2 = st.columns(2)
    fig_w = col_fs1.number_input("Figure Width (inches)", 4.0, 20.0, 8.0, step=0.5)
    fig_h = col_fs2.number_input("Figure Height (inches)", 4.0, 20.0, 8.0, step=0.5)

    n_blobs = st.slider("Number of blobs", 1, 20, 10 if version.startswith("A") else 9)
    n_hearts = st.slider("Number of hearts", 0, 40, 10 if version.startswith("A") else 12)

    lock_seed = st.checkbox("Fix random seed", value=True)
    seed_val = st.number_input("Seed (integer)", value=42 if version.startswith("A") else 123, step=1) if lock_seed else None

    if version.startswith("A"):
        n_points = st.slider("Points per blob", 50, 800, 300, step=50)
        min_radius = st.slider("Min radius", 0.1, 3.0, 0.5, step=0.1)
        max_radius = st.slider("Max radius", 0.5, 5.0, 2.5, step=0.1)
        wobble = st.slider("Wobble", 0.0, 1.0, 0.35, step=0.01)
    else:
        min_radius = st.slider("Min radius", 0.1, 3.0, 0.7, step=0.1)
        max_radius = st.slider("Max radius", 0.5, 5.0, 2.5, step=0.1)
        wobble_low = st.slider("Wobble low", 0.0, 1.0, 0.25, step=0.01)
        wobble_high = st.slider("Wobble high", 0.0, 1.5, 0.5, step=0.01)
        irregularity = st.slider("Irregularity", 0.0, 1.0, 0.15, step=0.01)

    generate_btn = st.button("🎬 Generate / Refresh")
    st.markdown("---")
    st.caption("Tip: click Generate before downloading to ensure the latest parameters are applied.")

# Draw figure
if generate_btn or True:
    seed = int(seed_val) if seed_val is not None else None
    if version.startswith("A"):
        fig = draw_poster_A(
            n_blobs=n_blobs,
            n_points=n_points,
            min_radius=min_radius,
            max_radius=max_radius,
            wobble=wobble,
            n_hearts=n_hearts,
            seed=seed,
            figsize=(fig_w, fig_h),
        )
    else:
        fig = draw_poster_B(
            n_blobs=n_blobs,
            n_hearts=n_hearts,
            min_radius=min_radius,
            max_radius=max_radius,
            seed=seed,
            figsize=(fig_w, fig_h),
            wobble_low=wobble_low,
            wobble_high=wobble_high,
            irregularity=irregularity
        )

    st.pyplot(fig, use_container_width=True)

    # Download PNG
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", pad_inches=0.05)
    buf.seek(0)
    st.download_button(
        "⬇️ Download PNG (300 DPI)",
        data=buf,
        file_name="poster.png",
        mime="image/png"
    )
