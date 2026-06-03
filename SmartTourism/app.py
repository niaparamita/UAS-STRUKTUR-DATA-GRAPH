import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Smart Tourism Karangasem",
    page_icon="🏝️",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp{
    background-color:#F6F8F5;
}

.hero{
    background:linear-gradient(
    rgba(0,0,0,0.45),
    rgba(0,0,0,0.45)),
    url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");

    background-size:cover;
    background-position:center;

    padding:80px;
    border-radius:25px;
    text-align:center;
    margin-bottom:25px;
}

.hero h1{
    color:white;
    font-size:55px;
}

.hero p{
    color:white;
    font-size:20px;
}

.card{
    background:white;
    padding:20px;
    border-radius:20px;
    border:1px solid #E5E7EB;
    margin-bottom:15px;
}

.route-card{
    background:white;
    padding:25px;
    border-left:8px solid #16A34A;
    border-radius:20px;
    border:1px solid #E5E7EB;
    margin-bottom:20px;
}

[data-testid="metric-container"]{
    background:white;
    border-radius:15px;
    border:1px solid #E5E7EB;
    padding:15px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HERO
# =====================================================

st.markdown("""
<div class="hero">

<h1>🏝️ SMART TOURISM KARANGASEM</h1>

<p>
Decision Support System Berbasis Graph dan Algoritma Dijkstra
</p>

</div>
""", unsafe_allow_html=True)

# =====================================================
# DASHBOARD
# =====================================================

c1,c2,c3,c4 = st.columns(4)

c1.metric("🌴 Destinasi", "8")
c2.metric("⭐ Rating Tertinggi", "4.9")
c3.metric("🗺️ Graph", "Weighted")
c4.metric("⚡ Algoritma", "Dijkstra")

# =====================================================
# DATA WISATA
# =====================================================

wisata = {

    "Taman Ujung":{
        "kategori":"Sejarah",
        "rating":4.8,
        "maps":"https://maps.google.com/?q=Taman+Ujung+Karangasem"
    },

    "Tirta Gangga":{
        "kategori":"Sejarah",
        "rating":4.8,
        "maps":"https://maps.google.com/?q=Tirta+Gangga"
    },

    "Virgin Beach":{
        "kategori":"Pantai",
        "rating":4.7,
        "maps":"https://maps.google.com/?q=Virgin+Beach+Karangasem"
    },

    "Bukit Asah":{
        "kategori":"Alam",
        "rating":4.9,
        "maps":"https://maps.google.com/?q=Bukit+Asah"
    },

    "Amed":{
        "kategori":"Pantai",
        "rating":4.9,
        "maps":"https://maps.google.com/?q=Amed+Bali"
    },

    "Lahangan Sweet":{
        "kategori":"Alam",
        "rating":4.8,
        "maps":"https://maps.google.com/?q=Lahangan+Sweet"
    },

    "Coklat Factory":{
        "kategori":"Kuliner",
        "rating":4.6,
        "maps":"https://maps.google.com/?q=Charlie+Chocolate+Factory"
    },

    "Pantai Labuan Amuk":{
        "kategori":"Pantai",
        "rating":4.5,
        "maps":"https://maps.google.com/?q=Labuan+Amuk"
    }

}

# =====================================================
# GRAPH
# =====================================================

G = nx.Graph()

edges = [

    ("Taman Ujung","Tirta Gangga",5),
    ("Taman Ujung","Virgin Beach",8),
    ("Virgin Beach","Bukit Asah",7),
    ("Bukit Asah","Amed",15),
    ("Amed","Coklat Factory",10),
    ("Coklat Factory","Pantai Labuan Amuk",6),
    ("Tirta Gangga","Lahangan Sweet",12),
    ("Lahangan Sweet","Amed",18)

]

for a,b,w in edges:
    G.add_edge(a,b,weight=w)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🗺️ Route Planner")

start = st.sidebar.selectbox(
    "Lokasi Awal",
    list(wisata.keys())
)

end = st.sidebar.selectbox(
    "Tujuan",
    list(wisata.keys())
)

# =====================================================
# DSS DIJKSTRA
# =====================================================

if st.sidebar.button("Cari Rute Terbaik"):

    path = nx.dijkstra_path(
        G,
        start,
        end,
        weight="weight"
    )

    distance = nx.dijkstra_path_length(
        G,
        start,
        end,
        weight="weight"
    )

    st.markdown(f"""
    <div class="route-card">

    <h2>🎯 Rekomendasi Rute Wisata</h2>

    <h3>{' ➜ '.join(path)}</h3>

    <p>📏 Total Jarak : {distance} km</p>

    <p>⏱️ Estimasi Waktu : {distance*2} menit</p>

    </div>
    """, unsafe_allow_html=True)

# =====================================================
# KATEGORI WISATA
# =====================================================

st.markdown("---")

st.subheader("🎯 Rekomendasi Berdasarkan Kategori")

kategori = st.selectbox(
    "Pilih Kategori Wisata",
    ["Pantai", "Alam", "Sejarah", "Kuliner"]
)

hasil = []

for nama, data in wisata.items():

    if data["kategori"] == kategori:
        hasil.append((nama, data["rating"]))

hasil.sort(
    key=lambda x: x[1],
    reverse=True
)

for nama, rating in hasil:

    st.markdown(f"""
    <div class="card">

    <h3>{nama}</h3>

    <p>⭐ Rating : {rating}</p>

    <p>📍 Kategori : {kategori}</p>

    </div>
    """, unsafe_allow_html=True)

# =====================================================
# INFORMASI DESTINASI
# =====================================================

st.markdown("---")

st.subheader("📍 Informasi Destinasi")

pilih = st.selectbox(
    "Pilih Destinasi",
    list(wisata.keys())
)

data = wisata[pilih]

st.markdown(f"""
<div class="card">

<h2>{pilih}</h2>

<p>📍 Kategori : {data['kategori']}</p>

<p>⭐ Rating : {data['rating']}</p>

</div>
""", unsafe_allow_html=True)

st.link_button(
    "🗺️ Buka di Google Maps",
    data["maps"]
)

# =====================================================
# GRAPH VISUALIZATION
# =====================================================

st.markdown("---")

st.subheader("🗺️ Tourism Network Graph")

fig, ax = plt.subplots(figsize=(10,6))

pos = nx.spring_layout(
    G,
    seed=42
)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="#22C55E",
    edge_color="#94A3B8",
    node_size=3500,
    font_size=9,
    font_weight="bold",
    ax=ax
)

labels = nx.get_edge_attributes(
    G,
    "weight"
)

nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=labels,
    ax=ax
)

st.pyplot(fig)

# =====================================================
# ANALISIS DSS
# =====================================================

st.markdown("---")

st.subheader("📈 Analisis DSS")

st.info("""
Jenis Graph:
• Weighted Graph
• Undirected Graph

Algoritma:
• Dijkstra

Fungsi DSS:
• Menentukan rute wisata terbaik
• Memberikan rekomendasi wisata berdasarkan kategori
• Menampilkan hubungan antar destinasi

Kompleksitas:
• O(E log V)
""")

# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<hr>

<center>

<h3>🌺 Smart Tourism Karangasem</h3>

<p>
Decision Support System Berbasis Struktur Data Graph
</p>

<p>
Weighted Graph • Dijkstra • Karangasem Tourism
</p>

</center>
""", unsafe_allow_html=True)