import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import os

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
    background:linear-gradient(rgba(0,0,0,0.45),rgba(0,0,0,0.45)),
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
    border-radius:15px;
    border:1px solid #E5E7EB;
    margin-bottom:12px;
}

.route-card{
    background:white;
    padding:20px;
    border-left:8px solid green;
    border-radius:15px;
    border:1px solid #E5E7EB;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HERO
# =====================================================
st.markdown("""
<div class="hero">
<h1>SMART TOURISM KARANGASEM</h1>
<p>DSS Berbasis Graph & Algoritma Dijkstra</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# DASHBOARD (JANGAN DIHAPUS)
# =====================================================
c1,c2,c3,c4 = st.columns(4)

c1.metric("🌴 Destinasi", "10")
c2.metric("⭐ Rating Tertinggi", "5.0")
c3.metric("🗺️ Graph", "Weighted")
c4.metric("⚡ Algoritma", "Dijkstra")

# =====================================================
# DATA WISATA (lengkap + foto + maps)
# =====================================================
wisata = {
    "Taman Ujung":{"kategori":"Taman","rating":4.6,"Harga Tiket Masuk":30000,"foto":"images/Taman_Ujung.jpg","maps":"https://maps.google.com/?q=Taman+Ujung+Karangasem"},
    "Tirta Gangga":{"kategori":"Taman","rating":4.6,"Harga Tiket Masuk":45000,"foto":"images/Tirta_Gangga.jpg","maps":"https://maps.google.com/?q=Tirta+Gangga"},
    "Virgin Beach":{"kategori":"Pantai","rating":4.7,"Harga Tiket Masuk":10000,"foto":"images/Virgin_Beach.jpg","maps":"https://maps.google.com/?q=Virgin+Beach+Karangasem"},
    "Bukit Asah":{"kategori":"Alam","rating":4.6,"Harga Tiket Masuk":10000,"foto":"images/Bukit_Asah.jpg","maps":"https://maps.google.com/?q=Bukit+Asah"},
    "Amed":{"kategori":"Pantai","rating":5.0,"Harga Tiket Masuk":5000,"foto":"images/Pantai_Amed.jpg","maps":"https://maps.google.com/?q=Amed+Bali"},
    "Lahangan Sweet":{"kategori":"Alam","rating":4.6,"Harga Tiket Masuk":20000,"foto":"images/Lahangan_Sweet.jpg","maps":"https://maps.google.com/?q=Lahangan+Sweet"},
    "Coklat Factory":{"kategori":"Kuliner","rating":3.8,"Harga Tiket Masuk":10000,"foto":"images/Coklat_Factory.jpeg","maps":"https://maps.google.com/?q=Charlie+Chocolate+Factory"},
    "Pantai Labuan Amuk":{"kategori":"Pantai","rating":4.5,"Harga Tiket Masuk":10000,"foto":"images/Pantai_Labuan_Amuk.jpg","maps":"https://maps.google.com/?q=Labuan+Amuk"},
    "Pantai Candidasa":{"kategori":"Pantai","rating":3.8,"Harga Tiket Masuk":10000,"foto":"images/Pantai_Candidasa.jpg","maps":"https://maps.google.com/?q=Candi+Dasa"},
    "Gembleng Waterfall":{"kategori":"Alam","rating":4.7,"Harga Tiket Masuk":20000,"foto":"images/Gembleng_Waterfall.jpg","maps":"https://maps.google.com/?q=Gembleng+Waterfall"}
}

# =====================================================
# DSS SCORE
# =====================================================
def hitung_skor(data):
    rating_norm = data["rating"] / 5
    harga_norm = 1 - (data["Harga Tiket Masuk"] / 50000)
    return round((0.7 * rating_norm) + (0.3 * harga_norm), 3)

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
    ("Pantai Candidasa","Taman Ujung",13),
    ("Pantai Candidasa","Virgin Beach",18),
    ("Gembleng Waterfall","Tirta Gangga",8)
]

G.add_weighted_edges_from(edges)

# =====================================================
# SIDEBAR ROUTE
# =====================================================
st.sidebar.title("🗺️ Route Planner")

start = st.sidebar.selectbox("Lokasi Awal", list(wisata.keys()))
end = st.sidebar.selectbox("Tujuan", list(wisata.keys()))

path = None

if st.sidebar.button("Cari Rute Terbaik"):
    try:
        path = nx.dijkstra_path(G, start, end, weight="weight")
        distance = nx.dijkstra_path_length(G, start, end, weight="weight")

        st.markdown(f"""
        <div class="route-card">
        <h2>🎯 Rute Terbaik</h2>
        <h3>{" ➜ ".join(path)}</h3>
        <p>📏 Jarak: {distance:.1f} km</p>
        <p>⏱️ Estimasi: {round(distance/40*60)} menit</p>
        </div>
        """, unsafe_allow_html=True)

    except nx.NetworkXNoPath:
        st.error("Tidak ditemukan jalur.")

# =====================================================
# DSS RECOMMENDATION
# =====================================================
st.markdown("---")
st.subheader("🎯 Rekomendasi Berdasarkan Kategori")

kategori = st.selectbox("Pilih Kategori", ["Pantai","Alam","Taman","Kuliner"])

hasil = []
for nama,data in wisata.items():
    if data["kategori"] == kategori:
        hasil.append({
            "nama": nama,
            "rating": data["rating"],
            "harga": data["Harga Tiket Masuk"],
            "skor": hitung_skor(data)
        })

hasil = sorted(hasil, key=lambda x:x["skor"], reverse=True)

for i,item in enumerate(hasil,1):
    st.markdown(f"""
    <div class="card">
    <h3>{i}. {item['nama']}</h3>
    <p>⭐ Rating: {item['rating']}</p>
    <p>🎟️ Harga: Rp {item['harga']:,}</p>
    <p>🏆 Skor DSS: {item['skor']}</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# DETAIL DESTINASI + FOTO + MAPS (FIXED)
# =====================================================
st.markdown("---")
st.subheader("📍 Detail Destinasi")

pilih = st.selectbox("Pilih Destinasi", list(wisata.keys()))
data = wisata[pilih]

col1,col2 = st.columns([1,2])

with col1:
    img_path = data["foto"]
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.warning("⚠️ Gambar tidak ditemukan")

with col2:
    st.markdown(f"""
    <div class="card">
    <h2>{pilih}</h2>
    <p>📍 Kategori: {data['kategori']}</p>
    <p>⭐ Rating: {data['rating']}</p>
    <p>🎟️ Harga: Rp {data['Harga Tiket Masuk']:,}</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button("🗺️ Buka di Google Maps", data["maps"])

# =====================================================
# TOP 5
# =====================================================
st.markdown("---")
st.subheader("🏆 Top 5 Destinasi")

ranking = [(nama, hitung_skor(data)) for nama,data in wisata.items()]
ranking = sorted(ranking, key=lambda x:x[1], reverse=True)

for i,(nama,skor) in enumerate(ranking[:5],1):
    st.success(f"{i}. {nama} | Skor DSS: {skor}")

# =====================================================
# GRAPH VISUALIZATION
# =====================================================
st.markdown("---")
st.subheader("🗺️ Graph Visualisasi")

fig, ax = plt.subplots(figsize=(18,7))
pos = nx.spring_layout(G, seed=42)

nx.draw(G,pos,with_labels=True,node_size=4000,ax=ax)
nx.draw_networkx_edge_labels(G,pos,edge_labels=nx.get_edge_attributes(G,"weight"),ax=ax)

if path:
    nx.draw_networkx_edges(
        G,pos,
        edgelist=list(zip(path,path[1:])),
        width=4,
        edge_color="red",
        ax=ax
    )

st.pyplot(fig)

# =====================================================
# INFO DASHBOARD
# =====================================================
st.markdown("---")
st.info("""
Weighted Graph • Dijkstra Algorithm • DSS Multi-Kriteria

• Rute Terbaik (Shortest Path)
• Ranking Wisata (Skor DSS)
• Analisis Jarak & Waktu

Kompleksitas: O(E log V)
""")