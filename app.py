import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import math, datetime, random

st.set_page_config(page_title="⚛️ ElementVerse", page_icon="⚛️", layout="wide")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&display=swap');
#MainMenu,footer,.stDeployButton,div[data-testid="stToolbar"]{visibility:hidden;display:none;}
html,body,[class*="css"]{font-family:'Rajdhani',sans-serif;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#050a14 0%,#0a1628 100%);}
div[data-testid="metric-container"]{background:linear-gradient(135deg,#0d1b2e,#111d30);
    border-radius:12px;padding:12px 16px;border:1px solid #1e3050;
    box-shadow:0 4px 15px rgba(0,0,0,0.3);}
.stButton>button{background:linear-gradient(135deg,#1a3a5c,#0d2a4a);color:#7eb8f7;
    border:1px solid #2a5080;border-radius:8px;font-family:'Rajdhani',sans-serif;
    font-weight:600;transition:all 0.2s;}
.stButton>button:hover{background:linear-gradient(135deg,#2a5080,#1a3a6a);color:#aad4ff;}
</style>""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("elements.csv")
df = load_data()

TYPE_COLORS = {
    "Alkali Metal":"#FF6B6B","Alkaline Earth":"#FFA94D",
    "Transition Metal":"#4DABF7","Post-transition":"#38D9A9",
    "Metalloid":"#CC5DE8","Nonmetal":"#69DB7C",
    "Halogen":"#FFD43B","Noble Gas":"#868E96",
    "Lanthanide":"#F06595","Actinide":"#FF8787",
}
PERIOD_COLORS = {1:"#4DABF7",2:"#69DB7C",3:"#FFA94D",4:"#FF6B6B",5:"#CC5DE8",6:"#F06595",7:"#38D9A9"}

# La at (3,6) and Ac at (3,7) fixes the blank gap after Ba and Ra
POSITIONS = {
    'H':(1,1),'He':(18,1),
    'Li':(1,2),'Be':(2,2),'B':(13,2),'C':(14,2),'N':(15,2),'O':(16,2),'F':(17,2),'Ne':(18,2),
    'Na':(1,3),'Mg':(2,3),'Al':(13,3),'Si':(14,3),'P':(15,3),'S':(16,3),'Cl':(17,3),'Ar':(18,3),
    'K':(1,4),'Ca':(2,4),'Sc':(3,4),'Ti':(4,4),'V':(5,4),'Cr':(6,4),'Mn':(7,4),'Fe':(8,4),
    'Co':(9,4),'Ni':(10,4),'Cu':(11,4),'Zn':(12,4),'Ga':(13,4),'Ge':(14,4),'As':(15,4),
    'Se':(16,4),'Br':(17,4),'Kr':(18,4),
    'Rb':(1,5),'Sr':(2,5),'Y':(3,5),'Zr':(4,5),'Nb':(5,5),'Mo':(6,5),'Tc':(7,5),'Ru':(8,5),
    'Rh':(9,5),'Pd':(10,5),'Ag':(11,5),'Cd':(12,5),'In':(13,5),'Sn':(14,5),'Sb':(15,5),
    'Te':(16,5),'I':(17,5),'Xe':(18,5),
    'Cs':(1,6),'Ba':(2,6),'La':(3,6),'Hf':(4,6),'Ta':(5,6),'W':(6,6),'Re':(7,6),'Os':(8,6),
    'Ir':(9,6),'Pt':(10,6),'Au':(11,6),'Hg':(12,6),'Tl':(13,6),'Pb':(14,6),'Bi':(15,6),
    'Po':(16,6),'At':(17,6),'Rn':(18,6),
    'Fr':(1,7),'Ra':(2,7),'Ac':(3,7),'Rf':(4,7),'Db':(5,7),'Sg':(6,7),'Bh':(7,7),'Hs':(8,7),
    'Mt':(9,7),'Ds':(10,7),'Rg':(11,7),'Cn':(12,7),'Nh':(13,7),'Fl':(14,7),'Mc':(15,7),
    'Lv':(16,7),'Ts':(17,7),'Og':(18,7),
    'Ce':(4,9),'Pr':(5,9),'Nd':(6,9),'Pm':(7,9),'Sm':(8,9),'Eu':(9,9),'Gd':(10,9),
    'Tb':(11,9),'Dy':(12,9),'Ho':(13,9),'Er':(14,9),'Tm':(15,9),'Yb':(16,9),'Lu':(17,9),
    'Th':(4,10),'Pa':(5,10),'U':(6,10),'Np':(7,10),'Pu':(8,10),'Am':(9,10),'Cm':(10,10),
    'Bk':(11,10),'Cf':(12,10),'Es':(13,10),'Fm':(14,10),'Md':(15,10),'No':(16,10),'Lr':(17,10),
}

FUN_FACTS = {
    'H':"Hydrogen makes up ~75% of all normal matter in the universe.",
    'He':"Helium was discovered in the Sun before it was found on Earth.",
    'Li':"Lithium powers your smartphone and electric vehicle batteries.",
    'C':"Diamond and graphite are both pure carbon — same element, totally different structure!",
    'N':"78% of the air you breathe is nitrogen gas.",
    'O':"Oxygen was independently discovered by two scientists who never collaborated.",
    'F':"Fluorine is so reactive it can set glass on fire!",
    'Na':"Sodium explodes violently when it touches water.",
    'Mg':"Magnesium burns with brilliant white light — used in early camera flashes.",
    'Al':"Once more valuable than gold — Napoleon served guests with aluminium cutlery.",
    'Si':"Silicon Valley is named after the element powering all modern computers.",
    'Fe':"Iron makes up about 85% of Earth's solid core.",
    'Cu':"Copper was the first metal worked by humans, over 10,000 years ago.",
    'Au':"All gold ever mined could fill only about 3.5 Olympic swimming pools.",
    'Ag':"Silver has the highest electrical conductivity of any element.",
    'Hg':"Mercury is the only metal that is liquid at room temperature.",
    'W':"Tungsten has the highest melting point of any element at 3695 K!",
    'Os':"Osmium is the densest naturally occurring element at 22.59 g/cm3.",
    'Pt':"All platinum ever mined would fit inside your living room.",
    'U':"Uranium powers about 10% of the world electricity via nuclear plants.",
    'Ra':"Radium was discovered by Marie Curie who coined the term radioactivity.",
    'K':"Potassium is essential for your heart to beat.",
    'Ca':"Calcium makes up 99% of the minerals in human bones and teeth.",
    'La':"Lanthanum is used in camera lenses, telescope glass, and hybrid car batteries.",
    'Ac':"Actinium is so radioactive it glows blue in the dark!",
}

COMMON_USES = {
    'H':"Rocket fuel, fuel cells, hydrogenation of oils, weather balloons",
    'He':"MRI machines, party balloons, cryogenics, deep-sea diving gas",
    'Li':"Rechargeable batteries, mood medication, aircraft alloys, glass",
    'C':"Steel, diamonds, graphite pencils, plastics, carbon fiber",
    'N':"Fertilizers, explosives, liquid nitrogen, food packaging",
    'O':"Medical life support, steel production, water treatment, rocket fuel",
    'Fe':"Construction steel, vehicles, magnets, hemoglobin in blood",
    'Au':"Jewelry, electronics contacts, dentistry, financial reserves",
    'Ag':"Photography, antimicrobial coatings, solar panels, mirrors",
    'Cu':"Electrical wiring, plumbing, coins, circuit boards",
    'Si':"Microchips, solar panels, glass, concrete, silicones",
    'Al':"Aircraft, food packaging, construction, electrical cables",
    'Cl':"Water purification, PVC plastic, disinfectants, pharmaceuticals",
    'Ca':"Cement, antacids, supplements, steelmaking, cheese",
    'Pt':"Catalytic converters, cancer drugs, laboratory equipment, jewelry",
    'W':"Light bulb filaments, cutting tools, armor-piercing ammunition",
}

PAGES = ["Home","Periodic Table","Property Trends","Compare Elements","Element Quiz","Full Database"]
PAGE_ICONS = {"Home":"🏠","Periodic Table":"⚛️","Property Trends":"📊","Compare Elements":"⚖️","Element Quiz":"🎯","Full Database":"📋"}

for k,v in [('selected_element','H'),('nav_page','Home'),
            ('quiz',{'active':False,'q_idx':0,'score':0,'answers':[],'questions':[]})]:
    if k not in st.session_state:
        st.session_state[k] = v

def safe(v, suf="", d=4):
    try:
        f = float(v)
        return "N/A" if math.isnan(f) else f"{f:.{d}g}{suf}"
    except:
        return "N/A"

def get_state(row):
    try:
        mp = float(row.get('MeltingPoint_K','nan'))
        bp = float(row.get('BoilingPoint_K','nan'))
        T = 298
        if not math.isnan(mp) and mp > T: return "Solid","#4DABF7"
        if not math.isnan(bp) and bp < T: return "Gas","#69DB7C"
        if not math.isnan(mp) and not math.isnan(bp) and mp < T < bp: return "Liquid","#FF6B6B"
    except:
        pass
    return "Unknown","#868E96"

def hex_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

def darken(h, f=0.55):
    r,g,b = hex_rgb(h)
    return f"rgb({int(r*f)},{int(g*f)},{int(b*f)})"

@st.cache_data
def precompute_ptable():
    _df = pd.read_csv("elements.csv")
    result = {}
    for _, row in _df.iterrows():
        sym = row['Symbol']
        if sym not in POSITIONS: continue
        gx,gy = POSITIONS[sym]
        py = -gy * 1.18
        col = TYPE_COLORS.get(str(row.get('Type','')), '#444')
        name = str(row['Name'])
        z = int(row['AtomicNumber'])

        ns = [
            dict(type="rect",x0=gx-.43+.05,y0=py-.48-.05,x1=gx+.43+.05,y1=py+.48-.05,
                 fillcolor='rgba(0,0,0,0.55)',line=dict(width=0),layer="below"),
            dict(type="rect",x0=gx-.43,y0=py-.48,x1=gx+.43,y1=py+.48,
                 fillcolor=col,line=dict(color=darken(col),width=0.8),opacity=0.90,layer="below"),
            dict(type="rect",x0=gx-.43,y0=py+.29,x1=gx+.43,y1=py+.48,
                 fillcolor='rgba(255,255,255,0.28)',line=dict(width=0),layer="below"),
            dict(type="rect",x0=gx-.43,y0=py-.48,x1=gx-.28,y1=py+.48,
                 fillcolor='rgba(255,255,255,0.11)',line=dict(width=0),layer="below"),
        ]
        ss = [
            dict(type="rect",x0=gx-.47,y0=py-.51,x1=gx+.47,y1=py+.51,
                 fillcolor='white',line=dict(color=col,width=3.5),layer="below"),
            dict(type="rect",x0=gx-.43,y0=py-.47,x1=gx+.43,y1=py+.47,
                 fillcolor=col,line=dict(width=0),opacity=0.18,layer="below"),
        ]
        na = [
            dict(x=gx,y=py+.32,text=str(z),showarrow=False,font=dict(size=5.5,color='rgba(255,255,255,0.58)')),
            dict(x=gx,y=py+.06,text=f"<b>{sym}</b>",showarrow=False,font=dict(size=10.5,color='white')),
            dict(x=gx,y=py-.27,text=name,showarrow=False,font=dict(size=4.5,color='rgba(255,255,255,0.55)')),
        ]
        sa = [
            dict(x=gx,y=py+.32,text=str(z),showarrow=False,font=dict(size=5.5,color=col)),
            dict(x=gx,y=py+.06,text=f"<b>{sym}</b>",showarrow=False,font=dict(size=10.5,color=col)),
            dict(x=gx,y=py-.27,text=name,showarrow=False,font=dict(size=4.5,color=col)),
        ]

        def fv(v, s=""):
            try:
                f = float(v)
                return f"{f:.4g}{s}" if not math.isnan(f) else "N/A"
            except:
                return "N/A"

        state_l,_ = get_state(row)
        hover = (f"<b>{name} ({sym})</b><br>"
                 f"Z={z} | {row.get('Type','')} | {state_l}<br>"
                 f"Period {int(row['Period'])} | Group {int(row['Group'])}<br><br>"
                 f"EN: {fv(row.get('Electronegativity'))} Pauling<br>"
                 f"Radius: {fv(row.get('AtomicRadius_pm'),' pm')}<br>"
                 f"Melting: {fv(row.get('MeltingPoint_K'),' K')}<br>"
                 f"Boiling: {fv(row.get('BoilingPoint_K'),' K')}<br>"
                 f"Density: {fv(row.get('Density_gcm3'),' g/cm3')}")

        result[sym] = {'ns':ns,'ss':ss,'na':na,'sa':sa,'gx':gx,'py':py,'hover':hover}
    return result

def build_ptable(sel):
    data = precompute_ptable()
    shapes,anns = [],[]
    cx,cy,csym,chov = [],[],[],[]
    for sym,d in data.items():
        shapes += (d['ss'] if sym==sel else d['ns'])
        anns   += (d['sa'] if sym==sel else d['na'])
        cx.append(d['gx']); cy.append(d['py'])
        csym.append(sym); chov.append(d['hover'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=cx,y=cy,mode='markers',
        marker=dict(size=24,opacity=0,symbol='square'),
        text=csym,customdata=csym,
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=chov,name=''))

    for p in range(1,8):
        fig.add_annotation(x=0.1,y=-p*1.18,text=str(p),showarrow=False,
                          font=dict(size=9,color='#2a4060'),xanchor='right')
    for g in range(1,19):
        fig.add_annotation(x=g,y=0.68,text=str(g),showarrow=False,font=dict(size=7,color='#2a4060'))
    fig.add_annotation(x=3.5,y=-8.5*1.18,text="Ce to Lu (Lanthanides)",
                      showarrow=False,font=dict(size=8,color='#F06595'),xanchor='left')
    fig.add_annotation(x=3.5,y=-9.5*1.18,text="Th to Lr (Actinides)",
                      showarrow=False,font=dict(size=8,color='#FF8787'),xanchor='left')
    fig.add_annotation(x=9.5,y=0.68,
                      text=f"Selected: {sel}  |  Scroll to zoom  |  Drag to pan",
                      showarrow=False,font=dict(size=9,color='#2a5070'))
    fig.update_layout(
        shapes=shapes,annotations=anns,
        paper_bgcolor='#050a14',plot_bgcolor='#050a14',height=610,
        margin=dict(l=28,r=10,t=10,b=10),
        xaxis=dict(range=[0.1,19.2],showgrid=False,zeroline=False,showticklabels=False,fixedrange=False),
        yaxis=dict(range=[-13.2,1.3],showgrid=False,zeroline=False,showticklabels=False,fixedrange=False),
        showlegend=False,dragmode='pan',
        hoverlabel=dict(bgcolor='#0a1628',bordercolor='#1e3050',font=dict(size=12,color='white')),
        modebar_add=['zoom','pan','zoomIn2d','zoomOut2d','resetScale2d'],
        modebar_bgcolor='#0a1628',modebar_color='#2a5070',modebar_activecolor='#4DABF7')
    return fig

def draw_bohr(z, symbol, el_type):
    sl = [2,8,18,32,32,18,8]
    shells,rem = [],z
    for lim in sl:
        if rem <= 0: break
        n = min(rem,lim); shells.append(n); rem -= n
    color = TYPE_COLORS.get(el_type,'#888')
    fs = min(5.5,2.5+len(shells)*0.55)
    fig,ax = plt.subplots(figsize=(fs,fs))
    fig.patch.set_facecolor('#050a14'); ax.set_facecolor('#050a14')
    ax.set_aspect('equal'); ax.axis('off')
    for rg in [0.40,0.31,0.22]:
        ax.add_patch(plt.Circle((0,0),rg,color=color,alpha=0.13,zorder=8))
    ax.add_patch(plt.Circle((0,0),0.20,color=color,zorder=10))
    ax.text(0,0,symbol,ha='center',va='center',fontsize=9,fontweight='bold',color='white',zorder=11)
    for i,ne in enumerate(shells):
        r = 0.42+i*0.40
        ax.add_patch(plt.Circle((0,0),r,fill=False,color='#1a2a40',linewidth=1.2,zorder=5))
        for j in range(ne):
            ang = 2*math.pi*j/ne-math.pi/2
            ex,ey = r*math.cos(ang),r*math.sin(ang)
            ax.add_patch(plt.Circle((ex,ey),0.09,color=color,alpha=0.25,zorder=9))
            ax.add_patch(plt.Circle((ex,ey),0.065,color=color,zorder=10))
        ax.text(r+0.08,0.04,f"n={i+1} ({ne}e)",fontsize=6.5,color='#3a5577',va='center')
    mr = 0.42+len(shells)*0.40+0.25
    ax.set_xlim(-mr,mr*1.5); ax.set_ylim(-mr,mr)
    ax.set_title(f'Bohr Model - {symbol} (Z={z})',color='#7eb8f7',fontsize=10,pad=8)
    plt.tight_layout(); return fig

def show_element_card(sym):
    rows = df[df['Symbol']==sym]
    if rows.empty: return
    row = rows.iloc[0]
    color = TYPE_COLORS.get(str(row.get('Type','')),'#888')
    state_l,state_c = get_state(row)
    r,g,b = hex_rgb(color)
    st.markdown("---")
    ci,cf,cb = st.columns([1,2.2,1.5])
    with ci:
        st.markdown(
            f"<div style='background:linear-gradient(145deg,rgba({r},{g},{b},0.12),rgba({r},{g},{b},0.05));"
            f"border:2px solid {color};border-radius:18px;padding:22px 12px;text-align:center;"
            f"box-shadow:0 8px 32px rgba({r},{g},{b},0.25)'>"
            f"<div style='font-size:64px;font-weight:900;color:{color};"
            f"line-height:1.05;text-shadow:0 0 20px rgba({r},{g},{b},0.5)'>{row['Symbol']}</div>"
            f"<div style='font-size:17px;color:#ccd6f6;margin-top:6px;font-weight:700'>{row['Name']}</div>"
            f"<div style='font-size:12px;color:#4a6a8a'>Z = {int(row['AtomicNumber'])}</div>"
            f"<div style='margin-top:10px;display:flex;gap:6px;justify-content:center;flex-wrap:wrap'>"
            f"<span style='background:rgba({r},{g},{b},0.2);border:1px solid {color};border-radius:20px;"
            f"padding:3px 10px;font-size:11px;color:{color};font-weight:700'>{row.get('Type','')}</span>"
            f"<span style='border:1px solid {state_c};border-radius:20px;padding:3px 10px;"
            f"font-size:11px;color:{state_c}'>{state_l}</span></div>"
            f"<div style='margin-top:6px;font-size:11px;color:#3a5577'>"
            f"Period {int(row['Period'])} | Group {int(row['Group'])}</div></div>",
            unsafe_allow_html=True)
        disc = row.get('Discoverer','Unknown')
        year = row.get('YearDiscovered','?')
        st.markdown(
            f"<div style='margin-top:10px;background:linear-gradient(135deg,#0a1628,#0d1e35);"
            f"border-radius:12px;padding:12px;text-align:center;border:1px solid #1e3050'>"
            f"<span style='color:#4a6a8a;font-size:11px'>Discovered by</span><br>"
            f"<span style='color:#ccd6f6;font-weight:600;font-size:13px'>{disc}</span><br>"
            f"<span style='color:{color};font-size:16px;font-weight:800'>{year}</span></div>",
            unsafe_allow_html=True)
        cfg = str(row.get('ElectronConfig',''))
        if cfg not in ['','Unknown','nan']:
            st.markdown(
                f"<div style='margin-top:10px;background:#080e1a;border-left:3px solid {color};"
                f"border-radius:6px;padding:8px 12px;color:{color};font-size:12px'>{cfg}</div>",
                unsafe_allow_html=True)
    with cf:
        st.markdown("**Physical Properties**")
        p1,p2,p3,p4 = st.columns(4)
        with p1: st.metric("Melting",safe(row.get('MeltingPoint_K')," K"))
        with p2: st.metric("Boiling",safe(row.get('BoilingPoint_K')," K"))
        with p3: st.metric("Density",safe(row.get('Density_gcm3')," g/cm3",3))
        with p4: st.metric("Radius",safe(row.get('AtomicRadius_pm')," pm",3))
        st.markdown("**Chemical Properties**")
        p5,p6,p7,p8 = st.columns(4)
        with p5: st.metric("Electronegativity",safe(row.get('Electronegativity'),"",3))
        with p6: st.metric("Ionization E",safe(row.get('IonizationEnergy_kJmol')," kJ/mol"))
        with p7: st.metric("Electron Affinity",safe(row.get('ElectronAffinity_kJmol')," kJ/mol"))
        with p8: st.metric("Atomic No.",int(row['AtomicNumber']))
        fact = FUN_FACTS.get(sym,"A fascinating element with unique properties in chemistry.")
        uses = COMMON_USES.get(sym,"Used in various industrial, scientific, and commercial applications.")
        st.info(f"**Fun Fact:** {fact}")
        st.success(f"**Common Uses:** {uses}")
    with cb:
        bf = draw_bohr(int(row['AtomicNumber']),row['Symbol'],str(row.get('Type','')))
        st.pyplot(bf,use_container_width=True); plt.close()

# Sidebar
st.sidebar.markdown("## ⚛ ElementVerse")
st.sidebar.caption("Periodic Table Explorer")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate",PAGES,key='nav_page')
st.sidebar.markdown("---")
st.sidebar.markdown("**Element Types**")
for t,c in TYPE_COLORS.items():
    cnt = len(df[df['Type']==t])
    r2,g2,b2 = hex_rgb(c)
    st.sidebar.markdown(
        f"<div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:4px'>"
        f"<span style='background:rgba({r2},{g2},{b2},0.15);border:1px solid {c};"
        f"padding:2px 8px;border-radius:4px;font-size:11px;color:{c}'>{t}</span>"
        f"<span style='font-size:10px;color:#1e3050'>{cnt}</span></div>",
        unsafe_allow_html=True)

# HOME
if page == "Home":
    st.markdown("# ⚛ ElementVerse")
    st.markdown("**Interactive Periodic Table Explorer** — 118 Elements | 3D Table | Bohr Models | Charts | Quiz")
    st.markdown("---")

    c1,c2,c3,c4 = st.columns(4)
    metals = len(df[df['Type'].isin(['Alkali Metal','Alkaline Earth','Transition Metal','Post-transition','Lanthanide','Actinide'])])
    with c1: st.metric("Total Elements","118")
    with c2: st.metric("Metals",str(metals))
    with c3: st.metric("Nonmetals and Gases",str(len(df[df['Type'].isin(['Nonmetal','Noble Gas','Halogen'])])))
    with c4: st.metric("Synthetic (Z>=95)",str(len(df[df['AtomicNumber']>=95])))

    st.markdown("---")
    col_a,col_b = st.columns([1.3,1])
    with col_a:
        st.subheader("Element of the Day")
        doy = datetime.date.today().timetuple().tm_yday
        valid = df[df['Symbol'].isin(POSITIONS.keys())]
        eod = valid.iloc[doy % len(valid)]
        color = TYPE_COLORS.get(str(eod.get('Type','')),'#888')
        state_l,state_c = get_state(eod)
        r2,g2,b2 = hex_rgb(color)
        st.markdown(
            f"<div style='background:linear-gradient(135deg,rgba({r2},{g2},{b2},0.10),rgba({r2},{g2},{b2},0.05));"
            f"border:2px solid {color};border-radius:16px;padding:24px;"
            f"box-shadow:0 8px 32px rgba({r2},{g2},{b2},0.2)'>"
            f"<div style='display:flex;align-items:center;gap:20px'>"
            f"<div style='font-size:56px;color:{color};min-width:80px;text-align:center;font-weight:900;"
            f"text-shadow:0 0 20px rgba({r2},{g2},{b2},0.5)'>{eod['Symbol']}</div>"
            f"<div><div style='font-size:22px;color:#ccd6f6;font-weight:700'>{eod['Name']}</div>"
            f"<div style='color:#4a6a8a;font-size:13px'>Z={int(eod['AtomicNumber'])} | Period {int(eod['Period'])} | Group {int(eod['Group'])}</div>"
            f"<div style='margin-top:8px;display:flex;gap:6px'>"
            f"<span style='background:rgba({r2},{g2},{b2},0.2);border:1px solid {color};"
            f"border-radius:20px;padding:2px 10px;font-size:11px;color:{color}'>{eod.get('Type','')}</span>"
            f"<span style='border:1px solid {state_c};border-radius:20px;padding:2px 10px;"
            f"font-size:11px;color:{state_c}'>{state_l}</span>"
            f"</div></div></div>"
            f"<div style='margin-top:14px;color:#7a9ab8;font-size:13px;line-height:1.6'>"
            f"{FUN_FACTS.get(eod['Symbol'],'A fascinating element with unique properties.')}</div>"
            f"</div>",unsafe_allow_html=True)

    with col_b:
        st.subheader("Quick Access")
        if st.button("Open Periodic Table",use_container_width=True):
            st.session_state.nav_page = "Periodic Table"; st.rerun()
        st.markdown("")
        if st.button("View Property Charts",use_container_width=True):
            st.session_state.nav_page = "Property Trends"; st.rerun()
        st.markdown("")
        if st.button("Compare Elements",use_container_width=True):
            st.session_state.nav_page = "Compare Elements"; st.rerun()
        st.markdown("")
        if st.button("Start Element Quiz",use_container_width=True):
            st.session_state.quiz = {'active':True,'q_idx':0,'score':0,'answers':[],'questions':[]}
            st.session_state.nav_page = "Element Quiz"; st.rerun()
        st.markdown("")
        if st.button("Browse Full Database",use_container_width=True):
            st.session_state.nav_page = "Full Database"; st.rerun()

# PERIODIC TABLE
elif page == "Periodic Table":
    @st.fragment
    def ptable_fragment():
        sel = st.session_state.get('selected_element','H')
        fig = build_ptable(sel)
        event = st.plotly_chart(fig,on_select="rerun",key="ptable",
                               use_container_width=True,selection_mode="points")
        if event and hasattr(event,'selection') and event.selection:
            pts = event.selection.get('points',[])
            if pts:
                clicked = pts[0].get('customdata') or pts[0].get('text','')
                if isinstance(clicked,(list,tuple)): clicked = clicked[0]
                if clicked and str(clicked) in df['Symbol'].values and str(clicked) != sel:
                    st.session_state.selected_element = str(clicked)
                    st.rerun(scope="fragment")
        lc = st.columns(len(TYPE_COLORS))
        for i,(t,c) in enumerate(TYPE_COLORS.items()):
            rr,gg,bb = hex_rgb(c)
            with lc[i]:
                st.markdown(
                    f"<div style='background:rgba({rr},{gg},{bb},0.15);border:1px solid {c};"
                    f"border-radius:6px;padding:4px;text-align:center;font-size:9px;color:{c}'>{t}</div>",
                    unsafe_allow_html=True)
        st.markdown("")
        sc,_ = st.columns([1.5,4])
        with sc:
            all_names = df['Name'].tolist()
            try: cur_idx = all_names.index(df[df['Symbol']==sel].iloc[0]['Name'])
            except: cur_idx = 0
            chosen = st.selectbox("Jump to element",all_names,index=cur_idx,label_visibility="collapsed")
            if chosen:
                new_sym = df[df['Name']==chosen].iloc[0]['Symbol']
                if new_sym != sel:
                    st.session_state.selected_element = new_sym
                    st.rerun(scope="fragment")
        show_element_card(sel)
    ptable_fragment()

# PROPERTY TRENDS
elif page == "Property Trends":
    st.markdown("# Property Trends")
    PROPS = {
        "Electronegativity":{"col":"Electronegativity","unit":"Pauling",
            "trend":"Increases left to right across a period; decreases top to bottom down a group.",
            "insight":"Fluorine (F) is the most electronegative element at 3.98."},
        "Atomic Radius":{"col":"AtomicRadius_pm","unit":"pm",
            "trend":"Decreases left to right; increases top to bottom.",
            "insight":"Francium (Fr) has the largest radius at 280 pm."},
        "Ionization Energy":{"col":"IonizationEnergy_kJmol","unit":"kJ/mol",
            "trend":"Increases left to right; noble gases have highest values.",
            "insight":"Helium has the highest 1st ionization energy at 2372 kJ/mol."},
        "Electron Affinity":{"col":"ElectronAffinity_kJmol","unit":"kJ/mol",
            "trend":"Halogens have the highest values; noble gases are near zero.",
            "insight":"Chlorine has the highest electron affinity at 349 kJ/mol."},
        "Melting Point":{"col":"MeltingPoint_K","unit":"K",
            "trend":"Transition metals generally have high melting points.",
            "insight":"Tungsten (W) melts at 3695 K, the highest of all elements."},
        "Boiling Point":{"col":"BoilingPoint_K","unit":"K",
            "trend":"Metals boil at very high temperatures; noble gases boil very low.",
            "insight":"Tungsten (W) has the highest boiling point at 5828 K."},
        "Density":{"col":"Density_gcm3","unit":"g/cm3",
            "trend":"Generally increases down a group.",
            "insight":"Osmium (Os) is the densest element at 22.59 g/cm3."},
    }
    ca,cb,cc = st.columns(3)
    with ca: sp = st.selectbox("Property",list(PROPS.keys()))
    with cb:
        per_opts = ["All Periods"]+[f"Period {p}" for p in sorted(df["Period"].unique())]
        sper = st.selectbox("Period",per_opts)
    with cc:
        cby = st.selectbox("Colour by",["Element Type","Period"])
        ctype = st.radio("Chart type",["Bar","Line","Scatter"],horizontal=True)

    prop = PROPS[sp]; col = prop["col"]
    fdf = df.copy() if sper=="All Periods" else df[df["Period"]==int(sper.split()[1])].copy()
    pdf = fdf.dropna(subset=[col]).copy()
    if sp != "Electron Affinity":
        pdf = pdf[pd.to_numeric(pdf[col],errors='coerce').fillna(0)!=0]
    pdf[col] = pd.to_numeric(pdf[col],errors='coerce')
    pdf = pdf.dropna(subset=[col])

    if not pdf.empty:
        m1,m2,m3,m4 = st.columns(4)
        mn = pdf.loc[pdf[col].idxmin()]; mx = pdf.loc[pdf[col].idxmax()]
        with m1: st.metric("Min",f"{mn[col]:.3g}",delta=mn['Name'])
        with m2: st.metric("Max",f"{mx[col]:.3g}",delta=mx['Name'])
        with m3: st.metric("Average",f"{pdf[col].mean():.3g}")
        with m4: st.metric("Elements",len(pdf))

        pdf['_color'] = (pdf['Type'].map(TYPE_COLORS) if cby=="Element Type" else pdf['Period'].map(PERIOD_COLORS))
        if ctype == "Bar":
            fig2 = go.Figure(go.Bar(x=pdf['Symbol'],y=pdf[col],marker_color=pdf['_color'],
                hovertemplate='<b>%{x}</b><br>'+prop['unit']+': %{y:.4g}<extra></extra>'))
        elif ctype == "Line":
            fig2 = go.Figure()
            for period in sorted(pdf['Period'].unique()):
                pd_ = pdf[pdf['Period']==period]
                fig2.add_trace(go.Scatter(x=pd_['Symbol'],y=pd_[col],mode='lines+markers',
                    name=f"Period {period}",line=dict(color=PERIOD_COLORS.get(period,'#aaa'),width=2.5),
                    marker=dict(size=7)))
        else:
            fig2 = go.Figure(go.Scatter(x=pdf['AtomicNumber'],y=pdf[col],mode='markers',
                marker=dict(color=pdf['_color'],size=10,line=dict(color='#050a14',width=1)),
                text=pdf['Symbol'],hovertemplate='<b>%{text}</b><br>%{y:.4g}<extra></extra>'))
            fig2.update_xaxes(title='Atomic Number')

        fig2.update_layout(template='plotly_dark',paper_bgcolor='#050a14',plot_bgcolor='#080e1a',
            height=420,yaxis_title=f"{sp} ({prop['unit']})",
            xaxis=dict(gridcolor='#0d1e35'),yaxis=dict(gridcolor='#0d1e35'),
            legend=dict(bgcolor='#0a1628',bordercolor='#1e3050'),
            margin=dict(l=60,r=20,t=20,b=60),showlegend=(ctype=="Line"))
        st.plotly_chart(fig2,use_container_width=True)
        t1,t2 = st.columns(2)
        with t1: st.info(f"**Trend:** {prop['trend']}")
        with t2: st.success(f"**Key Insight:** {prop['insight']}")

# COMPARE ELEMENTS
elif page == "Compare Elements":
    st.markdown("# Compare Elements")
    st.markdown("---")
    all_names = df["Name"].tolist()
    cc1,cc2 = st.columns(2)
    with cc1: el1 = st.selectbox("Element 1",all_names,index=0)
    with cc2: el2 = st.selectbox("Element 2",all_names,index=5)
    r1 = df[df["Name"]==el1].iloc[0]
    r2 = df[df["Name"]==el2].iloc[0]
    c1c = TYPE_COLORS.get(str(r1.get('Type','')),'#4DABF7')
    c2c = TYPE_COLORS.get(str(r2.get('Type','')),'#FF6B6B')

    props_r = ['Electronegativity','AtomicRadius_pm','IonizationEnergy_kJmol','ElectronAffinity_kJmol','Density_gcm3']
    labels_r = ['Electronegativity','Atomic Radius','Ionization Energy','Electron Affinity','Density']
    v1,v2 = [],[]
    for p in props_r:
        cd = pd.to_numeric(df[p],errors='coerce').dropna()
        mn2,mx2 = cd.min(),cd.max()
        for vals,row in [(v1,r1),(v2,r2)]:
            try:
                fv = float(row.get(p,0))
                vals.append(0 if math.isnan(fv) or mx2==mn2 else round((fv-mn2)/(mx2-mn2)*10,2))
            except:
                vals.append(0)

    rr1,rg1,rb1 = hex_rgb(c1c); rr2,rg2,rb2 = hex_rgb(c2c)
    radar = go.Figure()
    for vals,name,color,rgba in [
        (v1,r1['Name'],c1c,f"rgba({rr1},{rg1},{rb1},0.25)"),
        (v2,r2['Name'],c2c,f"rgba({rr2},{rg2},{rb2},0.25)")]:
        radar.add_trace(go.Scatterpolar(r=vals+[vals[0]],theta=labels_r+[labels_r[0]],
            fill='toself',name=name,line=dict(color=color,width=2.5),fillcolor=rgba))
    radar.update_layout(
        polar=dict(radialaxis=dict(visible=True,range=[0,10],color='#3a5577',gridcolor='#1a2a40'),
                  angularaxis=dict(color='#7eb8f7',gridcolor='#1a2a40'),bgcolor='#050a14'),
        showlegend=True,paper_bgcolor='#050a14',
        legend=dict(bgcolor='#0a1628',bordercolor='#1e3050'),height=380,
        margin=dict(l=60,r=60,t=30,b=30))
    st.plotly_chart(radar,use_container_width=True)

    fields = [("Atomic Number","AtomicNumber"),("Period","Period"),("Group","Group"),("Type","Type"),
              ("Electronegativity","Electronegativity"),("Atomic Radius (pm)","AtomicRadius_pm"),
              ("Ionization Energy (kJ/mol)","IonizationEnergy_kJmol"),
              ("Electron Affinity (kJ/mol)","ElectronAffinity_kJmol"),
              ("Melting Point (K)","MeltingPoint_K"),("Boiling Point (K)","BoilingPoint_K"),
              ("Density (g/cm3)","Density_gcm3"),("Electron Config","ElectronConfig"),
              ("Discoverer","Discoverer"),("Year Discovered","YearDiscovered")]

    def fmt(row,key):
        v = row.get(key)
        try: f = float(v); return f"{f:.4g}" if not math.isnan(f) else "N/A"
        except: return str(v) if pd.notna(v) and str(v) not in ['nan',''] else "N/A"

    cl,cm,cr = st.columns([5,1,5])
    for side,rd,color in [(cl,r1,c1c),(cr,r2,c2c)]:
        with side:
            rr,rg,rb = hex_rgb(color)
            st.markdown(
                f"<div style='background:linear-gradient(145deg,rgba({rr},{rg},{rb},0.12),rgba({rr},{rg},{rb},0.05));"
                f"border:2px solid {color};border-radius:14px;padding:18px;text-align:center;"
                f"margin-bottom:16px;box-shadow:0 4px 20px rgba({rr},{rg},{rb},0.2)'>"
                f"<div style='font-size:52px;color:{color};font-weight:900;"
                f"text-shadow:0 0 15px rgba({rr},{rg},{rb},0.5)'>{rd['Symbol']}</div>"
                f"<div style='font-size:15px;color:#ccd6f6;font-weight:600'>{rd['Name']}</div>"
                f"<div style='font-size:12px;color:#4a6a8a'>Z = {int(rd['AtomicNumber'])}</div></div>",
                unsafe_allow_html=True)
            for label,key in fields:
                v1s = fmt(rd,key)
                other = r2 if rd['Symbol']==r1['Symbol'] else r1
                v2s = fmt(other,key)
                try:
                    f1 = float(str(v1s)[:10]); f2 = float(str(v2s)[:10])
                    ind = (" **▲**" if f1>f2 else " **▼**" if f1<f2 else "")
                except: ind=""
                st.markdown(f"**{label}:** {v1s}{ind}")
    with cm:
        st.markdown("<div style='text-align:center;padding-top:100px;font-size:28px'>vs</div>",unsafe_allow_html=True)

# ELEMENT QUIZ
elif page == "Element Quiz":
    st.markdown("# Element Quiz")

    def gen_qs(n=10):
        vdf = df[df['Symbol'].isin(POSITIONS.keys())].copy()
        qs = []
        for _ in range(n):
            qt = random.choice(['symbol','name','period','type','property'])
            elem = vdf.sample(1).iloc[0]
            if qt == 'symbol':
                q = f"What is the chemical symbol for **{elem['Name']}**?"
                correct = elem['Symbol']
                wrong = vdf[vdf['Symbol']!=correct].sample(3)['Symbol'].tolist()
            elif qt == 'name':
                q = f"What is the name of element **{elem['Symbol']}** (Z={int(elem['AtomicNumber'])})?",
                q = q[0]
                correct = elem['Name']
                wrong = vdf[vdf['Name']!=correct].sample(3)['Name'].tolist()
            elif qt == 'period':
                q = f"Which period is **{elem['Name']} ({elem['Symbol']})** in?"
                correct = str(int(elem['Period']))
                wrong = [str(p) for p in range(1,8) if str(p)!=correct][:3]
            elif qt == 'type':
                q = f"What type of element is **{elem['Name']} ({elem['Symbol']})**?"
                correct = str(elem.get('Type',''))
                wrong = [t for t in TYPE_COLORS if t!=correct][:3]
            else:
                pr = random.choice(['Electronegativity','AtomicRadius_pm','IonizationEnergy_kJmol'])
                cd = pd.to_numeric(vdf[pr],errors='coerce').dropna()
                if len(cd) < 4: continue
                best = vdf.loc[cd.idxmax(),'Name']
                pn = {'Electronegativity':'highest electronegativity',
                      'AtomicRadius_pm':'largest atomic radius',
                      'IonizationEnergy_kJmol':'highest ionization energy'}[pr]
                q = f"Which element has the **{pn}**?"
                correct = best
                wrong = vdf[vdf['Name']!=best].sample(3)['Name'].tolist()
            opts = [correct]+wrong[:3]; random.shuffle(opts)
            qs.append({'q':q,'correct':correct,'options':opts})
        return qs

    qs = st.session_state.quiz
    if not qs['active']:
        st.info("Test your chemistry knowledge! 10 questions covering symbols, names, periods, types, and properties.")
        if qs.get('answers'):
            sc = qs['score']; tot = len(qs['questions'])
            pct = int(sc/tot*100) if tot else 0
            st.metric("Last Score",f"{sc}/{tot}",delta=f"{pct}%")
        if st.button("Start Quiz"):
            st.session_state.quiz = {'active':True,'q_idx':0,'score':0,'answers':[],'questions':gen_qs()}
            st.rerun()
    else:
        questions = qs['questions']; qi = qs['q_idx']
        if qi >= len(questions):
            sc = qs['score']; tot = len(questions)
            pct = int(sc/tot*100) if tot else 0
            emoji = '🏆' if pct>=80 else '🥈' if pct>=50 else '📚'
            msg = 'Outstanding! You know your elements!' if pct>=80 else 'Good job! Keep exploring!' if pct>=50 else 'Keep studying the periodic table!'
            st.markdown(f"## {emoji} Quiz Complete!")
            st.metric("Final Score",f"{sc}/{tot}",delta=f"{pct}% - {msg}")
            c1,c2,_ = st.columns([1,1,2])
            with c1:
                if st.button("Try Again"):
                    st.session_state.quiz = {'active':True,'q_idx':0,'score':0,'answers':[],'questions':gen_qs()}
                    st.rerun()
            with c2:
                if st.button("Go Home"):
                    st.session_state.quiz['active'] = False
                    st.session_state.nav_page = "Home"; st.rerun()
        else:
            q = questions[qi]
            st.progress(qi/len(questions))
            st.caption(f"Question {qi+1} of {len(questions)} | Score: {qs['score']}")
            st.markdown(
                f"<div style='background:#0a1628;border:1px solid #1e3050;border-radius:14px;"
                f"padding:24px;margin-bottom:20px'>"
                f"<div style='font-size:18px;color:#ccd6f6;line-height:1.5'>{q['q']}</div></div>",
                unsafe_allow_html=True)
            answered = len(qs['answers']) > qi
            if not answered:
                for opt in q['options']:
                    if st.button(opt,key=f"opt_{qi}_{opt}"):
                        correct = (opt==q['correct'])
                        qs['answers'].append({'chosen':opt,'correct':q['correct'],'result':correct})
                        if correct: qs['score'] += 1
                        st.rerun()
            else:
                ans = qs['answers'][qi]
                for opt in q['options']:
                    if opt == q['correct']: st.success(f"Correct: {opt}")
                    elif opt == ans['chosen'] and not ans['result']: st.error(f"Your answer: {opt}")
                    else: st.write(f"  {opt}")
                if st.button("Next Question"):
                    qs['q_idx'] += 1; st.rerun()

# FULL DATABASE
elif page == "Full Database":
    st.markdown("# Full Elements Database")
    st.markdown("---")
    fc1,fc2,fc3 = st.columns(3)
    with fc1: tf = st.multiselect("Filter by Type",sorted(df["Type"].dropna().unique()))
    with fc2: pf = st.multiselect("Filter by Period",sorted(df["Period"].unique()))
    with fc3: sf = st.text_input("Search",placeholder="Name or Symbol")
    tdf = df.copy()
    if tf: tdf = tdf[tdf["Type"].isin(tf)]
    if pf: tdf = tdf[tdf["Period"].isin(pf)]
    if sf: tdf = tdf[tdf["Name"].str.lower().str.contains(sf.lower())|
                     tdf["Symbol"].str.lower().str.contains(sf.lower())]
    st.markdown(f"Showing **{len(tdf)}** of 118 elements")
    cols_s = ["Symbol","Name","AtomicNumber","Period","Group","Type","Electronegativity",
              "AtomicRadius_pm","IonizationEnergy_kJmol","ElectronAffinity_kJmol",
              "MeltingPoint_K","BoilingPoint_K","Density_gcm3","ElectronConfig","Discoverer","YearDiscovered"]
    st.dataframe(tdf[cols_s].reset_index(drop=True),use_container_width=True,height=550)
    st.download_button("Download filtered data as CSV",
                      tdf[cols_s].to_csv(index=False),"elements_filtered.csv","text/csv")
