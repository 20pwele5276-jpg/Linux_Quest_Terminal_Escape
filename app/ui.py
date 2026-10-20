import html
import time
from pathlib import Path

import streamlit as st

from app.missions import MISSIONS
from app.game_engine import (
    check_command,
    execute_game_command,
    get_mission,
    reset_game_world,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="LINUX QUEST // TERMINAL ESCAPE",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# FUTURISTIC CYBERPUNK UI
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&display=swap');

    :root {
        --navy: #07111f;
        --panel: #0b192b;
        --panel-light: #10223a;
        --cyan: #45f3ff;
        --violet: #a78bfa;
        --green: #56ff9f;
        --red: #ff5277;
        --text: #e6f3ff;
        --muted: #8ca6c5;
        --border: rgba(69, 243, 255, 0.24);
    }

    .stApp {
        background:
            radial-gradient(ellipse at 12% 0%, rgba(32, 90, 145, 0.20), transparent 38%),
            radial-gradient(ellipse at 90% 15%, rgba(112, 55, 180, 0.15), transparent 35%),
            linear-gradient(rgba(69, 243, 255, 0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(69, 243, 255, 0.025) 1px, transparent 1px),
            var(--navy);
        background-size: auto, auto, 34px 34px, 34px 34px, auto;
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: rgba(7, 17, 31, 0.92);
    }

    [data-testid="stToolbar"] {
        right: 1rem;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.7rem;
        padding-bottom: 2.5rem;
    }

    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 1px;
    }

    h1 {
        color: var(--cyan) !important;
        font-size: clamp(1.5rem, 3vw, 2.4rem) !important;
        text-shadow: 0 0 18px rgba(69, 243, 255, 0.25);
    }

    h2, h3 {
        color: var(--text) !important;
    }

    p, label, li, .stMarkdown {
        color: var(--text);
    }

    [data-testid="stCaptionContainer"] p {
        color: var(--muted) !important;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 27px 30px;
        margin-bottom: 20px;
        border: 1px solid rgba(69, 243, 255, 0.42);
        border-left: 4px solid var(--cyan);
        border-radius: 12px;
        background: linear-gradient(
            110deg,
            rgba(12, 32, 54, 0.96),
            rgba(17, 24, 50, 0.93)
        );
        box-shadow:
            0 0 28px rgba(69, 243, 255, 0.07),
            inset 0 0 25px rgba(69, 243, 255, 0.025);
    }

    .hero-title {
        color: var(--cyan);
        font-family: 'Orbitron', sans-serif;
        font-weight: 800;
        letter-spacing: 2px;
        line-height: 1.4;
        font-size: clamp(1.3rem, 3vw, 2rem);
    }

    .hero-subtitle {
        margin-top: 8px;
        color: #b7cce5;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.86rem;
        letter-spacing: 1px;
    }

    .online {
        color: var(--green);
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.76rem;
        letter-spacing: 1px;
    }

    .section-label {
        color: var(--cyan);
        font-family: 'Orbitron', sans-serif;
        font-size: 0.92rem;
        letter-spacing: 1.4px;
        font-weight: 700;
        margin: 12px 0;
    }

    .panel {
        padding: 17px;
        margin-bottom: 14px;
        border: 1px solid var(--border);
        border-radius: 10px;
        background: linear-gradient(
            145deg,
            rgba(14, 32, 53, 0.97),
            rgba(8, 21, 37, 0.97)
        );
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.13);
    }

    .mission-card {
        position: relative;
        padding: 12px 13px;
        margin-bottom: 9px;
        border: 1px solid rgba(140, 166, 197, 0.15);
        border-radius: 7px;
        background: rgba(11, 25, 43, 0.90);
        transition: border-color 0.2s ease;
    }

    .mission-card.active {
        border-color: var(--cyan);
        background: linear-gradient(
            100deg,
            rgba(69, 243, 255, 0.11),
            rgba(12, 27, 46, 0.95)
        );
        box-shadow:
            inset 3px 0 0 var(--cyan),
            0 0 13px rgba(69, 243, 255, 0.08);
    }

    .mission-card.complete {
        border-color: rgba(86, 255, 159, 0.38);
        background: rgba(19, 57, 48, 0.35);
    }

    .mission-card.locked {
        opacity: 0.65;
    }

    .mission-number {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 1px;
        color: var(--muted);
    }

    .mission-name {
        color: var(--text);
        font-size: 1.02rem;
        font-weight: 700;
        margin-top: 4px;
    }

    .mission-status {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.69rem;
        letter-spacing: 0.8px;
        margin-top: 5px;
    }

    .mission-card.active .mission-status {
        color: var(--cyan);
    }

    .mission-card.complete .mission-status {
        color: var(--green);
    }

    .mission-card.locked .mission-status {
        color: var(--muted);
    }

    .terminal-frame {
        padding: 15px;
        border: 1px solid rgba(86, 255, 159, 0.42);
        border-radius: 9px;
        background: #040b13;
        box-shadow:
            0 0 22px rgba(86, 255, 159, 0.06),
            inset 0 0 20px rgba(86, 255, 159, 0.025);
    }

    .terminal-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        padding-bottom: 12px;
        margin-bottom: 12px;
        border-bottom: 1px solid rgba(86, 255, 159, 0.20);
        color: var(--green);
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.76rem;
    }

    .terminal-output {
        height: 245px;
        overflow-y: auto;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
        color: var(--green);
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.88rem;
        line-height: 1.8;
    }

    .terminal-output::-webkit-scrollbar {
        width: 5px;
    }

    .terminal-output::-webkit-scrollbar-thumb {
        background: rgba(86, 255, 159, 0.35);
        border-radius: 5px;
    }

    .hud-card {
        min-height: 100px;
        padding: 15px;
        border: 1px solid rgba(69, 243, 255, 0.26);
        border-radius: 9px;
        background: linear-gradient(
            145deg,
            rgba(15, 34, 56, 0.98),
            rgba(9, 22, 39, 0.98)
        );
    }

    .hud-label {
        color: var(--muted);
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 1px;
    }

    .hud-value {
        margin-top: 10px;
        color: var(--cyan);
        font-family: 'Orbitron', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
    }

    .hud-value.green {
        color: var(--green);
    }

    .objective-card {
        padding: 20px;
        margin: 10px 0 16px;
        border: 1px solid rgba(167, 139, 250, 0.38);
        border-left: 4px solid var(--violet);
        border-radius: 9px;
        background: linear-gradient(
            110deg,
            rgba(42, 31, 72, 0.45),
            rgba(12, 26, 45, 0.94)
        );
    }

    .objective-tag {
        color: var(--violet);
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.76rem;
        letter-spacing: 1px;
    }

    .objective-title {
        margin: 12px 0;
        color: var(--text);
        font-family: 'Orbitron', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
    }

    .objective-description {
        color: #c4d5e9;
        font-size: 1.05rem;
    }

    .reward {
        color: var(--green);
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.8rem;
        margin-top: 15px;
    }

    .footer {
        margin-top: 25px;
        padding-top: 13px;
        border-top: 1px solid rgba(69, 243, 255, 0.16);
        color: var(--muted);
        text-align: center;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.6px;
    }

    .stTextInput input {
        background: #07131d !important;
        color: var(--green) !important;
        border: 1px solid rgba(86, 255, 159, 0.35) !important;
        border-radius: 7px !important;
        font-family: 'Share Tech Mono', monospace !important;
    }

    .stTextInput input:focus {
        border-color: var(--green) !important;
        box-shadow: 0 0 10px rgba(86, 255, 159, 0.14) !important;
    }

    .stButton button {
        min-height: 42px;
        border: 1px solid rgba(69, 243, 255, 0.42);
        border-radius: 7px;
        background: linear-gradient(
            110deg,
            rgba(16, 45, 68, 0.98),
            rgba(28, 28, 61, 0.98)
        );
        color: var(--cyan);
        font-family: 'Orbitron', sans-serif;
        font-size: 0.73rem;
        font-weight: 600;
        letter-spacing: 0.6px;
        transition: all 0.2s ease;
    }

    .stButton button:hover {
        border-color: var(--cyan);
        color: #ffffff;
        box-shadow: 0 0 15px rgba(69, 243, 255, 0.15);
    }

    div[data-testid="stAlert"] {
        border-radius: 8px;
    }

    [data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, var(--cyan), var(--violet));
    }

    @media (max-width: 800px) {
        .block-container {
            padding-top: 1rem;
        }

        .hero {
            padding: 20px;
        }

        .terminal-output {
            height: 210px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# GAME STATE
# ============================================================

def initialize_game():
    defaults = {
        "current_mission": 1,
        "xp": 0,
        "lives": 3,
        "completed": [],
        "terminal_history": [
            "LINUX QUEST OPERATING SYSTEM",
            "SECURE CONNECTION ESTABLISHED.",
            "OPERATOR AUTHENTICATION: VERIFIED.",
            "AWAITING OPERATOR INPUT...",
        ],
        "hint_used": [],
        "game_over": False,
        "victory": False,
        "start_time": time.time(),
        "timer_seconds": 600,
        "command_input": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = (
                value.copy() if isinstance(value, list) else value
            )


def restart_game():
    reset_game_world()

    st.session_state.current_mission = 1
    st.session_state.xp = 0
    st.session_state.lives = 3
    st.session_state.completed = []
    st.session_state.terminal_history = [
        "LINUX QUEST OPERATING SYSTEM",
        "SECURE CONNECTION ESTABLISHED.",
        "OPERATOR AUTHENTICATION: VERIFIED.",
        "AWAITING OPERATOR INPUT...",
    ]
    st.session_state.hint_used = []
    st.session_state.game_over = False
    st.session_state.victory = False
    st.session_state.start_time = time.time()
    st.session_state.command_input = ""


def add_terminal(message):
    st.session_state.terminal_history.append(str(message))
    st.session_state.terminal_history = (
        st.session_state.terminal_history[-30:]
    )


def restart_callback():
    restart_game()


def use_hint():
    mission_id = st.session_state.current_mission
    mission = get_mission(mission_id)

    if mission is None:
        return

    if mission_id in st.session_state.hint_used:
        add_terminal("INTEL: This mission's hint has already been used.")
        return

    add_terminal(f"INTEL // {mission['hint']}")
    st.session_state.hint_used.append(mission_id)


def submit_command():
    command = st.session_state.command_input.strip()

    if not command:
        return

    add_terminal(f"operator@linux-quest:~$ {command}")

    if command == "clear":
        st.session_state.terminal_history = []
        st.session_state.command_input = ""
        return

    if st.session_state.game_over or st.session_state.victory:
        add_terminal("SESSION CLOSED // Restart to play again.")
        st.session_state.command_input = ""
        return

    mission = get_mission(st.session_state.current_mission)

    if mission is None:
        st.session_state.victory = True
        st.session_state.command_input = ""
        return

    # All commands are simulated; they do not execute on Ubuntu.
    output = execute_game_command(command)
    add_terminal(output)

    if command == mission["expected_command"]:
        result = check_command(
            st.session_state.current_mission,
            command,
        )

        if result["success"]:
            st.session_state.xp += result["points"]

            if st.session_state.current_mission not in st.session_state.completed:
                st.session_state.completed.append(
                    st.session_state.current_mission
                )

            add_terminal(f"ACCESS GRANTED // {result['message']}")
            add_terminal(f"REWARD RECEIVED // +{result['points']} XP")

            if st.session_state.current_mission >= len(MISSIONS):
                st.session_state.victory = True
            else:
                st.session_state.current_mission += 1

        else:
            add_terminal(f"MISSION ERROR // {result['message']}")

    else:
        # Exploration commands help learners practise without punishment.
        if command in ("help", "ls", "pwd", "ps"):
            add_terminal("PRACTICE MODE // Explore safely.")
        else:
            st.session_state.lives -= 1
            add_terminal("ACCESS DENIED // Incorrect mission command.")
            add_terminal(f"OPERATOR LIVES // {st.session_state.lives}")

            if st.session_state.lives <= 0:
                st.session_state.game_over = True

    st.session_state.command_input = ""


initialize_game()


# ============================================================
# TIMER AND STATUS
# ============================================================

elapsed = int(time.time() - st.session_state.start_time)
remaining = max(0, st.session_state.timer_seconds - elapsed)
minutes, seconds = divmod(remaining, 60)

if remaining == 0 and not st.session_state.victory:
    st.session_state.game_over = True


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="online">● SYSTEM ONLINE &nbsp; // &nbsp; SECURE CHANNEL</div>
        <div class="hero-title">LINUX QUEST // TERMINAL ESCAPE</div>
        <div class="hero-subtitle">
            OPERATION: ROOT ACCESS &nbsp; • &nbsp;
            ENVIRONMENT: SIMULATED LINUX &nbsp; • &nbsp;
            CLEARANCE: OPERATOR
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ============================================================
# BACKGROUND MUSIC
# ============================================================

music_path = (
    Path(__file__).resolve().parent.parent
    / "assets"
    / "hacker_theme.mp3"
)

with st.expander("🎵 BACKGROUND MUSIC // SYNTHETIC DECEPTION", expanded=False):
    if music_path.exists():
        st.caption("Cinematic cyberpunk soundtrack // Loop enabled")
        st.audio(
            music_path.read_bytes(),
            format="audio/mp3",
            loop=True,
        )
    else:
        st.warning("Soundtrack file not found in the assets folder.")


# VICTORY / GAME OVER
# ============================================================

if st.session_state.victory:
    st.markdown(
        """
        <div class="hero">
            <div class="online">● ALL SECURITY LOCKS CLEARED</div>
            <div class="hero-title">MISSION COMPLETE // ESCAPE SUCCESSFUL</div>
            <div class="hero-subtitle">
                THE SERVER IS BEHIND YOU. YOUR OPERATOR RECORD HAS BEEN UPDATED.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.metric("FINAL EXPERIENCE", st.session_state.xp)
    st.write(f"Sectors cleared: {len(st.session_state.completed)} / {len(MISSIONS)}")
    st.button(
        "↻ RESTART OPERATION",
        on_click=restart_callback,
        use_container_width=True,
    )
    st.stop()


if st.session_state.game_over:
    st.markdown(
        """
        <div class="hero">
            <div class="online" style="color:#ff5277;">● OPERATOR CONNECTION LOST</div>
            <div class="hero-title" style="color:#ff5277;">
                SYSTEM LOCKDOWN // GAME OVER
            </div>
            <div class="hero-subtitle">
                OPERATION TERMINATED. RESET THE SIMULATION TO TRY AGAIN.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.metric("EXPERIENCE RECOVERED", st.session_state.xp)
    st.button(
        "↻ RETRY OPERATION",
        on_click=restart_callback,
        use_container_width=True,
    )
    st.stop()


# ============================================================
# MISSION MAP AND TERMINAL
# ============================================================

map_column, game_column = st.columns([0.88, 1.75], gap="large")


with map_column:
    st.markdown(
        '<div class="section-label">◈ MISSION MAP</div>',
        unsafe_allow_html=True,
    )

    progress = len(st.session_state.completed) / len(MISSIONS)

    st.progress(
        progress,
        text=f"{len(st.session_state.completed):02d} / {len(MISSIONS):02d} SECTORS CLEARED",
    )

    for item in MISSIONS:
        mission_id = item["id"]

        if mission_id in st.session_state.completed:
            state_class = "complete"
            state_text = "✓ SECTOR CLEARED"

        elif mission_id == st.session_state.current_mission:
            state_class = "active"
            state_text = "▶ ACTIVE SECTOR"

        else:
            state_class = "locked"
            state_text = "🔒 LOCKED"

        st.markdown(
            f"""
            <div class="mission-card {state_class}">
                <div class="mission-number">SECTOR {mission_id:02d}</div>
                <div class="mission-name">{html.escape(item['title'].split(': ', 1)[-1])}</div>
                <div class="mission-status">{state_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


with game_column:
    st.markdown(
        '<div class="section-label">◈ ROOT ACCESS TERMINAL</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="terminal-frame">
            <div class="terminal-top">
                <span>● SSH // ENCRYPTED SIMULATION</span>
                <span>NODE: LQ-01</span>
            </div>
        """,
        unsafe_allow_html=True,
    )

    history = "\n".join(
        html.escape(str(line))
        for line in st.session_state.terminal_history
    )

    st.markdown(
        f'<div class="terminal-output">{history}</div></div>',
        unsafe_allow_html=True,
    )

    st.text_input(
        "COMMAND INPUT",
        key="command_input",
        placeholder="Enter Linux command...",
        on_change=submit_command,
    )

    execute_column, hint_column, restart_column = st.columns(
        [1.15, 0.8, 0.95],
        gap="small",
    )

    with execute_column:
        st.button(
            "▶ EXECUTE",
            key="execute_button",
            on_click=submit_command,
            use_container_width=True,
        )

    with hint_column:
        st.button(
            "◈ HINT",
            key="hint_button",
            on_click=use_hint,
            use_container_width=True,
        )

    with restart_column:
        st.button(
            "↻ RESTART",
            key="restart_button",
            on_click=restart_callback,
            use_container_width=True,
        )

    st.markdown(
        '<div class="section-label">◈ OPERATOR HUD</div>',
        unsafe_allow_html=True,
    )

    hud1, hud2, hud3 = st.columns(3, gap="small")

    with hud1:
        st.markdown(
            f"""
            <div class="hud-card">
                <div class="hud-label">EXPERIENCE POINTS</div>
                <div class="hud-value">{st.session_state.xp:04d}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hud2:
        hearts = "♥ " * st.session_state.lives
        st.markdown(
            f"""
            <div class="hud-card">
                <div class="hud-label">OPERATOR LIVES</div>
                <div class="hud-value green">{hearts or "0"}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hud3:
        timer_color = "#ff5277" if remaining < 120 else "#45f3ff"
        st.markdown(
            f"""
            <div class="hud-card">
                <div class="hud-label">COUNTDOWN</div>
                <div class="hud-value" style="color:{timer_color};">
                    {minutes:02d}:{seconds:02d}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    mission = get_mission(st.session_state.current_mission)

    if mission:
        st.markdown(
            f"""
            <div class="objective-card">
                <div class="objective-tag">
                    ◈ ACTIVE OBJECTIVE // SECTOR {mission['id']:02d}
                </div>
                <div class="objective-title">
                    {html.escape(mission['title'].split(': ', 1)[-1])}
                </div>
                <div class="objective-description">
                    {html.escape(mission['story'])}
                </div>
                <div class="objective-description" style="margin-top:10px;">
                    {html.escape(mission['objective'])}
                </div>
                <div class="reward">
                    REWARD: +{mission['points']} XP
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.markdown(
    """
    <div class="footer">
        LINUX QUEST // TERMINAL ESCAPE &nbsp; • &nbsp;
        COMMANDS ARE SIMULATED &nbsp; • &nbsp;
        LEARN. EXECUTE. ESCAPE.
    </div>
    """,
    unsafe_allow_html=True,
)
