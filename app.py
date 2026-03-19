import streamlit as st
import numpy as np
import pandas as pd
import httpx
import json
import os
from datetime import date, datetime

# ──────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="⚽ UCL 25/26 Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CSS PROFESIONAL
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: #0E1117;
    color: #e8f4fd;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #1C1F26 !important;
    border-right: 1px solid rgba(0,255,156,0.15);
}
section[data-testid="stSidebar"] * { color: #e8f4fd !important; }

/* HEADER */
.main-header {
    text-align: center; padding: 1.5rem 0 1rem 0;
    border-bottom: 2px solid rgba(0,255,156,0.3); margin-bottom: 1.5rem;
}
.main-header h1 {
    font-family: 'Bebas Neue', cursive; font-size: 3rem; letter-spacing: 6px;
    background: linear-gradient(90deg, #00FF9C, #00e5ff, #00FF9C);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0;
}
.main-header p { color: #8ab4c8; font-size: 0.8rem; letter-spacing: 3px; text-transform: uppercase; margin-top: 0.3rem; }

/* SECTION TITLE */
.section-title {
    font-family: 'Bebas Neue', cursive; font-size: 1.5rem; letter-spacing: 4px;
    color: #00FF9C; border-left: 4px solid #00FF9C; padding-left: 12px; margin: 1.5rem 0 1rem 0;
}

/* CARDS */
.card {
    background: #1C1F26; border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px; padding: 1.2rem; margin: 0.4rem 0;
}
.card-green { border-color: rgba(0,255,156,0.3); }
.card-red   { border-color: rgba(255,75,75,0.3); }
.card-gold  { border-color: rgba(255,215,0,0.3); }

/* METRIC BOX */
.metric-box {
    background: #1C1F26; border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 1.2rem; text-align: center; margin: 0.3rem 0;
    transition: all 0.2s;
}
.metric-box:hover { border-color: rgba(0,255,156,0.4); }
.metric-label { font-size: 0.68rem; color: #7aa8c0; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-bottom: 0.4rem; }
.metric-value { font-family: 'Bebas Neue', cursive; font-size: 2.4rem; letter-spacing: 2px; line-height: 1; color: #e8f4fd; }
.metric-value.green  { color: #00FF9C; }
.metric-value.yellow { color: #FFD700; }
.metric-value.red    { color: #FF4B4B; }
.metric-value.blue   { color: #00e5ff; }

/* APUESTAS SUGERIDAS */
.bet-green {
    background: linear-gradient(135deg, rgba(0,255,156,0.12), rgba(0,150,80,0.08));
    border: 1px solid #00FF9C; border-radius: 10px; padding: 0.9rem 1.2rem; margin: 0.4rem 0;
    display: flex; justify-content: space-between; align-items: center;
}
.bet-yellow {
    background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(200,160,0,0.06));
    border: 1px solid #FFD700; border-radius: 10px; padding: 0.9rem 1.2rem; margin: 0.4rem 0;
    display: flex; justify-content: space-between; align-items: center;
}
.bet-label { color: #e8f4fd; font-size: 0.92rem; font-weight: 500; }
.bet-pct-green  { color: #00FF9C; font-family: 'Bebas Neue', cursive; font-size: 1.4rem; }
.bet-pct-yellow { color: #FFD700; font-family: 'Bebas Neue', cursive; font-size: 1.4rem; }

/* PICK DEL DÍA */
.pick-del-dia {
    background: linear-gradient(135deg, rgba(255,215,0,0.15), rgba(255,140,0,0.08));
    border: 2px solid #FFD700; border-radius: 16px; padding: 1.4rem 1.8rem; margin: 1rem 0;
    text-align: center;
}
.pick-title { font-family: 'Bebas Neue', cursive; font-size: 1.8rem; letter-spacing: 4px; color: #FFD700; }
.pick-desc  { font-size: 1.1rem; font-weight: 600; color: #e8f4fd; margin: 0.4rem 0; }
.pick-conf  { font-size: 0.8rem; color: #aaa; letter-spacing: 1px; }

/* VALOR BET */
.valor-bet {
    background: linear-gradient(135deg, rgba(0,255,156,0.1), rgba(0,200,100,0.05));
    border: 1px dashed #00FF9C; border-radius: 10px; padding: 0.7rem 1rem; margin: 0.3rem 0;
    display: flex; justify-content: space-between; align-items: center; font-size: 0.88rem;
}

/* SCORE CARDS */
.score-card {
    background: #1C1F26; border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px; padding: 0.8rem 1rem; margin: 0.3rem 0;
    display: flex; justify-content: space-between; align-items: center;
}
.score-card:first-child { border-color: rgba(0,255,156,0.4); background: rgba(0,255,156,0.05); }
.score-text { font-family: 'Bebas Neue', cursive; font-size: 1.5rem; letter-spacing: 4px; }
.score-pct  { font-size: 0.82rem; color: #7aa8c0; font-weight: 600; }

/* PARTIDO ROW */
.partido-row {
    background: #1C1F26; border: 1px solid rgba(255,255,255,0.06);
    border-radius: 8px; padding: 0.6rem 1rem; margin: 0.25rem 0;
    display: flex; justify-content: space-between; align-items: center; font-size: 0.85rem;
}

/* BANKROLL */
.saldo-box {
    background: linear-gradient(135deg, #1C1F26, #222630);
    border: 2px solid rgba(0,255,156,0.4); border-radius: 16px;
    padding: 1.5rem; text-align: center; margin: 0.5rem 0;
}
.saldo-label { font-size: 0.75rem; color: #7aa8c0; text-transform: uppercase; letter-spacing: 3px; }
.saldo-value { font-family: 'Bebas Neue', cursive; font-size: 3rem; letter-spacing: 3px; color: #00FF9C; }

/* PREDICCIONES */
.pred-acierto { color: #00FF9C; font-weight: 700; }
.pred-error   { color: #FF4B4B; font-weight: 700; }
.pred-pending { color: #FFD700; font-weight: 700; }

/* BADGES */
.badge-auto { background: rgba(0,229,255,0.15); border: 1px solid rgba(0,229,255,0.4); border-radius: 20px; padding: 0.15rem 0.7rem; font-size: 0.65rem; color: #00e5ff; font-weight: 700; letter-spacing: 1px; margin-left: 0.4rem; }
.badge-db   { background: rgba(0,255,156,0.1); border: 1px solid rgba(0,255,156,0.3); border-radius: 20px; padding: 0.2rem 0.8rem; font-size: 0.65rem; color: #00FF9C; font-weight: 700; letter-spacing: 1px; }
.badge-valor { background: rgba(255,215,0,0.15); border: 1px solid #FFD700; border-radius: 20px; padding: 0.15rem 0.6rem; font-size: 0.65rem; color: #FFD700; font-weight: 700; letter-spacing: 1px; }

/* STATS AUTO BOX */
.stats-auto-box {
    background: rgba(0,255,156,0.05); border: 1px solid rgba(0,255,156,0.2);
    border-radius: 10px; padding: 0.8rem 1rem; margin: 0.4rem 0;
    font-size: 0.8rem; color: #8ab4c8; line-height: 1.6;
}

/* DIVIDER */
.divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(0,255,156,0.3), transparent); margin: 1.5rem 0; }
.vs-badge { text-align: center; font-family: 'Bebas Neue', cursive; font-size: 1.8rem; color: rgba(255,255,255,0.15); letter-spacing: 4px; padding: 0.5rem 0; }

/* EXPLANATION */
.explanation-box {
    background: rgba(0,229,255,0.03); border: 1px solid rgba(0,229,255,0.12);
    border-radius: 12px; padding: 1rem 1.4rem; font-size: 0.82rem; color: #7aa8c0; line-height: 1.7;
}

/* CONFIDENCE BAR */
.conf-bar-bg { background: #2a2e38; border-radius: 8px; height: 8px; margin: 0.3rem 0; overflow: hidden; }
.conf-bar-fill { height: 100%; border-radius: 8px; transition: width 0.3s; }

div.stButton > button {
    background: linear-gradient(135deg, #00FF9C, #00c864); color: #000;
    font-family: 'Bebas Neue', cursive; font-size: 1.3rem; letter-spacing: 4px;
    border: none; border-radius: 10px; padding: 0.75rem 2rem;
    cursor: pointer; transition: all 0.2s; width: 100%; margin-top: 0.5rem;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #00e574, #00FF9C);
    transform: translateY(-1px); box-shadow: 0 6px 20px rgba(0,255,156,0.3);
}
#MainMenu {visibility: hidden;} footer {visibility: hidden;} .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SUPABASE REST API
# ══════════════════════════════════════════════════════════════

def get_headers():
    key = st.secrets["SUPABASE_KEY"]
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def sb_get(table, params=None):
    url = f"{st.secrets['SUPABASE_URL']}/rest/v1/{table}"
    try:
        r = httpx.get(url, headers=get_headers(), params=params, timeout=10)
        return r.json() if r.status_code == 200 else []
    except:
        return []

def sb_post(table, data):
    url = f"{st.secrets['SUPABASE_URL']}/rest/v1/{table}"
    try:
        r = httpx.post(url, headers=get_headers(), json=data, timeout=10)
        return r.json() if r.status_code in [200, 201] else None
    except:
        return None

def sb_patch(table, match_field, match_value, data):
    url = f"{st.secrets['SUPABASE_URL']}/rest/v1/{table}"
    params = {match_field: f"eq.{match_value}"}
    try:
        r = httpx.patch(url, headers=get_headers(), params=params, json=data, timeout=10)
        return r.status_code in [200, 204]
    except:
        return False

# ══════════════════════════════════════════════════════════════
# CARGA DE DATOS EXTERNOS (teams_stats.json)
# ══════════════════════════════════════════════════════════════

@st.cache_data(ttl=300)
def load_teams_stats():
    """
    Carga estadísticas desde teams_stats.json.
    Permite actualizar sin tocar el código principal.
    """
    ruta = os.path.join(os.path.dirname(__file__), "teams_stats.json")
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"equipos": {}}

def update_data():
    """
    Recarga el cache de teams_stats.json.
    Llama esta función cuando actualices el JSON.
    """
    load_teams_stats.clear()
    return load_teams_stats()

def get_stats_from_json(nombre: str, teams_data: dict):
    """Calcula ataque, defensa, xG y forma desde el JSON externo."""
    equipo = teams_data.get("equipos", {}).get(nombre)
    if not equipo or not equipo.get("ultimos_5"):
        return None
    partidos = equipo["ultimos_5"]
    gf_list = [p["gf"] for p in partidos]
    gc_list = [p["gc"] for p in partidos]
    resultados = [p["resultado"] for p in partidos]
    corners_list = [p.get("corners", 10) for p in partidos]

    avg_gf = sum(gf_list) / len(gf_list)
    avg_gc = sum(gc_list) / len(gc_list)
    avg_corners = sum(corners_list) / len(corners_list)

    puntos = [3 if r == "W" else (1 if r == "D" else 0) for r in resultados]
    avg_pts = sum(puntos) / len(puntos)

    ataque  = max(0.5, min(3.5, round(avg_gf * 0.85 + 0.3, 2)))
    defensa = max(0.5, min(3.5, round(avg_gc * 0.75 + 0.4, 2)))
    xg      = max(0.5, min(3.5, round(avg_gf * 0.80 + 0.25, 2)))
    forma   = max(0.8, min(1.2, round(0.8 + (avg_pts / 3.0) * 0.4, 2)))

    return {
        "ataque": ataque, "defensa": defensa, "xg": xg, "forma": forma,
        "avg_gf": round(avg_gf, 2), "avg_gc": round(avg_gc, 2),
        "avg_corners": round(avg_corners, 1),
        "partidos": partidos, "resultados": resultados,
    }

# ══════════════════════════════════════════════════════════════
# SUPABASE: HELPERS
# ══════════════════════════════════════════════════════════════

def get_equipos():
    return sb_get("equipos", {"select": "*", "order": "nombre.asc"})

def get_partidos_equipo_db(nombre):
    local = sb_get("partidos_ucl", {"select": "*", "equipo_local": f"eq.{nombre}", "goles_local": "not.is.null", "order": "fecha.desc", "limit": "10"})
    visit = sb_get("partidos_ucl", {"select": "*", "equipo_visitante": f"eq.{nombre}", "goles_visitante": "not.is.null", "order": "fecha.desc", "limit": "10"})
    todos = (local or []) + (visit or [])
    todos.sort(key=lambda x: x.get("fecha", ""), reverse=True)
    return todos[:5]

def get_todos_partidos(fase=None):
    data = sb_get("partidos_ucl", {"select": "*", "order": "fecha.desc", "limit": "60"})
    if fase and fase != "Todos":
        data = [p for p in data if p.get("fase") == fase]
    return data

def guardar_simulacion(datos):
    sb_post("simulaciones", datos)

def get_historial_sims():
    return sb_get("simulaciones", {"select": "*", "order": "created_at.desc", "limit": "20"})

# BANKROLL
def get_bankroll():
    data = sb_get("bankroll", {"select": "*", "order": "id.asc", "limit": "1"})
    if data and len(data) > 0:
        return data[0]
    return {"id": None, "saldo_actual": 1000.0, "saldo_inicial": 1000.0}

def update_bankroll(id_bank, nuevo_saldo):
    return sb_patch("bankroll", "id", id_bank, {"saldo_actual": nuevo_saldo, "updated_at": datetime.now().isoformat()})

def get_apuestas():
    return sb_get("apuestas", {"select": "*", "order": "created_at.desc", "limit": "50"})

def crear_apuesta(datos):
    return sb_post("apuestas", datos)

def resolver_apuesta(apuesta_id, resultado, saldo_actual, monto, cuota):
    if resultado == "ganada":
        ganancia = round(monto * cuota - monto, 2)
        nuevo_saldo = round(saldo_actual + ganancia, 2)
    else:
        ganancia = -monto
        nuevo_saldo = round(saldo_actual - monto, 2)
    sb_patch("apuestas", "id", apuesta_id, {"resultado": resultado, "ganancia": ganancia})
    return nuevo_saldo, ganancia

# PREDICCIONES
def guardar_prediccion(datos):
    return sb_post("predicciones", datos)

def get_predicciones():
    return sb_get("predicciones", {"select": "*", "order": "created_at.desc", "limit": "50"})

def resolver_prediccion(pred_id, resultado_real, valor_predicho):
    acerto = resultado_real.lower() == valor_predicho.lower()
    sb_patch("predicciones", "id", pred_id, {"resultado_real": resultado_real, "acerto": acerto})
    return acerto

# ══════════════════════════════════════════════════════════════
# MODELO MATEMÁTICO
# ══════════════════════════════════════════════════════════════

def calcular_lambda(ataque, defensa_rival, xg, forma, ventaja_local, intensidad, factor_reg=0.93):
    lam = (0.60 * (ataque / defensa_rival) + 0.40 * xg) * forma
    if ventaja_local:
        lam *= 1.12
    return max(0.3, min(5.0, lam * intensidad * factor_reg))

def simular_partido(lam_l, lam_v, n=50000):
    rng = np.random.default_rng(42)
    return rng.poisson(lam_l, n), rng.poisson(lam_v, n)

def calcular_probabilidades(gl, gv):
    n = len(gl)
    return {
        "victoria_local":     np.sum(gl > gv) / n * 100,
        "empate":             np.sum(gl == gv) / n * 100,
        "victoria_visitante": np.sum(gl < gv) / n * 100,
        "over_25":            np.sum(gl + gv > 2.5) / n * 100,
        "btts":               np.sum((gl > 0) & (gv > 0)) / n * 100,
    }

def calcular_corners(avg, n=50000):
    return np.sum(np.random.default_rng(123).poisson(avg, n) > 9.5) / n * 100

def calcular_tarjetas(avg, n=50000):
    return np.sum(np.random.default_rng(456).poisson(avg, n) > 3.5) / n * 100

def top_marcadores(gl, gv, top=5):
    n = len(gl)
    conteo = {}
    for g_l, g_v in zip(gl.tolist(), gv.tolist()):
        k = (int(g_l), int(g_v))
        conteo[k] = conteo.get(k, 0) + 1
    return [(f"{g_l}-{g_v}", cnt / n * 100)
            for (g_l, g_v), cnt in sorted(conteo.items(), key=lambda x: x[1], reverse=True)[:top]]

def calcular_nivel_confianza(probs, lam_l, lam_v):
    """Calcula un nivel de confianza general basado en las probabilidades."""
    max_prob = max(probs["victoria_local"], probs["empate"], probs["victoria_visitante"])
    diferencia_lambda = abs(lam_l - lam_v)
    confianza = min(95, (max_prob * 0.6) + (diferencia_lambda * 10))
    return round(confianza, 1)

def detectar_valor(prob_real, cuota_mercado):
    """Detecta si hay valor en una apuesta comparando prob real vs cuota implícita."""
    prob_implicita = (1 / cuota_mercado) * 100
    valor = prob_real - prob_implicita
    return round(valor, 1), valor > 5

def pick_del_dia(probs, over_c, over_t, nombre_local, nombre_visitante):
    """Determina la mejor apuesta del día."""
    candidatos = [
        (f"🏠 Gana {nombre_local}", probs["victoria_local"], "1X2"),
        (f"✈️ Gana {nombre_visitante}", probs["victoria_visitante"], "1X2"),
        ("⚽ Over 2.5 Goles", probs["over_25"], "Goles"),
        ("🎯 BTTS — Ambos Marcan", probs["btts"], "BTTS"),
        ("🚩 Córners Over 9.5", over_c, "Córners"),
        ("🟨 Tarjetas Over 3.5", over_t, "Tarjetas"),
    ]
    mejor = max(candidatos, key=lambda x: x[1])
    return mejor

# ══════════════════════════════════════════════════════════════
# INICIALIZACIÓN
# ══════════════════════════════════════════════════════════════

teams_data = load_teams_stats()

db_ok = False
equipos_db = []
nombres_equipos = []
equipos_dict = {}

try:
    _ = st.secrets["SUPABASE_URL"]
    _ = st.secrets["SUPABASE_KEY"]
    equipos_db = get_equipos()
    if isinstance(equipos_db, list) and len(equipos_db) > 0 and "nombre" in equipos_db[0]:
        nombres_equipos = [e["nombre"] for e in equipos_db]
        equipos_dict = {e["nombre"]: e for e in equipos_db}
        db_ok = True
except Exception as e:
    st.sidebar.error(f"⚠️ Supabase: {e}")

# ══════════════════════════════════════════════════════════════
# SIDEBAR — NAVEGACIÓN
# ══════════════════════════════════════════════════════════════

st.sidebar.markdown("""
<div style="text-align:center;padding:1rem 0;border-bottom:1px solid rgba(0,255,156,0.2);margin-bottom:1rem">
    <div style="font-family:'Bebas Neue',cursive;font-size:1.8rem;letter-spacing:4px;color:#00FF9C">⚽ UCL</div>
    <div style="font-size:0.7rem;color:#5a9ab0;letter-spacing:2px">25/26 PREDICTOR</div>
</div>
""", unsafe_allow_html=True)

pagina = st.sidebar.radio("📍 Navegación", [
    "🎯 Simulador",
    "💰 Bankroll",
    "🧠 Aprendizaje",
    "📋 Partidos UCL",
    "📊 Historial Simulaciones",
], label_visibility="collapsed")

st.sidebar.markdown('<div style="height:1px;background:rgba(255,255,255,0.06);margin:1rem 0"></div>', unsafe_allow_html=True)

# Info del JSON
if teams_data:
    st.sidebar.markdown(f"""
    <div style="background:rgba(0,255,156,0.05);border:1px solid rgba(0,255,156,0.15);border-radius:8px;padding:0.7rem;font-size:0.75rem;color:#7aa8c0">
        📂 <strong style="color:#00FF9C">Datos externos cargados</strong><br>
        📅 {teams_data.get('ultima_actualizacion','—')}<br>
        🏆 {teams_data.get('fase_actual','—')}<br>
        👥 {len(teams_data.get('equipos',{}))} equipos
    </div>
    """, unsafe_allow_html=True)

if st.sidebar.button("🔄 Actualizar Datos", use_container_width=True):
    update_data()
    st.sidebar.success("✅ Datos recargados")

st.sidebar.markdown('<div style="height:1px;background:rgba(255,255,255,0.06);margin:1rem 0"></div>', unsafe_allow_html=True)

if db_ok:
    bankroll_data = get_bankroll()
    saldo = bankroll_data.get("saldo_actual", 1000)
    inicial = bankroll_data.get("saldo_inicial", 1000)
    ganancia_total = round(saldo - inicial, 2)
    color_g = "#00FF9C" if ganancia_total >= 0 else "#FF4B4B"
    signo = "+" if ganancia_total >= 0 else ""
    st.sidebar.markdown(f"""
    <div style="background:#1C1F26;border:1px solid rgba(0,255,156,0.2);border-radius:10px;padding:0.8rem;text-align:center">
        <div style="font-size:0.65rem;color:#7aa8c0;letter-spacing:2px;text-transform:uppercase">Bankroll</div>
        <div style="font-family:'Bebas Neue',cursive;font-size:2rem;color:#00FF9C">${saldo:,.2f}</div>
        <div style="font-size:0.75rem;color:{color_g}">{signo}${ganancia_total:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════

st.markdown("""
<div class="main-header">
    <h1>⚽ UCL 25/26 PREDICTOR</h1>
    <p>Poisson · Monte Carlo 50K · Supabase · Stats Automáticas · Bankroll</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PÁGINA 1: SIMULADOR
# ══════════════════════════════════════════════════════════════

if pagina == "🎯 Simulador":

    st.markdown('<div class="section-title">🏟️ SELECCIÓN DE EQUIPOS</div>', unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([5, 1, 5])

    # ── LOCAL ──
    with col_l:
        st.markdown("**🏠 Equipo Local**")
        lista = nombres_equipos if nombres_equipos else list(teams_data.get("equipos", {}).keys())
        idx_l = lista.index("Real Madrid") if "Real Madrid" in lista else 0
        sel_local = st.selectbox("Equipo local", lista, index=idx_l, key="sel_local")
        nombre_local = sel_local

        stats_l = get_stats_from_json(nombre_local, teams_data)
        eq_l = equipos_dict.get(nombre_local, {})

        if stats_l:
            def_atk_l, def_def_l, def_xg_l, def_forma_l = stats_l["ataque"], stats_l["defensa"], stats_l["xg"], stats_l["forma"]
            res_icons = {"W": "✅", "D": "🟡", "L": "❌"}
            forma_str = " ".join([res_icons.get(r, "?") for r in stats_l["resultados"]])
            st.markdown(f"""
            <div class="stats-auto-box">
                📊 <strong style="color:#00FF9C">Stats AUTO</strong>
                <span class="badge-auto">JSON</span><br>
                ⚽ {stats_l['avg_gf']} gf/p &nbsp;·&nbsp; 🛡️ {stats_l['avg_gc']} gc/p &nbsp;·&nbsp; 🚩 {stats_l['avg_corners']} córners/p<br>
                Forma: {forma_str}
            </div>""", unsafe_allow_html=True)
        else:
            def_atk_l   = float(eq_l.get("ataque", 1.8))
            def_def_l   = float(eq_l.get("defensa", 1.3))
            def_xg_l    = float(eq_l.get("xg_promedio", 1.6))
            def_forma_l = float(eq_l.get("forma", 1.05))

        c1, c2 = st.columns(2)
        with c1:
            ataque_local  = st.slider("⚔️ Ataque",  0.5, 3.5, def_atk_l,   0.05, key="atk_l")
            xg_local      = st.slider("🎯 xG",      0.5, 3.5, def_xg_l,    0.05, key="xg_l")
            forma_local   = st.slider("📈 Forma",   0.8, 1.2, def_forma_l, 0.01, key="forma_l")
        with c2:
            defensa_local = st.slider("🛡️ Defensa", 0.5, 3.5, def_def_l,   0.05, key="def_l")

    with col_m:
        st.markdown('<div class="vs-badge" style="margin-top:6rem">VS</div>', unsafe_allow_html=True)

    # ── VISITANTE ──
    with col_r:
        st.markdown("**✈️ Equipo Visitante**")
        idx_v = lista.index("Manchester City") if "Manchester City" in lista else 1
        sel_away = st.selectbox("Equipo visitante", lista, index=idx_v, key="sel_away")
        nombre_visitante = sel_away

        stats_v = get_stats_from_json(nombre_visitante, teams_data)
        eq_v = equipos_dict.get(nombre_visitante, {})

        if stats_v:
            def_atk_v, def_def_v, def_xg_v, def_forma_v = stats_v["ataque"], stats_v["defensa"], stats_v["xg"], stats_v["forma"]
            res_icons = {"W": "✅", "D": "🟡", "L": "❌"}
            forma_str_v = " ".join([res_icons.get(r, "?") for r in stats_v["resultados"]])
            st.markdown(f"""
            <div class="stats-auto-box">
                📊 <strong style="color:#00FF9C">Stats AUTO</strong>
                <span class="badge-auto">JSON</span><br>
                ⚽ {stats_v['avg_gf']} gf/p &nbsp;·&nbsp; 🛡️ {stats_v['avg_gc']} gc/p &nbsp;·&nbsp; 🚩 {stats_v['avg_corners']} córners/p<br>
                Forma: {forma_str_v}
            </div>""", unsafe_allow_html=True)
        else:
            def_atk_v   = float(eq_v.get("ataque", 1.7))
            def_def_v   = float(eq_v.get("defensa", 1.4))
            def_xg_v    = float(eq_v.get("xg_promedio", 1.5))
            def_forma_v = float(eq_v.get("forma", 1.0))

        c3, c4 = st.columns(2)
        with c3:
            ataque_visit  = st.slider("⚔️ Ataque",  0.5, 3.5, def_atk_v,   0.05, key="atk_v")
            xg_visit      = st.slider("🎯 xG",      0.5, 3.5, def_xg_v,    0.05, key="xg_v")
            forma_visit   = st.slider("📈 Forma",   0.8, 1.2, def_forma_v, 0.01, key="forma_v")
        with c4:
            defensa_visit = st.slider("🛡️ Defensa", 0.5, 3.5, def_def_v,   0.05, key="def_v")

    # Últimos 5 partidos desde JSON
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📅 ÚLTIMOS 5 PARTIDOS (JSON)</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    res_icons = {"W": "✅", "D": "🟡", "L": "❌"}
    for col, nombre, stats in [(p1, nombre_local, stats_l), (p2, nombre_visitante, stats_v)]:
        with col:
            st.markdown(f"**{nombre}**")
            if stats and stats.get("partidos"):
                for p in stats["partidos"]:
                    icono = res_icons.get(p["resultado"], "?")
                    corners_txt = f"🚩{p.get('corners','?')}" if p.get('corners') else ""
                    st.markdown(f"""
                    <div class="partido-row">
                        <span style="color:#5a9ab0;font-size:0.72rem">{p['fecha']}</span>
                        <span>vs <b>{p['rival'][:14]}</b></span>
                        <span style="font-family:'Bebas Neue',cursive;font-size:1.1rem;letter-spacing:2px">{p['gf']} – {p['gc']}</span>
                        <span>{icono} {corners_txt}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("Sin datos en JSON.")

    # Contexto
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚙️ CONTEXTO</div>', unsafe_allow_html=True)
    cp1, cp2, cp3, cp4, cp5 = st.columns([3, 3, 3, 3, 2])
    with cp1: intensidad    = st.slider("🏆 Intensidad Champions", 0.90, 1.20, 1.05, 0.01)
    with cp2: avg_corners   = st.slider("🚩 Córners promedio", 6, 14, 10, 1)
    with cp3: avg_tarjetas  = st.slider("🟨 Tarjetas promedio", 2, 7, 4, 1)
    with cp4: factor_reg    = st.slider("📉 Factor regresión", 0.88, 0.98, 0.93, 0.01)
    with cp5: ventaja_local = st.checkbox("🏟️ Ventaja de local", value=True)

    # Modo avanzado
    with st.expander("🔬 Modo Avanzado (Stats Detalladas)"):
        adv1, adv2, adv3 = st.columns(3)
        with adv1:
            st.markdown(f"**λ Local estimado:** `{calcular_lambda(ataque_local, defensa_visit, xg_local, forma_local, ventaja_local, intensidad, factor_reg):.3f}`")
        with adv2:
            st.markdown(f"**λ Visitante estimado:** `{calcular_lambda(ataque_visit, defensa_local, xg_visit, forma_visit, False, intensidad, factor_reg):.3f}`")
        with adv3:
            ratio = ataque_local / max(0.1, defensa_visit)
            st.markdown(f"**Ratio Ataque/Defensa:** `{ratio:.3f}`")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    simular = st.button("🎲 SIMULAR PARTIDO — 50,000 ITERACIONES", use_container_width=True)

    if simular:
        with st.spinner("⚙️ Simulando con Monte Carlo..."):
            lam_l  = calcular_lambda(ataque_local, defensa_visit, xg_local, forma_local, ventaja_local, intensidad, factor_reg)
            lam_v  = calcular_lambda(ataque_visit, defensa_local, xg_visit, forma_visit, False, intensidad, factor_reg)
            gl, gv = simular_partido(lam_l, lam_v)
            probs  = calcular_probabilidades(gl, gv)
            over_c = calcular_corners(avg_corners)
            over_t = calcular_tarjetas(avg_tarjetas)
            top5   = top_marcadores(gl, gv)
            confianza = calcular_nivel_confianza(probs, lam_l, lam_v)

        partido_str = f"{nombre_local} vs {nombre_visitante}"

        if db_ok:
            guardar_simulacion({
                "equipo_local": nombre_local, "equipo_visitante": nombre_visitante,
                "prob_victoria_local": round(probs["victoria_local"], 2),
                "prob_empate": round(probs["empate"], 2),
                "prob_victoria_visitante": round(probs["victoria_visitante"], 2),
                "prob_over25": round(probs["over_25"], 2),
                "prob_btts": round(probs["btts"], 2),
                "prob_corners_over95": round(over_c, 2),
                "prob_tarjetas_over35": round(over_t, 2),
                "lambda_local": round(lam_l, 3), "lambda_visitante": round(lam_v, 3),
                "marcador_probable": top5[0][0] if top5 else "N/A",
            })
            st.markdown('<span class="badge-db">✅ GUARDADO EN BD</span>', unsafe_allow_html=True)

        # NIVEL DE CONFIANZA
        conf_color = "#00FF9C" if confianza >= 70 else ("#FFD700" if confianza >= 50 else "#FF4B4B")
        st.markdown(f"""
        <div style="background:#1C1F26;border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:1rem;margin:0.8rem 0;display:flex;justify-content:space-between;align-items:center">
            <span style="font-size:0.8rem;color:#7aa8c0;text-transform:uppercase;letter-spacing:2px">🎯 Nivel de Confianza del Modelo</span>
            <div style="display:flex;align-items:center;gap:1rem">
                <div style="width:200px;background:#2a2e38;border-radius:8px;height:10px;overflow:hidden">
                    <div style="width:{confianza}%;height:100%;background:{conf_color};border-radius:8px"></div>
                </div>
                <span style="font-family:'Bebas Neue',cursive;font-size:1.8rem;color:{conf_color}">{confianza}%</span>
            </div>
        </div>""", unsafe_allow_html=True)

        # PROBABILIDADES 1X2
        st.markdown('<div class="section-title">📊 PROBABILIDADES</div>', unsafe_allow_html=True)
        vl, emp, vv = probs["victoria_local"], probs["empate"], probs["victoria_visitante"]
        r1, r2, r3 = st.columns(3)
        with r1:
            c = "green" if vl >= 60 else ("yellow" if vl >= 45 else "red")
            st.markdown(f'<div class="metric-box"><div class="metric-label">🏠 {nombre_local[:16]}</div><div class="metric-value {c}">{vl:.1f}%</div></div>', unsafe_allow_html=True)
        with r2:
            st.markdown(f'<div class="metric-box"><div class="metric-label">🤝 Empate</div><div class="metric-value">{emp:.1f}%</div></div>', unsafe_allow_html=True)
        with r3:
            c = "green" if vv >= 60 else ("yellow" if vv >= 45 else "red")
            st.markdown(f'<div class="metric-box"><div class="metric-label">✈️ {nombre_visitante[:16]}</div><div class="metric-value {c}">{vv:.1f}%</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        o25, btts = probs["over_25"], probs["btts"]
        m1, m2, m3, m4 = st.columns(4)
        for col, label, val in zip([m1, m2, m3, m4],
            ["⚽ Over 2.5", "🎯 BTTS", "🚩 Córners >9.5", "🟨 Tarjetas >3.5"],
            [o25, btts, over_c, over_t]):
            c = "green" if val >= 60 else ("yellow" if val >= 45 else "blue")
            col.markdown(f'<div class="metric-box"><div class="metric-label">{label}</div><div class="metric-value {c}">{val:.1f}%</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        x1, x2 = st.columns(2)
        x1.markdown(f'<div class="metric-box"><div class="metric-label">📐 λ {nombre_local[:14]}</div><div class="metric-value green">{lam_l:.2f}</div></div>', unsafe_allow_html=True)
        x2.markdown(f'<div class="metric-box"><div class="metric-label">📐 λ {nombre_visitante[:14]}</div><div class="metric-value">{lam_v:.2f}</div></div>', unsafe_allow_html=True)

        # PICK DEL DÍA
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        pick_label, pick_prob, pick_tipo = pick_del_dia(probs, over_c, over_t, nombre_local, nombre_visitante)
        st.markdown(f"""
        <div class="pick-del-dia">
            <div class="pick-title">⭐ PICK DEL DÍA</div>
            <div class="pick-desc">{pick_label}</div>
            <div style="font-family:'Bebas Neue',cursive;font-size:2.5rem;color:#FFD700">{pick_prob:.1f}%</div>
            <div class="pick-conf">Tipo: {pick_tipo} &nbsp;·&nbsp; Confianza modelo: {confianza}%</div>
        </div>""", unsafe_allow_html=True)

        # APUESTAS CON VALOR
        st.markdown('<div class="section-title">💎 APUESTAS CON VALOR</div>', unsafe_allow_html=True)
        st.markdown("*Cuotas de mercado estimadas — ajusta según tu casa de apuestas*")
        cuotas_est = {
            f"🏠 {nombre_local}": max(1.1, round(100/max(1, vl), 2)),
            "🤝 Empate": max(1.1, round(100/max(1, emp), 2)),
            f"✈️ {nombre_visitante}": max(1.1, round(100/max(1, vv), 2)),
            "⚽ Over 2.5": max(1.1, round(100/max(1, o25), 2)),
            "🎯 BTTS": max(1.1, round(100/max(1, btts), 2)),
        }
        v1, v2 = st.columns(2)
        i = 0
        for label, cuota in cuotas_est.items():
            prob = [vl, emp, vv, o25, btts][i]
            val_num, tiene_valor = detectar_valor(prob, cuota)
            if tiene_valor:
                col = v1 if i % 2 == 0 else v2
                col.markdown(f"""
                <div class="valor-bet">
                    <span>{label}</span>
                    <span>Prob: <b>{prob:.1f}%</b> &nbsp;·&nbsp; Cuota: <b>{cuota}</b></span>
                    <span class="badge-valor">+{val_num}% VALOR</span>
                </div>""", unsafe_allow_html=True)
            i += 1

        # TOP 5 MARCADORES
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎯 TOP 5 MARCADORES</div>', unsafe_allow_html=True)
        sc1, sc2 = st.columns([3, 2])
        with sc1:
            iconos = ["🥇","🥈","🥉","▪️","▪️"]
            for i, (marcador, pct) in enumerate(top5):
                g_l, g_v = marcador.split("-")
                st.markdown(f"""
                <div class="score-card">
                    <span style="font-size:1.2rem">{iconos[i]}</span>
                    <span class="score-text">{nombre_local[:11]} &nbsp; {g_l}–{g_v} &nbsp; {nombre_visitante[:11]}</span>
                    <span class="score-pct">{pct:.1f}%</span>
                </div>""", unsafe_allow_html=True)
        with sc2:
            df_s = pd.DataFrame({"Marcador": [m for m, _ in top5], "Prob (%)": [p for _, p in top5]})
            st.bar_chart(df_s.set_index("Marcador"), color="#00FF9C", height=220)

        # APUESTAS SUGERIDAS
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">💰 APUESTAS SUGERIDAS</div>', unsafe_allow_html=True)
        apuestas_lista = [
            (f"🏠 Gana {nombre_local}", vl), (f"✈️ Gana {nombre_visitante}", vv),
            ("⚽ Over 2.5 Goles", o25), ("🎯 BTTS — Ambos Marcan", btts),
            ("🚩 Córners Over 9.5", over_c), ("🟨 Tarjetas Over 3.5", over_t),
        ]
        sugeridas = [(l, p) for l, p in apuestas_lista if p >= 60]
        if sugeridas:
            ba1, ba2 = st.columns(2)
            for i, (label, pct) in enumerate(sugeridas):
                col = ba1 if i % 2 == 0 else ba2
                if pct >= 70:
                    col.markdown(f'<div class="bet-green"><span class="bet-label">{label}</span><span class="bet-pct-green">✅ {pct:.1f}%</span></div>', unsafe_allow_html=True)
                else:
                    col.markdown(f'<div class="bet-yellow"><span class="bet-label">{label}</span><span class="bet-pct-yellow">⚠️ {pct:.1f}%</span></div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.72rem;color:#556b80;margin-top:0.5rem">🟢 ≥70% &nbsp;|&nbsp; 🟡 60–69%</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="explanation-box">⚠️ Ninguna apuesta supera el 60% en este escenario.</div>', unsafe_allow_html=True)

        # GUARDAR PREDICCIÓN EN BD
        if db_ok:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            with st.expander("💾 Guardar predicción para seguimiento"):
                pred_tipo = st.selectbox("Tipo de predicción", ["1X2 - Local", "1X2 - Empate", "1X2 - Visitante", "Over 2.5", "BTTS Sí", "Córners Over 9.5", "Tarjetas Over 3.5"])
                pred_vals = {
                    "1X2 - Local": (vl, "Local"), "1X2 - Empate": (emp, "Empate"),
                    "1X2 - Visitante": (vv, "Visitante"), "Over 2.5": (o25, "Over"),
                    "BTTS Sí": (btts, "Si"), "Córners Over 9.5": (over_c, "Over"),
                    "Tarjetas Over 3.5": (over_t, "Over"),
                }
                prob_pred, valor_pred = pred_vals[pred_tipo]
                fecha_partido = st.date_input("Fecha del partido", value=date.today())
                if st.button("💾 Guardar Predicción"):
                    guardar_prediccion({
                        "partido": partido_str, "tipo_prediccion": pred_tipo,
                        "valor_predicho": valor_pred, "probabilidad": round(prob_pred, 2),
                        "fecha_partido": str(fecha_partido),
                    })
                    st.success("✅ Predicción guardada")

        st.markdown("""
        <div class="explanation-box" style="margin-top:1rem">
            <strong>📖 Metodología:</strong> Stats calculadas automáticamente desde <code>teams_stats.json</code>.
            Modelo: Ataque/Defensa (60%) + xG (40%) · Forma · Ventaja local (+12%) · Intensidad UCL · Regresión.
            50,000 simulaciones Monte Carlo con distribución de Poisson. El nivel de confianza refleja
            la certeza del modelo según la diferencia de lambdas y la concentración de probabilidades.
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PÁGINA 2: BANKROLL
# ══════════════════════════════════════════════════════════════

elif pagina == "💰 Bankroll":
    st.markdown('<div class="section-title">💰 GESTIÓN DE BANKROLL</div>', unsafe_allow_html=True)

    if not db_ok:
        st.warning("⚠️ Conecta Supabase para usar el Bankroll.")
    else:
        bankroll_data = get_bankroll()
        saldo_actual  = bankroll_data.get("saldo_actual", 1000.0)
        saldo_inicial = bankroll_data.get("saldo_inicial", 1000.0)
        bank_id       = bankroll_data.get("id")
        ganancia_total = round(saldo_actual - saldo_inicial, 2)

        # Saldo + resumen
        b1, b2, b3 = st.columns(3)
        with b1:
            st.markdown(f"""
            <div class="saldo-box">
                <div class="saldo-label">Saldo Actual</div>
                <div class="saldo-value">${saldo_actual:,.2f}</div>
            </div>""", unsafe_allow_html=True)
        with b2:
            color_g = "#00FF9C" if ganancia_total >= 0 else "#FF4B4B"
            signo = "+" if ganancia_total >= 0 else ""
            st.markdown(f"""
            <div class="saldo-box" style="border-color:rgba({('0,255,156' if ganancia_total >= 0 else '255,75,75')},0.4)">
                <div class="saldo-label">Ganancia / Pérdida</div>
                <div class="saldo-value" style="color:{color_g}">{signo}${ganancia_total:,.2f}</div>
            </div>""", unsafe_allow_html=True)
        with b3:
            roi = round((ganancia_total / saldo_inicial) * 100, 1) if saldo_inicial > 0 else 0
            color_roi = "#00FF9C" if roi >= 0 else "#FF4B4B"
            st.markdown(f"""
            <div class="saldo-box" style="border-color:rgba(0,229,255,0.4)">
                <div class="saldo-label">ROI</div>
                <div class="saldo-value" style="color:{color_roi}">{roi:+.1f}%</div>
            </div>""", unsafe_allow_html=True)

        # Ajustar saldo inicial
        with st.expander("⚙️ Ajustar Saldo Inicial"):
            nuevo_inicial = st.number_input("Nuevo saldo inicial ($)", min_value=100.0, value=float(saldo_inicial), step=50.0)
            if st.button("💾 Actualizar Saldo Inicial"):
                if bank_id:
                    sb_patch("bankroll", "id", bank_id, {"saldo_inicial": nuevo_inicial, "saldo_actual": nuevo_inicial})
                    st.success("✅ Saldo actualizado")
                    st.rerun()

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📝 REGISTRAR APUESTA</div>', unsafe_allow_html=True)

        ra1, ra2 = st.columns(2)
        with ra1:
            partido_ap = st.text_input("⚽ Partido", placeholder="ej: Real Madrid vs Arsenal")
            tipo_ap = st.selectbox("📋 Tipo de apuesta", [
                "1X2 - Gana Local", "1X2 - Empate", "1X2 - Gana Visitante",
                "Over 2.5 Goles", "Under 2.5 Goles", "BTTS Sí", "BTTS No",
                "Córners Over 9.5", "Tarjetas Over 3.5", "Otro"
            ])
            notas_ap = st.text_input("📝 Notas (opcional)")
        with ra2:
            cuota_ap = st.number_input("💱 Cuota", min_value=1.01, value=1.80, step=0.05)
            monto_ap = st.number_input("💵 Monto a apostar ($)", min_value=1.0, value=round(saldo_actual * 0.05, 2), step=5.0)
            ganancia_pot = round(monto_ap * cuota_ap - monto_ap, 2)
            st.markdown(f"""
            <div style="background:#1C1F26;border:1px solid rgba(0,255,156,0.2);border-radius:8px;padding:0.8rem;text-align:center;margin-top:0.5rem">
                <div style="font-size:0.7rem;color:#7aa8c0;text-transform:uppercase">Ganancia Potencial</div>
                <div style="font-family:'Bebas Neue',cursive;font-size:1.8rem;color:#00FF9C">+${ganancia_pot:,.2f}</div>
                <div style="font-size:0.72rem;color:#556b80">{round((monto_ap/saldo_actual)*100,1)}% del bankroll</div>
            </div>""", unsafe_allow_html=True)

        if st.button("💰 Registrar Apuesta", use_container_width=True):
            if partido_ap:
                crear_apuesta({
                    "partido": partido_ap, "tipo_apuesta": tipo_ap,
                    "cuota": cuota_ap, "monto": monto_ap,
                    "resultado": "pendiente", "ganancia": 0, "notas": notas_ap
                })
                st.success(f"✅ Apuesta registrada: {partido_ap} | {tipo_ap} | ${monto_ap}")
                st.rerun()
            else:
                st.error("⚠️ Escribe el nombre del partido")

        # HISTORIAL DE APUESTAS
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📋 HISTORIAL DE APUESTAS</div>', unsafe_allow_html=True)

        apuestas = get_apuestas()
        if apuestas:
            pendientes = [a for a in apuestas if a.get("resultado") == "pendiente"]
            if pendientes:
                st.markdown("**⏳ Apuestas Pendientes**")
                for ap in pendientes:
                    ap_col1, ap_col2, ap_col3 = st.columns([4, 2, 2])
                    with ap_col1:
                        st.markdown(f"**{ap['partido']}** — {ap['tipo_apuesta']}")
                        st.caption(f"Cuota: {ap['cuota']} | Monto: ${ap['monto']}")
                    with ap_col2:
                        res_sel = st.selectbox("Resultado", ["pendiente", "ganada", "perdida"],
                                               key=f"res_{ap['id']}", label_visibility="collapsed")
                    with ap_col3:
                        if st.button("✅ Resolver", key=f"btn_{ap['id']}", use_container_width=True):
                            if res_sel != "pendiente":
                                nuevo_saldo, ganancia = resolver_apuesta(ap["id"], res_sel, saldo_actual, ap["monto"], ap["cuota"])
                                if bank_id:
                                    update_bankroll(bank_id, nuevo_saldo)
                                st.success(f"{'✅ Ganada' if res_sel == 'ganada' else '❌ Perdida'} | {'+'if ganancia>0 else ''}${ganancia}")
                                st.rerun()

            st.markdown("**📊 Todas las Apuestas**")
            df_ap = pd.DataFrame(apuestas)
            if not df_ap.empty:
                cols_ap = ["created_at", "partido", "tipo_apuesta", "cuota", "monto", "resultado", "ganancia"]
                df_show = df_ap[[c for c in cols_ap if c in df_ap.columns]].copy()
                df_show.columns = ["Fecha", "Partido", "Tipo", "Cuota", "Monto", "Resultado", "Ganancia"][:len(df_show.columns)]
                if "Fecha" in df_show.columns:
                    df_show["Fecha"] = pd.to_datetime(df_show["Fecha"]).dt.strftime("%d/%m %H:%M")
                st.dataframe(df_show, use_container_width=True, hide_index=True)
        else:
            st.info("Aún no hay apuestas registradas.")

# ══════════════════════════════════════════════════════════════
# PÁGINA 3: SISTEMA DE APRENDIZAJE
# ══════════════════════════════════════════════════════════════

elif pagina == "🧠 Aprendizaje":
    st.markdown('<div class="section-title">🧠 SISTEMA DE APRENDIZAJE</div>', unsafe_allow_html=True)

    if not db_ok:
        st.warning("⚠️ Conecta Supabase para usar el sistema de aprendizaje.")
    else:
        predicciones = get_predicciones()
        resueltas = [p for p in predicciones if p.get("acerto") is not None]
        pendientes = [p for p in predicciones if p.get("acerto") is None]

        # MÉTRICAS GENERALES
        if resueltas:
            total = len(resueltas)
            aciertos = sum(1 for p in resueltas if p.get("acerto") == True)
            pct_acierto = round(aciertos / total * 100, 1)

            # Por tipo
            tipos = {}
            for p in resueltas:
                t = p.get("tipo_prediccion", "Otro")
                if t not in tipos:
                    tipos[t] = {"total": 0, "aciertos": 0}
                tipos[t]["total"] += 1
                if p.get("acerto"):
                    tipos[t]["aciertos"] += 1

            ap1, ap2, ap3, ap4 = st.columns(4)
            with ap1:
                st.markdown(f'<div class="metric-box"><div class="metric-label">✅ Predicciones Totales</div><div class="metric-value">{total}</div></div>', unsafe_allow_html=True)
            with ap2:
                c = "green" if pct_acierto >= 60 else ("yellow" if pct_acierto >= 45 else "red")
                st.markdown(f'<div class="metric-box"><div class="metric-label">🎯 % Acierto General</div><div class="metric-value {c}">{pct_acierto}%</div></div>', unsafe_allow_html=True)
            with ap3:
                st.markdown(f'<div class="metric-box"><div class="metric-label">✅ Aciertos</div><div class="metric-value green">{aciertos}</div></div>', unsafe_allow_html=True)
            with ap4:
                st.markdown(f'<div class="metric-box"><div class="metric-label">❌ Errores</div><div class="metric-value red">{total - aciertos}</div></div>', unsafe_allow_html=True)

            # Por tipo de predicción
            if tipos:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="section-title">📊 ACIERTO POR TIPO</div>', unsafe_allow_html=True)
                t_cols = st.columns(min(len(tipos), 4))
                for i, (tipo, data) in enumerate(tipos.items()):
                    pct_t = round(data["aciertos"] / data["total"] * 100, 1)
                    c = "green" if pct_t >= 60 else ("yellow" if pct_t >= 45 else "red")
                    t_cols[i % len(t_cols)].markdown(f'<div class="metric-box"><div class="metric-label">{tipo}</div><div class="metric-value {c}">{pct_t}%</div><div style="font-size:0.7rem;color:#5a9ab0">{data["aciertos"]}/{data["total"]}</div></div>', unsafe_allow_html=True)
        else:
            st.info("Aún no hay predicciones resueltas. ¡Simula partidos y registra los resultados!")

        # RESOLVER PREDICCIONES PENDIENTES
        if pendientes:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">⏳ PENDIENTES DE RESOLVER</div>', unsafe_allow_html=True)
            for pred in pendientes:
                pc1, pc2, pc3, pc4 = st.columns([3, 2, 2, 1])
                with pc1:
                    st.markdown(f"**{pred['partido']}**")
                    st.caption(f"{pred['tipo_prediccion']} — Predicho: **{pred['valor_predicho']}** ({pred.get('probabilidad','?')}%)")
                with pc2:
                    st.caption(f"📅 {pred.get('fecha_partido', '?')}")
                with pc3:
                    resultado_real = st.text_input("Resultado real", key=f"rr_{pred['id']}", placeholder="ej: Local, Over, Si...", label_visibility="collapsed")
                with pc4:
                    if st.button("✔️", key=f"rv_{pred['id']}", use_container_width=True):
                        if resultado_real:
                            acerto = resolver_prediccion(pred["id"], resultado_real, pred["valor_predicho"])
                            if acerto:
                                st.success("✅ ¡Acierto!")
                            else:
                                st.error("❌ Error")
                            st.rerun()

        # HISTORIAL COMPLETO
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📋 HISTORIAL DE PREDICCIONES</div>', unsafe_allow_html=True)
        if predicciones:
            for pred in predicciones:
                acerto = pred.get("acerto")
                if acerto is True:
                    icono, clase = "✅", "pred-acierto"
                elif acerto is False:
                    icono, clase = "❌", "pred-error"
                else:
                    icono, clase = "⏳", "pred-pending"
                st.markdown(f"""
                <div class="partido-row">
                    <span style="font-size:1.2rem">{icono}</span>
                    <span><b>{pred['partido']}</b></span>
                    <span style="color:#7aa8c0">{pred['tipo_prediccion']}</span>
                    <span>→ <b>{pred['valor_predicho']}</b></span>
                    <span style="color:#5a9ab0">{pred.get('probabilidad','?')}%</span>
                    <span class="{clase}">{pred.get('resultado_real', 'pendiente')}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No hay predicciones registradas aún.")

# ══════════════════════════════════════════════════════════════
# PÁGINA 4: PARTIDOS UCL
# ══════════════════════════════════════════════════════════════

elif pagina == "📋 Partidos UCL":
    st.markdown('<div class="section-title">📋 RESULTADOS UCL 2025/26</div>', unsafe_allow_html=True)
    if db_ok:
        fase_filter = st.selectbox("Filtrar por fase", ["Todos", "Fase Liga", "Octavos Ida", "Octavos Vuelta"])
        todos = get_todos_partidos(fase_filter)
        if todos:
            for p in todos:
                gl = p.get("goles_local") if p.get("goles_local") is not None else "–"
                gv = p.get("goles_visitante") if p.get("goles_visitante") is not None else "–"
                st.markdown(f"""
                <div class="partido-row">
                    <span style="color:#5a9ab0;font-size:0.75rem;min-width:90px">{p.get('fecha','')}</span>
                    <span style="min-width:80px;color:#3d6070;font-size:0.72rem">{p.get('fase','')}</span>
                    <span style="min-width:140px;text-align:right"><b>{p.get('equipo_local','')}</b></span>
                    <span style="font-family:'Bebas Neue',cursive;font-size:1.3rem;letter-spacing:4px;padding:0 1rem;color:#00FF9C">{gl} – {gv}</span>
                    <span style="min-width:140px"><b>{p.get('equipo_visitante','')}</b></span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No hay partidos para mostrar.")
    else:
        st.warning("Conecta Supabase para ver los partidos.")

# ══════════════════════════════════════════════════════════════
# PÁGINA 5: HISTORIAL SIMULACIONES
# ══════════════════════════════════════════════════════════════

elif pagina == "📊 Historial Simulaciones":
    st.markdown('<div class="section-title">📊 HISTORIAL DE SIMULACIONES</div>', unsafe_allow_html=True)
    if db_ok:
        sims = get_historial_sims()
        if sims:
            df = pd.DataFrame(sims)
            cols_show = ["created_at","equipo_local","equipo_visitante",
                         "prob_victoria_local","prob_empate","prob_victoria_visitante",
                         "prob_over25","prob_btts","marcador_probable"]
            df_show = df[[c for c in cols_show if c in df.columns]].copy()
            df_show.columns = ["Fecha","Local","Visitante","% Local","% Empate","% Visit.","Over 2.5","BTTS","Marcador"][:len(df_show.columns)]
            if "Fecha" in df_show.columns:
                df_show["Fecha"] = pd.to_datetime(df_show["Fecha"]).dt.strftime("%d/%m %H:%M")
            st.dataframe(df_show, use_container_width=True, hide_index=True)
        else:
            st.info("Aún no hay simulaciones. ¡Simula tu primer partido!")
    else:
        st.warning("Conecta Supabase para ver el historial.")
