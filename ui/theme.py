import streamlit as st


DEFAULT_THEME = {
    "primary_color": "#0B66C3",
    "button_color": "#E7F1FD",
    "background_color": "#FFFFFF",
    "sidebar_color": "#F5F7FA",
    "text_color": "#1F2937",
    "font_family": "Arial",
    "font_size": 16,
    "mode": "light",
}


def init_theme():
    for key, value in DEFAULT_THEME.items():
        session_key = f"theme_{key}"
        if session_key not in st.session_state:
            st.session_state[session_key] = value


def get_theme():
    init_theme()
    return {
        key: st.session_state[f"theme_{key}"]
        for key in DEFAULT_THEME
    }


def apply_theme():
    theme = get_theme()

    primary = theme["primary_color"]
    button = theme["button_color"]
    background = theme["background_color"]
    sidebar = theme["sidebar_color"]
    text = theme["text_color"]
    font = theme["font_family"]
    size = int(theme["font_size"])

    st.markdown(
        f"""
        <style>
        :root {{
            --erp-primary: {primary};
            --erp-button: {button};
            --erp-bg: {background};
            --erp-sidebar: {sidebar};
            --erp-text: {text};
        }}

        html, body, [class*="css"] {{
            font-family: "{font}", sans-serif !important;
            font-size: {size}px !important;
        }}

        .stApp {{
            background-color: {background} !important;
            color: {text} !important;
        }}

        [data-testid="stSidebar"] {{
            background-color: {sidebar} !important;
        }}

        [data-testid="stSidebar"] * {{
            color: {text};
        }}

        h1, h2, h3, h4, h5, h6, p, label {{
            color: {text};
        }}

        div[data-testid="stButton"] > button {{
            background-color: {button} !important;
            color: {primary} !important;
            border: 1px solid {primary}33 !important;
            border-radius: 12px !important;
        }}

        div[data-testid="stButton"] > button:hover {{
            border-color: {primary} !important;
            color: {primary} !important;
        }}

        div[data-testid="stMetric"] {{
            background-color: {button};
            border-radius: 12px;
            padding: 10px;
        }}

        a {{
            color: {primary} !important;
        }}

        div[role="radiogroup"] label[data-baseweb="radio"] {{
            border-radius: 8px;
        }}

        input, textarea {{
            color: {text} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def set_theme(values):
    for key in DEFAULT_THEME:
        if key in values:
            st.session_state[f"theme_{key}"] = values[key]
