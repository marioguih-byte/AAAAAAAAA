# ======================================================================
# PRECIPITAÇÃO HORÁRIA — UNIDADES PETROBRAS
# Google WeatherNext 3 (via dynamical.org / dynamical_catalog)
#
# Rodar:  streamlit run streamlit_app.py
# ======================================================================
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import xarray as xr

st.set_page_config(page_title="Precipitação horária · Unidades Petrobras", layout="wide", page_icon="🌧️")

# ----------------------------------------------------------------------
# CONFIGURAÇÕES PADRÃO (mesmas do seu script)
# ----------------------------------------------------------------------
CATALOGO_PADRAO = "google-weathernext3-forecast-48-hour-0-1-degree-virtual"
VARIAVEL_PADRAO = "precipitation_surface"
TZ = "America/Sao_Paulo"

# Unidades: nomes e coordenadas do cadastro ESTACOES_PADRAO do app rio-raios
UNIDADES = [
    {"nome": "ARM Macaé - Armazém Macaé", "curto": "ARM Macaé", "lat": -22.41532, "lon": -41.86135},
    {"nome": "Armazém Rio de Janeiro", "curto": "Armazém Rio de Janeiro", "lat": -22.81097, "lon": -43.28188},
    {"nome": "BOAVENTURA, Itaboraí-RJ", "curto": "BOAVENTURA, Itaboraí-RJ", "lat": -22.66071, "lon": -42.85363},
    {"nome": "CILEP - CENPES", "curto": "CENPES", "lat": -22.8542, "lon": -43.23383},
    {"nome": "Porto Açu", "curto": "Porto Açu", "lat": -21.86474, "lon": -41.01644},
    {"nome": "Porto Aratu", "curto": "Porto Aratu", "lat": -12.78013, "lon": -38.49676},
    {"nome": "Porto Baia de Guanabara", "curto": "Porto Baia de Guanabara", "lat": -22.87894, "lon": -43.20933},
    {"nome": "Porto Belém", "curto": "Porto Belém", "lat": -1.34148, "lon": -48.48131},
    {"nome": "Porto de Imbetiba - Macaé", "curto": "Porto de Imbetiba", "lat": -22.38683, "lon": -41.76874},
    {"nome": "Porto Guamaré", "curto": "Porto Guamaré", "lat": -5.10669, "lon": -36.31959},
    {"nome": "Porto Mucuripe", "curto": "Porto Mucuripe", "lat": -3.71312, "lon": -38.47404},
    {"nome": "Porto Paracuru", "curto": "Porto Paracuru", "lat": -3.40115, "lon": -39.0109},
    {"nome": "Porto TMIB", "curto": "Porto TMIB", "lat": -10.82413, "lon": -36.9463},
    {"nome": "Porto Valença", "curto": "Porto Valença", "lat": -13.36937, "lon": -39.07125},
    {"nome": "Refinaria Abreu e Lima - RNEST", "curto": "RNEST", "lat": -8.37966, "lon": -35.0102},
    {"nome": "Refinaria Alberto Pasqualini - REFAP", "curto": "REFAP", "lat": -29.8699, "lon": -51.17819},
    {"nome": "Refinaria de Capuava - RECAP", "curto": "RECAP", "lat": -23.65668, "lon": -46.48088},
    {"nome": "Refinaria de Paulínia - REPLAN", "curto": "REPLAN", "lat": -22.72959, "lon": -47.14771},
    {"nome": "Refinaria Duque de Caxias - REDUC", "curto": "REDUC", "lat": -22.7151, "lon": -43.28401},
    {"nome": "Refinaria Gabriel Passos - REGAP", "curto": "REGAP", "lat": -19.96428, "lon": -44.09514},
    {"nome": "Refinaria Henrique Lage - REVAP", "curto": "REVAP", "lat": -23.1848, "lon": -45.81581},
    {"nome": "Refinaria Presidente Bernardes - RPBC", "curto": "RPBC", "lat": -23.87333, "lon": -46.42757},
    {"nome": "Refinaria Presidente Getúlio Vargas - REPAR", "curto": "REPAR", "lat": -25.56614, "lon": -49.36942},
    {"nome": "UFN III - Unidade de Fertilizantes Nitrogenados III", "curto": "UFN III", "lat": -20.9859, "lon": -51.8383},
    {"nome": "Unidade de Tratamento de Gás de Cabiúnas - UTGCAB", "curto": "UTGCAB", "lat": -22.28533, "lon": -41.71791},
    {"nome": "Unidade de Tratamento de Gás de Cacimbas - UTGC", "curto": "UTGC", "lat": -19.4631, "lon": -39.7606},
    {"nome": "Unidade de Tratamento de Gás de Caraguatatuba - UTGCA", "curto": "UTGCA", "lat": -23.65419, "lon": -45.50121},
    {"nome": "Unidade de Tratamento de Gás Sul Capixaba - UTGSUL", "curto": "UTGSUL", "lat": -20.79446, "lon": -40.62091},
    {"nome": "UTE Canoas - UTE CAN", "curto": "UTE CAN", "lat": -29.87507, "lon": -51.14544},
    {"nome": "UTE Ibirité - UTE IBT", "curto": "UTE IBT", "lat": -19.98858, "lon": -44.09821},
    {"nome": "UTE Juiz de Fora - UTE JF", "curto": "UTE JF", "lat": -21.69062, "lon": -43.45672},
    {"nome": "UTE Nova Piratininga - UTE NPI", "curto": "UTE NPI", "lat": -23.69941, "lon": -46.67388},
    {"nome": "UTE Seropédica/Baixada Fluminense - UTE SRP/BF", "curto": "UTE SRP/BF", "lat": -22.72329, "lon": -43.64772},
    {"nome": "UTE Termobahia - UTE TBA", "curto": "UTE TBA", "lat": -12.70324, "lon": -38.5649},
    {"nome": "UTE Termocamaçari - UTE TCA", "curto": "UTE TCA", "lat": -12.66687, "lon": -38.31469},
    {"nome": "UTE Termoceará - UTE TCE", "curto": "UTE TCE", "lat": -3.69246, "lon": -38.87061},
    {"nome": "UTE Termomacaé - UTE TMA", "curto": "UTE TMA", "lat": -22.30616, "lon": -41.8767},
    {"nome": "UTE Termorio - UTE TRI", "curto": "UTE TRI", "lat": -22.71488, "lon": -43.25435},
    {"nome": "UTE Três Lagoas - UTE TLG", "curto": "UTE TLG", "lat": -20.7455, "lon": -51.66459},
    {"nome": "UTE Vale do Açu - UTE VLA", "curto": "UTE VLA", "lat": -5.38169, "lon": -36.81975},
]
NOMES = [u["nome"] for u in UNIDADES]
SEM_SEL = "(média de todas as unidades)"

