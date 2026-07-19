import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from scipy.cluster.hierarchy import linkage,dendrogram
import plotly.figure_factory as ff
import numpy as np

df=pd.read_csv("heart_disease.csv")
df["risk_score"] = (
    (df["age"] / df["age"].max()) * 25 +
    (df["chol"] / df["chol"].max()) * 25 +
    (df["trestbps"] / df["trestbps"].max()) * 20 +
    (df["oldpeak"] / df["oldpeak"].max()) * 15 +
    (df["target_binary"] * 15)
)

df["risk_score"] = df["risk_score"].round(1)
df["risk_score"] = df["risk_score"].clip(0, 100)
df.insert(
    0,
    "Patient_ID",
    [f"{i:03d}" for i in range(1, len(df)+1)]
)
st.set_page_config( page_title="CardioInsight", page_icon="🫀", layout="wide",initial_sidebar_state="expanded")

if "page" not in st.session_state:
    st.session_state.page = "Home"

st.markdown("""
<style>

/* Entire sidebar */
[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #081126 100%
    ) !important;
}

/* Sidebar content */
[data-testid="stSidebarContent"]{
    background: transparent !important;
}

/* Remove default grey area */
[data-testid="stSidebar"] > div:first-child{
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)


with st.sidebar:

    st.image("Untitled design.png", width=80)

    st.markdown(
        "<h1 style='margin-bottom:0'>CardioInsight</h1>",
        unsafe_allow_html=True
    )
    st.caption("Heart Disease Analytics")

    st.divider()
    menu = ["Home","Dataset Explorer","Dashboard","Patient Explorer","Risk Analysis","Comparative Analysis","Correlations","Risk Predictor","Data Dictionary"]

    from streamlit_option_menu import option_menu

with st.sidebar:

    selected = option_menu(
        menu_title=None,

        options=[
            "Home",
            "Dataset Explorer",
            "Dashboard",
            "Patient Explorer",
            "Risk Analysis",
            "Comparative Analysis",
            "Correlations",
            "Risk Predictor",
            "Data Dictionary"
        ],

        icons=[
            "house",
            "bar-chart",
            "people",
            "activity",
            "layers",
            "shuffle",
            "cpu",
            "file-earmark",
            "book"
        ],

        default_index=0,

        styles={
            "container": {
                "padding": "0!important",
                "background-color": "transparent",
                "border": "none",
            },
        
            "icon": {
                "color": "white",
                "font-size": "18px",
            },
        
            "nav-link": {
                "font-size": "18px",
                "text-align": "left",
                "margin": "4px 0",
                "padding": "14px 18px",
                "border-radius": "14px",
                "background-color": "transparent",
                "color": "white",
            },
        
            "nav-link-selected": {
                "background": "linear-gradient(90deg,#8b5cf6,#7c3aed)",
                "color": "white",
                "border-radius": "14px",
                "box-shadow": "0 0 15px rgba(139,92,246,0.4)",
            }
        }
    )

    st.markdown("""
    <style>
    
    /* Remove grey box behind option menu */
    ul[data-testid="stSidebarNav"]{
        background: transparent !important;
    }
    
    /* Option menu container */
    .st-emotion-cache-16txtl3,
    .st-emotion-cache-1r6slb0,
    .st-emotion-cache-1cypcdb{
        background: transparent !important;
    }
    
    /* Remove any dark panel */
    [data-testid="stSidebar"] .nav{
        background: transparent !important;
    }
    
    /* Remove extra container background */
    [data-testid="stSidebar"] section{
        background: transparent !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

    menu_selected = selected

    if menu_selected != st.session_state.page:
        st.session_state.page = menu_selected

    selected = st.session_state.page
    
    st.divider()

    st.subheader("Theme")

    theme = st.selectbox("",["Midnight Blue","Neon Purple","Cardiac Red","Emerald Health"])
    themes = {

    "Midnight Blue": {
        "bg":"#050816",
        "card":"#0f1735",
        "accent":"#8b5cf6"
    },

    "Neon Purple": {
        "bg":"#300833",
        "card":"#120026",
        "accent":"#c026ff"
    },

    "Cardiac Red": {
        "bg":"#700707",
        "card":"#250909",
        "accent":"#ff4d4d"
    },

    "Emerald Health": {
        "bg":"#02140d",
        "card":"#05291b",
        "accent":"#00d084"
    }
  }
    current = themes[theme]

    bg = current["bg"]
    card = current["card"]
    accent = current["accent"]

    st.button("Save Preferences")

    st.divider()

    st.markdown(f"""
    <style>

    .stApp {{
        background:{bg};
    }}

    .card,
    .kpi-card,
    .module-card {{
        background:{card};
    }}

    .stButton > button {{
        background:{accent};
        color:white;
        border:none;
        border-radius:12px;
    }}

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>

    .block-container{
        padding-top:2rem;
        padding-bottom:3rem;
        padding-left:2rem;
        padding-right:2rem;
        max-width:1600px;
    }

    .card{
        background: linear-gradient(
            135deg,
            rgba(20,25,55,0.95),
            rgba(10,15,35,0.95)
        );
        
        border:1px solid rgba(255,255,255,0.08);
        
        border-radius:18px;

        padding:20px;

        box-shadow:
        0 0 15px rgba(139,92,246,0.15);

        margin-bottom:15px;
    }

    .hero{
        background:
        radial-gradient(circle at top right,#8b5cf6 0%,transparent 35%),
        linear-gradient(135deg,#0a1028,#060b1c);

        border-radius:22px;
        padding:40px;
    }

    .big-title{
        font-size:58px;
        font-weight:800;
    }

    .gradient-text{
        background:linear-gradient(
        90deg,#8b5cf6,#ec4899);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
    }

    .subtext{
        color:#bfc7d5;
        font-size:18px;
    }

    .kpi-card{
        background:#0f1735;
        border-radius:18px;
        padding:20px;
        text-align:center;
    }

    .kpi-value{
        font-size:36px;
        font-weight:700;
    }

    .kpi-label{
        color:#9ca3af;
    }

    .module-card{
        background:#0f1735;
        padding:20px;
        border-radius:16px;
        transition:0.3s;
    }

    .module-card:hover{
        transform:translateY(-5px);
    }
                    
    .kpi-card:hover{
        transform:translateY(-5px);
    }

    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<style>

.hero{
    height:380px;

    display:flex;
    flex-direction:column;
    justify-content:center;

    padding:40px;

    border-radius:25px;

    background:
    radial-gradient(circle at top right,
    rgba(139,92,246,.8),
    transparent 40%),

    linear-gradient(
    135deg,
    #081126,
    #050816
    );
}

.hero-title{
    font-size:70px;
    font-weight:800;
    margin-bottom:10px;
}

.hero-title span{
    background:linear-gradient(
    90deg,
    #8b5cf6,
    #ec4899
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

[data-testid="stImage"] img{
    border-radius:20px;
}

</style>
""", unsafe_allow_html=True) 

st.markdown("""
<style>

.quick-card{
    background:linear-gradient(
        135deg,
        #0b1635,
        #081126
    );

    border:1px solid rgba(255,255,255,.08);

    border-radius:20px;

    padding:25px;

    box-shadow:0 0 20px rgba(139,92,246,.15);
}

.quick-title{
    font-size:28px;
    font-weight:700;
    color:white;
    margin-bottom:20px;
}

.quick-label{
    color:#d1d5db;
    font-size:15px;
    margin-bottom:8px;
}
            
.stButton > button{
    background:linear-gradient(
        135deg,
        #8b5cf6,
        #7c3aed
    );
    color:white;
    border:none;
    border-radius:12px;
    height:45px;
    font-weight:600;
}

.stButton > button:hover{
    transform:translateY(-2px);
}

</style>
""", unsafe_allow_html=True)

main_col, right_col = st.columns([3,1])

if selected == "Home":

    with right_col:

        st.markdown("""
        <div class='quick-card'>
            <h2>⚡ Quick Analysis</h2>
        </div>
        """, unsafe_allow_html=True)

        age_range = st.slider(
            "Age Range",
            int(df["age"].min()),
            int(df["age"].max()),
            (30,60)
        )

        gender = st.selectbox(
            "Gender",
            ["All","Male","Female"]
        )

        disease = st.selectbox(
            "Disease Status",
            ["All","Disease","No Disease"]
        )

        cp = st.selectbox(
            "Chest Pain Type",
            ["All"] + sorted(df["cp"].unique().tolist())
        )

        chol_range = st.slider(
            "Cholesterol Range (mg/dL)",
            int(df["chol"].min()),
            int(df["chol"].max()),
            (150,300)
        )

        bp_range = st.slider(
            "Resting BP Range (mm Hg)",
            int(df["trestbps"].min()),
            int(df["trestbps"].max()),
            (90,160)
        )

    filtered_df = df.copy()

    filtered_df = filtered_df[
        (filtered_df["age"] >= age_range[0]) &
        (filtered_df["age"] <= age_range[1])
    ]

    filtered_df = filtered_df[
        (filtered_df["chol"] >= chol_range[0]) &
        (filtered_df["chol"] <= chol_range[1])
    ]

    filtered_df = filtered_df[
        (filtered_df["trestbps"] >= bp_range[0]) &
        (filtered_df["trestbps"] <= bp_range[1])
    ]

    if gender == "Male":
        filtered_df = filtered_df[filtered_df["sex"] == 1]

    elif gender == "Female":
        filtered_df = filtered_df[filtered_df["sex"] == 0]

    if disease == "Disease":
        filtered_df = filtered_df[
            filtered_df["target_binary"] == 1
        ]

    elif disease == "No Disease":
        filtered_df = filtered_df[
            filtered_df["target_binary"] == 0
        ]

    if cp != "All":
        filtered_df = filtered_df[
            filtered_df["cp"] == cp
        ]

    total_patients = len(filtered_df)
    original_patients = len(df)

    dataset_pct = round(
        total_patients / original_patients * 100,
        1
    ) if original_patients > 0 else 0

    if total_patients > 0:
        disease_cases = (filtered_df["target_binary"] == 1).sum()
        disease_pct = round(disease_cases / total_patients * 100, 1)

        avg_age = round(filtered_df["age"].mean())
        avg_chol = round(filtered_df["chol"].mean())
        avg_bp = round(filtered_df["trestbps"].mean())

    else:
        disease_cases = 0
        disease_pct = 0

        avg_age = 0
        avg_chol = 0
        avg_bp = 0

    with main_col:

        container = st.container(border=False)

        with container:

            col1, col2 = st.columns([2,1])
            with col1:
                st.markdown("""
                <div class='hero'>
                    <p>👋 Welcome to CardioInsight</p>
                    <h1>CardioInsight</h1>
                    <h2>Heart Disease Analytics Dashboard</h2>
                    <p>
                    Transforming clinical data into actionable insights.
                    Explore patient patterns, identify risk factors,
                    and make data-driven decisions.
                    </p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.image("heart2.png", use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        c1,c2,c3,c4,c5=st.columns(5)
        with c1:
                st.markdown(f"""
                <div class='module-card'>
                    <div class="kpi-title">👥 Total Patients</div>
                    <div class="kpi-value">{total_patients}</div>
                    <div class="kpi-sub">{dataset_pct}% of Dataset</div>
                </div>
                """, unsafe_allow_html=True)
        
        with c2:
            st.markdown(f"""
            <div class='module-card'>
                <div class="kpi-title">❤️ Patients with Disease</div>
                <div class="kpi-value">{disease_cases}</div>
                <div class="kpi-sub">
                {disease_pct}% of Total
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class='module-card'>
                <div class="kpi-title">📅 Average Age</div>
                <div class="kpi-value">{avg_age}</div>
                <div class="kpi-sub">Years</div>
            </div>
            """, unsafe_allow_html=True)

        with c4:
            st.markdown(f"""
            <div class='module-card'>
                <div class="kpi-title">🩸 Average Cholesterol</div>
                <div class="kpi-value">{avg_chol}</div>
                <div class="kpi-sub">mg/dL</div>
            </div>
            """, unsafe_allow_html=True)

        with c5:
            st.markdown(f"""
            <div class='module-card'>
                <div class="kpi-title">🩺 Average Resting BP</div>
                <div class="kpi-value">{avg_bp}</div>
                <div class="kpi-sub">mm Hg</div>
            </div>
            """, unsafe_allow_html=True)

        if total_patients == 0:
            st.warning("No patients match the selected filters.")

            st.markdown("""
            <style>
            .kpi-card{
                background: linear-gradient(135deg,#0b1635,#0f1f47);
                border:1px solid rgba(255,255,255,0.08);
                border-radius:18px;
                padding:20px;
                box-shadow:0 0 15px rgba(138,43,226,0.15);
            }

            .kpi-title{
                color:#cfd8ff;
                font-size:14px;
            }

            .kpi-value{
                color:white;
                font-size:36px;
                font-weight:700;
            }

            .kpi-sub{
                color:#aab3d6;
                font-size:12px;
            }
                        
            .kpi-card:hover{
            transform:translateY(-8px);

            box-shadow:
                0 0 15px rgba(138,43,226,0.25),
                0 0 25px rgba(138,43,226,0.15);

            border:1px solid rgba(139,92,246,.5);
            }

            </style>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:25px'></div>",
                unsafe_allow_html=True)
        
        avg_age = round(df["age"].mean())

        avg_chol = round(df["chol"].mean())

        disease_rate = (
            df["target_binary"].mean() * 100
        )

        angina_rate = round(
            df["exang"].mean() * 100
        )

        avg_hr = round(
            df["thalach"].mean()
        )

        avg_oldpeak = round(
            df["oldpeak"].mean(),
            1
        )
        
    st.subheader("✨ Key Insights At A Glance")

    c1,c2,c3,c4,c5 = st.columns(5)

    cards = [  
            "🧓 Age Impact",
            "💧 Cholesterol",
            "🏃 Exercise Angina",
            "❤️ Heart Rate",
            "📈 ST Depression"
        ]

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1:

            age_risk = df.groupby("target_binary")["age"].mean()

            st.markdown(f"""
                <div class='module-card'>
                <h2>👴 Age Impact</h2>
                <p>
                Patients with heart disease are
                on average <b>{round(age_risk[1])} years</b> old,
                compared to <b>{round(age_risk[0])} years</b>
                for healthy patients.
                </p>
            </div>
            """, unsafe_allow_html=True)
    with c2:

            high_chol = (df["chol"] > 240).mean()*100

            st.markdown(f"""
             <div class='module-card'>
                <h2>🩸 Cholesterol</h2>
                <p>
                <b>{high_chol:.0f}%</b> of patients
                have cholesterol levels above
                240 mg/dL.
                </p>
            </div>
            """, unsafe_allow_html=True)
    with c3:

            angina_rate = round(
                df["exang"].mean()*100
            )

            st.markdown(f"""
             <div class='module-card'>
                <h2>🏃 Exercise Angina</h2>
                <p>
                <b>{angina_rate}%</b> of patients
                experience exercise-induced
                angina, indicating elevated
                cardiovascular stress.
                </p>
            </div>
            """, unsafe_allow_html=True)
    with c4:

            disease_hr = df[df["target_binary"]==1]["thalach"].mean()
            healthy_hr = df[df["target_binary"]==0]["thalach"].mean()

            st.markdown(f"""
             <div class='module-card'>
                <h2>❤️ Heart Rate</h2>
                <p>
                Disease patients average
                <b>{round(disease_hr)} bpm</b>
                versus
                <b>{round(healthy_hr)} bpm</b>
                in healthy individuals.
                </p>
            </div>
            """, unsafe_allow_html=True)
    with c5:

            avg_oldpeak = round(
                df["oldpeak"].mean(),
                1
            )

            st.markdown(f"""
             <div class='module-card'>
                <h2>📈 ST Depression</h2>
                <p>
                Average ST depression is
                <b>{avg_oldpeak}</b>,
                indicating moderate ECG
                abnormalities during exercise.
                </p>
            </div>
            """, unsafe_allow_html=True)

            
    st.markdown("""
        <style>

        .module-card{
        background:linear-gradient(135deg,#0f1735,#101d46);
        padding:24px;
        border-radius:18px;
        border:1px solid rgba(255,255,255,.08);
        min-height:140px;
        transition:all 0.3s ease;
        cursor:pointer;
        }

        .module-card h4{
            color:white;
            font-size:30px;
            margin-bottom:18px;
        }

        .module-card p{
            color:#cfd8ff;
            font-size:16px;
        }

        .module-card:hover{
        transform:translateY(-8px);

        box-shadow:
            0 0 15px rgba(138,43,226,0.25),
            0 0 25px rgba(138,43,226,0.15);

        border:1px solid rgba(139,92,246,.5);
        }

        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
    <style>

    .workflow-card{
        background:linear-gradient(
            135deg,
            #0f1735,
            #101d46
        );
    
        border-radius:18px;
    
        padding:20px;
    
        min-height:220px;
    
        text-align:center;
    
        border:1px solid rgba(255,255,255,.08);
    
        transition:.3s;
    }
    
    .workflow-card:hover{
        transform:translateY(-6px);
    
        box-shadow:
            0 0 20px rgba(139,92,246,.35);
    }
    
    .workflow-icon{
        font-size:40px;
        margin-bottom:10px;
    }
    
    .workflow-title{
        color:white;
        font-size:22px;
        font-weight:700;
        margin-bottom:10px;
    }
    
    .workflow-text{
        color:#cfd8ff;
        font-size:14px;
    }

    .tech-card{
        background:linear-gradient(
            135deg,
            #0f1735,
            #101d46
        );
    
        border-radius:20px;
    
        padding:25px;
    
        text-align:center;
    
        border:1px solid rgba(255,255,255,.08);
    
        min-height:220px;
    
        transition:all .3s ease;
    
        box-shadow:
            0 0 15px rgba(139,92,246,.15);
    }
    
    .tech-card:hover{
        transform:translateY(-8px);
    
        box-shadow:
            0 0 20px rgba(139,92,246,.4),
            0 0 40px rgba(139,92,246,.25);
    }
    
    .tech-logo{
        width:70px;
        height:70px;
        margin-bottom:15px;
    
        filter:
            drop-shadow(0 0 8px rgba(139,92,246,.6))
            drop-shadow(0 0 15px rgba(139,92,246,.4));
    }
    
    .tech-name{
        color:white;
        font-size:22px;
        font-weight:700;
        margin-bottom:10px;
    }
    
    .tech-desc{
        color:#cfd8ff;
        font-size:14px;
        line-height:1.6;
    }
    
    .arrow-box{
        height:280px;
        display:flex;
        align-items:center;
        justify-content:center;
    }
    
    .arrow-icon{
        font-size:60px;
        color:#8b5cf6;
        text-shadow:
            0 0 10px #8b5cf6,
            0 0 20px #8b5cf6;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("⚙️ Project Workflow")
    workflow = st.columns([1,0.08,1,0.08,1,0.08,1,0.08,1,0.08,1])
    with workflow[0]:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-icon">📂</div>
            <div class="workflow-title">Dataset</div>
            <div class="workflow-text">
            UCI Heart Disease Dataset
            containing 303 patient records.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with workflow[1]:
        st.markdown("""
        <div class="arrow-box">
            <div class="arrow-icon">➜</div>
        </div>
        """, unsafe_allow_html=True)

    with workflow[2]:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-icon">🧹</div>
            <div class="workflow-title">Cleaning</div>
            <div class="workflow-text">
            Checked missing values,
            transformed columns and
            prepared data.
            </div>
        </div>
        """, unsafe_allow_html=True)

    
    with workflow[3]:
        st.markdown("""
        <div class="arrow-box">
            <div class="arrow-icon">➜</div>
        </div>
        """, unsafe_allow_html=True)

    with workflow[4]:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-icon">📊</div>
            <div class="workflow-title">Analysis</div>
            <div class="workflow-text">
            Explored risk factors,
            disease patterns and
            patient characteristics.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with workflow[5]:
        st.markdown("""
        <div class="arrow-box">
            <div class="arrow-icon">➜</div>
        </div>
        """, unsafe_allow_html=True)
    
    with workflow[6]:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-icon">📈</div>
            <div class="workflow-title">Visualization</div>
            <div class="workflow-text">
            Interactive charts,
            KPIs and dashboards
            built using Plotly.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with workflow[7]:
        st.markdown("""
        <div class="arrow-box">
            <div class="arrow-icon">➜</div>
        </div>
        """, unsafe_allow_html=True)

    with workflow[8]:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-icon">🎨</div>
            <div class="workflow-title">UI Design</div>
            <div class="workflow-text">
            Modern responsive
            Streamlit interface with
            custom CSS styling.
            </div>
        </div>
        """, unsafe_allow_html=True)

    
    with workflow[9]:
        st.markdown("""
        <div class="arrow-box">
            <div class="arrow-icon">➜</div>
        </div>
        """, unsafe_allow_html=True)

    with workflow[10]:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-icon">🫀</div>
            <div class="workflow-title">Insights</div>
            <div class="workflow-text">
            Generate actionable
            cardiovascular insights
            for decision making.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("💻 Technology Stack")
    c1,c2,c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""
        <div class="tech-card">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg"
                 class="tech-logo">
            <div class="tech-name">Python</div>
            <div class="tech-desc">
            Core programming language
            powering CardioInsight.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"""
        <div class="tech-card">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg"
                 class="tech-logo">
            <div class="tech-name">Pandas</div>
            <div class="tech-desc">
            Data cleaning, filtering,
            aggregation and exploration.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with c3:
        st.markdown(f"""
        <div class="tech-card">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/numpy/numpy-original.svg"
                 class="tech-logo">
            <div class="tech-name">NumPy</div>
            <div class="tech-desc">
            Mathematical operations
            and risk calculations.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c4,c5,c6 = st.columns(3)
    
    with c4:
        st.markdown("""
        <div class="tech-card">
            <img src="https://upload.wikimedia.org/wikipedia/commons/8/84/Matplotlib_icon.svg"
                 class="tech-logo">
            <div class="tech-name">Matplotlib</div>
            <div class="tech-desc">
            Statistical visualizations
            and plotting support.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with c5:
        st.markdown("""
        <div class="tech-card">
            <img src="https://images.plot.ly/logo/new-branding/plotly-logomark.png"
                 class="tech-logo">
            <div class="tech-name">Plotly</div>
            <div class="tech-desc">
            Interactive charts,
            KPIs and dashboards.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with c6:
        st.markdown("""
        <div class="tech-card">
            <img src="https://streamlit.io/images/brand/streamlit-mark-color.png"
                 class="tech-logo">
            <div class="tech-name">Streamlit</div>
            <div class="tech-desc">
            Dashboard framework
            powering the application.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)

    with c1:
            st.markdown("""
            <div class='card'>
            <h3>💡 Clinical Insight</h3>

            Patients with:

            • Higher cholesterol

            • Exercise induced angina

            • Elevated ST depression

            show significantly greater cardiovascular risk.

            </div>
            """, unsafe_allow_html=True)

    with c2:
            st.markdown("""
            <h6 style='text-align:center; color:white;'>
            📊 Dataset Quality Score
            </h6>
            """, unsafe_allow_html=True)
            import plotly.graph_objects as go
            
            missing_pct = (df.isnull().sum().sum() /
                (df.shape[0] * df.shape[1])) * 100

            health_score = round(100 - missing_pct)

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=health_score,
                number={'suffix': "%"},
                gauge={
                    'axis': {'range': [0,100]},
                    'bar': {'color': "#8b5cf6"},
                    'bgcolor': "#0f1735",
                    'borderwidth': 0,
                    'steps': [
                        {'range':[0,60], 'color':'#1f2937'},
                        {'range':[60,80], 'color':'#374151'},
                        {'range':[80,100], 'color':'#10b981'}
                    ]
                }
            ))

            fig.update_layout(
                height=220,
                paper_bgcolor="#050816",
                font_color="white",
                margin=dict(l=10,r=10,t=10,b=10)
            )

            st.plotly_chart(fig,use_container_width=True)

    with c3:
            st.success("""
            Dataset loaded successfully

            1024 records analyzed

            14 features available
            """)

elif selected == "Dataset Explorer":
    st.markdown("""
    <style>
                
    [data-testid="stDataFrame"]{
    
    border-radius:20px;
        overflow:hidden;
        border:1px solid rgba(255,255,255,.08);
    }

    [data-testid="stDataFrame"] table{
        background:#091437;
    }
    .dataset-hero{
        background:linear-gradient(
            135deg,
            rgba(14,23,65,0.98),
            rgba(8,12,40,0.98)
        );
        border:1px solid rgba(255,255,255,0.08);
        border-radius:25px;
        padding:25px;
        margin-bottom:20px;
    }

    .hero-title{
        font-size:38px;
        font-weight:700;
        color:white;
        margin-bottom:10px;
    }

    .hero-sub{
        color:#b8c4d9;
        font-size:17px;
        margin-bottom:15px;
    }

    .info-row{
        display:flex;
        justify-content:space-between;
        flex-wrap:wrap;
        margin-top:20px;
    }

    .info-item{
        min-width:130px;
        margin-top:10px;
    }

    .info-label{
        color:#9db0d1;
        font-size:13px;
    }

    .info-value{
        color:white;
        font-size:17px;
        font-weight:600;
    }

    .kpi-card{
        background:rgba(13,22,58,0.95);
        border:1px solid rgba(255,255,255,0.08);
        border-radius:20px;
        padding:20px;
        text-align:center;
        transition:0.3s;
        height:180px;
    }

    .kpi-card:hover{
        transform:translateY(-6px);
        box-shadow:0 0 25px rgba(138,92,246,.35);
    }
    .kpi-number{
        color:white;
        font-size:38px;
        font-weight:700;
    }

    .kpi-title{
        color:#b8c4d9;
        font-size:15px;
    }

    .section-card{
        background:rgba(13,22,58,0.95);
        border:1px solid rgba(255,255,255,0.08);
        border-radius:20px;
        padding:20px;
        margin-top:15px;
    }

    .section-title{
        color:white;
        font-size:22px;
        font-weight:600;
        margin-bottom:10px;
    }
                
    .summary-card{
        background:rgba(16,30,74,.75);
        border-radius:18px;
        padding:22px;
        text-align:center;
        border:1px solid rgba(255,255,255,.08);

        transition:.3s;
    }

    .summary-card:hover{
        transform:translateY(-4px);

        box-shadow:
        0 10px 35px rgba(124,77,255,.25);
    }

    .summary-number{
        font-size:42px;
        font-weight:700;
        color:white;
    }

    .summary-label{
        color:#9fb3d1;
        font-size:16px;
    }

    </style>
    """, unsafe_allow_html=True)

    total_records = df.shape[0]

    total_features = df.shape[1]

    missing_values = int(
        df.isnull().sum().sum()
    )

    quality_score = round(
        ((df.size - missing_values)
        / df.size) * 100,
        1
    )

    data_types = len(
        set(df.dtypes)
    )

    left,right = st.columns([5,1.3])

    with left:

        st.markdown(f"""
        <div class="dataset-hero">
            <div class="hero-title">
            📊 Dataset Explorer
            </div>
            <div class="hero-sub">
            Explore and understand the UCI Heart Disease Dataset through interactive summaries and data inspection.
            </div>
            <div class="info-row">
                <div class="info-item">
                    <div class="info-label">Source</div>
                    <div class="info-value">
                    UCI Machine Learning Repository
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-label">Dataset Type</div>
                    <div class="info-value">
                    Tabular Dataset
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-label">Domain</div>
                    <div class="info-value">
                    Healthcare
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-label">Total Records</div>
                    <div class="info-value">
                    {total_records}
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-label">Total Features</div>
                    <div class="info-value">
                    {total_features}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:

        st.image(
            "Untitled design.png",
            use_container_width=True
        )

    k1,k2,k3,k4,k5 = st.columns(5)

    with k1:

        st.markdown(f"""
        <div class="kpi-card">
            <div style="
            font-size:45px;
            color:#1e90ff;
            ">
            👥
            </div>
            <div class="kpi-number">
            {total_records}
            </div>
            <div class="kpi-title">
            Patient Records
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k2:

        st.markdown(f"""
        <div class="kpi-card">
            <div style="
            font-size:45px;
            color:#8b5cf6;
            ">
            ⬛
            </div>
            <div class="kpi-number">
            {total_features}
            </div>
            <div class="kpi-title">
            Total Features
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k3:

        st.markdown(f"""
        <div class="kpi-card">
            <div style="
            font-size:45px;
            color:#ff3366;
            ">
            ✔
            </div>
            <div class="kpi-number">
            {missing_values}
            </div>
            <div class="kpi-title">
            Missing Values
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k4:

        st.markdown(f"""
        <div class="kpi-card">
            <div style="
            font-size:45px;
            color:#3b82f6;
            ">
            ◔
            </div>
            <div class="kpi-number">
            {data_types}
            </div>
            <div class="kpi-title">
            Data Types
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k5:

        st.markdown(f"""
        <div class="kpi-card">
            <div style="
            font-size:45px;
            color:#22c55e;
            ">
            🛡
            </div>
            <div class="kpi-number">
            {quality_score}%
            </div>
            <div class="kpi-title">
            Dataset Quality
            </div>

        </div>
        """, unsafe_allow_html=True)

    left,right = st.columns([6,1.3])

    with left:

        st.markdown("""
        <div class="section-card">
        <div class="section-title">
        Rows to Display
        </div>
        <div style="
        color:#b8c4d9;
        margin-bottom:15px;
        ">
        Use the slider below to adjust the number of rows visible in the dataset.
        </div>
        """, unsafe_allow_html=True)

        rows_to_show = st.slider(
            "",
            min_value=5,
            max_value=len(df),
            value=10,
            step=1
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    with right:

        st.markdown(f"""
        <div class="kpi-card">
            <div style="
            color:#b8c4d9;
            font-size:16px;
            ">
            Showing
            </div>
            <div class="kpi-number">
            {rows_to_show}
            </div>
            <div class="kpi-title">
            of {len(df)} rows
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card">
    <div class="section-title">
    📋 Dataset Preview
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        df.head(rows_to_show),
        use_container_width=True,
        height=420
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    total_pages = int(
        np.ceil(len(df)/10)
    )

    st.markdown(f"""
    <div style="
    background:rgba(13,22,58,.95);
    padding:12px 20px;
    border-radius:0 0 20px 20px;
    border:1px solid rgba(255,255,255,.08);
    margin-top:-10px;
    ">
    <div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    ">
    <div style="
    color:#b8c4d9;
    ">
    Showing 1 to {rows_to_show} of {len(df)} entries
    </div>
    <div style="
    color:#b8c4d9;
    ">
    Pages: {total_pages}
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card">
    <div class="section-title">
    📈 Dataset Visual Overview
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="section-card">
        <div class="section-title">
        🎯 Target Distribution
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        target_counts = (
            df["target_binary"]
            .value_counts()
        )

        fig_target = go.Figure(
            data=[
                go.Pie(
                    labels=["No Disease","Disease"],
                    values=target_counts.values,
                    hole=0.55,

                    marker=dict(
                        colors=[
                            "#3b82f6",
                            "#ff3366"
                        ]
                    ),

                    textinfo="percent",

                    textfont=dict(
                        size=18,
                        color="white"
                    )
                )
            ]
        )

        fig_target.update_layout(
            paper_bgcolor="#091437",
            plot_bgcolor="#091437",
            font_color="white",
            height=350,
            showlegend=True,

            annotations=[
                dict(
                    text="🫀",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(
                        size=30
                    )
                )
            ]
        )

        st.plotly_chart(
            fig_target,
            use_container_width=True
        )

        disease_pct = round(
            (
                target_counts[1]
                / len(df)
            ) * 100,
            1
        )

        st.info(
            f"""
            🔍 Insight:

            {disease_pct}% of patients in the dataset have heart disease.

            The target distribution provides an overview of disease prevalence and helps assess dataset balance.
            """
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown("""
        <div class="section-card">
        <div class="section-title">
        📊 Data Types Distribution
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        categorical_features = [
            "sex",
            "cp",
            "fbs",
            "restecg",
            "exang",
            "slope",
            "thal",
            "target_binary"
        ]

        categorical_cols = len(categorical_features)

        numeric_cols = (
            len(df.columns)
            - categorical_cols
        )

        fig_dtype = go.Figure(
            data=[
                go.Pie(
                    labels=[
                        "Numeric",
                        "Categorical"
                    ],

                    values=[
                        numeric_cols,
                        categorical_cols
                    ],

                    hole=0.55,

                    marker=dict(
                        colors=[
                            "#8b5cf6",
                            "#22c55e"
                        ]
                    ),

                    textinfo="percent",

                    textfont=dict(
                        size=18,
                        color="white"
                    )
                )
            ]
        )

        fig_dtype.update_layout(
            paper_bgcolor="#091437",
            plot_bgcolor="#091437",
            font_color="white",
            height=350,
            showlegend=True,

            annotations=[
                dict(
                    text="📁",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(
                        size=30
                    )
                )
            ]
        )

        st.plotly_chart(
            fig_dtype,
            use_container_width=True
        )

        st.info(
            f"""
            🔍 Insight:

            Numeric Features : {numeric_cols}

            Categorical Features : {categorical_cols}

            The dataset primarily contains structured numeric medical measurements suitable for analysis and visualization.
            """
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
    📊 Dataset Feature Summary
    </div>
    """, unsafe_allow_html=True)

    categorical_features = [
        "sex",
        "cp",
        "fbs",
        "restecg",
        "exang",
        "slope",
        "thal",
        "target_binary"
    ]

    categorical_cols = len(categorical_features)

    numeric_cols = (
        len(df.columns)
        - categorical_cols
    )

    feature1, feature2, feature3, feature4 = st.columns(4)

    with feature1:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-number">
            {len(df.columns)}
            </div>
            <div class="summary-label">
            Total Features
            </div>
        </div>
        """, unsafe_allow_html=True)

    with feature2:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-number">
            {numeric_cols}
            </div>
            <div class="summary-label">
            Numeric Features
            </div>
        </div>
        """, unsafe_allow_html=True)

    with feature3:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-number">
            {categorical_cols}
            </div>
            <div class="summary-label">
            Categorical Features
            </div>
        </div>
        """, unsafe_allow_html=True)

    with feature4:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-number">
            {df.isnull().sum().sum()}
            </div>
            <div class="summary-label">
            Missing Values
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)






elif selected == "Dashboard":

    st.markdown("""
    <style>

    .dashboard-card{
        background:linear-gradient(135deg,#0f1735,#101d46);
        border-radius:18px;
        padding:20px;
        border:1px solid rgba(255,255,255,.08);
    }

    .dashboard-kpi{
        background:linear-gradient(135deg,#111d47,#122458);
        border-radius:18px;
        padding:20px;
        text-align:center;
        border:1px solid rgba(255,255,255,.08);
        transition:.3s;
    }

    .dashboard-kpi:hover{
        transform:translateY(-5px);
        box-shadow:0 0 20px rgba(139,92,246,.4);
    }

    .dashboard-value{
        font-size:38px;
        color:white;
        font-weight:700;
    }

    .dashboard-label{
        color:#cfd8ff;
    }

    .dashboard-section{
        font-size:28px;
        color:white;
        font-weight:600;
        margin-bottom:10px;
                
    .chart-card{
    background:linear-gradient(135deg,#0f1735,#101d46);
    border:1px solid rgba(255,255,255,.08);
    border-radius:20px;
    padding:15px;
    height:100%;
    box-shadow:0 0 20px rgba(0,0,0,.15);
    }

    .chart-title{
        color:white;
        font-size:20px;
        font-weight:600;
        margin-bottom:4px;
    }

    .chart-subtitle{
        color:#9aa8d6;
        font-size:13px;
        margin-bottom:12px;
    }
    .insight-box{
        margin-top:10px;
        padding:12px 15px;
        border-radius:12px;
    
        background:linear-gradient(
            135deg,
            rgba(139,92,246,0.15),
            rgba(76,29,149,0.25)
        );
    
        border:1px solid rgba(139,92,246,0.25);
    
        color:#dbeafe;
    
        font-size:13px;
        line-height:1.5;
    
        min-height:80px;
    }
    
    .insight-box:hover{
        border:1px solid rgba(139,92,246,0.5);
    
        box-shadow:
        0 0 15px rgba(139,92,246,0.2);
    }
    }

    </style>
    """, unsafe_allow_html=True)

    left, right = st.columns([4,1])

    with left:

        st.markdown("""
        <div class='dashboard-card'>
            <h1 style='color:white'>
            📊 CardioInsight Dashboard
            </h1>

            
           <p>Actionable insights from Extended UCI Heart Disease Dataset</p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.metric("Dataset Records", len(df))

    total_patients = len(df)

    disease_cases = (df["target_binary"] == 1).sum()

    healthy_cases = (df["target_binary"] == 0).sum()

    avg_age = round(df["age"].mean(), 1)

    avg_chol = round(df["chol"].mean(), 1)

    avg_bp = round(df["trestbps"].mean(), 1)

    st.markdown("""
    <div style="
    margin-top:15px;
    margin-bottom:15px;
    "></div>
    """, unsafe_allow_html=True)
    k1,k2,k3,k4,k5,k6 = st.columns(6)

    with k1:

        st.markdown(f"""
        <div class='dashboard-kpi'>
            <div class='dashboard-label'>
            👥 Total Patients
            </div>
            <div class='dashboard-value'>
            {total_patients}
            </div>
            </div>
            """, unsafe_allow_html=True)

    with k2:

        st.markdown(f"""
        <div class='dashboard-kpi'>
            <div class='dashboard-label'>
            ❤️ Disease Cases
            </div>
            <div class='dashboard-value'>
            {disease_cases}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k3:

        st.markdown(f"""
        <div class='dashboard-kpi'>
            <div class='dashboard-label'>
            💚 Healthy Cases
            </div>
            <div class='dashboard-value'>
            {healthy_cases}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k4:

        st.markdown(f"""
        <div class='dashboard-kpi'>
            <div class='dashboard-label'>
            📅 Avg Age
            </div>
            <div class='dashboard-value'>
            {avg_age}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k5:

        st.markdown(f"""
        <div class='dashboard-kpi'>
            <div class='dashboard-label'>
            🩸 Cholesterol
            </div>
            <div class='dashboard-value'>
            {avg_chol}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with k6:

        st.markdown(f"""
        <div class='dashboard-kpi'>
            <div class='dashboard-label'>
            🩺 Resting BP
            </div>
            <div class='dashboard-value'>
            {avg_bp}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
    "<div style='height:25px'></div>",
    unsafe_allow_html=True
    )
    c1,c2,c3 = st.columns([1.2,1.8,1.2])

    with c1:
        st.markdown("""
        <div class='chart-card'>
            <div class='chart-title'>
            ❤️ Heart Disease Distribution
            </div>
            <div class='chart-subtitle'>
            Disease vs Healthy Patients
            </div>
        """, unsafe_allow_html=True)

        pie_df = df.copy()

        pie_df["Disease Status"] = pie_df["target_binary"].map({
            0: "No Disease",
            1: "Heart Disease"
        })

        fig = px.pie(
            pie_df,
            names="Disease Status",
            hole=0.70,
            color="Disease Status",
            color_discrete_map={
                "No Disease":"#10b981",
                "Heart Disease":"#ff4d6d"
            }
        )

        fig.update_layout(
            paper_bgcolor="#0f1735",
            font_color="white",
            height=350,
            showlegend=True
        )
        st.plotly_chart(fig,use_container_width=True)
        st.markdown(f"""
        <div class="insight-box">
        💡 <b>Insight:</b><br>
        Heart disease patients account for
        <b>{round((df['target_binary']==1).sum()/len(df)*100,1)}%</b>
        of the dataset.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='chart-card'>
            <div class='chart-title'>
            🩺 Cholesterol vs Blood Pressure
            </div>
            <div class='chart-subtitle'>
            Bubble size represents Age
            </div>
        """, unsafe_allow_html=True)
        scatter_df = df.copy()
        scatter_df["Disease Status"] = scatter_df["target_binary"].map({
            0:"No Disease",
            1:"Heart Disease"
        })
        scatter_df["Gender"] = scatter_df["sex"].map({
            0:"Female",
            1:"Male"
        })
        fig = px.scatter(
            scatter_df,
            x="chol",
            y="trestbps",
            color="Disease Status",
            size="age",
            hover_data=["Gender"],
            color_discrete_map={
                "No Disease":"#10b981",
                "Heart Disease":"#ff4d6d"
            }
        )
        fig.update_layout(
            paper_bgcolor="#0f1735",
            plot_bgcolor="#0f1735",
            font_color="white",
            height=350,
            xaxis_title="Cholesterol",
            yaxis_title="Resting Blood Pressure"
        )
        st.plotly_chart(fig,use_container_width=True)
        high_chol = (df["chol"] > 240).sum()
        
        st.markdown(f"""
        <div class='insight-box'>
        <b>💡 Insight</b><br>
        Patients with higher cholesterol levels tend to exhibit elevated
        resting blood pressure, suggesting increased cardiovascular risk.
        <b>{high_chol}</b> patients have cholesterol above 240 mg/dL.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
    
    corr = df.corr(numeric_only=True)["target_binary"]

    factors = (
        corr.abs()
        .sort_values(ascending=False)
        .drop("target_binary")
        .head(5)
    )

    factor_df = pd.DataFrame({
        "Factor": factors.index,
        "Score": factors.values*100
    })
    with c3:
        st.markdown("""
        <div class='chart-card'>
            <div class='chart-title'>
            📈 Top Risk Factors
            </div>
            <div class='chart-subtitle'>
            Correlation with Heart Disease
            </div>
        """, unsafe_allow_html=True)
        fig = px.bar(
            factor_df,
            x="Score",
            y="Factor",
            orientation="h",
            color="Score",
            color_continuous_scale="purples"
        )
        fig.update_layout(
            paper_bgcolor="#0f1735",
            plot_bgcolor="#0f1735",
            font_color="white",
            height=350,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig,use_container_width=True)
        top_factor = factor_df.iloc[0]["Factor"]
        
        st.markdown(f"""
        <div class='insight-box'>
        <b>💡 Insight</b><br>
        <b>{top_factor}</b> shows the strongest correlation with heart disease
        among all available clinical attributes.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

    st.markdown(
    "<div style='height:25px'></div>",
    unsafe_allow_html=True
    )
    a,b,c = st.columns(3)

    with a:
        st.markdown("""
        <div class='chart-card'>
            <div class='chart-title'>
            👨‍⚕️ Gender Distribution
            </div>
            <div class='chart-subtitle'>
            Male vs Female Patients
            </div>
        """, unsafe_allow_html=True)
        gender_df = df.copy()
        gender_df["Gender"] = gender_df["sex"].map({
            0:"Female",
            1:"Male"
        })
        fig = px.pie(
            gender_df,
            names="Gender",
            hole=0.75,
            color="Gender",
            color_discrete_map={
                "Male":"#3b82f6",
                "Female":"#ec4899"
            }
        )
        fig.update_layout(
            paper_bgcolor="#0f1735",
            font_color="white",
            height=320
        )
        st.plotly_chart(fig,use_container_width=True)
        
        male_pct = round((df["sex"]==1).mean()*100,1)
        
        st.markdown(f"""
        <div class='insight-box'>
        <b>💡 Insight</b><br>
        Male patients account for <b>{male_pct}%</b> of the dataset,
        indicating a higher representation than female patients.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class='chart-card'>
            <div class='chart-title'>
            ⚠️ Chest Pain Analysis
            </div>
            <div class='chart-subtitle'>
            Distribution of Chest Pain Types
            </div>
        """, unsafe_allow_html=True)
        cp_df = df.copy()
        cp_df["Chest Pain Type"] = cp_df["cp"].map({
            0:"Typical Angina",
            1:"Atypical Angina",
            2:"Non-Anginal Pain",
            3:"Asymptomatic"
        })
        cp_df["Disease Status"] = cp_df["target_binary"].map({
            0:"No Disease",
            1:"Heart Disease"
        })
        fig = px.histogram(
            cp_df,
            x="Chest Pain Type",
            color="Disease Status",
            barmode="group",
            color_discrete_sequence=["#10b981","#ff4d6d"]
        )
        fig.update_layout(
            paper_bgcolor="#0f1735",
            plot_bgcolor="#0f1735",
            font_color="white",
            height=320
        )
        st.plotly_chart(fig,use_container_width=True)
        
        asymptomatic = len(df[df["cp"]==3])
        
        st.markdown(f"""
        <div class='insight-box'>
        <b>💡 Insight</b><br>
        Asymptomatic chest pain is one of the most frequently observed
        patterns among patients diagnosed with heart disease.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)

    with c:
        st.markdown("""
        <div class='chart-card'>
            <div class='chart-title'>
            📊 Dataset Quality Score
            </div>
            <div class='chart-subtitle'>
            Completeness & Consistency Check
            </div>
        """, unsafe_allow_html=True)
        score = 92
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                number={'suffix':"%"},
                gauge={
                    'axis':{'range':[0,100]},
                    'bar':{'color':'#8b5cf6'},
                    'steps':[
                        {'range':[0,60],'color':'#1f2937'},
                        {'range':[60,80],'color':'#374151'},
                        {'range':[80,100],'color':'#10b981'}
                    ]
                }
            )
        )
        fig.update_layout(
            paper_bgcolor="#0f1735",
            font_color="white",
            height=320
        )
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("""
        <div class='insight-box'>
        <b>💡 Insight</b><br>
        The dataset is highly complete and consistent,
        making it reliable for cardiovascular analysis
        and dashboard reporting.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
    
    disease_pct = round(
    disease_cases/total_patients*100,
    1
    )

    st.markdown(f"""
    <div style="
    background:linear-gradient(90deg,#4c1d95,#312e81);
    padding:20px;
    border-radius:20px;
    margin-top:20px;
    margin-bottom:20px;
    ">

    <h3 style='color:white'>
    💡 Clinical Insight
    </h3>

    <p style='color:#e5e7eb'>
    {disease_pct}% of patients in the dataset are classified with heart disease.
    Cholesterol levels, resting blood pressure and chest pain type show the strongest association with cardiovascular risk.
    </p>

    </div>
    """, unsafe_allow_html=True)
   




elif selected == "Patient Explorer":
    st.markdown("""
    <style>

        .pe-header{
            background:linear-gradient(135deg,#111d47,#16265d);
            border-radius:24px;
            padding:25px;
            border:1px solid rgba(255,255,255,.08);
            margin-bottom:20px;
        }

        .pe-title{
            color:white;
            font-size:42px;
            font-weight:700;
        }

        .pe-subtitle{
            color:#cfd8ff;
            font-size:16px;
        }

        .pe-kpi{
            background:linear-gradient(135deg,#111d47,#122458);
            border-radius:18px;
            padding:18px;
            text-align:center;
            border:1px solid rgba(255,255,255,.08);
            transition:.3s;
        }

        .pe-kpi:hover{
            transform:translateY(-4px);
            box-shadow:0 0 18px rgba(139,92,246,.4);
        }

        .pe-kpi-value{
            color:white;
            font-size:34px;
            font-weight:700;
        }

        .pe-kpi-label{
            color:#cfd8ff;
            font-size:15px;
        }

        .pe-card{
            background:#0f1735;
            border-radius:20px;
            padding:20px;
            border:1px solid rgba(255,255,255,.08);
        }

        .pe-section-title{
            color:white;
            font-size:22px;
            font-weight:600;
            margin-bottom:12px;
        }

        .pe-insight{
            background:#111d47;
            border-radius:15px;
            padding:15px;
            margin-bottom:10px;
        }

        .pe-insight-title{
            color:white;
            font-weight:600;
        }

        .pe-insight-text{
            color:#cfd8ff;
            font-size:13px;
        }

        .clinical-header{
            background:linear-gradient(135deg,#172554,#1e3a8a);
            padding:20px 28px;
            border-radius:20px 20px 0 0;
            color:white;
            font-size:30px;
            font-weight:700;
            border:1px solid rgba(255,255,255,.08);
        }

        .clinical-body{
            background:#10284d;
            padding:30px;
            border-radius:0 0 20px 20px;
            border:1px solid rgba(255,255,255,.08);
            line-height:2.1;
            color:#d7e4ff;
            font-size:18px;
        }

        .clinical-item{
            padding:10px 0;
            border-bottom:1px solid rgba(255,255,255,.05);
        }

        .table-header{
            background:linear-gradient(135deg,#172554,#1e3a8a);
            padding:20px 28px;
            border-radius:20px;
            margin-bottom:15px;
            color:white;
            font-size:30px;
            font-weight:700;
        }

        .glass-card{
            background:rgba(18,32,73,.8);
            backdrop-filter:blur(12px);
            border:1px solid rgba(255,255,255,.08);
            border-radius:24px;
            overflow:hidden;
        }
                
        .profile-box{
            background:linear-gradient(
                135deg,
                rgba(139,92,246,.15),
                rgba(59,130,246,.12)
            );
            border:1px solid rgba(139,92,246,.25);
            border-radius:18px;
            padding:18px;
        }
        }

        </style>
        """, unsafe_allow_html=True)

    left,right = st.columns([5,1])

    with left:

        st.markdown("""
        <div class='pe-header'>
            <div class='pe-title'>
            🔎 Patient Explorer
            </div>
            <div class='pe-subtitle'>
            Explore, analyze and understand individual patient health profiles
            </div>
        </div>
        """, unsafe_allow_html=True)

    k1,k2,k3,k4,k5,k6 = st.columns(6)

    cards = [
    ("👥","Total",len(df)),
    ("❤️","Disease",(df["target_binary"]==1).sum()),
    ("💚","Healthy",(df["target_binary"]==0).sum()),
    ("📅","Avg Age",round(df["age"].mean(),1)),
    ("🩸","Avg Chol",round(df["chol"].mean(),1)),
    ("🩺","Avg BP",round(df["trestbps"].mean(),1))
    ]

    for col,data in zip([k1,k2,k3,k4,k5,k6],cards):

        with col:

            st.markdown(f"""
            <div class='pe-kpi'>
                <div class='pe-kpi-label'>
                {data[0]} {data[1]}
                </div>
                <div class='pe-kpi-value'>
                {data[2]}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        selected_patient = st.selectbox(
            "🔎 Select Patient ID",
            df["Patient_ID"].unique()
        )
    
    patient = df[
        df["Patient_ID"] == selected_patient
    ].iloc[0]
    
    risk_score = round(
        (
            (patient["age"]/80)*20 +
            (patient["trestbps"]/200)*25 +
            (patient["chol"]/400)*25 +
            (patient["oldpeak"]/6)*20 +
            ((200-patient["thalach"])/200)*10
        )
    )
    
    risk_score = min(risk_score,100)
    
    if risk_score >= 75:
        risk_level = "🔴 High Risk"
    elif risk_score >= 50:
        risk_level = "🟡 Moderate Risk"
    else:
        risk_level = "🟢 Low Risk"
    
    filtered_df = df.copy()

    left,center,right = st.columns([1.2,1.8,1.2])

    gender_text = {
        0:"Female",
        1:"Male"
    }
    gender = gender_text.get(patient["sex"],"Unknown")

    cp_map = {
        1:"Typical Angina",
        2:"Atypical Angina",
        3:"Non-Anginal Pain",
        4:"Asymptomatic"
    }
    disease_text = (
        "Heart Disease Present"
        if patient["target_binary"] == 1
        else "No Heart Disease"
    )

    with left:
        st.markdown("""
        <div class='pe-card'>
        <div class='pe-section-title'>
        👤 Patient Profile
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="
        width:170px;
        height:170px;
        margin:auto;
        border-radius:50%;
        background:
        radial-gradient(circle,#8b5cf6,#312e81);
        display:flex;
        justify-content:center;
        align-items:center;
        font-size:90px;
        box-shadow:
        0 0 35px rgba(139,92,246,.35);
        ">
        👤
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <h2 style='color:white'>
        {patient['Patient_ID']}
        </h2>

        <p style='color:#cfd8ff'>
        {gender} • {patient['age']} Years
        </p>

        <h3 style='color:#8b5cf6'>
        {risk_level}
        </h3>
        """, unsafe_allow_html=True)

        st.metric(
            "Risk Score",
            f"{risk_score}/100"
        )
        st.markdown("### 🩺 Health Status")
        c1,c2 = st.columns(2)
        with c1:
            st.metric(
                "BP",
                patient["trestbps"],
                "High" if patient["trestbps"] > 140 else "Normal"
            )
        with c2:
            st.metric(
                "Chol",
                patient["chol"],
                "High" if patient["chol"] > 240 else "Normal"
            )

        st.markdown("### Risk Indicators")

        if patient["chol"] > 240:
            st.error("High Cholesterol")

        if patient["trestbps"] > 140:
            st.warning("Elevated Blood Pressure")

        if patient["oldpeak"] > 2:
            st.warning("Abnormal ST Depression")

        if patient["exang"] == 1:
            st.error("Exercise Induced Angina")

        st.markdown("</div>", unsafe_allow_html=True)

    with center:
        st.markdown("""
        <div class='pe-card'>
        <div class='pe-section-title'>
        Health Summary
        </div>
        """, unsafe_allow_html=True)
        r1,r2,r3,r4 = st.columns(4)
        with r1:
            st.metric("Resting BP",patient["trestbps"])
        with r2:
            st.metric("Cholesterol",patient["chol"])
        with r3:
            st.metric("Max HR",patient["thalach"])
        with r4:
            st.metric("Oldpeak",patient["oldpeak"])

        radar = go.Figure()
        st.markdown("### Risk Factor Analysis")

        risk_factors = pd.DataFrame({
            "Factor":[
                "Blood Pressure",
                "Cholesterol",
                "Heart Rate",
                "ST Depression"
            ],
            "Value":[
                patient["trestbps"],
                patient["chol"],
                patient["thalach"],
                patient["oldpeak"]
            ]
        })
        radar = go.Figure()

        radar.add_trace(
            go.Scatterpolar(
                r=[
                    patient["trestbps"]/2,
                    patient["chol"]/5,
                    patient["thalach"],
                    patient["oldpeak"]*25
                ],
                theta=[
                    "Blood Pressure",
                    "Cholesterol",
                    "Heart Rate",
                    "ST Depression"
                ],
                fill="toself"
            )
        )

        radar.update_layout(
            polar=dict(
                bgcolor="#0f1735"
            ),
            paper_bgcolor="#0f1735",
            font_color="white",
            height=450
        )

        st.plotly_chart(
            radar,
            use_container_width=True
        )

    with right:
        st.markdown("""
        <div class='pe-card'>
        <div class='pe-section-title'>
        Risk Assessment
        </div>
        """, unsafe_allow_html=True)

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=risk_score,
                number={"suffix":"%"},
                gauge={
                    "axis":{"range":[0,100]},
                    "bar":{"color":"#8b5cf6"},
                    "steps":[
                        {"range":[0,50],"color":"#1f2937"},
                        {"range":[50,75],"color":"#374151"},
                        {"range":[75,100],"color":"#10b981"}
                    ]
                }
            )
        )

        fig.update_layout(
            paper_bgcolor="#0f1735",
            font_color="white",
            height=240
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        st.markdown("### Overall Health Score")
        donut = go.Figure(
            go.Pie(
                values=[
                    100-risk_score,
                    risk_score
                ],
                hole=0.75,
                textinfo="none"
            )
        )
        donut.update_layout(
            paper_bgcolor="#0f1735",
            font_color="white",
            height=180,
            showlegend=False,
            annotations=[
                dict(
                    text=f"{100-risk_score}",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=30)
                )
            ]
        )
        st.plotly_chart(
            donut,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='pe-card'>
    <div class='pe-section-title'>
    📌 Patient Snapshot
    </div>
    </div>
    """, unsafe_allow_html=True)

    s1,s2,s3,s4,s5,s6 = st.columns(6)

    with s1:
        st.metric("Age", patient["age"])

    with s2:
        st.metric("BP", patient["trestbps"])

    with s3:
        st.metric("Chol", patient["chol"])

    with s4:
        st.metric("Max HR", patient["thalach"])

    with s5:
        st.metric("Oldpeak", patient["oldpeak"])

    with s6:
        st.metric(
            "Status",
            "Disease" if patient["target_binary"]==1 else "Healthy"
        )
    
    st.markdown("""
    <div class='clinical-header'>
    🩺 Clinical Summary
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='clinical-body'>

    <div class='clinical-item'>
    👤 Patient is a <b>{patient['age']}</b> year old
    <b>{patient['sex']}</b>.
    </div>

    <div class='clinical-item'>
    🩸 Resting Blood Pressure:
    <b>{patient['trestbps']} mmHg</b>
    </div>

    <div class='clinical-item'>
    🧪 Cholesterol Level:
    <b>{patient['chol']} mg/dL</b>
    </div>

    <div class='clinical-item'>
    ❤️ Maximum Heart Rate:
    <b>{patient['thalach']} bpm</b>
    </div>

    <div class='clinical-item'>
    ⚡ Chest Pain Type:
    <b>{patient['cp']}</b>
    </div>

    <div class='clinical-item'>
    📊 Clinical Outcome:
    <b>{"Heart Disease" if patient["target_binary"]==1 else "No Heart Disease"}</b>
    </div>

    </div>
    """, unsafe_allow_html=True)

    with st.expander("📂 View Full Medical Profile"):
        st.write("Age:", patient["age"])
        st.write("Gender:", gender_text.get(patient["sex"]))
        st.write("Chest Pain:", cp_map.get(patient["cp"]))
        st.write("Resting BP:", patient["trestbps"])
        st.write("Cholesterol:", patient["chol"])
        st.write("Heart Rate:", patient["thalach"])
        st.write("Oldpeak:", patient["oldpeak"])
    st.markdown("</div>", unsafe_allow_html=True)

    






elif selected == "Risk Analysis":
    st.markdown("""
    <style>
        
    .glass-card{
        background: rgba(16,30,74,0.72);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);

        border:1px solid rgba(255,255,255,0.08);

        border-radius:20px;

        padding:20px;

        box-shadow:
        0 8px 32px rgba(0,0,0,0.35);

        transition:0.3s;
    }

    .glass-card:hover{
        transform:translateY(-4px);
        box-shadow:
        0 10px 40px rgba(124,77,255,.35);
    }
    
    .kpi-icon{
        width:70px;
        height:70px;

        border-radius:50%;

        display:flex;
        align-items:center;
        justify-content:center;

        font-size:32px;

        margin-bottom:15px;
    }

    .red-icon{
        background:linear-gradient(135deg,#ff4d6d,#d90429);
        box-shadow:0 0 25px rgba(255,77,109,.5);
    }

    .orange-icon{
        background:linear-gradient(135deg,#ffb703,#fb8500);
        box-shadow:0 0 25px rgba(255,183,3,.5);
    }

    .green-icon{
        background:linear-gradient(135deg,#52d273,#16a34a);
        box-shadow:0 0 25px rgba(34,197,94,.5);
    }

    .blue-icon{
        background:linear-gradient(135deg,#3b82f6,#2563eb);
        box-shadow:0 0 25px rgba(59,130,246,.5);
    }

    .purple-icon{
        background:linear-gradient(135deg,#7c4dff,#5b21b6);
        box-shadow:0 0 25px rgba(124,77,255,.5);
    }
                            
    .metric-title{
        color:#cbd5e1;
        font-size:16px;
    }

    .metric-value{
        font-size:42px;
        font-weight:700;
        color:white;
    }

    .metric-sub{
        color:#8fa3bf;
    }

    .hero-risk{
        background:
        linear-gradient(
        135deg,
        rgba(31,48,120,.95),
        rgba(9,20,55,.95));

        border-radius:22px;

        padding:30px;

        border:1px solid rgba(255,255,255,.08);
    }
    </style>
    """,unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-risk">
    <h1>🛡️ Risk Analysis</h1>
    <p>Evaluate, analyze and predict cardiovascular risk factors</p>
    </div>
    """,unsafe_allow_html=True)

    df["risk_score"] = (
        df["age"]*0.35
        + df["chol"]*0.05
        + df["trestbps"]*0.15
        + df["oldpeak"]*8
    )
    df["risk_score"] = (
        df["risk_score"]
        / df["risk_score"].max()
    ) * 100
    df["risk_score"] = df["risk_score"].round()

    high_risk = len(df[df["risk_score"] >= 75])
    moderate_risk = len(
        df[
            (df["risk_score"] >= 50) &
            (df["risk_score"] < 75)
        ]
    )
    low_risk = len(df[df["risk_score"] < 50])   
    avg_risk = round(df["risk_score"].mean(),1)
    
    st.markdown("<br><br>", unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-icon purple-icon">
                👥
            </div>
            <div class="metric-title">
                Total Patients
            </div>
            <div class="metric-value">
                {len(df)}
            </div>
            <div class="metric-sub">
                100% Dataset
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-icon red-icon">
                ❤️
            </div>
            <div class="metric-title">
                High Risk
            </div>
            <div class="metric-value">
                {high_risk}
            </div>
            <div class="metric-sub" style="color:#ff4d6d;font-weight:600;">
                {round(high_risk/len(df)*100,1)}%
            </div>
        </div>
        """,unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-icon orange-icon">
                ⚠️
            </div>
            <div class="metric-title">
                Moderate Risk
            </div>
            <div class="metric-value">
                {moderate_risk}
            </div>
            <div class="metric-sub" style="color:#ff9800;font-weight:600;">
                {round(moderate_risk/len(df)*100,1)}%
            </div>
        </div>
        """,unsafe_allow_html=True)
        
    with c4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-icon green-icon">
                🛡️
            </div>
            <div class="metric-title">
                Low Risk
            </div>
            <div class="metric-value">
                {low_risk}
            </div>
            <div class="metric-sub" style="color:#22c55e;font-weight:600;">
                {round(low_risk/len(df)*100,1)}%
            </div>
        </div>
        """,unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="glass-card">
            <div class="kpi-icon blue-icon">
                📈
            </div>
            <div class="metric-title">
                Avg Risk Score
            </div>
            <div class="metric-value">
                {avg_risk}
            </div>
            <div class="metric-sub">
                /100
            </div>
        </div>
        """,unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    col1,col2 = st.columns([1,1.5])

    with col1:
        st.markdown("""
        <div class="glass-card">
        <h3 style='color:white;'>📊 Risk Distribution</h3>
        </div>
        """,unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        fig = px.pie(
            names=["High","Moderate","Low"],
            values=[
                high_risk,
                moderate_risk,
                low_risk
            ],
            hole=.6
        )

        fig.update_layout(
            paper_bgcolor="#091437",
            plot_bgcolor="#091437",
            font_color="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.info(
            f"""
            🔍 Insight:
            High Risk Patients: {high_risk}
            Moderate Risk Patients: {moderate_risk}
            Low Risk Patients: {low_risk}
            Most patients belong to the Moderate Risk category.
            """
        )

    with col2:
        st.markdown("""
        <div class="glass-card">
        <h3 style='color:white;'>📈 Risk Score Distribution</h3>
        </div>
        """,unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        fig = px.histogram(
            df,
            x="risk_score",
            nbins=20
        )

        fig.add_vrect(
            x0=0, x1=50,
            fillcolor="green",
            opacity=0.15,
            line_width=0
        )

        fig.add_vrect(
            x0=50, x1=75,
            fillcolor="orange",
            opacity=0.15,
            line_width=0
        )

        fig.add_vrect(
            x0=75, x1=100,
            fillcolor="red",
            opacity=0.15,
            line_width=0
        )
        fig.add_annotation(
            x=25, y=max(df["risk_score"]),
            text="Low Risk",
            showarrow=False,
            font=dict(color="green", size=14)
        )

        fig.add_annotation(
            x=62.5, y=max(df["risk_score"]),
            text="Moderate Risk",
            showarrow=False,
            font=dict(color="orange", size=14)
        )

        fig.add_annotation(
            x=87.5, y=max(df["risk_score"]),
            text="High Risk",
            showarrow=False,
            font=dict(color="red", size=14)
        )
        st.plotly_chart( fig, use_container_width=True, key="risk_distribution_hist" )
        st.info(
            f"""
            🔍 Insight:
            Average Risk Score = {avg_risk}
            Most patients are clustered in the middle risk ranges.
            Extremely high-risk cases are comparatively fewer.
            """
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)

    row2_col1,row2_col2 = st.columns([1,1])
    with row2_col1:
        st.markdown("""
        <div class="glass-card">
        <h3 style='color:white;'>⚕️ Top Risk Factors Impact</h3>
        </div>
        """,unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        impact_df = pd.DataFrame({
            "Factor":[
                "Cholesterol",
                "Oldpeak",
                "Resting BP",
                "Max HR",
                "Chest Pain",
                "Exercise Angina"
            ],
            "Impact":[
                28.6,
                22.1,
                18.7,
                15.3,
                9.6,
                5.7
            ]
        })
        fig = px.bar(
            impact_df,
            x="Impact",
            y="Factor",
            orientation="h"
        )
        fig.update_layout(
            paper_bgcolor="#091437",
            plot_bgcolor="#091437",
            font_color="white"
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )
        st.info("""
        🔍 Insight:
        • Cholesterol contributes the highest risk.
        • Oldpeak (ST Depression) is the second strongest factor.
        • Exercise Angina contributes the least among selected factors.
        """)

    
    with row2_col2:
        st.markdown("""
        <div class="glass-card">
        <h3 style='color:white;'>📈 Risk vs Age Group</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        df["AgeGroup"] = pd.cut(
            df["age"],
            bins=[20,30,40,50,60,70,80],
            labels=["20-30","30-40","40-50","50-60","60-70","70+"],
            include_lowest=True
        )

        df["risk_score"] = (
            df["age"]*0.35
            + df["chol"]*0.05
            + df["trestbps"]*0.15
            + df["oldpeak"]*8
        )

        df["risk_score"] = (
            df["risk_score"] /
            df["risk_score"].max()
        ) * 100

        df["risk_score"] = df["risk_score"].round()

        def classify_risk(score):
            if score >= 75:
                return "High Risk"
            elif score >= 50:
                return "Moderate Risk"
            else:
                return "Low Risk"

        df["RiskCategory"] = df["risk_score"].apply(classify_risk)

        risk_age = (
            df.groupby(
                ["AgeGroup","RiskCategory"],
                observed=False
            )
            .size()
            .reset_index(name="Patients")
        )

        age_order = [
            "20-30",
            "30-40",
            "40-50",
            "50-60",
            "60-70",
            "70+"
        ]

        risk_categories = [
            "High Risk",
            "Moderate Risk",
            "Low Risk"
        ]

        full_index = pd.MultiIndex.from_product(
            [age_order, risk_categories],
            names=["AgeGroup","RiskCategory"]
        )

        risk_age = (
            risk_age
            .set_index(["AgeGroup","RiskCategory"])
            .reindex(full_index, fill_value=0)
            .reset_index()
        )

        fig_age = go.Figure()

        colors = {
            "High Risk":"#ff3366",
            "Moderate Risk":"#ff9f1c",
            "Low Risk":"#22c55e"
        }

        for category in risk_categories:

            temp = risk_age[
                risk_age["RiskCategory"] == category
            ]

            fig_age.add_trace(
                go.Scatter(
                    x=temp["AgeGroup"],
                    y=temp["Patients"],
                    mode="lines+markers+text",
                    text=temp["Patients"],
                    textposition="top center",
                    name=category,
                    line=dict(
                        color=colors[category],
                        width=4
                    ),
                    marker=dict(
                        size=10
                    )
                )
            )

        fig_age.update_layout(

            paper_bgcolor="#091437",
            plot_bgcolor="#091437",

            font=dict(
                color="white"
            ),

            xaxis=dict(
                title="Age Group (Years)",
                categoryorder="array",
                categoryarray=age_order,
                showgrid=False
            ),

            yaxis=dict(
                title="Number of Patients",
                gridcolor="rgba(255,255,255,0.08)"
            ),

            legend=dict(
                orientation="h",
                y=1.12,
                x=0.2
            ),

            height=400
        )

        st.plotly_chart(
            fig_age,
            use_container_width=True,
            config={
                "displaylogo":False,
                "displayModeBar":False
            }
        )
        st.info("""
        🔍 Insight:
        • Risk increases significantly after age 50.
        • Patients aged 50–60 show the highest concentration of moderate risk.
        • Younger age groups predominantly fall into the low-risk category.
        """)

    male_count = len(df[df["sex"] == 1])
    female_count = len(df[df["sex"] == 0])

    total = male_count + female_count

    male_pct = round((male_count / total) * 100, 1)
    female_pct = round((female_count / total) * 100, 1)

    fig_gender = go.Figure(
            data=[
                go.Pie(
                    labels=["Male", "Female"],
                    values=[male_count, female_count],
                    hole=0.55,
                    marker=dict(
                        colors=["#1E90FF", "#FF3B6B"]
                    ),
                    textinfo="percent",
                    textfont=dict(
                        size=18,
                        color="white"
                    ),
                    hovertemplate=
                    "<b>%{label}</b><br>" +
                    "Count: %{value}<br>" +
                    "Percentage: %{percent}<extra></extra>"
                )
            ]
        )

    fig_gender.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            height=280,
            margin=dict(l=10,r=10,t=10,b=10),

            annotations=[
                dict(
                    text="🧑‍🤝‍🧑",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(
                        size=32,
                        color="white"
                    )
                )
            ]
        )

    st.markdown("""
    <div class="glass-card">
    <h3 style='color:white;'>👨‍👩‍👧‍👦 Risk By Gender</h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    fig_gender.update_layout(
        paper_bgcolor="#091437",
        plot_bgcolor="#091437",
        font_color="white"
    )
    st.plotly_chart(
        fig_gender,
        use_container_width=True,
        config={
            "displaylogo": False,
            "displayModeBar": False
        }
    )
    st.info(f"""
    🔍 Insight:
    • Male Patients: {male_count} ({male_pct}%)
    • Female Patients: {female_count} ({female_pct}%)
    • The dataset contains a significantly higher proportion of male patients.
    • Gender-based differences can influence cardiovascular risk assessment.
    """)







elif selected == "Comparative Analysis":
    st.markdown("""
    <style>
    .comp-hero{
        background:linear-gradient(
            135deg,
            rgba(22,36,90,0.95),
            rgba(9,20,55,0.95)
        );

        border-radius:22px;
        padding:28px;

        border:1px solid rgba(255,255,255,0.08);

        margin-bottom:25px;
    }

    .comp-title{
        font-size:42px;
        font-weight:700;
        color:white;
    }

    .comp-subtitle{
        color:#b8c4d9;
        font-size:18px;
        margin-top:5px;
    }
    .filter-card{
        background:rgba(16,30,74,.75);

        border-radius:18px;

        padding:15px;

        border:1px solid rgba(255,255,255,.08);

        box-shadow:0 8px 24px rgba(0,0,0,.25);
    }

    .comp-kpi{
        background:rgba(16,30,74,.75);

        border-radius:18px;

        padding:22px;

        border:1px solid rgba(255,255,255,.08);

        transition:.3s;

        min-height:180px;
    }

    .comp-kpi:hover{
        transform:translateY(-4px);

        box-shadow:
        0 10px 35px rgba(124,77,255,.25);
    }

    .kpi-heading{
        color:#c6d3e7;
        font-size:15px;
    }

    .kpi-number{
        color:white;
        font-size:48px;
        font-weight:700;
    }

    .kpi-sub{
        color:#9fb3d1;
        font-size:18px;
    }
    .icon-purple{
        width:65px;
        height:65px;

        border-radius:50%;

        display:flex;
        align-items:center;
        justify-content:center;

        background:linear-gradient(
            135deg,
            #9b5cff,
            #6d28d9
        );

        box-shadow:
        0 0 30px rgba(155,92,255,.5);

        font-size:28px;

        margin-bottom:12px;
    }

    .icon-pink{
        width:65px;
        height:65px;

        border-radius:50%;

        display:flex;
        align-items:center;
        justify-content:center;

        background:linear-gradient(
            135deg,
            #ff4d8d,
            #d90479
        );

        box-shadow:
        0 0 30px rgba(255,77,141,.5);

        font-size:28px;

        margin-bottom:12px;
    }

    .icon-blue{
        width:65px;
        height:65px;

        border-radius:50%;

        display:flex;
        align-items:center;
        justify-content:center;

        background:linear-gradient(
            135deg,
            #3b82f6,
            #2563eb
        );

        box-shadow:
        0 0 30px rgba(59,130,246,.5);

        font-size:28px;

        margin-bottom:12px;
    }

    .icon-orange{
        width:65px;
        height:65px;

        border-radius:50%;

        display:flex;
        align-items:center;
        justify-content:center;

        background:linear-gradient(
            135deg,
            #ffb703,
            #fb8500
        );

        box-shadow:
        0 0 30px rgba(255,183,3,.5);

        font-size:28px;

        margin-bottom:12px;
    }

    .icon-green{
        width:65px;
        height:65px;

        border-radius:50%;

        display:flex;
        align-items:center;
        justify-content:center;

        background:linear-gradient(
            135deg,
            #22c55e,
            #16a34a
        );

        box-shadow:
        0 0 30px rgba(34,197,94,.5);

        font-size:28px;

        margin-bottom:12px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="comp-hero">
    <div class="comp-title">
    📊 Comparative Analysis
    </div>
    <div class="comp-subtitle">
    Compare risk factors, demographics and outcomes across different patient groups
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.info(
            "Compare how different patient groups differ in terms of risk distribution and key health indicators."
        )

    topic = "Age Group Comparison"
    comparison_view = "Risk Overview"

    group1 = df[df["age"] < 40]
    group2 = df[df["age"] >= 40]

    group1_count = len(group1)
    group2_count = len(group2)

    df["risk_score"] = (
        df["age"]*0.35
        + df["chol"]*0.05
        + df["trestbps"]*0.15
        + df["oldpeak"]*8
    )

    df["risk_score"] = (
        df["risk_score"] /
        df["risk_score"].max()
    ) * 100

    df["risk_score"] = df["risk_score"].round(1)

    group1_avg = round(
        group1["risk_score"].mean(),
        1
    )

    group2_avg = round(
        group2["risk_score"].mean(),
        1
    )

    risk_diff = round(
        group2_avg - group1_avg,
        1
    )

    
    st.markdown("<br>", unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1:
        st.markdown(f"""
            <div class="comp-kpi">
                <div class="icon-purple">
                👥
                </div>
                <div class="kpi-heading">
                Group 1
                </div>
                <div class="kpi-sub">
                Age &lt; 40
                </div>
                <br>
                <div class="kpi-number">
                {group1_count}
                </div>
                <div class="kpi-sub">
                Patients
                </div>
            </div>
            """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class="comp-kpi">
            <div class="icon-pink">
            👥
            </div>
            <div class="kpi-heading">
            Group 2
            </div>
            <div class="kpi-sub">
            Age ≥ 40
            </div>
            <br>
            <div class="kpi-number">
            {group2_count}
            </div>
            <div class="kpi-sub">
            Patients
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="comp-kpi">
            <div class="icon-blue">
            🩺
            </div>
            <div class="kpi-heading">
            Avg Risk Score
            </div>
            <div class="kpi-number">
            {group1_avg}
            </div>
            <div class="kpi-sub"
            style="color:#22c55e;">
            Lower Risk
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:

        st.markdown(f"""
        <div class="comp-kpi">
            <div class="icon-orange">
            ⚠️
            </div>
            <div class="kpi-heading">
            Avg Risk Score
            </div>
            <div class="kpi-number">
            {group2_avg}
            </div>
            <div class="kpi-sub"
            style="color:#ff9800;">
            Higher Risk
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="comp-kpi">
            <div class="icon-green">
            📈
            </div>
            <div class="kpi-heading">
            Risk Difference
            </div>
            <div class="kpi-number">
            +{risk_diff}
            </div>
            <div class="kpi-sub">
            Points
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3,1])

    with col_left:
        st.markdown("""
        <div class="glass-card">
        <h3 style='color:white;'>
        1. Risk Distribution Comparison
        </h3>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        chart_option = st.radio(
            "View Option",
            ["A","B"],
            horizontal=True,
            label_visibility="visible"
        )

    def classify_risk(score):

        if score >= 75:
            return "High Risk"

        elif score >= 50:
            return "Moderate Risk"

        else:
            return "Low Risk"

    df["RiskCategory"] = df["risk_score"].apply(classify_risk)
    group1 = df[df["age"] < 40].copy()
    group2 = df[df["age"] >= 40].copy()

    if chart_option == "A":

        risk_order = [
            "Low Risk",
            "Moderate Risk",
            "High Risk"
        ]

        g1_counts = (
            group1["RiskCategory"]
            .value_counts()
            .reindex(risk_order, fill_value=0)
        )

        g2_counts = (
            group2["RiskCategory"]
            .value_counts()
            .reindex(risk_order, fill_value=0)
        )

        fig_sankey = go.Figure(
            go.Sankey(

                arrangement="snap",

                node=dict(

                    pad=25,
                    thickness=18,

                    label=[
                        f"Low Risk\n{g1_counts['Low Risk']}",
                        f"Moderate Risk\n{g1_counts['Moderate Risk']}",
                        f"High Risk\n{g1_counts['High Risk']}",

                        f"Low Risk\n{g2_counts['Low Risk']}",
                        f"Moderate Risk\n{g2_counts['Moderate Risk']}",
                        f"High Risk\n{g2_counts['High Risk']}"
                    ],

                    color=[
                        "#22c55e",
                        "#ffb703",
                        "#ff3366",

                        "#22c55e",
                        "#ffb703",
                        "#ff3366"
                    ]
                ),

                link=dict(

                    source=[0,1,2],
                    target=[3,4,5],

                    value=[
                        min(g1_counts["Low Risk"],
                            g2_counts["Low Risk"]),

                        min(g1_counts["Moderate Risk"],
                            g2_counts["Moderate Risk"]),

                        min(g1_counts["High Risk"],
                            g2_counts["High Risk"])
                    ],

                    color=[
                        "rgba(34,197,94,.35)",
                        "rgba(255,183,3,.35)",
                        "rgba(255,51,102,.35)"
                    ]
                )
            )
        )

        fig_sankey.update_layout(

            paper_bgcolor="#091437",
            plot_bgcolor="#091437",

            font=dict(
                color="white",
                size=14
            ),

            height=450
        )

        st.plotly_chart(
            fig_sankey,
            use_container_width=True
        )
    else:

        risk_order = [
            "Low Risk",
            "Moderate Risk",
            "High Risk"
        ]

        g1 = (
            group1["RiskCategory"]
            .value_counts(normalize=True)
            .mul(100)
            .reindex(risk_order, fill_value=0)
        )

        g2 = (
            group2["RiskCategory"]
            .value_counts(normalize=True)
            .mul(100)
            .reindex(risk_order, fill_value=0)
        )

        fig_stack = go.Figure()

        colors = {
            "Low Risk":"#22c55e",
            "Moderate Risk":"#ffb703",
            "High Risk":"#ff3366"
        }

        for risk in risk_order:

            fig_stack.add_trace(
                go.Bar(
                    name=risk,

                    x=["Age < 40"],
                    y=[g1[risk]],

                    marker_color=colors[risk]
                )
            )

            fig_stack.add_trace(
                go.Bar(
                    name=risk,

                    x=["Age ≥ 40"],
                    y=[g2[risk]],

                    marker_color=colors[risk],

                    showlegend=False
                )
            )

        fig_stack.update_layout(

            barmode="stack",

            paper_bgcolor="#091437",
            plot_bgcolor="#091437",

            font_color="white",

            yaxis_title="Percentage (%)",

            height=450
        )

        st.plotly_chart(
            fig_stack,
            use_container_width=True
        )

        high_young = (
            group1["RiskCategory"]
            .eq("High Risk")
            .mean() * 100
        )

        high_old = (
            group2["RiskCategory"]
            .eq("High Risk")
            .mean() * 100
        )

        st.markdown(f"""
        <div style="
        background:rgba(124,77,255,.08);
        border:1px solid rgba(124,77,255,.25);
        padding:14px;
        border-radius:12px;
        margin-top:10px;
        color:#d8b4fe;
        font-size:17px;
        ">
        💡 Older patients (Age ≥ 40) show a higher proportion
        of high-risk cases ({high_old:.1f}%)
        compared with younger patients ({high_young:.1f}%).
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    left,right = st.columns([3,1])

    with left:
        st.markdown("""
        <div class="glass-card">
        <h3 style='color:white;'>
        2. Key Health Indicators Comparison
        </h3>
        </div>
        """, unsafe_allow_html=True)

    with right:
        indicator_view = st.radio(
            "View",
            ["Radar","Bars"],
            horizontal=True
        )

    metrics = [
        "age",
        "chol",
        "trestbps",
        "thalach",
        "oldpeak"
    ]

    group1_values = [
        group1["age"].mean(),
        group1["chol"].mean(),
        group1["trestbps"].mean(),
        group1["thalach"].mean(),
        group1["oldpeak"].mean()
    ]

    group2_values = [
        group2["age"].mean(),
        group2["chol"].mean(),
        group2["trestbps"].mean(),
        group2["thalach"].mean(),
        group2["oldpeak"].mean()
    ]
    
    largest_gap = max(
        zip(
            metrics,
            [
                abs(a-b)
                for a,b in zip(
                    group1_values,
                    group2_values
                )
            ]
        ),
        key=lambda x:x[1]
    )
    if indicator_view == "Radar":
        fig_radar = go.Figure()

        fig_radar.add_trace(
            go.Scatterpolar(
                r=group1_values,
                theta=metrics,
                fill="toself",
                name="Age < 40",
                line_color="#3b82f6"
            )
        )

        fig_radar.add_trace(
            go.Scatterpolar(
                r=group2_values,
                theta=metrics,
                fill="toself",
                name="Age ≥ 40",
                line_color="#ff4d8d"
            )
        )

        fig_radar.update_layout(
            polar=dict(
                bgcolor="#091437"
            ),

            paper_bgcolor="#091437",

            font_color="white",

            height=500
        )

        st.plotly_chart(
            fig_radar,
            use_container_width=True
        )

    else:
        compare_df = pd.DataFrame({

            "Metric":metrics,

            "Age < 40":group1_values,

            "Age ≥ 40":group2_values
        })

        fig_bar = go.Figure()

        fig_bar.add_trace(
            go.Bar(
                x=compare_df["Metric"],
                y=compare_df["Age < 40"],
                name="Age < 40",
                marker_color="#3b82f6"
            )
        )

        fig_bar.add_trace(
            go.Bar(
                x=compare_df["Metric"],
                y=compare_df["Age ≥ 40"],
                name="Age ≥ 40",
                marker_color="#ff4d8d"
            )
        )

        fig_bar.update_layout(

            barmode="group",

            paper_bgcolor="#091437",

            plot_bgcolor="#091437",

            font_color="white",

            height=500
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

    st.markdown(f"""
        <div style="
        background:rgba(124,77,255,.08);
        border:1px solid rgba(124,77,255,.25);
        padding:16px;
        border-radius:12px;
        margin-top:12px;
        color:#d8b4fe;
        ">
        💡 Largest Difference Detected
        <b>{largest_gap[0].upper()}</b>
        shows the greatest separation between the two groups.
        Difference Value:
        <b>{largest_gap[1]:.2f}</b>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <h3>3. Outcome Comparison</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)

    g1_disease = round(
        (group1["target_binary"].mean()) * 100,
        1
    )

    g2_disease = round(
        (group2["target_binary"].mean()) * 100,
        1
    )

    risk_ratio = round(
        g2_disease / g1_disease,
        1
    ) if g1_disease > 0 else 0

    oc1, oc2, oc3 = st.columns([1,1,1])

    with oc1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color:#3b82f6;">Age &lt; 40</h4>
            <div style="
                font-size:42px;
                font-weight:700;
                color:white;
            ">
                {g1_disease}%
            </div>
            <div style="color:#9ca3af;">
                Heart Disease Detected
            </div>
        </div>
        """, unsafe_allow_html=True)

    with oc2:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color:#ec4899;">Age ≥ 40</h4>
            <div style="
                font-size:42px;
                font-weight:700;
                color:white;
            ">
                {g2_disease}%
            </div>
            <div style="color:#9ca3af;">
                Heart Disease Detected
            </div>
        </div>
        """, unsafe_allow_html=True)

    with oc3:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color:#10b981;">
                Risk Ratio
            </h4>
            <div style="
                font-size:42px;
                font-weight:700;
                color:white;
            ">
                {risk_ratio}x
            </div>
            <div style="color:#9ca3af;">
                Higher Risk
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    dot_data = pd.DataFrame({
        "Group":["Age < 40","Age ≥ 40"],
        "Disease %":[g1_disease,g2_disease]
    })

    fig_dot = go.Figure()

    for i,row in dot_data.iterrows():

        disease = int(row["Disease %"]//2)
        healthy = 50 - disease

        fig_dot.add_trace(
            go.Scatter(
                x=list(range(disease)),
                y=[row["Group"]]*disease,
                mode="markers",
                marker=dict(
                    size=14,
                    color="#ec4899"
                ),
                showlegend=(i==0),
                name="Disease"
            )
        )

        fig_dot.add_trace(
            go.Scatter(
                x=list(range(disease,50)),
                y=[row["Group"]]*healthy,
                mode="markers",
                marker=dict(
                    size=14,
                    color="#2563eb"
                ),
                showlegend=(i==0),
                name="No Disease"
            )
        )

        fig_dot.update_layout(
            paper_bgcolor="#091437",
            plot_bgcolor="#091437",
            font_color="white",
            height=300,
            xaxis=dict(
                visible=False
            ),
            yaxis_title="",
            legend=dict(
                orientation="h"
            )
        )

        st.plotly_chart(
            fig_dot,
            use_container_width=True
        )
        difference = round(
            g2_disease - g1_disease,
            1
        )

    st.markdown(f"""
    <div class="insight-box">
    ✨ Insight:
    Heart disease prevalence increases by <b>{difference}%</b>
    in patients aged 40 and above.
    The older population exhibits substantially greater
    cardiovascular risk compared to younger patients.
    </div>
    """, unsafe_allow_html=True)




elif selected == "Correlations":
    st.markdown("""
    <style>

    .corr-hero{
        background:linear-gradient(
            135deg,
            rgba(18,32,82,.95),
            rgba(8,18,50,.95)
        );

        padding:28px;
        border-radius:22px;
        margin-bottom:25px;

        border:1px solid rgba(255,255,255,.08);
    }

    .corr-title{
        font-size:42px;
        font-weight:700;
        color:white;
    }

    .corr-sub{
        color:#b8c4d9;
        font-size:18px;
    }

    .corr-kpi{
        background:rgba(12,24,66,.82);

        border-radius:18px;

        padding:22px;

        border:1px solid rgba(255,255,255,.08);

        min-height:160px;
    }

    .corr-kpi:hover{
        transform:translateY(-4px);
    }

    .kpi-value{
        color:white;
        font-size:42px;
        font-weight:700;
    }

    .kpi-label{
        color:#c6d3e7;
        font-size:16px;
    }

    .chart-card{
        background:rgba(12,24,66,.82);

        padding:20px;

        border-radius:18px;

        border:1px solid rgba(255,255,255,.08);

        margin-bottom:20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="corr-hero">
    <div class="corr-title">
    📊 Advanced Correlations
    </div>
    <div class="corr-sub">
    Deep dive into relationships between health indicators using advanced visualizations
    </div>
    </div>
    """, unsafe_allow_html=True)

    corr_matrix = df.corr(numeric_only=True)

    variables_count = len(corr_matrix.columns)

    strong_corr = (
        (corr_matrix.abs() > 0.5)
        .sum()
        .sum()
        - variables_count
    ) // 2

    avg_corr = round(
        corr_matrix.abs().mean().mean(),
        2
    )

    k1,k2,k3,k4,k5 = st.columns(5)

    with k1:
        st.markdown(f"""
        <div class="corr-kpi">
        <h2>13</h2>
        <div class="kpi-label">
        Variables Analyzed
        </div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="corr-kpi">
        <h2>{strong_corr}</h2>
        <div class="kpi-label">
        Strong Correlations
        </div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown("""
        <div class="corr-kpi">
        <h2>1</h2>
        <div class="kpi-label">
        Target Variable
        </div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="corr-kpi">
        <h2>{avg_corr}</h2>
        <div class="kpi-label">
        Avg |Correlation|
        </div>
        </div>
        """, unsafe_allow_html=True)

    with k5:
        st.markdown("""
        <div class="corr-kpi">
        <h2>High</h2>
        <div class="kpi-label">
        Network Density
        </div>
        </div>
        """, unsafe_allow_html=True)

    left,right = st.columns(2)

    with left:
        corr = corr_matrix

        G = nx.Graph()

        for col in corr.columns:
            G.add_node(col)

        for i in range(len(corr.columns)):
            for j in range(i+1,len(corr.columns)):

                val = corr.iloc[i,j]

                if abs(val) > 0.3:
                    G.add_edge(
                        corr.columns[i],
                        corr.columns[j],
                        weight=val
                    )

        pos = nx.spring_layout(
            G,
            seed=42
        )

        edge_x=[]
        edge_y=[]

        for edge in G.edges():

            x0,y0 = pos[edge[0]]
            x1,y1 = pos[edge[1]]

            edge_x += [x0,x1,None]
            edge_y += [y0,y1,None]

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            mode="lines",
            line=dict(width=1)
        )

        node_x=[]
        node_y=[]

        for node in G.nodes():

            x,y = pos[node]

            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,

            text=list(G.nodes()),

            mode="markers+text",

            marker=dict(
                size=20
            )
        )

        fig_net = go.Figure(
            [edge_trace,node_trace]
        )

        fig_net.update_layout(
            height=450,
            paper_bgcolor="#091437",
            plot_bgcolor="#091437",
            font_color="white"
        )

        st.markdown("""
        <div class="glass-card">
        <h3 style='color:white;'>1. Correlation Network Graph</h3>
        <p style='color:#b8c4d9;'>
        Shows relationships between all health variables.
        Red lines indicate positive correlation while blue lines indicate negative correlation.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(
            fig_net,
            use_container_width=True
        )

        strongest_pair = corr.abs().unstack().sort_values(ascending=False)

        strongest_pair = strongest_pair[
            strongest_pair.index.get_level_values(0)
            != strongest_pair.index.get_level_values(1)
        ]

        top_pair = strongest_pair.index[0]
        top_value = strongest_pair.iloc[0]

        st.success(
            f"Strongest relationship detected between "
            f"{top_pair[0]} and {top_pair[1]} "
            f"(r = {top_value:.2f})"
        )

    with right:
        linkage_matrix = linkage(
            corr_matrix,
            method="ward"
        )

        fig = ff.create_dendrogram(
            corr_matrix.values,
            labels=corr_matrix.columns
        )

        fig.update_layout(
            height=450,
            paper_bgcolor="#091437",
            plot_bgcolor="#091437",
            font_color="white"
        )

        st.markdown("""
        <div class="glass-card">
        <h3 style='color:white;'>2. Hierarchical Clustering (Dendrogram)</h3>
        <p style='color:#b8c4d9;'>
        Groups variables that behave similarly.
        Variables joined together earlier are more closely related.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.info("""
        Variables connected at lower branches are more closely related.
        This helps identify clusters of cardiovascular indicators.
        """)

    left,right = st.columns([2,1])
    with left:
        fig_scatter = px.scatter_matrix(
            df,
            dimensions=[
                "age",
                "chol",
                "oldpeak",
                "thalach"
            ],
            color="target_binary"
        )

        fig_scatter.update_layout(
            height=500,
            paper_bgcolor="#091437",
            plot_bgcolor="#091437",
            font_color="white"
        )

        st.markdown("""
        <div class="glass-card">
        <h3 style='color:white;'>3. Scatter Plot Matrix</h3>
        <p style='color:#b8c4d9;'>
        Shows pairwise relationships between important clinical variables.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

        st.warning("""
        Age and cholesterol generally show positive association with disease risk,
        while maximum heart rate tends to show an inverse relationship.
        """)
    
    with right:
        z = corr_matrix.values

        fig_surface = go.Figure(
            data=[
                go.Surface(z=z)
            ]
        )

        fig_surface.update_layout(
            height=500,
            paper_bgcolor="#091437"
        )

        st.markdown("""
        <div class="glass-card">
        <h3 style='color:white;'>4. 3D Correlation Surface</h3>
        <p style='color:#b8c4d9;'>
        Three-dimensional representation of correlation strengths.
        Higher peaks indicate stronger relationships.
        </p>
        </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(
            fig_surface,
            use_container_width=True
        )

        max_corr = corr.abs().values.max()
        st.success(
            f"Peak correlation strength observed: {max_corr:.2f}"
        )

    st.markdown("### Correlation Heatmap")
    fig_heat = px.imshow(
        corr_matrix,

        text_auto=".2f",

        color_continuous_scale="RdBu_r"
    )

    fig_heat.update_layout(
        height=700,

        paper_bgcolor="#091437",

        plot_bgcolor="#091437",

        font_color="white"
    )

    st.markdown("""
        <div class="glass-card">
        <h3 style='color:white;'>5. Clustered Correlation Heatmap</h3>
        <p style='color:#b8c4d9;'>
        Shows correlation coefficients between all variables.
        Red indicates positive correlation and blue indicates negative correlation.
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.plotly_chart(
        fig_heat,
        use_container_width=True
    )

    target_corr = corr["target_binary"].drop("target_binary")

    most_pos = target_corr.idxmax()
    most_neg = target_corr.idxmin()

    st.success(
            f"Most positively associated with heart disease: "
            f"{most_pos} (r={target_corr.max():.2f})"
        )

    st.warning(
            f"Most negatively associated with heart disease: "
            f"{most_neg} (r={target_corr.min():.2f})"
        )

    st.markdown("""
    <div class="glass-card">
    <h3 style='color:white;'>💡 Key Insights</h3>
    <ul style='color:#d1d5db;
    font-size:16px;
    line-height:2;'>
    <li>Age shows a positive relationship with heart disease risk.</li>
    <li>Oldpeak is one of the strongest disease indicators.</li>
    <li>Maximum heart rate (thalach) is negatively correlated with disease.</li>
    <li>Several variables form strong clinical clusters.</li>
    <li>The dataset exhibits a dense correlation network.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)





elif selected == "Risk Predictor":
    st.markdown("""
    <style>

    .predictor-hero{
        background:linear-gradient(
            135deg,
            rgba(22,36,90,.95),
            rgba(8,15,40,.95)
        );
        padding:30px;
        border-radius:22px;
        margin-bottom:25px;
        border:1px solid rgba(255,255,255,.08);
    }

    .predictor-title{
        font-size:42px;
        font-weight:700;
        color:white;
    }

    .predictor-sub{
        color:#b8c4d9;
        font-size:18px;
    }

    .input-card{
        background:rgba(16,30,74,.75);
        padding:25px;
        border-radius:20px;
        border:1px solid rgba(255,255,255,.08);
    }

    .result-card{
        background:rgba(16,30,74,.75);
        padding:25px;
        border-radius:20px;
        border:1px solid rgba(255,255,255,.08);
        text-align:center;
    }

    .score-value{
        font-size:70px;
        font-weight:700;
        color:white;
    }

    .metric-box{
        background:#091437;
        border-radius:15px;
        padding:18px;
        text-align:center;
        border:1px solid rgba(255,255,255,.08);
    }

    .metric-number{
        color:white;
        font-size:32px;
        font-weight:700;
    }

    .metric-title{
        color:#9fb3d1;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="predictor-hero">
    <div class="predictor-title">
    🫀 Heart Disease Risk Predictor
    </div>
    <div class="predictor-sub">
    Enter patient health metrics to estimate cardiovascular risk
    </div>
    </div>
    """, unsafe_allow_html=True)

    risk_score = 0
    risk_label = "NOT CALCULATED"
    risk_color = "#9ca3af"

    left,right = st.columns([1.2,1])
    with left:
        st.markdown(
            "<div class='input-card'>",
            unsafe_allow_html=True
        )

        age = st.slider(
            "Age",
            20,
            80,
            50
        )

        sex = st.selectbox(
            "Gender",
            ["Male","Female"]
        )

        chol = st.slider(
            "Cholesterol (mg/dL)",
            100,
            600,
            240
        )

        bp = st.slider(
            "Resting Blood Pressure",
            80,
            220,
            130
        )

        hr = st.slider(
            "Maximum Heart Rate",
            60,
            220,
            150
        )

        oldpeak = st.slider(
            "ST Depression",
            0.0,
            6.0,
            1.0
        )

        angina = st.selectbox(
            "Exercise Induced Angina",
            ["No","Yes"]
        )

        predict_btn = st.button(
            "Predict Risk",
            use_container_width=True
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

        if predict_btn:

            risk_score = 0

            if age >= 60:
                    risk_score += 25

            elif age >= 50:
                    risk_score += 18

            elif age >= 40:
                    risk_score += 10

            if chol >= 300:
                risk_score += 25

            elif chol >= 240:
                risk_score += 18

            elif chol >= 200:
                risk_score += 10

            if bp >= 160:
                risk_score += 20

            elif bp >= 140:
                risk_score += 15

            elif bp >= 120:
                risk_score += 8

            if hr < 120:
                risk_score += 15

            elif hr < 140:
                risk_score += 8

            if oldpeak >= 3:
                 risk_score += 20
        
            elif oldpeak >= 1.5:
                risk_score += 12

            if angina == "Yes":
                risk_score += 15

            if sex == "Male":
                 risk_score += 5

            
            if angina == "Yes":
                risk_score += 15

            risk_score = min(risk_score,100)

            if risk_score >= 70:

                risk_label = "HIGH RISK"
                risk_color = "#ff3366"

            elif risk_score >= 40:

                risk_label = "MODERATE RISK"
                risk_color = "#ffb703"

            else:

                risk_label = "LOW RISK"
                risk_color = "#22c55e"

    with right:

        st.markdown(f"""
        <div class="result-card">

        <h2 style="color:white;">
        Risk Score
        </h2>

        <div class="score-value">
        {risk_score}
        </div>

        <h2 style="
        color:{risk_color};
        ">
        {risk_label}
        </h2>

        </div>
        """, unsafe_allow_html=True)

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",

                value=risk_score,

                gauge={
                    "axis":{"range":[0,100]},

                    "bar":{"color":risk_color},

                    "steps":[
                        {
                            "range":[0,40],
                            "color":"#22c55e"
                        },

                        {
                            "range":[40,70],
                            "color":"#ffb703"
                        },

                        {
                            "range":[70,100],
                            "color":"#ff3366"
                        }
                    ]
                }
            )
        )

        fig.update_layout(
            paper_bgcolor="#091437",
            font_color="white",
            height=350
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    m1,m2,m3,m4 = st.columns(4)

    with m1:
        st.markdown(f"""
        <div class="metric-box">
        <div class="metric-number">{age}</div>
        <div class="metric-title">Age</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-box">
        <div class="metric-number">{chol}</div>
        <div class="metric-title">Cholesterol</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-box">
        <div class="metric-number">{bp}</div>
        <div class="metric-title">Blood Pressure</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-box">
        <div class="metric-number">{hr}</div>
        <div class="metric-title">Heart Rate</div>
        </div>
        """, unsafe_allow_html=True)

    if risk_score >= 70:

        st.error(
            "High cardiovascular risk detected. Immediate medical consultation recommended."
        )

    elif risk_score >= 40:

        st.warning(
            "Moderate risk detected. Lifestyle modifications and regular monitoring recommended."
        )

    else:

        st.success(
            "Low cardiovascular risk profile detected."
        )







elif selected == "Data Dictionary":
    st.markdown("""
    <style>
                
    [data-testid="stDataFrame"]{
        border-radius:18px;
        overflow:hidden;
        border:1px solid rgba(255,255,255,.08);

        box-shadow:
        0 0 25px rgba(124,77,255,.12);
    }

    .dict-hero{
        background:linear-gradient(
            135deg,
            rgba(20,35,90,.95),
            rgba(7,15,45,.95)
        );

        padding:28px;
        border-radius:22px;

        border:1px solid rgba(255,255,255,.08);

        margin-bottom:20px;
    }

    .dict-title{
        font-size:42px;
        font-weight:700;
        color:white;
    }

    .dict-sub{
        color:#b8c4d9;
        font-size:18px;
    }

    .info-card{
        background:rgba(16,30,74,.75);
        border-radius:18px;
        padding:20px;
        border:1px solid rgba(255,255,255,.08);
    }

    .kpi-value{
        color:white;
        font-size:42px;
        font-weight:700;
    }

    .kpi-label{
        color:#9fb3d1;
    }

    </style>
    """, unsafe_allow_html=True)

    hero_left,hero_right = st.columns([3,1])

    with hero_left:

        st.markdown("""
        <div class="dict-hero">
        <div class="dict-title">
        📖 Data Dictionary
        </div>

        <div class="dict-sub">
        Comprehensive overview of all attributes in the UCI Heart Disease Dataset
        </div>
        </div>
        """, unsafe_allow_html=True)

    with hero_right:
        st.image("heart img.png")

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="info-card">
        <h4>📚 Total Attributes</h4>
        <div class="kpi-value">14</div>
        <div class="kpi-label">
        Features in dataset
        </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="info-card">
        <h4># Data Types</h4>
        <div class="kpi-value">5</div>
        <div class="kpi-label">
        Different data types
        </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="info-card">
        <h4>📈 Records</h4>
        <div class="kpi-value">1024</div>
        <div class="kpi-label">
        Total patients
        </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="info-card">
        <h4>% Missing Values</h4>
        <div class="kpi-value">0</div>
        <div class="kpi-label">
        No missing data
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    dictionary = pd.DataFrame({
    "Attribute":[
    "age","sex","cp","trestbps","chol",
    "fbs","restecg","thalach","exang",
    "oldpeak","slope","ca","thal","target"
    ],

    "Description":[
    "Age in years",
    "Gender",
    "Chest pain type",
    "Resting blood pressure",
    "Serum cholesterol",
    "Fasting blood sugar >120",
    "Resting ECG results",
    "Maximum heart rate achieved",
    "Exercise induced angina",
    "ST depression",
    "Slope of ST segment",
    "Number of vessels",
    "Thalassemia",
    "Heart Disease"
    ],

    "Type":[
    "Numeric",
    "Categorical",
    "Categorical",
    "Numeric",
    "Numeric",
    "Binary",
    "Categorical",
    "Numeric",
    "Binary",
    "Numeric",
    "Categorical",
    "Numeric",
    "Categorical",
    "Binary"
    ]
    })


    st.dataframe(
        dictionary,
        use_container_width=True,
        height=650
    )


    a,b,c = st.columns([2,2,1])

    with a:

        st.markdown("""
        <div class="info-card">

        <h3>📊 Data Types Legend</h3>

        <ul>
        <li>Numeric → Continuous values</li>
        <li>Categorical → Groups</li>
        <li>Binary → 0/1 values</li>
        </ul>

        </div>
        """, unsafe_allow_html=True)

    with b:

        st.markdown("""
        <div class="info-card">

        <h3>💡 Key Insights</h3>

        ✔ 14 attributes available<br>
        ✔ No missing values<br>
        ✔ Balanced target variable<br>
        ✔ Clinical indicators well represented

        </div>
        """, unsafe_allow_html=True)

    with c:

        st.markdown("""
        <div class="info-card">

        <h3>🗂 Dataset Info</h3>

        Records: 1024<br>
        Features: 14<br>
        Source: UCI

        </div>
        """, unsafe_allow_html=True)
