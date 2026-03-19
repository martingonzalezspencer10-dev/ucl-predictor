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
    page_title="⚽ Predictor UCL + Chile",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CSS PROFESIONAL LIMPIO
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0E1117; color: #dce8f0; }

section[data-testid="stSidebar"] {
    background: #13161e !important;
    border-right: 1px solid #1e2535;
}
section[data-testid="stSidebar"] * { color: #dce8f0 !important; }

/* HEADER */
.main-header {
    text-align: center; padding: 1.5rem 0 1rem;
    border-bottom: 1px solid #1e2535; margin-bottom: 1.5rem;
}
.main-header h1 {
    font-family: 'Bebas Neue', cursive; font-size: 2.8rem; letter-spacing: 6px;
    background: linear-gradient(90deg, #3ecf8e, #5ab4d6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0;
}
.main-header p { color: #5a7a8a; font-size: 0.75rem; letter-spacing: 3px; text-transform: uppercase; margin-top: 0.3rem; }

/* SECTION TITLE */
.section-title {
    font-family: 'Bebas Neue', cursive; font-size: 1.3rem; letter-spacing: 4px;
    color: #3ecf8e; border-left: 3px solid #3ecf8e; padding-left: 10px; margin: 1.2rem 0 0.8rem;
}
.section-title-chile {
    font-family: 'Bebas Neue', cursive; font-size: 1.3rem; letter-spacing: 4px;
    color: #e05c5c; border-left: 3px solid #e05c5c; padding-left: 10px; margin: 1.2rem 0 0.8rem;
}

/* CARDS */
.card {
    background: #1C1F26; border: 1px solid #252a35;
    border-radius: 12px; padding: 1.2rem; margin: 0.4rem 0;
}

/* METRIC BOX */
.metric-box {
    background: #1C1F26; border: 1px solid #252a35;
    border-radius: 10px; padding: 1rem; text-align: center; margin: 0.3rem 0;
}
.metric-label { font-size: 0.65rem; color: #5a7a8a; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-bottom: 0.3rem; }
.metric-value { font-family: 'Bebas Neue', cursive; font-size: 2.2rem; letter-spacing: 2px; line-height: 1; color: #dce8f0; }
.metric-value.green  { color: #3ecf8e; }
.metric-value.yellow { color: #d4a843; }
.metric-value.red    { color: #e05c5c; }
.metric-value.blue   { color: #5ab4d6; }

/* PARTIDO CARD */
.partido-card {
    background: #1C1F26; border: 1px solid #252a35;
    border-radius: 10px; padding: 1rem 1.2rem; margin: 0.4rem 0;
    cursor: pointer; transition: border-color 0.2s;
}
.partido-card:hover { border-color: #e05c5c; }
.partido-card.selected { border-color: #e05c5c; background: #21161a; }
.partido-equipos {
    display: flex; justify-content: space-between; align-items: center;
    font-weight: 600; font-size: 0.95rem;
}
.partido-meta { font-size: 0.72rem; color: #5a7a8a; margin-top: 0.3rem; }
.vs-text {
    font-family: 'Bebas Neue', cursive; font-size: 1.2rem;
    color: #2a3545; letter-spacing: 2px; padding: 0 0.8rem;
}

/* PARTIDO ROW SMALL */
.partido-row {
    background: #1C1F26; border: 1px solid #1e2535;
    border-radius: 8px; padding: 0.55rem 0.9rem; margin: 0.2rem 0;
    display: flex; justify-content: space-between; align-items: center; font-size: 0.82rem;
}

/* APUESTA BETS */
.bet-green {
    background: rgba(62,207,142,0.07); border: 1px solid rgba(62,207,142,0.35);
    border-radius: 8px; padding: 0.8rem 1rem; margin: 0.3rem 0;
    display: flex; justify-content: space-between; align-items: center;
}
.bet-yellow {
    background: rgba(212,168,67,0.07); border: 1px solid rgba(212,168,67,0.35);
    border-radius: 8px; padding: 0.8rem 1rem; margin: 0.3rem 0;
    display: flex; justify-content: space-between; align-items: center;
}
.bet-label { color: #c0d0dc; font-size: 0.88rem; font-weight: 500; }
.bet-pct-green  { color: #3ecf8e; font-family: 'Bebas Neue', cursive; font-size: 1.3rem; }
.bet-pct-yellow { color: #d4a843; font-family: 'Bebas Neue', cursive; font-size: 1.3rem; }

/* PICK DEL DÍA */
.pick-box {
    background: #1a1d12; border: 1px solid rgba(212,168,67,0.4);
    border-radius: 12px; padding: 1.2rem 1.5rem; margin: 0.8rem 0; text-align: center;
}
.pick-title { font-family: 'Bebas Neue', cursive; font-size: 1.5rem; letter-spacing: 4px; color: #d4a843; }
.pick-value { font-family: 'Bebas Neue', cursive; font-size: 2.2rem; color: #dce8f0; margin: 0.2rem 0; }

/* VALOR BET */
.valor-bet {
    background: rgba(62,207,142,0.05); border: 1px dashed rgba(62,207,142,0.3);
    border-radius: 8px; padding: 0.6rem 0.9rem; margin: 0.25rem 0;
    display: flex; justify-content: space-between; align-items: center; font-size: 0.83rem;
}

/* SCORE CARD */
.score-card {
    background: #1C1F26; border: 1px solid #252a35;
    border-radius: 8px; padding: 0.7rem 0.9rem; margin: 0.25rem 0;
    display: flex; justify-content: space-between; align-items: center;
}
.score-card:first-child { border-color: rgba(62,207,142,0.4); }
.score-text { font-family: 'Bebas Neue', cursive; font-size: 1.4rem; letter-spacing: 3px; }
.score-pct  { font-size: 0.78rem; color: #5a7a8a; font-weight: 600; }

/* BANKROLL */
.saldo-box {
    background: #1C1F26; border: 1px solid rgba(62,207,142,0.3);
    border-radius: 12px; padding: 1.3rem; text-align: center; margin: 0.4rem 0;
}
.saldo-label { font-size: 0.65rem; color: #5a7a8a; text-transform: uppercase; letter-spacing: 3px; }
.saldo-value { font-family: 'Bebas Neue', cursive; font-size: 2.8rem; letter-spacing: 2px; color: #3ecf8e; }

/* STATS AUTO */
.stats-box {
    background: rgba(62,207,142,0.04); border: 1px solid rgba(62,207,142,0.15);
    border-radius: 8px; padding: 0.7rem 0.9rem; margin: 0.35rem 0;
    font-size: 0.78rem; color: #7a9aaa; line-height: 1.6;
}

/* FORMA ICONS */
.forma-w { color: #3ecf8e; font-weight: 700; }
.forma-d { color: #d4a843; font-weight: 700; }
.forma-l { color: #e05c5c; font-weight: 700; }

/* BADGES */
.badge { display:inline-block; border-radius:20px; padding:0.1rem 0.6rem; font-size:0.62rem; font-weight:700; letter-spacing:1px; }
.badge-green  { background:rgba(62,207,142,0.12); border:1px solid rgba(62,207,142,0.3); color:#3ecf8e; }
.badge-blue   { background:rgba(90,180,214,0.12); border:1px solid rgba(90,180,214,0.3); color:#5ab4d6; }
.badge-red    { background:rgba(224,92,92,0.12);  border:1px solid rgba(224,92,92,0.3);  color:#e05c5c; }
.badge-yellow { background:rgba(212,168,67,0.12); border:1px solid rgba(212,168,67,0.3); color:#d4a843; }

/* CONF BAR */
.conf-bar-bg   { background:#1e2535; border-radius:6px; height:7px; overflow:hidden; margin:0.25rem 0; }
.conf-bar-fill { height:100%; border-radius:6px; }

/* DIVIDER */
.divider { height:1px; background:#1e2535; margin:1.2rem 0; }

/* PREDICCION ROW */
.pred-row {
    background:#1C1F26; border:1px solid #1e2535; border-radius:8px;
    padding:0.55rem 0.9rem; margin:0.2rem 0;
    display:flex; justify-content:space-between; align-items:center; font-size:0.82rem;
}

div.stButton > button {
    background: linear-gradient(135deg, #3ecf8e, #2aaa72); color: #0a0f0a;
    font-family: 'Bebas Neue', cursive; font-size: 1.2rem; letter-spacing: 3px;
    border: none; border-radius: 8px; padding: 0.65rem 1.5rem;
    cursor: pointer; transition: all 0.2s; width: 100%;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #4adfa0, #3ecf8e);
    transform: translateY(-1px); box-shadow: 0 4px 15px rgba(62,207,142,0.25);
}
#MainMenu {visibility:hidden;} footer {visibility:hidden;} .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SUPABASE REST API
# ══════════════════════════════════════════════════════════════

def get_headers():
    key = st.secrets["SUPABASE_KEY"]
    return {"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json", "Prefer": "return=representation"}

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
    try:
        r = httpx.patch(url, headers=get_headers(), params={match_field: f"eq.{match_value}"}, json=data, timeout=10)
        return r.status_code in [200, 204]
    except:
        return False

# ══════════════════════════════════════════════════════════════
# CARGA DE DATOS EXTERNOS
# ══════════════════════════════════════════════════════════════

@st.cache_data(ttl=300)
def load_teams_stats():
    ruta = os.path.join(os.path.dirname(__file__), "teams_stats.json")
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"equipos": {}}

@st.cache_data(ttl=300)
def load_chile_stats():
    ruta = os.path.join(os.path.dirname(__file__), "chile_stats.json")
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"equipos": {}, "proximos_partidos": []}

def update_data():
    load_teams_stats.clear()
    load_chile_stats.clear()

def get_stats_from_json(nombre, teams_data):
    equipo = teams_data.get("equipos", {}).get(nombre)
    if not equipo or not equipo.get("ultimos_5"):
        return None
    partidos = equipo["ultimos_5"]
    gf_list = [p["gf"] for p in partidos]
    gc_list = [p["gc"] for p in partidos]
    corners_list = [p.get("corners", 8) for p in partidos]
    tarjetas_list = [p.get("tarjetas", 3) for p in partidos]
    resultados = [p["resultado"] for p in partidos]
    puntos = [3 if r == "W" else (1 if r == "D" else 0) for r in resultados]
    avg_gf = sum(gf_list) / len(gf_list)
    avg_gc = sum(gc_list) / len(gc_list)
    avg_pts = sum(puntos) / len(puntos)
    avg_corners = sum(corners_list) / len(corners_list)
    avg_tarjetas = sum(tarjetas_list) / len(tarjetas_list)
    return {
        "ataque":  max(0.5, min(3.5, round(avg_gf * 0.85 + 0.3, 2))),
        "defensa": max(0.5, min(3.5, round(avg_gc * 0.75 + 0.4, 2))),
        "xg":      max(0.5, min(3.5, round(avg_gf * 0.80 + 0.25, 2))),
        "forma":   max(0.8, min(1.2, round(0.8 + (avg_pts / 3.0) * 0.4, 2))),
        "avg_gf": round(avg_gf, 2), "avg_gc": round(avg_gc, 2),
        "avg_corners": round(avg_corners, 1), "avg_tarjetas": round(avg_tarjetas, 1),
        "partidos": partidos, "resultados": resultados,
    }

# ══════════════════════════════════════════════════════════════
# SUPABASE HELPERS
# ══════════════════════════════════════════════════════════════

def get_equipos():
    return sb_get("equipos", {"select": "*", "order": "nombre.asc"})

def get_todos_partidos(fase=None):
    data = sb_get("partidos_ucl", {"select": "*", "order": "fecha.desc", "limit": "80"})
    if fase and fase != "Todos":
        data = [p for p in data if p.get("fase") == fase]
    return data

def guardar_simulacion(datos):
    sb_post("simulaciones", datos)

def get_historial_sims():
    return sb_get("simulaciones", {"select": "*", "order": "created_at.desc", "limit": "20"})

def get_bankroll():
    data = sb_get("bankroll", {"select": "*", "order": "id.asc", "limit": "1"})
    return data[0] if data else {"id": None, "saldo_actual": 1000.0, "saldo_inicial": 1000.0}

def update_bankroll(id_bank, nuevo_saldo):
    return sb_patch("bankroll", "id", id_bank, {"saldo_actual": nuevo_saldo, "updated_at": datetime.now().isoformat()})

def get_apuestas():
    return sb_get("apuestas", {"select": "*", "order": "created_at.desc", "limit": "50"})

def crear_apuesta(datos):
    return sb_post("apuestas", datos)

def resolver_apuesta(apuesta_id, resultado, saldo_actual, monto, cuota):
    ganancia = round(monto * cuota - monto, 2) if resultado == "ganada" else -monto
    nuevo_saldo = round(saldo_actual + ganancia, 2)
    sb_patch("apuestas", "id", apuesta_id, {"resultado": resultado, "ganancia": ganancia})
    return nuevo_saldo, ganancia

def guardar_prediccion(datos):
    return sb_post("predicciones", datos)

def get_predicciones():
    return sb_get("predicciones", {"select": "*", "order": "created_at.desc", "limit": "50"})

def resolver_prediccion(pred_id, resultado_real, valor_predicho):
    acerto = resultado_real.strip().lower() == valor_predicho.strip().lower()
    sb_patch("predicciones", "id", pred_id, {"resultado_real": resultado_real, "acerto": acerto})
    return acerto

# ══════════════════════════════════════════════════════════════
# MODELO MATEMÁTICO (compartido UCL + Chile)
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

def calcular_corners_prob(avg, n=50000):
    return np.sum(np.random.default_rng(123).poisson(avg, n) > 9.5) / n * 100

def calcular_tarjetas_prob(avg, n=50000):
    return np.sum(np.random.default_rng(456).poisson(avg, n) > 3.5) / n * 100

def top_marcadores(gl, gv, top=5):
    n = len(gl)
    conteo = {}
    for g_l, g_v in zip(gl.tolist(), gv.tolist()):
        k = (int(g_l), int(g_v))
        conteo[k] = conteo.get(k, 0) + 1
    return [(f"{g_l}-{g_v}", cnt / n * 100)
            for (g_l, g_v), cnt in sorted(conteo.items(), key=lambda x: x[1], reverse=True)[:top]]

def calcular_confianza(probs, lam_l, lam_v):
    max_p = max(probs["victoria_local"], probs["empate"], probs["victoria_visitante"])
    return min(95, round((max_p * 0.6) + (abs(lam_l - lam_v) * 10), 1))

def detectar_valor(prob_real, cuota):
    prob_imp = (1 / cuota) * 100
    val = round(prob_real - prob_imp, 1)
    return val, val > 5

def pick_del_dia(probs, over_c, over_t, nl, nv):
    candidatos = [
        (f"🏠 Gana {nl}", probs["victoria_local"], "1X2"),
        (f"✈️ Gana {nv}", probs["victoria_visitante"], "1X2"),
        ("⚽ Over 2.5", probs["over_25"], "Goles"),
        ("🎯 BTTS Sí", probs["btts"], "BTTS"),
        ("🚩 Córners +9.5", over_c, "Córners"),
        ("🟨 Tarjetas +3.5", over_t, "Tarjetas"),
    ]
    return max(candidatos, key=lambda x: x[1])

# ══════════════════════════════════════════════════════════════
# HELPER UI: RENDERIZAR RESULTADOS DE SIMULACIÓN
# ══════════════════════════════════════════════════════════════

def render_resultados_simulacion(probs, over_c, over_t, top5, lam_l, lam_v, nl, nv, confianza, db_ok, partido_str):
    # Confianza
    conf_color = "#3ecf8e" if confianza >= 70 else ("#d4a843" if confianza >= 50 else "#e05c5c")
    st.markdown(f"""
    <div style="background:#1C1F26;border:1px solid #252a35;border-radius:10px;padding:0.9rem 1.2rem;
    margin:0.8rem 0;display:flex;justify-content:space-between;align-items:center">
        <span style="font-size:0.75rem;color:#5a7a8a;text-transform:uppercase;letter-spacing:2px">🎯 Nivel de Confianza</span>
        <div style="display:flex;align-items:center;gap:0.8rem">
            <div style="width:160px;background:#1e2535;border-radius:6px;height:7px;overflow:hidden">
                <div style="width:{confianza}%;height:100%;background:{conf_color};border-radius:6px"></div>
            </div>
            <span style="font-family:'Bebas Neue',cursive;font-size:1.6rem;color:{conf_color}">{confianza}%</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # 1X2
    st.markdown('<div class="section-title">📊 PROBABILIDADES</div>', unsafe_allow_html=True)
    vl, emp, vv = probs["victoria_local"], probs["empate"], probs["victoria_visitante"]
    r1, r2, r3 = st.columns(3)
    for col, label, val in [(r1, f"🏠 {nl[:14]}", vl), (r2, "🤝 Empate", emp), (r3, f"✈️ {nv[:14]}", vv)]:
        c = "green" if val >= 55 else ("yellow" if val >= 40 else "red")
        col.markdown(f'<div class="metric-box"><div class="metric-label">{label}</div><div class="metric-value {c}">{val:.1f}%</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    o25, btts = probs["over_25"], probs["btts"]
    m1, m2, m3, m4 = st.columns(4)
    for col, label, val in zip([m1, m2, m3, m4],
        ["⚽ Over 2.5", "🎯 BTTS", "🚩 Córners +9.5", "🟨 Tarjetas +3.5"],
        [o25, btts, over_c, over_t]):
        c = "green" if val >= 60 else ("yellow" if val >= 45 else "blue")
        col.markdown(f'<div class="metric-box"><div class="metric-label">{label}</div><div class="metric-value {c}">{val:.1f}%</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    x1, x2 = st.columns(2)
    x1.markdown(f'<div class="metric-box"><div class="metric-label">λ {nl[:14]}</div><div class="metric-value green">{lam_l:.2f}</div></div>', unsafe_allow_html=True)
    x2.markdown(f'<div class="metric-box"><div class="metric-label">λ {nv[:14]}</div><div class="metric-value blue">{lam_v:.2f}</div></div>', unsafe_allow_html=True)

    # PICK
    pick_label, pick_prob, pick_tipo = pick_del_dia(probs, over_c, over_t, nl, nv)
    st.markdown(f"""
    <div class="pick-box">
        <div class="pick-title">⭐ PICK DEL DÍA</div>
        <div class="pick-value">{pick_label}</div>
        <div style="font-family:'Bebas Neue',cursive;font-size:2rem;color:#d4a843">{pick_prob:.1f}%</div>
        <div style="font-size:0.72rem;color:#5a7a8a;margin-top:0.2rem">Tipo: {pick_tipo} · Confianza: {confianza}%</div>
    </div>""", unsafe_allow_html=True)

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
                <span style="font-size:1.1rem">{iconos[i]}</span>
                <span class="score-text">{nl[:11]} {g_l}–{g_v} {nv[:11]}</span>
                <span class="score-pct">{pct:.1f}%</span>
            </div>""", unsafe_allow_html=True)
    with sc2:
        df_s = pd.DataFrame({"Marcador": [m for m, _ in top5], "Prob (%)": [p for _, p in top5]})
        st.bar_chart(df_s.set_index("Marcador"), color="#3ecf8e", height=200)

    # APUESTAS CON VALOR
    cuotas_est = {
        f"🏠 {nl}": max(1.1, round(100/max(1, vl), 2)),
        "🤝 Empate": max(1.1, round(100/max(1, emp), 2)),
        f"✈️ {nv}": max(1.1, round(100/max(1, vv), 2)),
        "⚽ Over 2.5": max(1.1, round(100/max(1, o25), 2)),
        "🎯 BTTS": max(1.1, round(100/max(1, btts), 2)),
    }
    valores = [(l, p, c) for (l, c), p in zip(cuotas_est.items(), [vl, emp, vv, o25, btts]) if detectar_valor(p, c)[1]]
    if valores:
        st.markdown('<div class="section-title">💎 VALOR DETECTADO</div>', unsafe_allow_html=True)
        v1, v2 = st.columns(2)
        for i, (label, prob, cuota) in enumerate(valores):
            val_num, _ = detectar_valor(prob, cuota)
            col = v1 if i % 2 == 0 else v2
            col.markdown(f"""
            <div class="valor-bet">
                <span>{label}</span>
                <span style="color:#5a7a8a">{prob:.1f}% · cuota {cuota}</span>
                <span class="badge badge-green">+{val_num}%</span>
            </div>""", unsafe_allow_html=True)

    # APUESTAS SUGERIDAS
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💰 APUESTAS SUGERIDAS</div>', unsafe_allow_html=True)
    apuestas_lista = [
        (f"🏠 Gana {nl}", vl), (f"✈️ Gana {nv}", vv),
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
        st.markdown('<div style="font-size:0.7rem;color:#3a5060;margin-top:0.4rem">🟢 ≥70% · 🟡 60–69%</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background:#1C1F26;border:1px solid #252a35;border-radius:8px;padding:0.8rem;color:#5a7a8a;font-size:0.83rem">⚠️ Ninguna apuesta supera el 60% en este escenario.</div>', unsafe_allow_html=True)

    # GUARDAR PREDICCIÓN
    if db_ok:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        with st.expander("💾 Guardar predicción para seguimiento"):
            pred_tipo = st.selectbox("Tipo", ["1X2 - Local", "1X2 - Empate", "1X2 - Visitante", "Over 2.5", "BTTS Sí", "Córners Over 9.5", "Tarjetas Over 3.5"], key=f"pred_tipo_{partido_str}")
            pred_vals = {"1X2 - Local": (vl,"Local"), "1X2 - Empate": (emp,"Empate"), "1X2 - Visitante": (vv,"Visitante"),
                        "Over 2.5": (o25,"Over"), "BTTS Sí": (btts,"Si"), "Córners Over 9.5": (over_c,"Over"), "Tarjetas Over 3.5": (over_t,"Over")}
            prob_p, val_p = pred_vals[pred_tipo]
            fecha_p = st.date_input("Fecha del partido", value=date.today(), key=f"fecha_p_{partido_str}")
            if st.button("💾 Guardar", key=f"save_pred_{partido_str}", use_container_width=True):
                guardar_prediccion({"partido": partido_str, "tipo_prediccion": pred_tipo, "valor_predicho": val_p, "probabilidad": round(prob_p, 2), "fecha_partido": str(fecha_p)})
                st.success("✅ Predicción guardada")

# ══════════════════════════════════════════════════════════════
# INICIALIZACIÓN
# ══════════════════════════════════════════════════════════════

teams_data  = load_teams_stats()
chile_data  = load_chile_stats()

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
# SIDEBAR
# ══════════════════════════════════════════════════════════════

st.sidebar.markdown("""
<div style="text-align:center;padding:0.8rem 0;border-bottom:1px solid #1e2535;margin-bottom:0.8rem">
    <div style="font-family:'Bebas Neue',cursive;font-size:1.6rem;letter-spacing:4px;color:#3ecf8e">⚽ PREDICTOR</div>
    <div style="font-size:0.65rem;color:#3a5060;letter-spacing:2px">UCL 25/26 + LIGA CHILENA</div>
</div>
""", unsafe_allow_html=True)

pagina = st.sidebar.radio("Navegación", [
    "🏆 UCL — Simulador",
    "🇨🇱 Liga Chilena",
    "💰 Bankroll",
    "🧠 Aprendizaje",
    "📋 Partidos UCL",
    "📊 Historial",
], label_visibility="collapsed")

st.sidebar.markdown('<div style="height:1px;background:#1e2535;margin:0.8rem 0"></div>', unsafe_allow_html=True)

# Info JSONs
col_s1, col_s2 = st.sidebar.columns(2)
with col_s1:
    st.markdown(f"""<div style="background:#13161e;border:1px solid #1e2535;border-radius:6px;padding:0.5rem;font-size:0.68rem;color:#5a7a8a;text-align:center">
    🏆 UCL<br><span style="color:#3ecf8e">{len(teams_data.get('equipos',{}))} equipos</span></div>""", unsafe_allow_html=True)
with col_s2:
    st.markdown(f"""<div style="background:#13161e;border:1px solid #1e2535;border-radius:6px;padding:0.5rem;font-size:0.68rem;color:#5a7a8a;text-align:center">
    🇨🇱 Chile<br><span style="color:#e05c5c">{len(chile_data.get('equipos',{}))} equipos</span></div>""", unsafe_allow_html=True)

if st.sidebar.button("🔄 Actualizar Datos", use_container_width=True):
    update_data()
    st.rerun()

st.sidebar.markdown('<div style="height:1px;background:#1e2535;margin:0.8rem 0"></div>', unsafe_allow_html=True)

if db_ok:
    bankroll_data = get_bankroll()
    saldo = bankroll_data.get("saldo_actual", 1000)
    inicial = bankroll_data.get("saldo_inicial", 1000)
    gan = round(saldo - inicial, 2)
    color_g = "#3ecf8e" if gan >= 0 else "#e05c5c"
    st.sidebar.markdown(f"""
    <div style="background:#1C1F26;border:1px solid rgba(62,207,142,0.2);border-radius:8px;padding:0.7rem;text-align:center">
        <div style="font-size:0.6rem;color:#5a7a8a;text-transform:uppercase;letter-spacing:2px">Bankroll</div>
        <div style="font-family:'Bebas Neue',cursive;font-size:1.8rem;color:#3ecf8e">${saldo:,.2f}</div>
        <div style="font-size:0.7rem;color:{color_g}">{'+'if gan>=0 else ''}${gan:,.2f}</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════

st.markdown("""
<div class="main-header">
    <h1>⚽ PREDICTOR</h1>
    <p>UCL 25/26 · Liga Chilena · Monte Carlo 50K · Bankroll · Aprendizaje</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PÁGINA: UCL SIMULADOR
# ══════════════════════════════════════════════════════════════

if pagina == "🏆 UCL — Simulador":

    st.markdown('<div class="section-title">🏟️ SELECCIÓN DE EQUIPOS — UCL</div>', unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([5, 1, 5])
    lista_ucl = nombres_equipos if nombres_equipos else list(teams_data.get("equipos", {}).keys())

    with col_l:
        st.markdown("**🏠 Local**")
        idx_l = lista_ucl.index("Real Madrid") if "Real Madrid" in lista_ucl else 0
        sel_local = st.selectbox("Local", lista_ucl, index=idx_l, key="ucl_local")
        nombre_local = sel_local
        stats_l = get_stats_from_json(nombre_local, teams_data)
        eq_l = equipos_dict.get(nombre_local, {})
        if stats_l:
            def_atk_l, def_def_l, def_xg_l, def_forma_l = stats_l["ataque"], stats_l["defensa"], stats_l["xg"], stats_l["forma"]
            forma_str = " ".join([f'<span class="forma-{"w" if r=="W" else ("d" if r=="D" else "l")}">{r}</span>' for r in stats_l["resultados"]])
            st.markdown(f"""<div class="stats-box">
                ⚽ {stats_l['avg_gf']} gf/p &nbsp;·&nbsp; 🛡️ {stats_l['avg_gc']} gc/p &nbsp;·&nbsp;
                🚩 {stats_l['avg_corners']} córn/p &nbsp;·&nbsp; 🟨 {stats_l['avg_tarjetas']} tarj/p<br>
                Forma: {forma_str}</div>""", unsafe_allow_html=True)
        else:
            def_atk_l, def_def_l, def_xg_l, def_forma_l = float(eq_l.get("ataque",1.8)), float(eq_l.get("defensa",1.3)), float(eq_l.get("xg_promedio",1.6)), float(eq_l.get("forma",1.05))
        c1, c2 = st.columns(2)
        with c1:
            ataque_local  = st.slider("⚔️ Ataque",  0.5, 3.5, def_atk_l,   0.05, key="ucl_atk_l")
            xg_local      = st.slider("🎯 xG",      0.5, 3.5, def_xg_l,    0.05, key="ucl_xg_l")
            forma_local   = st.slider("📈 Forma",   0.8, 1.2, def_forma_l, 0.01, key="ucl_forma_l")
        with c2:
            defensa_local = st.slider("🛡️ Defensa", 0.5, 3.5, def_def_l,   0.05, key="ucl_def_l")

    with col_m:
        st.markdown('<div style="text-align:center;font-family:\'Bebas Neue\',cursive;font-size:1.6rem;color:#1e2535;letter-spacing:3px;margin-top:5rem">VS</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown("**✈️ Visitante**")
        idx_v = lista_ucl.index("Arsenal") if "Arsenal" in lista_ucl else 1
        sel_away = st.selectbox("Visitante", lista_ucl, index=idx_v, key="ucl_away")
        nombre_visitante = sel_away
        stats_v = get_stats_from_json(nombre_visitante, teams_data)
        eq_v = equipos_dict.get(nombre_visitante, {})
        if stats_v:
            def_atk_v, def_def_v, def_xg_v, def_forma_v = stats_v["ataque"], stats_v["defensa"], stats_v["xg"], stats_v["forma"]
            forma_str_v = " ".join([f'<span class="forma-{"w" if r=="W" else ("d" if r=="D" else "l")}">{r}</span>' for r in stats_v["resultados"]])
            st.markdown(f"""<div class="stats-box">
                ⚽ {stats_v['avg_gf']} gf/p &nbsp;·&nbsp; 🛡️ {stats_v['avg_gc']} gc/p &nbsp;·&nbsp;
                🚩 {stats_v['avg_corners']} córn/p &nbsp;·&nbsp; 🟨 {stats_v['avg_tarjetas']} tarj/p<br>
                Forma: {forma_str_v}</div>""", unsafe_allow_html=True)
        else:
            def_atk_v, def_def_v, def_xg_v, def_forma_v = float(eq_v.get("ataque",1.7)), float(eq_v.get("defensa",1.4)), float(eq_v.get("xg_promedio",1.5)), float(eq_v.get("forma",1.0))
        c3, c4 = st.columns(2)
        with c3:
            ataque_visit  = st.slider("⚔️ Ataque",  0.5, 3.5, def_atk_v,   0.05, key="ucl_atk_v")
            xg_visit      = st.slider("🎯 xG",      0.5, 3.5, def_xg_v,    0.05, key="ucl_xg_v")
            forma_visit   = st.slider("📈 Forma",   0.8, 1.2, def_forma_v, 0.01, key="ucl_forma_v")
        with c4:
            defensa_visit = st.slider("🛡️ Defensa", 0.5, 3.5, def_def_v,   0.05, key="ucl_def_v")

    # Últimos 5 partidos
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📅 ÚLTIMOS 5 PARTIDOS UCL</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    res_map = {"W": "✅", "D": "🟡", "L": "❌"}
    for col, nombre, stats in [(p1, nombre_local, stats_l), (p2, nombre_visitante, stats_v)]:
        with col:
            st.markdown(f"**{nombre}**")
            if stats and stats.get("partidos"):
                for p in stats["partidos"]:
                    st.markdown(f"""<div class="partido-row">
                        <span style="color:#3a5060;font-size:0.7rem">{p['fecha']}</span>
                        <span>vs <b>{p['rival'][:14]}</b></span>
                        <span style="font-family:'Bebas Neue',cursive;font-size:1rem;letter-spacing:2px">{p['gf']} – {p['gc']}</span>
                        <span>{res_map.get(p['resultado'],'?')} 🚩{p.get('corners','?')}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("Sin datos.")

    # Contexto
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚙️ CONTEXTO</div>', unsafe_allow_html=True)
    cp1, cp2, cp3, cp4, cp5 = st.columns([3, 3, 3, 3, 2])
    with cp1: intensidad    = st.slider("🏆 Intensidad", 0.90, 1.20, 1.05, 0.01, key="ucl_int")
    with cp2: avg_corners_s = st.slider("🚩 Córners prom.", 6, 14, int(((stats_l["avg_corners"] if stats_l else 9) + (stats_v["avg_corners"] if stats_v else 9)) / 2), 1, key="ucl_corn")
    with cp3: avg_tarj_s    = st.slider("🟨 Tarjetas prom.", 2, 7, int(((stats_l["avg_tarjetas"] if stats_l else 3) + (stats_v["avg_tarjetas"] if stats_v else 3)) / 2), 1, key="ucl_tarj")
    with cp4: factor_reg    = st.slider("📉 Regresión", 0.88, 0.98, 0.93, 0.01, key="ucl_reg")
    with cp5: ventaja_local = st.checkbox("🏟️ Ventaja local", value=True, key="ucl_vtj")

    with st.expander("🔬 Modo Avanzado"):
        a1, a2, a3 = st.columns(3)
        lam_l_prev = calcular_lambda(ataque_local, defensa_visit, xg_local, forma_local, ventaja_local, intensidad, factor_reg)
        lam_v_prev = calcular_lambda(ataque_visit, defensa_local, xg_visit, forma_visit, False, intensidad, factor_reg)
        a1.markdown(f"**λ Local:** `{lam_l_prev:.3f}`")
        a2.markdown(f"**λ Visitante:** `{lam_v_prev:.3f}`")
        a3.markdown(f"**Ratio A/D:** `{ataque_local/max(0.1,defensa_visit):.3f}`")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    simular_ucl = st.button("🎲 SIMULAR PARTIDO UCL", use_container_width=True, key="btn_ucl")

    if simular_ucl:
        with st.spinner("Simulando 50,000 iteraciones..."):
            lam_l = calcular_lambda(ataque_local, defensa_visit, xg_local, forma_local, ventaja_local, intensidad, factor_reg)
            lam_v = calcular_lambda(ataque_visit, defensa_local, xg_visit, forma_visit, False, intensidad, factor_reg)
            gl, gv = simular_partido(lam_l, lam_v)
            probs  = calcular_probabilidades(gl, gv)
            over_c = calcular_corners_prob(avg_corners_s)
            over_t = calcular_tarjetas_prob(avg_tarj_s)
            top5   = top_marcadores(gl, gv)
            conf   = calcular_confianza(probs, lam_l, lam_v)

        if db_ok:
            guardar_simulacion({"equipo_local": nombre_local, "equipo_visitante": nombre_visitante,
                "prob_victoria_local": round(probs["victoria_local"],2), "prob_empate": round(probs["empate"],2),
                "prob_victoria_visitante": round(probs["victoria_visitante"],2), "prob_over25": round(probs["over_25"],2),
                "prob_btts": round(probs["btts"],2), "prob_corners_over95": round(over_c,2),
                "prob_tarjetas_over35": round(over_t,2), "lambda_local": round(lam_l,3),
                "lambda_visitante": round(lam_v,3), "marcador_probable": top5[0][0] if top5 else "N/A"})
            st.markdown('<span class="badge badge-green">✅ GUARDADO EN BD</span>', unsafe_allow_html=True)

        render_resultados_simulacion(probs, over_c, over_t, top5, lam_l, lam_v,
                                     nombre_local, nombre_visitante, conf, db_ok,
                                     f"{nombre_local} vs {nombre_visitante}")

# ══════════════════════════════════════════════════════════════
# PÁGINA: LIGA CHILENA
# ══════════════════════════════════════════════════════════════

elif pagina == "🇨🇱 Liga Chilena":

    st.markdown('<div class="section-title-chile">🇨🇱 LIGA CHILENA 2026</div>', unsafe_allow_html=True)

    jornada_info = chile_data.get("jornada_actual", "?")
    liga_nombre  = chile_data.get("liga", "Primera División Chile")
    fecha_act    = chile_data.get("ultima_actualizacion", "—")

    i1, i2, i3 = st.columns(3)
    i1.markdown(f'<div class="metric-box"><div class="metric-label">🏆 Liga</div><div style="font-size:0.9rem;font-weight:600;color:#e05c5c;margin-top:0.3rem">{liga_nombre}</div></div>', unsafe_allow_html=True)
    i2.markdown(f'<div class="metric-box"><div class="metric-label">📅 Jornada Actual</div><div class="metric-value red">{jornada_info}</div></div>', unsafe_allow_html=True)
    i3.markdown(f'<div class="metric-box"><div class="metric-label">🔄 Actualizado</div><div style="font-size:0.9rem;font-weight:600;color:#d4a843;margin-top:0.3rem">{fecha_act}</div></div>', unsafe_allow_html=True)

    # PRÓXIMOS PARTIDOS
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title-chile">📅 PRÓXIMOS PARTIDOS — JORNADA 9</div>', unsafe_allow_html=True)

    proximos = chile_data.get("proximos_partidos", [])
    if not proximos:
        st.info("No hay partidos cargados. Actualiza chile_stats.json")
    else:
        opciones_partidos = [f"{p['local']} vs {p['visitante']} — {p['fecha']} {p['hora']}" for p in proximos]
        partido_sel_idx = st.selectbox("Selecciona un partido para analizar", range(len(opciones_partidos)),
                                       format_func=lambda i: opciones_partidos[i], key="chile_partido_sel")
        partido_sel = proximos[partido_sel_idx]

        # Mostrar todos los partidos de la jornada
        st.markdown("**Todos los partidos de la jornada:**")
        for i, p in enumerate(proximos):
            activo = "selected" if i == partido_sel_idx else ""
            st.markdown(f"""
            <div class="partido-card {activo}">
                <div class="partido-equipos">
                    <span>{p['local']}</span>
                    <span class="vs-text">VS</span>
                    <span>{p['visitante']}</span>
                </div>
                <div class="partido-meta">📅 {p['fecha']} &nbsp;·&nbsp; ⏰ {p['hora']} &nbsp;·&nbsp; 🏟️ {p['estadio']}</div>
            </div>""", unsafe_allow_html=True)

    if proximos:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        nombre_local_ch  = partido_sel["local"]
        nombre_visit_ch  = partido_sel["visitante"]
        estadio_ch       = partido_sel["estadio"]

        st.markdown(f'<div class="section-title-chile">📊 ANÁLISIS: {nombre_local_ch.upper()} VS {nombre_visit_ch.upper()}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.75rem;color:#5a7a8a;margin-bottom:1rem">🏟️ {estadio_ch} &nbsp;·&nbsp; 📅 {partido_sel["fecha"]} {partido_sel["hora"]}</div>', unsafe_allow_html=True)

        stats_cl = get_stats_from_json(nombre_local_ch, chile_data)
        stats_cv = get_stats_from_json(nombre_visit_ch, chile_data)

        # STATS COMPARATIVAS
        sc1, sc2 = st.columns(2)
        for col, nombre, stats, color in [(sc1, nombre_local_ch, stats_cl, "#3ecf8e"), (sc2, nombre_visit_ch, stats_cv, "#5ab4d6")]:
            with col:
                st.markdown(f"**🏠 {nombre}**" if col == sc1 else f"**✈️ {nombre}**")
                if stats:
                    forma_str = " ".join([f'<span class="forma-{"w" if r=="W" else ("d" if r=="D" else "l")}">{r}</span>' for r in stats["resultados"]])
                    st.markdown(f"""<div class="stats-box">
                        ⚽ <b>{stats['avg_gf']}</b> goles/p &nbsp;·&nbsp; 🛡️ <b>{stats['avg_gc']}</b> recibidos/p<br>
                        🚩 <b>{stats['avg_corners']}</b> córners/p &nbsp;·&nbsp; 🟨 <b>{stats['avg_tarjetas']}</b> tarjetas/p<br>
                        Forma: {forma_str}
                    </div>""", unsafe_allow_html=True)

                    st.markdown("**Últimos 5 partidos:**")
                    for p in stats["partidos"]:
                        st.markdown(f"""<div class="partido-row">
                            <span style="color:#3a5060;font-size:0.7rem">{p['fecha']}</span>
                            <span>vs <b>{p['rival'][:14]}</b></span>
                            <span style="font-family:'Bebas Neue',cursive;font-size:1rem;letter-spacing:2px">{p['gf']} – {p['gc']}</span>
                            <span>{res_map.get(p['resultado'],'?')} 🚩{p.get('corners','?')} 🟨{p.get('tarjetas','?')}</span>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.warning(f"Sin datos para {nombre}")

        # PARÁMETROS
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title-chile">⚙️ PARÁMETROS</div>', unsafe_allow_html=True)

        def_atk_cl   = stats_cl["ataque"]   if stats_cl else 1.5
        def_def_cl   = stats_cl["defensa"]  if stats_cl else 1.4
        def_xg_cl    = stats_cl["xg"]       if stats_cl else 1.3
        def_forma_cl = stats_cl["forma"]    if stats_cl else 1.0
        def_atk_cv   = stats_cv["ataque"]   if stats_cv else 1.4
        def_def_cv   = stats_cv["defensa"]  if stats_cv else 1.4
        def_xg_cv    = stats_cv["xg"]       if stats_cv else 1.2
        def_forma_cv = stats_cv["forma"]    if stats_cv else 1.0
        avg_corn_ch  = round(((stats_cl["avg_corners"] if stats_cl else 7) + (stats_cv["avg_corners"] if stats_cv else 7)) / 2)
        avg_tarj_ch  = round(((stats_cl["avg_tarjetas"] if stats_cl else 3) + (stats_cv["avg_tarjetas"] if stats_cv else 3)) / 2)

        pa1, pa2 = st.columns(2)
        with pa1:
            st.markdown(f"**🏠 {nombre_local_ch}**")
            atk_cl   = st.slider("⚔️ Ataque",  0.5, 3.5, def_atk_cl,   0.05, key="ch_atk_l")
            def_l_ch = st.slider("🛡️ Defensa", 0.5, 3.5, def_def_cl,   0.05, key="ch_def_l")
            xg_cl    = st.slider("🎯 xG",      0.5, 3.5, def_xg_cl,    0.05, key="ch_xg_l")
            forma_cl = st.slider("📈 Forma",   0.8, 1.2, def_forma_cl, 0.01, key="ch_forma_l")
        with pa2:
            st.markdown(f"**✈️ {nombre_visit_ch}**")
            atk_cv   = st.slider("⚔️ Ataque",  0.5, 3.5, def_atk_cv,   0.05, key="ch_atk_v")
            def_v_ch = st.slider("🛡️ Defensa", 0.5, 3.5, def_def_cv,   0.05, key="ch_def_v")
            xg_cv    = st.slider("🎯 xG",      0.5, 3.5, def_xg_cv,    0.05, key="ch_xg_v")
            forma_cv = st.slider("📈 Forma",   0.8, 1.2, def_forma_cv, 0.01, key="ch_forma_v")

        ch1, ch2, ch3 = st.columns(3)
        with ch1: vtj_ch  = st.checkbox("🏟️ Ventaja local", value=True, key="ch_vtj")
        with ch2: corn_ch = st.slider("🚩 Córners prom.", 4, 12, avg_corn_ch, 1, key="ch_corn")
        with ch3: tarj_ch = st.slider("🟨 Tarjetas prom.", 2, 7, avg_tarj_ch, 1, key="ch_tarj")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        simular_ch = st.button(f"🎲 SIMULAR {nombre_local_ch.upper()} VS {nombre_visit_ch.upper()}", use_container_width=True, key="btn_chile")

        if simular_ch:
            with st.spinner("Simulando 50,000 iteraciones..."):
                lam_l_ch = calcular_lambda(atk_cl, def_v_ch, xg_cl, forma_cl, vtj_ch, 1.0, 0.93)
                lam_v_ch = calcular_lambda(atk_cv, def_l_ch, xg_cv, forma_cv, False, 1.0, 0.93)
                gl_ch, gv_ch = simular_partido(lam_l_ch, lam_v_ch)
                probs_ch  = calcular_probabilidades(gl_ch, gv_ch)
                over_c_ch = calcular_corners_prob(corn_ch)
                over_t_ch = calcular_tarjetas_prob(tarj_ch)
                top5_ch   = top_marcadores(gl_ch, gv_ch)
                conf_ch   = calcular_confianza(probs_ch, lam_l_ch, lam_v_ch)

            render_resultados_simulacion(probs_ch, over_c_ch, over_t_ch, top5_ch,
                                        lam_l_ch, lam_v_ch, nombre_local_ch, nombre_visit_ch,
                                        conf_ch, db_ok, f"{nombre_local_ch} vs {nombre_visit_ch}")

# ══════════════════════════════════════════════════════════════
# PÁGINA: BANKROLL
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

        b1, b2, b3 = st.columns(3)
        with b1:
            st.markdown(f'<div class="saldo-box"><div class="saldo-label">Saldo Actual</div><div class="saldo-value">${saldo_actual:,.2f}</div></div>', unsafe_allow_html=True)
        with b2:
            color_g = "#3ecf8e" if ganancia_total >= 0 else "#e05c5c"
            st.markdown(f'<div class="saldo-box" style="border-color:rgba({("62,207,142" if ganancia_total>=0 else "224,92,92")},0.3)"><div class="saldo-label">Ganancia/Pérdida</div><div class="saldo-value" style="color:{color_g}">{"+" if ganancia_total>=0 else ""}${ganancia_total:,.2f}</div></div>', unsafe_allow_html=True)
        with b3:
            roi = round((ganancia_total / saldo_inicial) * 100, 1) if saldo_inicial > 0 else 0
            color_roi = "#3ecf8e" if roi >= 0 else "#e05c5c"
            st.markdown(f'<div class="saldo-box" style="border-color:rgba(90,180,214,0.3)"><div class="saldo-label">ROI</div><div class="saldo-value" style="color:{color_roi}">{roi:+.1f}%</div></div>', unsafe_allow_html=True)

        with st.expander("⚙️ Ajustar Saldo Inicial"):
            nuevo_inicial = st.number_input("Nuevo saldo ($)", min_value=100.0, value=float(saldo_inicial), step=50.0)
            if st.button("💾 Actualizar"):
                if bank_id:
                    sb_patch("bankroll", "id", bank_id, {"saldo_inicial": nuevo_inicial, "saldo_actual": nuevo_inicial})
                    st.success("✅ Actualizado"); st.rerun()

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📝 NUEVA APUESTA</div>', unsafe_allow_html=True)
        ra1, ra2 = st.columns(2)
        with ra1:
            partido_ap = st.text_input("⚽ Partido", placeholder="ej: Colo-Colo vs Universidad de Chile")
            tipo_ap = st.selectbox("📋 Tipo", ["1X2 - Gana Local","1X2 - Empate","1X2 - Gana Visitante","Over 2.5","Under 2.5","BTTS Sí","BTTS No","Córners Over 9.5","Tarjetas Over 3.5","Otro"])
            notas_ap = st.text_input("📝 Notas")
        with ra2:
            cuota_ap = st.number_input("💱 Cuota", min_value=1.01, value=1.80, step=0.05)
            monto_ap = st.number_input("💵 Monto ($)", min_value=1.0, value=round(saldo_actual * 0.05, 2), step=5.0)
            gan_pot = round(monto_ap * cuota_ap - monto_ap, 2)
            st.markdown(f"""<div style="background:#1C1F26;border:1px solid #252a35;border-radius:8px;padding:0.8rem;text-align:center;margin-top:0.5rem">
                <div style="font-size:0.65rem;color:#5a7a8a;text-transform:uppercase">Ganancia potencial</div>
                <div style="font-family:'Bebas Neue',cursive;font-size:1.8rem;color:#3ecf8e">+${gan_pot:,.2f}</div>
                <div style="font-size:0.7rem;color:#3a5060">{round((monto_ap/saldo_actual)*100,1)}% del bankroll</div>
            </div>""", unsafe_allow_html=True)

        if st.button("💰 Registrar Apuesta", use_container_width=True):
            if partido_ap:
                crear_apuesta({"partido": partido_ap, "tipo_apuesta": tipo_ap, "cuota": cuota_ap, "monto": monto_ap, "resultado": "pendiente", "ganancia": 0, "notas": notas_ap})
                st.success("✅ Registrada"); st.rerun()
            else:
                st.error("⚠️ Escribe el partido")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📋 APUESTAS</div>', unsafe_allow_html=True)
        apuestas = get_apuestas()
        if apuestas:
            pendientes = [a for a in apuestas if a.get("resultado") == "pendiente"]
            if pendientes:
                st.markdown("**⏳ Pendientes**")
                for ap in pendientes:
                    c1, c2, c3 = st.columns([4, 2, 2])
                    with c1:
                        st.markdown(f"**{ap['partido']}** — {ap['tipo_apuesta']}")
                        st.caption(f"Cuota: {ap['cuota']} · ${ap['monto']}")
                    with c2:
                        res_sel = st.selectbox("", ["pendiente","ganada","perdida"], key=f"res_{ap['id']}", label_visibility="collapsed")
                    with c3:
                        if st.button("✔️ Resolver", key=f"btn_{ap['id']}", use_container_width=True):
                            if res_sel != "pendiente":
                                ns, g = resolver_apuesta(ap["id"], res_sel, saldo_actual, ap["monto"], ap["cuota"])
                                if bank_id: update_bankroll(bank_id, ns)
                                st.success(f"{'✅' if res_sel=='ganada' else '❌'} {'+'if g>0 else ''}${g}"); st.rerun()

            df_ap = pd.DataFrame(apuestas)
            if not df_ap.empty:
                cols_ap = ["created_at","partido","tipo_apuesta","cuota","monto","resultado","ganancia"]
                df_s = df_ap[[c for c in cols_ap if c in df_ap.columns]].copy()
                df_s.columns = ["Fecha","Partido","Tipo","Cuota","Monto","Resultado","Ganancia"][:len(df_s.columns)]
                if "Fecha" in df_s.columns: df_s["Fecha"] = pd.to_datetime(df_s["Fecha"]).dt.strftime("%d/%m %H:%M")
                st.dataframe(df_s, use_container_width=True, hide_index=True)
        else:
            st.info("Sin apuestas registradas.")

# ══════════════════════════════════════════════════════════════
# PÁGINA: APRENDIZAJE
# ══════════════════════════════════════════════════════════════

elif pagina == "🧠 Aprendizaje":
    st.markdown('<div class="section-title">🧠 SISTEMA DE APRENDIZAJE</div>', unsafe_allow_html=True)
    if not db_ok:
        st.warning("⚠️ Conecta Supabase.")
    else:
        predicciones = get_predicciones()
        resueltas = [p for p in predicciones if p.get("acerto") is not None]
        pendientes = [p for p in predicciones if p.get("acerto") is None]

        if resueltas:
            total = len(resueltas)
            aciertos = sum(1 for p in resueltas if p.get("acerto") == True)
            pct = round(aciertos / total * 100, 1)
            tipos = {}
            for p in resueltas:
                t = p.get("tipo_prediccion","Otro")
                if t not in tipos: tipos[t] = {"total":0,"aciertos":0}
                tipos[t]["total"] += 1
                if p.get("acerto"): tipos[t]["aciertos"] += 1

            a1, a2, a3, a4 = st.columns(4)
            a1.markdown(f'<div class="metric-box"><div class="metric-label">Total</div><div class="metric-value">{total}</div></div>', unsafe_allow_html=True)
            c = "green" if pct >= 60 else ("yellow" if pct >= 45 else "red")
            a2.markdown(f'<div class="metric-box"><div class="metric-label">% Acierto</div><div class="metric-value {c}">{pct}%</div></div>', unsafe_allow_html=True)
            a3.markdown(f'<div class="metric-box"><div class="metric-label">Aciertos</div><div class="metric-value green">{aciertos}</div></div>', unsafe_allow_html=True)
            a4.markdown(f'<div class="metric-box"><div class="metric-label">Errores</div><div class="metric-value red">{total-aciertos}</div></div>', unsafe_allow_html=True)

            if tipos:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="section-title">📊 POR TIPO</div>', unsafe_allow_html=True)
                t_cols = st.columns(min(len(tipos), 4))
                for i, (tipo, data) in enumerate(tipos.items()):
                    pt = round(data["aciertos"]/data["total"]*100, 1)
                    c = "green" if pt >= 60 else ("yellow" if pt >= 45 else "red")
                    t_cols[i%len(t_cols)].markdown(f'<div class="metric-box"><div class="metric-label">{tipo}</div><div class="metric-value {c}">{pt}%</div><div style="font-size:0.68rem;color:#3a5060">{data["aciertos"]}/{data["total"]}</div></div>', unsafe_allow_html=True)
        else:
            st.info("Sin predicciones resueltas aún.")

        if pendientes:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">⏳ PENDIENTES</div>', unsafe_allow_html=True)
            for pred in pendientes:
                pc1, pc2, pc3, pc4 = st.columns([3, 2, 2, 1])
                with pc1:
                    st.markdown(f"**{pred['partido']}**")
                    st.caption(f"{pred['tipo_prediccion']} → **{pred['valor_predicho']}** ({pred.get('probabilidad','?')}%)")
                with pc2: st.caption(f"📅 {pred.get('fecha_partido','?')}")
                with pc3:
                    rr = st.text_input("Resultado real", key=f"rr_{pred['id']}", placeholder="Local, Over, Si...", label_visibility="collapsed")
                with pc4:
                    if st.button("✔️", key=f"rv_{pred['id']}", use_container_width=True):
                        if rr:
                            acerto = resolver_prediccion(pred["id"], rr, pred["valor_predicho"])
                            st.success("✅ Acierto!" if acerto else "❌ Error"); st.rerun()

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📋 HISTORIAL</div>', unsafe_allow_html=True)
        if predicciones:
            for pred in predicciones:
                a = pred.get("acerto")
                icono = "✅" if a is True else ("❌" if a is False else "⏳")
                clase = "color:#3ecf8e" if a is True else ("color:#e05c5c" if a is False else "color:#d4a843")
                st.markdown(f"""<div class="pred-row">
                    <span>{icono}</span>
                    <span><b>{pred['partido']}</b></span>
                    <span style="color:#5a7a8a">{pred['tipo_prediccion']}</span>
                    <span>→ <b>{pred['valor_predicho']}</b> ({pred.get('probabilidad','?')}%)</span>
                    <span style="{clase}">{pred.get('resultado_real','pendiente')}</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No hay predicciones aún.")

# ══════════════════════════════════════════════════════════════
# PÁGINA: PARTIDOS UCL
# ══════════════════════════════════════════════════════════════

elif pagina == "📋 Partidos UCL":
    st.markdown('<div class="section-title">📋 RESULTADOS UCL 2025/26</div>', unsafe_allow_html=True)
    if db_ok:
        fase_filter = st.selectbox("Fase", ["Todos","Fase Liga","Octavos Ida","Octavos Vuelta","Cuartos Ida","Cuartos Vuelta"])
        todos = get_todos_partidos(fase_filter)
        if todos:
            for p in todos:
                gl = p.get("goles_local") if p.get("goles_local") is not None else "–"
                gv = p.get("goles_visitante") if p.get("goles_visitante") is not None else "–"
                st.markdown(f"""<div class="partido-row">
                    <span style="color:#3a5060;font-size:0.7rem;min-width:90px">{p.get('fecha','')}</span>
                    <span style="min-width:80px;color:#2a4050;font-size:0.7rem">{p.get('fase','')}</span>
                    <span style="min-width:140px;text-align:right"><b>{p.get('equipo_local','')}</b></span>
                    <span style="font-family:'Bebas Neue',cursive;font-size:1.2rem;letter-spacing:4px;padding:0 0.8rem;color:#3ecf8e">{gl} – {gv}</span>
                    <span style="min-width:140px"><b>{p.get('equipo_visitante','')}</b></span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No hay partidos.")
    else:
        st.warning("Conecta Supabase.")

# ══════════════════════════════════════════════════════════════
# PÁGINA: HISTORIAL SIMULACIONES
# ══════════════════════════════════════════════════════════════

elif pagina == "📊 Historial":
    st.markdown('<div class="section-title">📊 HISTORIAL DE SIMULACIONES</div>', unsafe_allow_html=True)
    if db_ok:
        sims = get_historial_sims()
        if sims:
            df = pd.DataFrame(sims)
            cols_show = ["created_at","equipo_local","equipo_visitante","prob_victoria_local","prob_empate","prob_victoria_visitante","prob_over25","prob_btts","marcador_probable"]
            df_show = df[[c for c in cols_show if c in df.columns]].copy()
            df_show.columns = ["Fecha","Local","Visitante","% Local","% Empate","% Visit.","Over 2.5","BTTS","Marcador"][:len(df_show.columns)]
            if "Fecha" in df_show.columns: df_show["Fecha"] = pd.to_datetime(df_show["Fecha"]).dt.strftime("%d/%m %H:%M")
            st.dataframe(df_show, use_container_width=True, hide_index=True)
        else:
            st.info("Sin simulaciones aún.")
    else:
        st.warning("Conecta Supabase.")