# Classes de cor
ACC_EDGES = [0.1, 1, 5, 10, 25, 50, 100]       # mm acumulados
HORA_EDGES = [0.1, 0.5, 1, 2.5, 5, 10, 20]     # mm em 1 h
CORES = ["#dfe5ec", "#bfe3f5", "#7cc4ec", "#3d9be0", "#2b6fd0", "#6a3fc4", "#b0309f", "#d41f3a"]


# ----------------------------------------------------------------------
# ACESSO AOS DADOS
# ----------------------------------------------------------------------
@st.cache_resource(show_spinner="Abrindo catálogo da dynamical.org…")
def abrir_dataset(catalogo: str):
    import dynamical_catalog
    return dynamical_catalog.open(catalogo, chunks=None)


def _primeiro(da, opcoes):
    for n in opcoes:
        if n in da.dims:
            return n
    raise KeyError(f"Nenhuma das dimensões {opcoes} em {list(da.dims)}")


@st.cache_data(show_spinner=False, ttl=900)
def listar_opcoes(catalogo: str, variavel: str):
    ds = abrir_dataset(catalogo)
    if variavel not in ds.data_vars:
        raise ValueError(f"Variável '{variavel}' não encontrada. Disponíveis: {list(ds.data_vars)}")
    da = ds[variavel]
    inits = pd.to_datetime(ds["init_time"].values)
    inits = sorted(inits)[-40:][::-1]
    stats = [str(s) for s in da["statistic"].values] if "statistic" in da.dims else []
    return [i.isoformat() for i in inits], stats


