import streamlit as st
import random

# --- Constants ---
EMOJI_POOL = [
    '🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐯', '🦁', '🐷', '🐸', '🐵', '🐔', '🐧', '🐦',
    '🐤', '🐣', '🐥', '🐺', '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦟', '🦗', '🕷',
    '🦂', '🐢', '🐍', '🦎', '🦖', '🦕', '🐙', '🦑', '🦐', '🦞', '🦀', '🐡', '🐠', '🐟', '🐬', '🐳',
    '🐋', '🦈', '🐊', '🐅', '🐆', '🦓', '🦍', '🦧', '🐘', '🦛', '🦏', '🐪', '🐫', '🦒', '🦘', '🐃'
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
    # 현재 풀에서 무작위로 선택
    emojis = random.sample(EMOJI_POOL, size - 1)
    pair = random.choice(emojis)
    board = emojis + [pair]
    random.shuffle(board)
    return [{'id': i, 'emoji': e} for i, e in enumerate(board)]

def get_new_emoji(current_emojis):
    # 보드에 없는 새로운 이모지 하나 반환
    available = [e for e in EMOJI_POOL if e not in current_emojis]
    return random.choice(available) if available else '🍎'

def handle_card_click(index, emoji):
    # 클릭한 카드 기록
    st.session_state.selected_cards.append((index, emoji))

    if len(st.session_state.selected_cards) == 2:
        (idx1, emj1), (idx2, emj2) = st.session_state.selected_cards
        
        if emj1 == emj2:
            st.session_state.score += MATCH_SCORE
            st.toast("팡! 100점 획득!", icon="🎉")
            
            # 맞춘 두 카드 교체
            current_emojis = [c['emoji'] for c in st.session_state.cards]
            for idx in [idx1, idx2]:
                st.session_state.cards[idx]['emoji'] = get_new_emoji(current_emojis)
                # 교체 후 중복이 발생하지 않도록 짝을 맞춰주는 로직
            
            # 교체 후 짝을 다시 보장하기 위해 무작위로 하나 더 교체
            target_idx = random.choice([i for i in range(len(st.session_state.cards)) if i not in [idx1, idx2]])
            st.session_state.cards[target_idx]['emoji'] = st.session_state.cards[idx1]['emoji']
            
        else:
            st.toast("틀렸어요!", icon="❌")
        
        st.session_state.selected_cards = []

# --- UI Screens ---
def render_game():
    st.subheader(f"점수: {st.session_state.score}")
    
    cols_count = 4 if st.session_state.difficulty == 'EASY' else 5
    cols = st.columns(cols_count)
    
    for i, card in enumerate(st.session_state.cards):
        if cols[i % cols_count].button(card['emoji'], key=card['id']):
            handle_card_click(card['id'], card['emoji'])
            st.rerun()

# --- Main Flow ---
# ... 이전 Start 화면 로직 동일 ...