import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Smart Tourism Karangasem",
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
    url("https://images.unsplash.com/photo-1537996194471-e657df975ab4");

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

<h1>SMART TOURISM KARANGASEM</h1>

<p>
Decision Support System Berbasis Graph dan Algoritma Dijkstra
</p>

</div>
""", unsafe_allow_html=True)

# =====================================================
# DASHBOARD
# =====================================================

c1,c2,c3,c4 = st.columns(4)

c1.metric("🌴 Destinasi", "10")
c2.metric("⭐ Rating Tertinggi", "4.9")
c3.metric("🗺️ Graph", "Weighted")
c4.metric("⚡ Algoritma", "Dijkstra")

# =====================================================
# DATA WISATA
# =====================================================

wisata = {

    "Taman Ujung":{
        "kategori":"Taman",
        "rating":4.8,
        "Harga Tiket Masuk":30000,
        "foto":"images/Taman_Ujung.jpg",
        "maps":"https://maps.google.com/?q=Taman+Ujung+Karangasem"
    },

    "Tirta Gangga":{
        "kategori":"Taman",
        "rating":4.8,
        "Harga Tiket Masuk":45000,
        "foto":"images/Tirta_Gangga.jpg",
        "maps":"https://maps.google.com/?q=Tirta+Gangga"
    },

    "Virgin Beach":{
        "kategori":"Pantai",
        "rating":4.7,
        "Harga Tiket Masuk":10000,
        "foto":"images/Virgin_Beach.jpg",
        "maps":"https://maps.google.com/?q=Virgin+Beach+Karangasem"
    },

    "Bukit Asah":{
        "kategori":"Alam",
        "rating":4.9,
        "Harga Tiket Masuk":10000,
        "foto":"images/Bukit_Asah.jpg",
        "maps":"https://maps.google.com/?q=Bukit+Asah"
    },

    "Amed":{
        "kategori":"Pantai",
        "rating":4.9,
        "Harga Tiket Masuk":5000,
        "foto":"images/Pantai_Amed.jpg",
        "maps":"https://maps.google.com/?q=Amed+Bali"
    },

    "Lahangan Sweet":{
        "kategori":"Alam",
        "rating":4.8,
        "Harga Tiket Masuk":20000,
        "foto":"images/Lahangan_Sweet.jpg",
        "maps":"https://maps.google.com/?q=Lahangan+Sweet"
    },

    "Coklat Factory":{
        "kategori":"Kuliner",
        "rating":4.6,
        "Harga Tiket Masuk":10000,
        "foto":"images/Coklat_Factory.jpeg",
        "maps":"https://maps.google.com/?q=Charlie+Chocolate+Factory"
    },

    "Pantai Labuan Amuk":{
        "kategori":"Pantai",
        "rating":4.5,
        "Harga Tiket Masuk":10000,
        "foto":"images/Pantai_Labuan_Amuk.jpg",
        "maps":"https://maps.google.com/?q=Labuan+Amuk"
    },

    "Pantai Candidasa":{
        "kategori":"Pantai",
        "rating":3.8,
        "Harga Tiket Masuk":10000,
        "foto":"images/Pantai_Candidasa.jpg",
        "maps":"https://maps.google.com/?q=Candi+Dasa"
    },

    "Gembleng Waterfall":{
        "kategori":"Alam",
        "rating":4.7,
        "Harga Tiket Masuk":20000,
        "foto":"images/Gembleng_Waterfall.jpg",
        "maps":"https://maps.google.com/?q=Gembleng+Waterfall"
    }

}

# =====================================================
# GRAPH
# =====================================================

G = nx.Graph()

edges = [

    ("Taman Ujung","Tirta Gangga",11),
    ("Taman Ujung","Virgin Beach",10),
    ("Virgin Beach","Bukit Asah",3),
    ("Bukit Asah","Amed",30),
    ("Amed","Coklat Factory",26),
    ("Coklat Factory","Pantai Labuan Amuk",19),
    ("Tirta Gangga","Lahangan Sweet",13),
    ("Lahangan Sweet","Amed",13),
    ("Pantai_Candidasa","Taman Ujung",13)

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
    ["Pantai", "Alam", "Taman", "Kuliner"]
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

    <p>🎟️ Harga Tiket Masuk : Rp {wisata[nama]['Harga Tiket Masuk']:,}</p>

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

col1, col2 = st.columns([1,2])

with col1:

    st.image(
        data["foto"],
        use_container_width=True
    )

with col2:

    st.markdown(f"""
    <div class="card">

    <h2>{pilih}</h2>

    <p>📍 Kategori : {data['kategori']}</p>

    <p>⭐ Rating : {data['rating']}</p>

    <p>🎟️ Harga Tiket Masuk : Rp {data['Harga Tiket Masuk']:,}</p>

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

fig, ax = plt.subplots(figsize=(17,10))

pos = nx.spring_layout(
    G,
    seed=42
)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_color="#2BAFD3",
    edge_color="#94A3B8",
    node_size=4000,
    font_size=12,
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