@st.cache_data(show_spinner="Lendo WeatherNext 3 nos pontos das unidades…", ttl=3600)
def extrair(catalogo: str, variavel: str, init_iso: str, estatistica: str, metodo: str):
    """Devolve (mm por passo [valid_time local × unidade], passo em horas, unidade original, aviso)."""
    ds = abrir_dataset(catalogo)
    da = ds[variavel].sel(init_time=np.datetime64(init_iso))
    if estatistica and "statistic" in da.dims:
        da = da.sel(statistic=estatistica)
    unidade_orig = str(da.attrs.get("units", ""))

    xn = _primeiro(da, ("x", "longitude", "lon"))
    yn = _primeiro(da, ("y", "latitude", "lat"))
    xs, ys = np.asarray(da[xn].values), np.asarray(da[yn].values)

    lons = np.array([u["lon"] for u in UNIDADES], dtype=float)
    lats = np.array([u["lat"] for u in UNIDADES], dtype=float)
    lon_q = lons % 360 if np.nanmax(xs) > 180 else lons          # grade 0–360 ou −180–180

    pad = 1.0
    ix = np.where((xs >= lon_q.min() - pad) & (xs <= lon_q.max() + pad))[0]
    iy = np.where((ys >= lats.min() - pad) & (ys <= lats.max() + pad))[0]
    if len(ix) == 0 or len(iy) == 0:
        raise ValueError("As unidades estão fora da grade do dataset.")
    sub = da.isel({xn: slice(ix.min(), ix.max() + 1), yn: slice(iy.min(), iy.max() + 1)}).load()
    sub = sub.sortby(xn).sortby(yn)

    px = xr.DataArray(lon_q, dims="unidade")
    py = xr.DataArray(lats, dims="unidade")
    if metodo == "Bilinear":
        pts = sub.interp({xn: px, yn: py}, method="linear")
    else:
        pts = sub.sel({xn: px, yn: py}, method="nearest")
    pts = pts.squeeze(drop=True)
    if set(pts.dims) != {"lead_time", "unidade"}:
        raise ValueError(f"Dimensões inesperadas após a seleção: {pts.dims}")
    pts = pts.transpose("lead_time", "unidade")

    leads = pd.to_timedelta(pts["lead_time"].values)
    lead_h = np.asarray(leads.total_seconds() / 3600.0, dtype=float)
    dt_h = np.empty_like(lead_h)
    dt_h[1:] = np.diff(lead_h)
    dt_h[0] = lead_h[0] if lead_h[0] > 0 else np.nan             # lead 0 não tem "passo anterior"
    valores = np.asarray(pts.values, dtype=float)

    # Conversão para mm acumulados em cada passo
    u = unidade_orig.lower().replace(" ", "")
    aviso = ""
    if u in ("mm/h", "mmh-1", "mm/hr"):
        taxa_h = valores
    elif u in ("mm/s", "mms-1", "kgm-2s-1", "kg/m2/s", "kgm**-2s**-1", "kgm^-2s^-1"):
        taxa_h = valores * 3600.0
    else:
        taxa_h = valores * 3600.0
        aviso = (f"Unidade '{unidade_orig}' não reconhecida; assumi taxa em kg m⁻² s⁻¹ (= mm/s), "
                 "como no seu script original.")
    mm = np.clip(taxa_h * dt_h[:, None], 0, None)

    valid = pd.DatetimeIndex(pd.Timestamp(init_iso) + leads).tz_localize("UTC").tz_convert(TZ).tz_localize(None)
    df = pd.DataFrame(mm, index=valid, columns=NOMES)
    passos = dt_h[np.isfinite(dt_h) & (dt_h > 0)]
    passo_h = float(np.median(passos)) if len(passos) else 1.0
    return df, passo_h, unidade_orig, aviso


