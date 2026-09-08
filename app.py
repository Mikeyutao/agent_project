import streamlit as st
from agent.react_agent import ReactAgent

st.set_page_config(
    page_title="智扫通 · 智能服务台",
    page_icon="⌂",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #17241f;
        --muted: #718079;
        --line: #dce7e0;
        --paper: #f6faf7;
        --mint: #d9f1df;
        --green: #1d6849;
        --lime: #a8d86c;
        --orange: #f09a62;
    }
    .stApp {
        background: radial-gradient(circle at 80% 0%, #e9f6e3 0, transparent 32%), var(--paper);
        color: var(--ink);
        font-family: 'DM Sans', 'Noto Sans SC', sans-serif;
    }
    [data-testid='stHeader'] { background: transparent; }
    [data-testid='stToolbar'] { visibility: hidden; }
    .block-container { max-width: 1480px; padding: 2.1rem 3.5rem 5rem; }
    [data-testid='stSidebar'] { background: #edf6ef; border-right: 1px solid var(--line); }
    [data-testid='stSidebar'] > div:first-child { padding: 2rem 1.3rem; }
    .brand { display: flex; align-items: center; gap: 12px; margin-bottom: 2.1rem; }
    .brand-mark { width: 42px; height: 42px; border-radius: 14px; background: var(--green); color: #fff; display: grid; place-items: center; font-size: 22px; box-shadow: 0 8px 18px #1d684933; }
    .brand-name { font-size: 1.15rem; font-weight: 800; letter-spacing: -.02em; }
    .brand-sub { color: var(--muted); font-size: .72rem; margin-top: 2px; }
    .eyebrow { color: var(--green); font-size: .75rem; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; margin-bottom: .6rem; }
    h1 { font-size: clamp(2.1rem, 4vw, 4.4rem) !important; line-height: 1.03 !important; letter-spacing: -.055em !important; margin: 0 !important; }
    .hero-copy { color: var(--muted); font-size: 1rem; max-width: 600px; line-height: 1.75; margin: 1rem 0 0; }
    .hero { display: flex; align-items: flex-end; justify-content: space-between; gap: 2rem; margin-bottom: 2.2rem; }
    .status-pill { display: inline-flex; align-items: center; gap: 8px; padding: 10px 14px; background: #fff; border: 1px solid var(--line); border-radius: 999px; color: var(--green); font-size: .82rem; font-weight: 700; white-space: nowrap; box-shadow: 0 8px 24px #2446340b; }
    .status-dot { width: 8px; height: 8px; border-radius: 50%; background: #67bd51; box-shadow: 0 0 0 4px #67bd5126; }
    .section-label { color: var(--muted); font-size: .75rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; margin: 1.4rem 0 .65rem; }
    .side-section { border-top: 1px solid var(--line); padding-top: 1.2rem; margin-top: 1.4rem; }
    .side-stat { display: flex; justify-content: space-between; padding: 9px 0; color: var(--muted); font-size: .82rem; }
    .side-stat strong { color: var(--ink); }
    .feature-card { height: 100%; padding: 1.35rem; border-radius: 20px; background: #fff; border: 1px solid var(--line); box-shadow: 0 12px 35px #2446340b; }
    .feature-icon { font-size: 1.4rem; margin-bottom: .65rem; }
    .feature-title { font-weight: 800; margin-bottom: .3rem; }
    .feature-text { color: var(--muted); font-size: .82rem; line-height: 1.55; }
    [data-testid='stChatMessage'] { background: #fff; border: 1px solid var(--line); border-radius: 18px; padding: 1rem 1.15rem; box-shadow: 0 8px 26px #24463408; }
    [data-testid='stChatMessage'][aria-label='assistant'] { border-left: 3px solid var(--lime); }
    [data-testid='stChatInput'] { border-color: #b8d4c1; box-shadow: 0 10px 30px #24463414; }
    .empty-state { margin: 2rem 0 1.3rem; padding: 2.4rem; border-radius: 24px; background: linear-gradient(135deg, #e4f5e4, #fff); border: 1px solid var(--line); }
    .empty-kicker { color: var(--green); font-size: .8rem; font-weight: 800; letter-spacing: .12em; }
    .empty-title { font-size: 1.55rem; font-weight: 800; margin: .45rem 0; letter-spacing: -.03em; }
    .empty-text { color: var(--muted); max-width: 650px; line-height: 1.6; }
    .footer-note { color: #93a19a; font-size: .75rem; text-align: center; margin-top: 2.2rem; }
    .stButton > button { border: 1px solid var(--line); background: #fff; color: var(--ink); border-radius: 12px; text-align: left; min-height: 42px; font-weight: 600; }
    .stButton > button:hover { border-color: var(--green); color: var(--green); }
    </style>
    """,
    unsafe_allow_html=True,
)

if "agent" not in st.session_state:
    st.session_state["agent"] = ReactAgent()

if "message" not in st.session_state:
    st.session_state["message"] = []

if "pending_prompt" not in st.session_state:
    st.session_state["pending_prompt"] = None

with st.sidebar:
    st.markdown(
        "<div class='brand'><div class='brand-mark'>⌁</div><div><div class='brand-name'>智扫通</div><div class='brand-sub'>INTELLIGENT SERVICE DESK</div></div></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-label'>服务能力</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='side-stat'><span>知识库问答</span><strong>在线</strong></div>
    <div class='side-stat'><span>使用报告</span><strong>可生成</strong></div>
    <div class='side-stat'><span>实时天气</span><strong>已接入</strong></div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='side-section'><div class='section-label'>当前会话</div></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='side-stat'><span>消息数量</span><strong>{len(st.session_state['message'])}</strong></div><div class='side-stat'><span>状态</span><strong>准备就绪</strong></div>",
        unsafe_allow_html=True,
    )
    if st.button("清空当前会话", use_container_width=True):
        st.session_state["message"] = []
        st.rerun()

st.markdown(
    "<div class='hero'><div><div class='eyebrow'>SMART HOME CARE · 01</div><h1>让每一次清洁，<br>都有答案。</h1><p class='hero-copy'>围绕扫地机器人使用、维护与选购的智能服务台。连接知识库与个性化使用记录，快速解决问题，也帮你把设备用得更好。</p></div><div class='status-pill'><span class='status-dot'></span>服务在线 · 智能响应中</div></div>",
    unsafe_allow_html=True,
)

feature_columns = st.columns(3)
features = [
    ("◌", "即时答疑", "操作指导、故障排查与日常维护，一问即得清晰建议。"),
    ("⌁", "个性报告", "分析你的使用记录，生成更贴合家庭场景的优化方案。"),
    ("◒", "场景联动", "查询天气、耗材状态与清洁策略，让服务更主动。"),
]
for column, (icon, title, text) in zip(feature_columns, features):
    with column:
        st.markdown(f"<div class='feature-card'><div class='feature-icon'>{icon}</div><div class='feature-title'>{title}</div><div class='feature-text'>{text}</div></div>", unsafe_allow_html=True)

st.markdown("<div class='section-label'>推荐从这里开始</div>", unsafe_allow_html=True)
quick_columns = st.columns(3)
quick_prompts = [
    "帮我生成本月扫地机器人使用报告",
    "扫地机器人应该多久清理一次尘盒？",
    "我想选购一台适合养宠家庭的扫地机器人",
]
for column, quick_prompt in zip(quick_columns, quick_prompts):
    with column:
        if st.button(quick_prompt, use_container_width=True):
            st.session_state["pending_prompt"] = quick_prompt
            st.rerun()

if not st.session_state["message"]:
    st.markdown(
        "<div class='empty-state'><div class='empty-kicker'>YOUR HOME, BETTER MAINTAINED</div><div class='empty-title'>从一个具体问题开始吧</div><div class='empty-text'>你可以询问设备操作、清洁维护、故障处理，也可以直接让智扫通分析你的月度使用情况。</div></div>",
        unsafe_allow_html=True,
    )

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

prompt = st.chat_input("输入你关于扫地机器人的问题...")
prompt = prompt or st.session_state.pop("pending_prompt", None)

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role": "user", "content": prompt})

    response_messages = []
    with st.spinner("正在整理你的专属建议..."):
        res_stream = st.session_state["agent"].execute_stream(prompt)

        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.chat_message("assistant").write_stream(capture(res_stream, response_messages))
        st.session_state["message"].append({"role": "assistant", "content": "".join(response_messages)})
        st.rerun()

st.markdown("<div class='footer-note'>智扫通智能客服 · 基于领域知识库与 Agent 协作能力</div>", unsafe_allow_html=True)
