import streamlit as st


def apply_styles():
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #eef6ff 0%, #f8fbff 45%, #f3fff8 100%);
            color: #102a43 !important;
        }

        main,
        main p,
        main div,
        main span,
        main label {
            color: #102a43 !important;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #143b66 0%, #1d588f 100%);
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] label span {
            color: white !important;
        }

        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] textarea {
            background-color: #ffffff !important;
            color: #102a43 !important;
            border: 1px solid #d0d7e2 !important;
            border-radius: 10px !important;
        }

        section[data-testid="stSidebar"] input::placeholder,
        section[data-testid="stSidebar"] textarea::placeholder {
            color: #6b7280 !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #102a43 !important;
            border-radius: 10px !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] span {
            color: #102a43 !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="tag"] {
            background-color: #e7f0ff !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="tag"] span {
            color: #102a43 !important;
        }

        .hero-box {
            background: linear-gradient(135deg, #1d588f 0%, #2f80ed 55%, #57cc99 100%);
            padding: 32px;
            border-radius: 26px;
            color: white !important;
            box-shadow: 0 12px 32px rgba(0,0,0,0.14);
            margin-bottom: 18px;
        }

        .hero-title {
            font-size: 36px;
            font-weight: 850;
            margin-bottom: 8px;
            color: white !important;
        }

        .hero-subtitle {
            font-size: 16px;
            opacity: 0.96;
            line-height: 1.6;
            color: white !important;
        }

        .custom-card {
            background: #ffffff;
            padding: 22px;
            border-radius: 22px;
            box-shadow: 0 8px 24px rgba(27, 55, 90, 0.08);
            border: 1px solid rgba(29,88,143,0.10);
            margin-bottom: 16px;
            color: #102a43 !important;
        }

        .custom-card p,
        .custom-card div,
        .custom-card b,
        .custom-card span {
            color: #102a43 !important;
        }

        .section-title {
            font-size: 22px;
            font-weight: 800;
            color: #0b2e4a !important;
            margin-bottom: 12px;
        }

        .soft-text {
            color: #34495e !important;
            font-size: 15px;
            line-height: 1.7;
        }

        button[data-baseweb="tab"] p,
        button[data-baseweb="tab"] div,
        button[data-baseweb="tab"] span {
            color: #0b2e4a !important;
            font-weight: 700 !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] p,
        button[data-baseweb="tab"][aria-selected="true"] div,
        button[data-baseweb="tab"][aria-selected="true"] span {
            color: #1d588f !important;
            font-weight: 800 !important;
        }

        .badge-low {
            display: inline-block;
            padding: 8px 16px;
            background: #d7f8df !important;
            color: #176c2f !important;
            border-radius: 999px;
            font-weight: 800;
            font-size: 14px;
        }

        .badge-mid {
            display: inline-block;
            padding: 8px 16px;
            background: #fff3cd !important;
            color: #8a6500 !important;
            border-radius: 999px;
            font-weight: 800;
            font-size: 14px;
        }

        .badge-high {
            display: inline-block;
            padding: 8px 16px;
            background: #ffd7d7 !important;
            color: #a31c1c !important;
            border-radius: 999px;
            font-weight: 800;
            font-size: 14px;
        }

        .mini-pill {
            display: inline-block;
            background: #eef5ff !important;
            color: #17406b !important;
            padding: 8px 13px;
            border-radius: 999px;
            margin: 4px 6px 4px 0;
            font-size: 13px;
            font-weight: 700;
            border: 1px solid #c8ddff !important;
        }

        .recommend-box {
            background: #f8fbff;
            border-left: 5px solid #57cc99;
            padding: 14px 16px;
            border-radius: 14px;
            margin-bottom: 10px;
            color: #17324d !important;
            font-size: 15px;
        }

        .warning-box {
            background: #fff8e6;
            border-left: 5px solid #f2c94c;
            padding: 15px 17px;
            border-radius: 14px;
            color: #5e4600 !important;
            margin-bottom: 14px;
            font-weight: 600;
        }

        .danger-box {
            background: #fff1f1;
            border-left: 5px solid #eb5757;
            padding: 15px 17px;
            border-radius: 14px;
            color: #7a1212 !important;
            margin-bottom: 14px;
            font-weight: 600;
        }

        .success-box {
            background: #effaf2;
            border-left: 5px solid #27ae60;
            padding: 15px 17px;
            border-radius: 14px;
            color: #176c2f !important;
            margin-bottom: 14px;
            font-weight: 600;
        }

        .qr-link-box {
            background: #f4f8ff !important;
            padding: 12px;
            border-radius: 12px;
            border: 1px solid #bcd7ff !important;
            color: #0b2e4a !important;
            font-size: 14px;
            word-break: break-all;
        }

        .note-box {
            background: #fffde7 !important;
            padding: 16px;
            border-radius: 14px;
            border: 1px solid #f2e98f;
            color: #5e5200 !important;
            font-weight: 600;
            line-height: 1.6;
        }

        .note-box b,
        .note-box span,
        .note-box div {
            color: #5e5200 !important;
        }

        .passport-url-box {
            background: #ffffff !important;
            border: 1px solid #bcd7ff !important;
            border-radius: 14px;
            padding: 14px 16px;
            margin-top: 8px;
            color: #0b2e4a !important;
            font-size: 15px;
            font-weight: 700;
            word-break: break-all;
            box-shadow: 0 4px 14px rgba(27, 55, 90, 0.06);
        }

        .passport-url-box a {
            color: #0b63ce !important;
            text-decoration: none;
            font-weight: 800;
        }

        .passport-url-box a:hover {
            text-decoration: underline;
        }

        .stButton > button {
            background: linear-gradient(135deg, #2f80ed 0%, #57cc99 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.65rem 1.15rem !important;
            font-weight: 800 !important;
        }

        .stButton > button p,
        .stButton > button span,
        .stButton > button div {
            color: white !important;
        }

        div[data-testid="stFormSubmitButton"] button {
            background: linear-gradient(135deg, #2f80ed 0%, #57cc99 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 800 !important;
        }

        div[data-testid="stFormSubmitButton"] button p,
        div[data-testid="stFormSubmitButton"] button span,
        div[data-testid="stFormSubmitButton"] button div {
            color: white !important;
        }

        .stDownloadButton > button {
            background: #1d588f !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.65rem 1.15rem !important;
            font-weight: 800 !important;
        }

        .stDownloadButton > button p,
        .stDownloadButton > button span,
        .stDownloadButton > button div {
            color: white !important;
        }

        .stDownloadButton > button:hover {
            background: #143b66 !important;
            color: white !important;
        }

        div[data-testid="stMetric"] {
            background: white;
            padding: 16px;
            border-radius: 18px;
            box-shadow: 0 6px 18px rgba(27, 55, 90, 0.07);
            border: 1px solid rgba(29,88,143,0.10);
        }

        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] div {
            color: #102a43 !important;
        }

        div[data-testid="stAlert"],
        div[data-testid="stAlert"] p,
        div[data-testid="stAlert"] div,
        div[data-testid="stAlert"] span {
            color: #102a43 !important;
        }

                .profile-card {
            background: #ffffff;
            border: 1px solid rgba(29,88,143,0.10);
            border-radius: 18px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 4px 12px rgba(27, 55, 90, 0.05);
        }

        .profile-row {
            margin-bottom: 16px;
        }

        .profile-row:last-child {
            margin-bottom: 0;
        }

        .profile-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            gap: 12px;
        }

        .profile-label {
            font-size: 15px;
            font-weight: 700;
            color: #0b2e4a !important;
        }

        .profile-score {
            font-size: 14px;
            font-weight: 800;
            color: #1d588f !important;
            background: #eef5ff;
            border: 1px solid #c8ddff;
            border-radius: 999px;
            padding: 4px 10px;
            min-width: 52px;
            text-align: center;
        }

        .profile-bar {
            width: 100%;
            height: 12px;
            background: #eaf1f8;
            border-radius: 999px;
            overflow: hidden;
        }

        .profile-fill {
            height: 12px;
            border-radius: 999px;
            background: linear-gradient(90deg, #2f80ed 0%, #57cc99 100%);
        }

        .profile-desc {
            font-size: 13px;
            color: #4f6478 !important;
            margin-top: 6px;
        }
                
        code {
            color: #0b2e4a !important;
        }
    </style>
    """, unsafe_allow_html=True)