# ----------------------------------------------------------------------
# CÁLCULOS
# ----------------------------------------------------------------------
def acumulado(df: pd.DataFrame, a, b) -> pd.Series:
    """Soma dos passos cujo FIM está em (a, b]. Ex.: 08/11 15h → 09/11 15h = 24 h."""
    m = (df.index > pd.Timestamp(a)) & (df.index <= pd.Timestamp(b))
    return df.loc[m].sum(min_count=1)


def fmt(v, casas=1):
    if v is None or not np.isfinite(v):
        return "—"
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_t(t):
    t = pd.Timestamp(t)
    dow = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"][t.dayofweek]
    return f"{dow} {t:%d/%m %Hh}"


def classes(vals, edges):
    v = np.asarray(vals, dtype=float)
    k = np.digitize(np.nan_to_num(v, nan=0.0), edges)
    k[~np.isfinite(v)] = -1
    return k


# ----------------------------------------------------------------------
# FIGURAS
# ----------------------------------------------------------------------
def fig_mapa(vals, edges, titulo_unid, destaque, mostrar_valores, altura=640):
    k = classes(vals, edges)
    lat = np.array([u["lat"] for u in UNIDADES])
    lon = np.array([u["lon"] for u in UNIDADES])
    fig = go.Figure()

    if destaque is not None:
        i = NOMES.index(destaque)
        fig.add_trace(go.Scattermap(lat=[lat[i]], lon=[lon[i]], mode="markers",
                                    marker=dict(size=36, color="#18212f"), hoverinfo="skip", showlegend=False))

    rotulos = [f"sem chuva (< {fmt(edges[0])})"]
    rotulos += [f"{fmt(edges[j - 1])} – {fmt(edges[j])}" for j in range(1, len(edges))]
    rotulos += [f"≥ {fmt(edges[-1])}"]

    for cls in range(len(edges) + 1):
        idx = np.where(k == cls)[0]
        textos = [fmt(vals[i]) for i in idx] if mostrar_valores else None
        hover = [f"<b>{UNIDADES[i]['nome']}</b><br>{fmt(vals[i])} {titulo_unid}<br>"
                 f"{lat[i]:.4f}, {lon[i]:.4f}" for i in idx]
        fig.add_trace(go.Scattermap(
            lat=lat[idx], lon=lon[idx], mode="markers+text" if mostrar_valores else "markers",
            marker=dict(size=14 + 2.6 * cls, color=CORES[cls], opacity=0.95),
            text=textos, textposition="top center", textfont=dict(size=11, color="#18212f"),
            hovertext=hover, hoverinfo="text", customdata=idx, name=rotulos[cls], legendgroup=str(cls)))
    idx_nan = np.where(k == -1)[0]
    if len(idx_nan):
        fig.add_trace(go.Scattermap(lat=lat[idx_nan], lon=lon[idx_nan], mode="markers",
                                    marker=dict(size=12, color="#9aa4b2"), customdata=idx_nan, name="sem dado",
                                    hovertext=[UNIDADES[i]["nome"] for i in idx_nan], hoverinfo="text"))
    fig.update_layout(
        map=dict(style="carto-positron", center=dict(lat=-15.5, lon=-46), zoom=3.5),
        height=altura, margin=dict(l=0, r=0, t=0, b=0), uirevision="mapa",
        legend=dict(title=dict(text=f"<b>{titulo_unid}</b>"), x=0.01, y=0.01, yanchor="bottom",
                    bgcolor="rgba(255,255,255,.92)", bordercolor="#e3e7ee", borderwidth=1),
        clickmode="event+select")
    return fig


