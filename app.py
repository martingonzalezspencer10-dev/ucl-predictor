import streamlit as st
import numpy as np
import pandas as pd
import httpx

# ──────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="⚽ UCL 25/26 Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 40%, #0a1628 70%, #060d1a 100%);
    color: #e8f4fd;
}
.main-header { text-align: center; padding: 2rem 0 1rem 0; border-bottom: 2px solid rgba(0,200,100,0.3); margin-bottom: 2rem; }
.main-header h1 {
    font-family: 'Bebas Neue', cursive; font-size: 3.5rem; letter-spacing: 6px;
    background: linear-gradient(90deg, #00c864, #00e5ff, #00c864);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 0;
}
.main-header p { color: #8ab4c8; font-size: 0.9rem; letter-spacing: 3px; text-transform: uppercase; margin-top: 0.4rem; }
.section-title {
    font-family: 'Bebas Neue', cursive; font-size: 1.6rem; letter-spacing: 4px;
    color: #00c864; border-left: 4px solid #00c864; padding-left: 12px; margin: 1.5rem 0 1rem 0;
}
.metric-box {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px; padding: 1.2rem; text-align: center; margin: 0.3rem 0;
}
.metric-box:hover { border-color: rgba(0,200,100,0.4); background: rgba(0,200,100,0.06); }
.metric-label { font-size: 0.72rem; color: #7aa8c0; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-bottom: 0.4rem; }
.metric-value { font-family: 'Bebas Neue', cursive; font-size: 2.4rem; letter-spacing: 2px; color: #e8f4fd; line-height: 1; }
.metric-value.green { color: #00c864; }
.metric-value.yellow { color: #ffd700; }
.metric-value.red { color: #ff6b6b; }
.metric-value.blue { color: #00e5ff; }
.bet-green {
    background: linear-gradient(135deg, rgba(0,200,100,0.15), rgba(0,150,80,0.1));
    border: 1px solid #00c864; border-radius: 10px; padding: 0.9rem 1.2rem; margin: 0.4rem 0;
    display: flex; justify-content: space-between; align-items: center; font-weight: 600;
}
.bet-yellow {
    background: linear-gradient(135deg, rgba(255,215,0,0.12), rgba(200,160,0,0.08));
    border: 1px solid #ffd700; border-radius: 10px; padding: 0.9rem 1.2rem; margin: 0.4rem 0;
    display: flex; justify-content: space-between; align-items: center; font-weight: 600;
}
.bet-label { color: #e8f4fd; font-size: 0.95rem; }
.bet-pct-green { color: #00c864; font-family: 'Bebas Neue', cursive; font-size: 1.4rem; }
.bet-pct-yellow { color: #ffd700; font-family: 'Bebas Neue', cursive; font-size: 1.4rem; }
.score-card {
    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px; padding: 0.8rem 1rem; margin: 0.3rem 0;
    display: flex; justify-content: space-between; align-items: center;
}
.score-card:first-child { border-color: rgba(0,200,100,0.5); background: rgba(0,200,100,0.07); }
.score-text { font-family: 'Bebas Neue', cursive; font-size: 1.6rem; letter-spacing: 4px; color: #e8f4fd; }
.score-pct { font-size: 0.85rem; color: #7aa8c0; font-weight: 600; }
.divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(0,200,100,0.4), transparent); margin: 1.5rem 0; }
.vs-badge { text-align: center; font-family: 'Bebas Neue', cursive; font-size: 2rem; color: rgba(255,255,255,0.2); letter-spacing: 4px; padding: 0.5rem 0; }
.explanation-box {
    background: rgba(0,229,255,0.04); border: 1px solid rgba(0,229,255,0.15);
    border-radius: 12px; padding: 1.2rem 1.5rem; margin-top: 1rem;
    font-size: 0.85rem; color: #8ab4c8; line-height: 1.7;
}
.partido-row {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 8px; padding: 0.6rem 1rem; margin: 0.25rem 0;
    display: flex; justify-content: space-between; align-items: center; font-size: 0.88rem;
}
.db-badge {
    background: rgba(0,200,100,0.1); border: 1px solid rgba(0,200,100,0.3);
    border-radius: 20px; padding: 0.2rem 0.8rem; font-size: 0.7rem;
    color: #00c864; font-weight: 600; letter-spacing: 1px;
}
div.stButton > button {
    width: 100%; background: linear-gradient(135deg, #00c864, #00a050); color: #000;
    font-family: 'Bebas Neue', cursive; font-size: 1.4rem; letter-spacing: 4px;
    border: none; border-radius: 12px; padding: 0.9rem; cursor: pointer; transition: all 0.2s; margin-top: 1rem;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #00e574, #00c864);
    transform: translateY(-1px); box-shadow: 0 8px 25px rgba(0,200,100,0.35);
}
#MainMenu {visibility: hidden;} footer {visibility: hidden;} .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SUPABASE VÍA REST API (sin librería supabase-py)
# ──────────────────────────────────────────────

def get_headers():
    key = st.secrets["SUPABASE_KEY"]
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

def sb_get(table: str, params: dict = None):
    url = f"{st.secrets['SUPABASE_URL']}/rest/v1/{table}"
    try:
        r = httpx.get(url, headers=get_headers(), params=params, timeout=10)
        return r.json() if r.status_code == 200 else []
    except Exception as e:
        st.error(f"Error BD ({table}): {e}")
        return []

def sb_post(table: str, data: dict):
    url = f"{st.secrets['SUPABASE_URL']}/rest/v1/{table}"
    try:
        r = httpx.post(url, headers=get_headers(), json=data, timeout=10)
        return r.status_code in [200, 201]
    except Exception as e:
        st.warning(f"No se pudo guardar: {e}")
        return False

def get_equipos():
    return sb_get("equipos", {"select": "*", "order": "nombre.asc"})

def get_partidos_equipo(nombre: str):
    local = sb_get("partidos_ucl", {
        "select": "*",
        "equipo_local": f"eq.{nombre}",
        "goles_local": "not.is.null",
        "order": "fecha.desc",
        "limit": "5"
    })
    visit = sb_get("partidos_ucl", {
        "select": "*",
        "equipo_visitante": f"eq.{nombre}",
        "goles_visitante": "not.is.null",
        "order": "fecha.desc",
        "limit": "5"
    })
    partidos = (local or []) + (visit or [])
    partidos.sort(key=lambda x: x.get("fecha", ""), reverse=True)
    return partidos[:5]

def get_todos_partidos(fase: str = None):
    params = {"select": "*", "order": "fecha.desc", "limit": "60"}
    data = sb_get("partidos_ucl", params)
    if fase and fase != "Todos":
        data = [p for p in data if p.get("fase") == fase]
    return data

def guardar_simulacion(datos: dict):
    sb_post("simulaciones", datos)

def get_historial():
    return sb_get("simulaciones", {"select": "*", "order": "created_at.desc", "limit": "20"})

# ──────────────────────────────────────────────
# MODELO
# ──────────────────────────────────────────────
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

# ──────────────────────────────────────────────
# HEADER
# ──────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>⚽ UCL 25/26 PREDICTOR</h1>
    <p>Supabase · Poisson · Monte Carlo 50,000 Iteraciones · Datos Reales Champions</p>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# CARGAR DATOS
# ──────────────────────────────────────────────
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
    else:
        st.error("⚠️ Supabase conectado pero sin datos. ¿Ejecutaste el SQL?")
except Exception as e:
    st.error(f"⚠️ Error conectando Supabase: {e}")

# ──────────────────────────────────────────────
# PESTAÑAS
# ──────────────────────────────────────────────
tab_pred, tab_partidos, tab_historial = st.tabs([
    "🎯 Simulador de Partidos",
    "📋 Partidos UCL 25/26",
    "📊 Historial de Simulaciones"
])

# ══════════════════════════════════════════════
# TAB 1: SIMULADOR
# ══════════════════════════════════════════════
with tab_pred:
    st.markdown('<div class="section-title">🏟️ SELECCIÓN DE EQUIPOS</div>', unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([5, 1, 5])

    with col_l:
        st.markdown("**🏠 Equipo Local**")
        if nombres_equipos:
            idx_l = nombres_equipos.index("Real Madrid") if "Real Madrid" in nombres_equipos else 0
            sel_local = st.selectbox("Equipo local", nombres_equipos, index=idx_l, key="sel_local")
            eq_l = equipos_dict.get(sel_local, {})
        else:
            sel_local = st.text_input("Nombre equipo local", "Real Madrid")
            eq_l = {}
        nombre_local = sel_local
        c1, c2 = st.columns(2)
        with c1:
            ataque_local  = st.slider("⚔️ Ataque",  0.5, 3.5, float(eq_l.get("ataque", 1.8)),      0.05, key="atk_l")
            xg_local      = st.slider("🎯 xG",      0.5, 3.5, float(eq_l.get("xg_promedio", 1.6)), 0.05, key="xg_l")
            forma_local   = st.slider("📈 Forma",   0.8, 1.2, float(eq_l.get("forma", 1.05)),       0.01, key="forma_l")
        with c2:
            defensa_local = st.slider("🛡️ Defensa", 0.5, 3.5, float(eq_l.get("defensa", 1.3)),     0.05, key="def_l")

    with col_m:
        st.markdown('<div class="vs-badge" style="margin-top:4rem">VS</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown("**✈️ Equipo Visitante**")
        if nombres_equipos:
            idx_v = nombres_equipos.index("Manchester City") if "Manchester City" in nombres_equipos else 1
            sel_away = st.selectbox("Equipo visitante", nombres_equipos, index=idx_v, key="sel_away")
            eq_v = equipos_dict.get(sel_away, {})
        else:
            sel_away = st.text_input("Nombre equipo visitante", "Manchester City")
            eq_v = {}
        nombre_visitante = sel_away
        c3, c4 = st.columns(2)
        with c3:
            ataque_visit  = st.slider("⚔️ Ataque",  0.5, 3.5, float(eq_v.get("ataque", 1.7)),      0.05, key="atk_v")
            xg_visit      = st.slider("🎯 xG",      0.5, 3.5, float(eq_v.get("xg_promedio", 1.5)), 0.05, key="xg_v")
            forma_visit   = st.slider("📈 Forma",   0.8, 1.2, float(eq_v.get("forma", 1.0)),        0.01, key="forma_v")
        with c4:
            defensa_visit = st.slider("🛡️ Defensa", 0.5, 3.5, float(eq_v.get("defensa", 1.4)),     0.05, key="def_v")

    # Últimos 5 partidos
    if db_ok:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📅 ÚLTIMOS 5 PARTIDOS EN UCL 25/26</div>', unsafe_allow_html=True)
        p_col1, p_col2 = st.columns(2)
        for col, nombre in [(p_col1, nombre_local), (p_col2, nombre_visitante)]:
            with col:
                st.markdown(f"**{nombre}**")
                partidos = get_partidos_equipo(nombre)
                if partidos:
                    for p in partidos:
                        es_local = p["equipo_local"] == nombre
                        rival = p["equipo_visitante"] if es_local else p["equipo_local"]
                        gl, gv = p.get("goles_local"), p.get("goles_visitante")
                        if es_local:
                            marcador = f"{gl} – {gv}"
                            res = "✅" if gl > gv else ("🟡" if gl == gv else "❌")
                        else:
                            marcador = f"{gv} – {gl}"
                            res = "✅" if gv > gl else ("🟡" if gv == gl else "❌")
                        st.markdown(f"""
                        <div class="partido-row">
                            <span style="color:#7aa8c0;font-size:0.75rem">{p.get('fecha','')}</span>
                            <span>vs <b>{rival[:15]}</b></span>
                            <span style="font-family:'Bebas Neue',cursive;font-size:1.1rem;letter-spacing:2px">{marcador}</span>
                            <span>{res}</span>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.info("Sin partidos registrados.")

    # Contexto
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚙️ CONTEXTO DEL PARTIDO</div>', unsafe_allow_html=True)
    cp1, cp2, cp3, cp4, cp5 = st.columns([3, 3, 3, 3, 2])
    with cp1: intensidad    = st.slider("🏆 Intensidad Champions", 0.90, 1.20, 1.05, 0.01)
    with cp2: avg_corners   = st.slider("🚩 Córners promedio", 6, 14, 10, 1)
    with cp3: avg_tarjetas  = st.slider("🟨 Tarjetas promedio", 2, 7, 4, 1)
    with cp4: factor_reg    = st.slider("📉 Factor regresión", 0.88, 0.98, 0.93, 0.01)
    with cp5: ventaja_local = st.checkbox("🏟️ Ventaja de local", value=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    simular = st.button("🎲 SIMULAR PARTIDO", use_container_width=True)

    if simular:
        with st.spinner("⚙️ Ejecutando 50,000 simulaciones Monte Carlo..."):
            lam_l  = calcular_lambda(ataque_local, defensa_visit, xg_local, forma_local, ventaja_local, intensidad, factor_reg)
            lam_v  = calcular_lambda(ataque_visit, defensa_local, xg_visit, forma_visit, False, intensidad, factor_reg)
            gl, gv = simular_partido(lam_l, lam_v)
            probs  = calcular_probabilidades(gl, gv)
            over_c = calcular_corners(avg_corners)
            over_t = calcular_tarjetas(avg_tarjetas)
            top5   = top_marcadores(gl, gv)

        if db_ok:
            guardar_simulacion({
                "equipo_local": nombre_local,
                "equipo_visitante": nombre_visitante,
                "prob_victoria_local": round(probs["victoria_local"], 2),
                "prob_empate": round(probs["empate"], 2),
                "prob_victoria_visitante": round(probs["victoria_visitante"], 2),
                "prob_over25": round(probs["over_25"], 2),
                "prob_btts": round(probs["btts"], 2),
                "prob_corners_over95": round(over_c, 2),
                "prob_tarjetas_over35": round(over_t, 2),
                "lambda_local": round(lam_l, 3),
                "lambda_visitante": round(lam_v, 3),
                "marcador_probable": top5[0][0] if top5 else "N/A",
            })
            st.markdown('<span class="db-badge">✅ SIMULACIÓN GUARDADA EN BD</span>', unsafe_allow_html=True)

        # Probabilidades 1X2
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 PROBABILIDADES</div>', unsafe_allow_html=True)
        vl, emp, vv = probs["victoria_local"], probs["empate"], probs["victoria_visitante"]
        r1, r2, r3 = st.columns(3)
        with r1:
            c = "green" if vl >= 60 else ("yellow" if vl >= 45 else "red")
            st.markdown(f'<div class="metric-box"><div class="metric-label">🏠 {nombre_local}</div><div class="metric-value {c}">{vl:.1f}%</div></div>', unsafe_allow_html=True)
        with r2:
            st.markdown(f'<div class="metric-box"><div class="metric-label">🤝 Empate</div><div class="metric-value">{emp:.1f}%</div></div>', unsafe_allow_html=True)
        with r3:
            c = "green" if vv >= 60 else ("yellow" if vv >= 45 else "red")
            st.markdown(f'<div class="metric-box"><div class="metric-label">✈️ {nombre_visitante}</div><div class="metric-value {c}">{vv:.1f}%</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        o25, btts = probs["over_25"], probs["btts"]
        m1, m2, m3, m4 = st.columns(4)
        for col, label, val in zip([m1, m2, m3, m4],
            ["⚽ Over 2.5", "🎯 BTTS", "🚩 Córners Over 9.5", "🟨 Tarjetas Over 3.5"],
            [o25, btts, over_c, over_t]):
            c = "green" if val >= 60 else ("yellow" if val >= 45 else "blue")
            col.markdown(f'<div class="metric-box"><div class="metric-label">{label}</div><div class="metric-value {c}">{val:.1f}%</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        x1, x2 = st.columns(2)
        x1.markdown(f'<div class="metric-box"><div class="metric-label">📐 λ {nombre_local}</div><div class="metric-value green">{lam_l:.2f}</div></div>', unsafe_allow_html=True)
        x2.markdown(f'<div class="metric-box"><div class="metric-label">📐 λ {nombre_visitante}</div><div class="metric-value">{lam_v:.2f}</div></div>', unsafe_allow_html=True)

        # Top 5
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎯 TOP 5 MARCADORES MÁS PROBABLES</div>', unsafe_allow_html=True)
        sc1, sc2 = st.columns([3, 2])
        with sc1:
            iconos = ["🥇","🥈","🥉","▪️","▪️"]
            for i, (marcador, pct) in enumerate(top5):
                g_l, g_v = marcador.split("-")
                st.markdown(f"""
                <div class="score-card">
                    <span style="font-size:1.3rem">{iconos[i]}</span>
                    <span class="score-text">{nombre_local[:12]} &nbsp; {g_l} – {g_v} &nbsp; {nombre_visitante[:12]}</span>
                    <span class="score-pct">{pct:.1f}%</span>
                </div>""", unsafe_allow_html=True)
        with sc2:
            df_s = pd.DataFrame({"Marcador": [m for m, _ in top5], "Prob (%)": [p for _, p in top5]})
            st.bar_chart(df_s.set_index("Marcador"), color="#00c864", height=240)

        # Apuestas sugeridas
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">💰 APUESTAS SUGERIDAS</div>', unsafe_allow_html=True)
        apuestas = [
            (f"🏠 Gana {nombre_local}", vl),
            (f"✈️ Gana {nombre_visitante}", vv),
            ("⚽ Over 2.5 Goles", o25),
            ("🎯 BTTS — Ambos Marcan", btts),
            ("🚩 Córners Over 9.5", over_c),
            ("🟨 Tarjetas Over 3.5", over_t),
        ]
        sugeridas = [(l, p) for l, p in apuestas if p >= 60]
        if sugeridas:
            ba1, ba2 = st.columns(2)
            for i, (label, pct) in enumerate(sugeridas):
                col = ba1 if i % 2 == 0 else ba2
                if pct >= 70:
                    col.markdown(f'<div class="bet-green"><span class="bet-label">{label}</span><span class="bet-pct-green">✅ {pct:.1f}%</span></div>', unsafe_allow_html=True)
                else:
                    col.markdown(f'<div class="bet-yellow"><span class="bet-label">{label}</span><span class="bet-pct-yellow">⚠️ {pct:.1f}%</span></div>', unsafe_allow_html=True)
            st.markdown('<div style="margin-top:0.8rem;font-size:0.78rem;color:#556b80">🟢 ≥70% &nbsp;|&nbsp; 🟡 60–69%</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="explanation-box">⚠️ Ninguna apuesta supera el 60% en este escenario.</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="explanation-box">
            <strong>📖 Metodología:</strong> Combina Ataque/Defensa (60%) + xG (40%), con modificadores de forma,
            ventaja local (+12%), intensidad Champions y factor de regresión.
            50,000 simulaciones Monte Carlo con distribución de Poisson.
            Resultados guardados automáticamente en Supabase.
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 2: PARTIDOS UCL
# ══════════════════════════════════════════════
with tab_partidos:
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
                    <span style="color:#7aa8c0;font-size:0.78rem;min-width:90px">{p.get('fecha','')}</span>
                    <span style="min-width:80px;color:#5a9ab0;font-size:0.75rem">{p.get('fase','')}</span>
                    <span style="min-width:150px;text-align:right"><b>{p.get('equipo_local','')}</b></span>
                    <span style="font-family:'Bebas Neue',cursive;font-size:1.3rem;letter-spacing:4px;padding:0 1.2rem;color:#00c864">{gl} – {gv}</span>
                    <span style="min-width:150px"><b>{p.get('equipo_visitante','')}</b></span>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No hay partidos para mostrar.")
    else:
        st.warning("Conecta Supabase para ver los partidos.")

# ══════════════════════════════════════════════
# TAB 3: HISTORIAL
# ══════════════════════════════════════════════
with tab_historial:
    st.markdown('<div class="section-title">📊 HISTORIAL DE SIMULACIONES</div>', unsafe_allow_html=True)
    if db_ok:
        sims = get_historial()
        if sims:
            df = pd.DataFrame(sims)
            cols_show = ["created_at","equipo_local","equipo_visitante",
                         "prob_victoria_local","prob_empate","prob_victoria_visitante",
                         "prob_over25","prob_btts","marcador_probable"]
            df_show = df[[c for c in cols_show if c in df.columns]].copy()
            df_show.columns = ["Fecha","Local","Visitante","% Local","% Empate",
                                "% Visit.","Over 2.5","BTTS","Marcador +prob."][:len(df_show.columns)]
            if "Fecha" in df_show.columns:
                df_show["Fecha"] = pd.to_datetime(df_show["Fecha"]).dt.strftime("%d/%m %H:%M")
            st.dataframe(df_show, use_container_width=True, hide_index=True)
        else:
            st.info("Aún no hay simulaciones. ¡Simula tu primer partido!")
    else:
        st.warning("Conecta Supabase para ver el historial.")
