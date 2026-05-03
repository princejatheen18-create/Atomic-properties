import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(
    page_title="Atomic Properties Visualizer",
    page_icon="⚛️",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("elements.csv")
    return df

df = load_data()

PROPERTIES = {
    "Electronegativity": {
        "col": "Electronegativity", "unit": "Pauling units",
        "trend": "Increases left → right across a period. Decreases top → bottom down a group.",
        "insight": "Fluorine (F) is the most electronegative element (3.98). Noble gases have no assigned value."
    },
    "Atomic Radius": {
        "col": "AtomicRadius_pm", "unit": "Picometres (pm)",
        "trend": "Decreases left → right across a period. Increases top → bottom down a group.",
        "insight": "Francium (Fr) has the largest radius at 280 pm. Radius shrinks as nuclear charge increases."
    },
    "Ionization Energy": {
        "col": "IonizationEnergy_kJmol", "unit": "kJ/mol",
        "trend": "Generally increases left → right. Noble gases have exceptionally high values.",
        "insight": "Helium has the highest first IE at 2372 kJ/mol. More nuclear charge = harder to remove electron."
    },
    "Electron Affinity": {
        "col": "ElectronAffinity_kJmol", "unit": "kJ/mol",
        "trend": "Halogens have the highest values. Noble gases and alkaline earths are near zero.",
        "insight": "Chlorine (Cl) has the highest electron affinity at 349 kJ/mol."
    },
    "Melting Point": {
        "col": "MeltingPoint_K", "unit": "Kelvin (K)",
        "trend": "Varies widely. Tungsten has the highest melting point of all elements.",
        "insight": "Tungsten (W) melts at 3695 K — the highest of any element. Helium has the lowest at 1 K."
    },
    "Boiling Point": {
        "col": "BoilingPoint_K", "unit": "Kelvin (K)",
        "trend": "Metals generally boil at very high temperatures. Noble gases boil at very low temperatures.",
        "insight": "Tungsten (W) also has the highest boiling point at 5828 K."
    },
    "Density": {
        "col": "Density_gcm3", "unit": "g/cm³",
        "trend": "Generally increases down a group. Transition metals are very dense.",
        "insight": "Osmium (Os) is the densest element at 22.59 g/cm³. Hydrogen is the least dense at 0.00009 g/cm³."
    }
}

TYPE_COLORS = {
    "Alkali Metal": "#E74C3C",
    "Alkaline Earth": "#E67E22",
    "Transition Metal": "#3498DB",
    "Post-transition": "#1ABC9C",
    "Metalloid": "#9B59B6",
    "Nonmetal": "#2ECC71",
    "Halogen": "#F39C12",
    "Noble Gas": "#95A5A6",
    "Lanthanide": "#E91E63",
    "Actinide": "#FF5722",
}

PERIOD_COLORS = {
    1:"#378ADD", 2:"#1D9E75", 3:"#D85A30",
    4:"#7F77DD", 5:"#E8A838", 6:"#D64E8B", 7:"#5BBFBF"
}

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.title("⚛️ Controls")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📂 Section",
    ["📊 Property Charts", "🔍 Element Explorer", "⚖️ Compare Elements", "📋 Full Data Table"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Covers all 118 elements across 7 periods.")

# ══════════════════════════════════════════════════════════════
# PAGE 1 — PROPERTY CHARTS
# ══════════════════════════════════════════════════════════════
if page == "📊 Property Charts":
    st.title("⚛️ Atomic Properties Visualizer")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        selected_prop = st.selectbox("Property", list(PROPERTIES.keys()))
    with col_b:
        period_options = ["All Periods"] + [f"Period {p}" for p in sorted(df["Period"].unique())]
        selected_period = st.selectbox("Filter by Period", period_options)
    with col_c:
        color_by = st.selectbox("Color by", ["Period", "Element Type"])
        chart_type = st.radio("Chart Type", ["Bar Chart", "Line Graph"], horizontal=True)

    if selected_period == "All Periods":
        filtered_df = df.copy()
    else:
        period_num = int(selected_period.split()[1])
        filtered_df = df[df["Period"] == period_num].copy()

    prop_info = PROPERTIES[selected_prop]
    col = prop_info["col"]
    plot_df = filtered_df.dropna(subset=[col]).copy()
    plot_df = plot_df[plot_df[col] != 0] if selected_prop not in ["Electron Affinity"] else plot_df

    st.caption(f"Showing **{selected_prop}** · {prop_info['unit']} · {selected_period} · {len(plot_df)} elements")
    st.markdown("---")

    m1, m2, m3, m4 = st.columns(4)
    min_row = plot_df.loc[plot_df[col].idxmin()]
    max_row = plot_df.loc[plot_df[col].idxmax()]
    avg_val = plot_df[col].mean()
    with m1:
        st.metric("🔽 Minimum", f"{min_row[col]:.2f}", delta=min_row["Name"])
    with m2:
        st.metric("🔼 Maximum", f"{max_row[col]:.2f}", delta=max_row["Name"])
    with m3:
        st.metric("📊 Average", f"{avg_val:.2f}", delta="across shown elements")
    with m4:
        st.metric("🧪 Elements", len(plot_df))

    st.markdown("---")

    fig, ax = plt.subplots(figsize=(20, 5))
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")

    if color_by == "Period":
        colors = [PERIOD_COLORS.get(p, "#aaaaaa") for p in plot_df["Period"]]
    else:
        colors = [TYPE_COLORS.get(t, "#aaaaaa") for t in plot_df["Type"]]

    x = range(len(plot_df))

    if chart_type == "Bar Chart":
        bars = ax.bar(x, plot_df[col], color=colors, width=0.6, edgecolor="none", zorder=3)
        if len(plot_df) <= 40:
            for bar, val in zip(bars, plot_df[col]):
                ax.text(bar.get_x() + bar.get_width()/2,
                        bar.get_height() + max(plot_df[col])*0.01,
                        f"{val:.1f}", ha="center", va="bottom", fontsize=7, color="#aaaaaa")
    else:
        for period in sorted(plot_df["Period"].unique()):
            p_data = plot_df[plot_df["Period"] == period]
            p_indices = [list(plot_df["Symbol"]).index(s) for s in p_data["Symbol"]]
            ax.plot(p_indices, p_data[col],
                    color=PERIOD_COLORS.get(period, "#aaaaaa"),
                    marker="o", linewidth=2, markersize=6, zorder=3)

    ax.set_xticks(list(x))
    ax.set_xticklabels(plot_df["Symbol"], fontsize=8, color="#cccccc", rotation=45)
    ax.set_ylabel(prop_info["unit"], color="#888", fontsize=10)
    ax.tick_params(axis="y", colors="#888")
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color("#333")
    ax.yaxis.grid(True, color="#222", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)

    if color_by == "Period":
        patches = [mpatches.Patch(color=PERIOD_COLORS.get(p,"#aaa"), label=f"Period {p}")
                   for p in sorted(plot_df["Period"].unique())]
    else:
        types_present = plot_df["Type"].dropna().unique()
        patches = [mpatches.Patch(color=TYPE_COLORS.get(t,"#aaa"), label=t) for t in types_present]

    ax.legend(handles=patches, facecolor="#1a1a2e", edgecolor="#333",
              labelcolor="white", fontsize=8, loc="upper right", ncol=2)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📈 Periodic Trend")
        st.info(prop_info["trend"])
    with c2:
        st.subheader("🔬 Key Insight")
        st.success(prop_info["insight"])

# ══════════════════════════════════════════════════════════════
# PAGE 2 — ELEMENT EXPLORER
# ══════════════════════════════════════════════════════════════
elif page == "🔍 Element Explorer":
    st.title("🔍 Element Explorer")
    st.caption("Search any element to see all its properties")
    st.markdown("---")

    search = st.text_input("🔎 Search by element name or symbol", placeholder="e.g. Gold or Au")

    if search:
        result = df[
            df["Name"].str.lower().str.contains(search.lower()) |
            df["Symbol"].str.lower().str.contains(search.lower())
        ]

        if result.empty:
            st.warning("No element found. Try a different name or symbol.")
        else:
            for _, row in result.iterrows():
                type_color = TYPE_COLORS.get(row.get("Type", ""), "#888888")
                st.markdown("---")

                h1, h2 = st.columns([1, 3])
                with h1:
                    st.markdown(
                        f"""<div style='background:{type_color}22; border:2px solid {type_color};
                        border-radius:12px; padding:20px; text-align:center;'>
                        <div style='font-size:52px; font-weight:bold; color:{type_color}'>{row['Symbol']}</div>
                        <div style='font-size:14px; color:#ccc'>{row['Name']}</div>
                        <div style='font-size:12px; color:#888'>Z = {int(row['AtomicNumber'])}</div>
                        </div>""", unsafe_allow_html=True
                    )
                with h2:
                    st.markdown(f"## {row['Name']}")
                    type_val = row.get('Type', 'Unknown')
                    st.markdown(
                        f"<span style='background:{type_color}33; color:{type_color}; "
                        f"padding:4px 12px; border-radius:20px; font-size:13px'>{type_val}</span>",
                        unsafe_allow_html=True
                    )
                    st.markdown("")

                    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
                    with r1c1:
                        st.metric("Atomic Number", int(row["AtomicNumber"]))
                    with r1c2:
                        st.metric("Period", int(row["Period"]))
                    with r1c3:
                        st.metric("Group", int(row["Group"]))
                    with r1c4:
                        disc_year = row.get("YearDiscovered", "Unknown")
                        st.metric("Discovered", disc_year)

                st.markdown("")
                p1, p2, p3, p4 = st.columns(4)
                with p1:
                    val = row.get("Electronegativity", None)
                    st.metric("⚡ Electronegativity", f"{val:.2f}" if pd.notna(val) else "N/A", delta="Pauling")
                with p2:
                    val = row.get("AtomicRadius_pm", None)
                    st.metric("📏 Atomic Radius", f"{val:.0f} pm" if pd.notna(val) else "N/A")
                with p3:
                    val = row.get("IonizationEnergy_kJmol", None)
                    st.metric("⚡ Ionization Energy", f"{val:.0f} kJ/mol" if pd.notna(val) else "N/A")
                with p4:
                    val = row.get("ElectronAffinity_kJmol", None)
                    st.metric("🧲 Electron Affinity", f"{val:.0f} kJ/mol" if pd.notna(val) else "N/A")

                p5, p6, p7, p8 = st.columns(4)
                with p5:
                    val = row.get("MeltingPoint_K", None)
                    st.metric("🌡️ Melting Point", f"{val:.0f} K" if pd.notna(val) else "N/A")
                with p6:
                    val = row.get("BoilingPoint_K", None)
                    st.metric("💨 Boiling Point", f"{val:.0f} K" if pd.notna(val) else "N/A")
                with p7:
                    val = row.get("Density_gcm3", None)
                    st.metric("⚖️ Density", f"{val:.3f} g/cm³" if pd.notna(val) else "N/A")
                with p8:
                    discoverer = row.get("Discoverer", "Unknown")
                    st.metric("🔭 Discoverer", discoverer)

                config = row.get("ElectronConfig", None)
                if pd.notna(config):
                    st.markdown(f"**Electron Configuration:** `{config}`")
    else:
        st.info("👆 Type an element name or symbol above to see its full property card.")

        st.markdown("### Quick access — click any element type")
        type_cols = st.columns(5)
        types = list(TYPE_COLORS.keys())
        for i, t in enumerate(types):
            with type_cols[i % 5]:
                color = TYPE_COLORS[t]
                count = len(df[df["Type"] == t])
                st.markdown(
                    f"<div style='background:{color}22; border:1px solid {color}; border-radius:8px; "
                    f"padding:8px; text-align:center; margin-bottom:8px;'>"
                    f"<div style='color:{color}; font-size:12px; font-weight:bold'>{t}</div>"
                    f"<div style='color:#888; font-size:11px'>{count} elements</div></div>",
                    unsafe_allow_html=True
                )

# ══════════════════════════════════════════════════════════════
# PAGE 3 — COMPARE ELEMENTS
# ══════════════════════════════════════════════════════════════
elif page == "⚖️ Compare Elements":
    st.title("⚖️ Compare Two Elements")
    st.caption("Select any two elements to compare their properties side by side")
    st.markdown("---")

    all_elements = df["Name"].tolist()
    c1, c2 = st.columns(2)
    with c1:
        el1 = st.selectbox("Element 1", all_elements, index=0)
    with c2:
        el2 = st.selectbox("Element 2", all_elements, index=5)

    row1 = df[df["Name"] == el1].iloc[0]
    row2 = df[df["Name"] == el2].iloc[0]

    st.markdown("---")
    col1, col_mid, col2 = st.columns([5, 1, 5])

    def element_card(row, color):
        st.markdown(
            f"""<div style='background:{color}22; border:2px solid {color};
            border-radius:12px; padding:16px; text-align:center; margin-bottom:16px;'>
            <div style='font-size:48px; font-weight:bold; color:{color}'>{row['Symbol']}</div>
            <div style='font-size:16px; color:#ccc'>{row['Name']}</div>
            <div style='font-size:13px; color:#888'>Atomic No. {int(row['AtomicNumber'])}</div>
            </div>""", unsafe_allow_html=True
        )

    compare_props = [
        ("Period", "Period"),
        ("Group", "Group"),
        ("Type", "Type"),
        ("Electronegativity (Pauling)", "Electronegativity"),
        ("Atomic Radius (pm)", "AtomicRadius_pm"),
        ("Ionization Energy (kJ/mol)", "IonizationEnergy_kJmol"),
        ("Electron Affinity (kJ/mol)", "ElectronAffinity_kJmol"),
        ("Melting Point (K)", "MeltingPoint_K"),
        ("Boiling Point (K)", "BoilingPoint_K"),
        ("Density (g/cm³)", "Density_gcm3"),
        ("Electron Config", "ElectronConfig"),
        ("Discoverer", "Discoverer"),
        ("Year Discovered", "YearDiscovered"),
    ]

    color1 = TYPE_COLORS.get(row1.get("Type", ""), "#378ADD")
    color2 = TYPE_COLORS.get(row2.get("Type", ""), "#1D9E75")

    with col1:
        element_card(row1, color1)
        for label, key in compare_props:
            val = row1.get(key, None)
            display = f"{val:.3f}" if isinstance(val, float) and pd.notna(val) else (str(int(val)) if isinstance(val, float) and pd.notna(val) else str(val) if pd.notna(val) else "N/A")
            st.markdown(f"**{label}:** {display}")

    with col_mid:
        st.markdown("<div style='text-align:center; padding-top:80px; font-size:28px'>⚡</div>", unsafe_allow_html=True)

    with col2:
        element_card(row2, color2)
        for label, key in compare_props:
            val = row2.get(key, None)
            display = f"{val:.3f}" if isinstance(val, float) and pd.notna(val) else (str(int(val)) if isinstance(val, float) and pd.notna(val) else str(val) if pd.notna(val) else "N/A")
            st.markdown(f"**{label}:** {display}")

# ══════════════════════════════════════════════════════════════
# PAGE 4 — FULL DATA TABLE
# ══════════════════════════════════════════════════════════════
elif page == "📋 Full Data Table":
    st.title("📋 Full Elements Database")
    st.caption("All 118 elements with complete properties")
    st.markdown("---")

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        type_filter = st.multiselect("Filter by Type", sorted(df["Type"].dropna().unique()))
    with fc2:
        period_filter = st.multiselect("Filter by Period", sorted(df["Period"].unique()))
    with fc3:
        search_table = st.text_input("Search element", placeholder="Name or Symbol")

    table_df = df.copy()
    if type_filter:
        table_df = table_df[table_df["Type"].isin(type_filter)]
    if period_filter:
        table_df = table_df[table_df["Period"].isin(period_filter)]
    if search_table:
        table_df = table_df[
            table_df["Name"].str.lower().str.contains(search_table.lower()) |
            table_df["Symbol"].str.lower().str.contains(search_table.lower())
        ]

    st.markdown(f"Showing **{len(table_df)}** elements")
    st.dataframe(
        table_df[[
            "Symbol","Name","AtomicNumber","Period","Group","Type",
            "Electronegativity","AtomicRadius_pm","IonizationEnergy_kJmol",
            "ElectronAffinity_kJmol","MeltingPoint_K","BoilingPoint_K",
            "Density_gcm3","ElectronConfig","Discoverer","YearDiscovered"
        ]].reset_index(drop=True),
        use_container_width=True,
        height=600
    )