def fig_serie(df, serie, passo_h, modo, a, b, hora, titulo):
    x = df.index
    fig = go.Figure()
    if modo == "acc":
        dentro = (x > pd.Timestamp(a)) & (x <= pd.Timestamp(b))
        cores = np.where(dentro, "#2b6fd0", "#bcd0ee")
        fig.add_shape(type="rect", xref="x", yref="paper", x0=pd.Timestamp(a).to_pydatetime(),
                      x1=pd.Timestamp(b).to_pydatetime(), y0=0, y1=1, fillcolor="rgba(43,111,208,.10)", line_width=0)
        cum = serie.where(dentro, 0).cumsum().where(dentro)
        fig.add_trace(go.Scatter(x=x, y=cum, mode="lines", name="acumulado no intervalo (mm)", yaxis="y2",
                                 line=dict(color="#d41f3a", width=2)))
    else:
        cores = np.where(x == pd.Timestamp(hora), "#d41f3a", "#2b6fd0")
        fig.add_shape(type="line", xref="x", yref="paper", x0=pd.Timestamp(hora).to_pydatetime(),
                      x1=pd.Timestamp(hora).to_pydatetime(), y0=0, y1=1, line=dict(color="#18212f", width=1.5))
    rot = "mm/h" if passo_h <= 1.01 else f"mm por passo de {fmt(passo_h, 0)} h"
    fig.add_trace(go.Bar(x=x, y=serie, name=rot, marker_color=cores,
                         hovertemplate="%{x|%d/%m %Hh}<br>%{y:.2f} mm<extra></extra>"))
    fig.update_layout(
        title=dict(text=titulo, font=dict(size=14)), height=300, margin=dict(l=10, r=10, t=40, b=10),
        bargap=0.15, showlegend=True, legend=dict(orientation="h", y=1.14, x=0),
        yaxis=dict(title=rot, rangemode="tozero"),
        yaxis2=dict(title="acumulado (mm)", overlaying="y", side="right", rangemode="tozero", showgrid=False),
        xaxis=dict(tickformat="%d/%m\n%Hh"), plot_bgcolor="white")
    fig.update_yaxes(gridcolor="#e8ecf2")
    return fig


# ----------------------------------------------------------------------
# BARRA LATERAL — DADOS
# ----------------------------------------------------------------------
def _on_map_select():
    try:
        pts = st.session_state["mapa"]["selection"]["points"]
        if pts:
            cd = pts[0].get("customdata")
            cd = cd[0] if isinstance(cd, (list, tuple)) else cd
            st.session_state["sel_unit"] = NOMES[int(cd)]
    except Exception:
        pass


with st.sidebar:
    st.header("Dados")
    with st.expander("Catálogo (avançado)"):
        catalogo = st.text_input("Catálogo", CATALOGO_PADRAO)
        variavel = st.text_input("Variável", VARIAVEL_PADRAO)
    if st.button("Recarregar dados", use_container_width=True):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()

try:
    inits, stats = listar_opcoes(catalogo, variavel)
except Exception as e:
    st.error(f"Não consegui abrir o catálogo: {e}")
    st.info("Confira se o pacote `dynamical-catalog` está instalado e se há acesso à internet.")
    st.stop()

with st.sidebar:
    init_iso = st.selectbox("Inicialização (UTC)", inits, format_func=lambda s: pd.Timestamp(s).strftime("%d/%m/%Y %H UTC"))
    if stats:
        estatistica = st.selectbox("Estatística", stats, index=stats.index("mean") if "mean" in stats else 0)
    else:
        estatistica = ""
    metodo = st.radio("Amostragem no ponto", ["Bilinear", "Vizinho mais próximo"], horizontal=True)

try:
    df, passo_h, unidade_orig, aviso = extrair(catalogo, variavel, init_iso, estatistica, metodo)
except Exception as e:
    st.error(f"Erro ao ler o WeatherNext 3: {e}")
    st.stop()

t_idx = df.index
n = len(t_idx)
if n < 2:
    st.error("O dataset retornou menos de 2 instantes de previsão.")
    st.stop()
dt_step = timedelta(hours=passo_h)
py = lambda i: t_idx[i].to_pydatetime()

