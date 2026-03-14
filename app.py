import streamlit as st
import random
import time

# --- CSS: 이모지를 아주 크게, 간격 없이 딱 붙임 ---
st.markdown("""
    <style>
    /* 전체 레이아웃 밀착 */
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    
    /* 버튼 크기 및 간격 조정 */
    div.stButton > button {
        width: 100% !important;
        height: 110px !important;
        font-size: 60px !important;
        padding: 0 !important;
        margin: 0 !important;
        border-radius: 5px !important;
        background-color: #ffffff !important;
        border: 1px solid #ccc !important;
    }
    
    /* 컬럼 간격 최소화 */
    [data-testid="column"] {
        padding: 0px !important;
        gap: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- State 초기화 ---
if 'screen' not in st.session_state: st.session_state.screen = 'START'
if 'cards' not in st.session_state: st.session_state.cards = []
if 'score' not in st.session_state: st.session_state.score = 0
if 'time_left' not in st.session_state: st.session_state.time_left = 15

# --- Sound (HTML5) ---
def play_sound(type):
    url = "https://actions.google.com/sounds/v1/ui/positive_tap.ogg" if type == 'correct' else "https://actions.google.com/sounds/v1/ui/error.ogg"
    st.markdown(f'<audio src="{url}" autoplay="true"></audio>', unsafe_allow_html=True)

# --- 게임 화면 ---
def render_game():
    st.subheader(f"닉네임: {st.session_state.nickname} | 점수: {st.session_state.score}")
    
    # 타이머 표시용 플레이스홀더
    timer_placeholder = st.empty()
    
    # 시간 표시 루프
    start_time = st.session_state.get('start_time', time.time())
    elapsed = time.time() - start_time
    st.session_state.time_left = max(0, 15 - int(elapsed))
    
    timer_placeholder.metric("남은 시간", f"{st.session_state.time_left}초")
    
    if st.session_state.time_left <= 0:
        st.session_state.screen = 'RESULT'
        st.rerun()

    # 카드 배열 (4x4 또는 5x5)
    cols_count = 4 if st.session_state.difficulty == 'EASY' else 5
    # 전체 버튼을 담을 컨테이너
    container = st.container()
    
    # 2차원 처럼 보이게 컬럼 생성
    for row in range(cols_count):
        cols = container.columns(cols_count)
        for col_idx in range(cols_count):
            idx = row * cols_count + col_idx
            if idx < len(st.session_state.cards):
                card = st.session_state.cards[idx]
                if cols[col_idx].button(card['emoji'], key=card['id']):
                    # 매칭 로직 (예시: 여기서는 클릭 시 100점 추가 및 시간 연장)
                    st.session_state.score += 100
                    st.session_state.start_time += 3 # 3초 추가
                    play_sound('correct')
                    st.rerun()

# --- 시작 화면 ---
def render_start():
    st.title("🧩 이모지 팡!")
    st.session_state.nickname = st.text_input("닉네임을 입력하세요", "플레이어")
    st.session_state.difficulty = st.radio("난이도", ['EASY', 'NORMAL'])
    if st.button("게임 시작!"):
        st.session_state.cards = [{'id': i, 'emoji': '🍎'} for i in range(16)] # 예시 카드
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.session_state.screen = 'GAME'
        st.rerun()

# --- 실행 ---
if st.session_state.screen == 'START': render_start()
elif st.session_state.screen == 'GAME': render_game()
elif st.session_state.screen == 'RESULT':
    st.title(f"게임 종료! {st.session_state.score}점")
    if st.button("다시 하기"): st.session_state.screen = 'START'; st.rerun()