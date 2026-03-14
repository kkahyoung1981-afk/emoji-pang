import streamlit as st
import random
import json

# --- CSS 스타일링 ---
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 80px;
        font-size: 30px;
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Constants ---
EMOJI_POOL = [
    '🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐯', '🦁', '🐷', '🐸', '🐵', '🐔', '🐧', '🐦',
    '🐤', '🐣', '🐥', '🐺', '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦟', '🦗', '🕷',
    '🦂', '🐢', '🐍', '🦎', '🦖', '🦕', '🐙', '🦑', '🦐', '🦞', '🦀', '🐡', '🐠', '🐟', '🐬', '🐳'
]
MATCH_SCORE = 100

# --- State Initialization ---
if 'screen' not in st.session_state: st.session_state.screen = 'START'
if 'cards' not in st.session_state: st.session_state.cards = []
if 'selected_cards' not in st.session_state: st.session_state.selected_cards = [] 
if 'score' not in st.session_state: st.session_state.score = 0
if 'difficulty' not in st.session_state: st.session_state.difficulty = 'EASY'

# --- Game Logic ---
def generate_board(difficulty):
    size = 16 if difficulty == 'EASY' else 25
    emojis = random.sample(EMOJI_POOL, size - 1)
    pair = random.choice(emojis)
    board = emojis + [pair]
    random.shuffle(board)
    return [{'id': i, 'emoji': e} for i, e in enumerate(board)]

def get_new_emoji(current_emojis):
    available = [e for e in EMOJI_POOL if e not in current_emojis]
    return random.choice(available) if available else '🍎'

def handle_card_click(index, emoji):
    st.session_state.selected_cards.append((index, emoji))
    if len(st.session_state.selected_cards) == 2:
        (idx1, emj1), (idx2, emj2) = st.session_state.selected_cards
        if emj1 == emj2:
            st.session_state.score += MATCH_SCORE
            st.toast("팡! 100점 획득!", icon="🎉")
            
            # 카드 교체 로직
            current_emojis = [c['emoji'] for c in st.session_state.cards]
            for idx in [idx1, idx2]:
                st.session_state.cards[idx]['emoji'] = get_new_emoji(current_emojis)
            
            # 짝 맞추기 로직
            others = [i for i in range(len(st.session_state.cards)) if i not in [idx1, idx2]]
            if others:
                target_idx = random.choice(others)
                st.session_state.cards[target_idx]['emoji'] = st.session_state.cards[idx1]['emoji']
        else:
            st.toast("틀렸어요!", icon="❌")
        st.session_state.selected_cards = []

# --- UI Screens ---
def render_start():
    st.title("이모지 팡! 팡!")
    st.session_state.difficulty = st.radio("난이도 선택", ['EASY', 'NORMAL'])
    if st.button("게임 시작!"):
        st.session_state.cards = generate_board(st.session_state.difficulty)
        st.session_state.score = 0
        st.session_state.screen = 'GAME'
        st.rerun()

def render_game():
    st.subheader(f"현재 점수: {st.session_state.score}")
    cols_count = 4 if st.session_state.difficulty == 'EASY' else 5
    cols = st.columns(cols_count)
    
    for i, card in enumerate(st.session_state.cards):
        if cols[i % cols_count].button(card['emoji'], key=card['id']):
            handle_card_click(card['id'], card['emoji'])
            st.rerun()
    
    if st.button("처음으로"):
        st.session_state.screen = 'START'
        st.rerun()

# --- Main Flow ---
if st.session_state.screen == 'START':
    render_start()
else:
    render_game()