# Reinicia controles quando muda o conjunto de dados
sig = (catalogo, variavel, init_iso, estatistica, passo_h)
if st.session_state.get("sig") != sig:
    agora = pd.Timestamp.now(tz=TZ).tz_localize(None).floor("h")
    i0 = int(t_idx.searchsorted(agora))
    i0 = i0 if i0 < n - 1 else 0
    i1 = int(t_idx.searchsorted(t_idx[i0] + pd.Timedelta(hours=24)))
    i1 = min(max(i1, i0 + 1), n - 1)
    st.session_state["rng"] = (py(i0), py(i1))
    st.session_state["hora"] = py(min(i0 + 1, n - 1))
    st.session_state["sig"] = sig
    st.session_state["agora_idx"] = i0


def _set_range(a, b):
    st.session_state["rng"] = (a, b)


with st.sidebar:
    st.divider()
    st.header("Visualização")
    modo_lbl = st.radio("Modo", ["Acumulado no intervalo", "Hora a hora"], label_visibility="collapsed")
    modo = "acc" if modo_lbl.startswith("Acum") else "hora"

    if modo == "acc":
        st.slider("Intervalo do acumulado", min_value=py(0), max_value=py(n - 1), step=dt_step,
                  key="rng", format="DD/MM HH:mm")
        i0 = st.session_state["agora_idx"]

        def preset_h(h):
            j = int(t_idx.searchsorted(t_idx[i0] + pd.Timedelta(hours=h)))
            return py(i0), py(min(max(j, i0 + 1), n - 1))

        def preset_dia(d):
            ini = t_idx[0].normalize() + pd.Timedelta(days=d)
            fim = ini + pd.Timedelta(days=1)
            a = int(t_idx.searchsorted(ini))
            b = int(t_idx.searchsorted(fim, side="right")) - 1
            a = min(a, n - 2)
            return py(a), py(min(max(b, a + 1), n - 1))

        st.caption("Atalhos")
        c = st.columns(4)
        for col, h in zip(c, (6, 12, 24, 48)):
            col.button(f"{h} h", key=f"p{h}", on_click=_set_range, args=preset_h(h), use_container_width=True)
        c = st.columns(3)
        c[0].button("Hoje", on_click=_set_range, args=preset_dia(0), use_container_width=True)
        c[1].button("Amanhã", on_click=_set_range, args=preset_dia(1), use_container_width=True)
        c[2].button("Tudo", on_click=_set_range, args=(py(0), py(n - 1)), use_container_width=True)
    else:
        st.toggle("▶ Reproduzir animação", key="tocando")
        st.select_slider("Velocidade", options=[2.0, 1.2, 0.6], value=1.2, key="vel",
                         format_func=lambda s: {2.0: "1×", 1.2: "2×", 0.6: "4×"}[s])

    mostrar_valores = st.checkbox("Mostrar valores no mapa", value=True)

# ----------------------------------------------------------------------
# CORPO PRINCIPAL
# ----------------------------------------------------------------------
st.title("🌧️ Precipitação horária · Unidades Petrobras")
cap = (f"Google WeatherNext 3 · inicialização {pd.Timestamp(init_iso):%d/%m/%Y %H UTC} · "
       f"estatística: {estatistica or '—'} · passo de {fmt(passo_h, 0)} h · horário de Brasília · "
       f"amostragem: {metodo.lower()}")
st.caption(cap)
if aviso:
    st.warning(aviso)
if passo_h > 1.01:
    st.info(f"Este conjunto de dados tem passo de {fmt(passo_h, 0)} h (não horário). "
            "Os valores 'hora a hora' representam a chuva em cada passo.")


def painel():
    # --- escolha do valor exibido -------------------------------------
    if modo == "acc":
        a, b = st.session_state["rng"]
        a, b = pd.Timestamp(a), pd.Timestamp(b)
        if b <= a:
            b = a + pd.Timedelta(hours=passo_h)
        vals = acumulado(df, a, b)
        edges = ACC_EDGES
        unid = "mm no intervalo"
        horas = (b - a).total_seconds() / 3600
        st.subheader(f"Acumulado de {fmt_t(a)} até {fmt_t(b)} · {fmt(horas, 0)} h")
        hora = None
    else:
        if st.session_state.get("tocando"):
            i = int(t_idx.searchsorted(pd.Timestamp(st.session_state["hora"])))
            st.session_state["hora"] = py(i + 1 if i < n - 1 else 1)
        st.slider("Instante (fim do passo)", min_value=py(1), max_value=py(n - 1), step=dt_step,
                  key="hora", format="DD/MM HH:mm")
        hora = pd.Timestamp(st.session_state["hora"])
        vals = df.loc[hora]
        edges = HORA_EDGES if passo_h <= 1.01 else ACC_EDGES
        unid = "mm/h" if passo_h <= 1.01 else f"mm em {fmt(passo_h, 0)} h"
        st.subheader(f"Chuva no passo encerrado em {fmt_t(hora)}")
        a = b = None

    v = vals.to_numpy(dtype=float)
    ok = np.isfinite(v)

    # --- métricas -----------------------------------------------------
    m1, m2, m3 = st.columns(3)
    if ok.any():
        im = int(np.nanargmax(v))
        m1.metric("Maior valor", f"{fmt(v[im])} {unid}", UNIDADES[im]["curto"], delta_color="off")
        m2.metric("Unidades com chuva (≥ 0,1)", f"{int((v[ok] >= 0.1).sum())} de {len(v)}")
        m3.metric("Média das unidades", f"{fmt(float(np.nanmean(v)))} {unid}")

    # --- seleção + mapa -----------------------------------------------
    st.selectbox("Unidade em destaque", [SEM_SEL] + NOMES, key="sel_unit",
                 help="Também dá para clicar numa unidade no mapa.")
    destaque = st.session_state["sel_unit"] if st.session_state["sel_unit"] != SEM_SEL else None
    st.plotly_chart(fig_mapa(v, edges, unid, destaque, mostrar_valores), width="stretch",
                    key="mapa", on_select=_on_map_select, selection_mode=("points",))

    # --- série temporal -----------------------------------------------
    if destaque:
        serie, titulo = df[destaque], destaque
    else:
        serie, titulo = df.mean(axis=1), f"Média das {len(NOMES)} unidades"
    st.plotly_chart(fig_serie(df, serie, passo_h, modo, a, b, hora, titulo), width="stretch")

    # --- ranking e downloads -------------------------------------------
    rank = pd.DataFrame({"Unidade": NOMES, unid: v}).sort_values(unid, ascending=False, na_position="last")
    st.dataframe(rank, hide_index=True, width="stretch", height=420,
                 column_config={unid: st.column_config.ProgressColumn(
                     unid, format="%.1f", min_value=0.0, max_value=float(max(np.nanmax(v) if ok.any() else 1.0, 1.0)))})
    d1, d2 = st.columns(2)
    d1.download_button("Baixar ranking (CSV)", rank.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig"),
                       file_name="ranking_precipitacao.csv", mime="text/csv", use_container_width=True)
    serie_csv = df.copy()
    serie_csv.index.name = "horario_brasilia"
    d2.download_button("Baixar série completa (CSV)", serie_csv.to_csv(sep=";", decimal=",").encode("utf-8-sig"),
                       file_name="precipitacao_series_unidades.csv", mime="text/csv", use_container_width=True)


if "sel_unit" not in st.session_state:
    st.session_state["sel_unit"] = SEM_SEL

tocando = modo == "hora" and st.session_state.get("tocando", False)
st.fragment(run_every=float(st.session_state.get("vel", 1.2)) if tocando else None)(painel)()

st.caption("Convenção: o valor de cada instante é a chuva do passo que termina nele; o acumulado entre A e B soma "
           "os passos depois de A até B, inclusive. Valores em mm (kg m⁻² s⁻¹ × 3600 × duração do passo).")
