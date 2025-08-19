import random
import streamlit as st

st.set_page_config(page_title="Guess the Number", page_icon="🎯", layout="centered")

# --- Init state ---
ss = st.session_state
if "low" not in ss:
    ss.low, ss.high = 1, 100
if "game_id" not in ss:
    ss.game_id = 0                    # increments on "Play again" or difficulty change
if "secret" not in ss:
    ss.secret = random.randint(ss.low, ss.high)
if "attempts" not in ss:
    ss.attempts = 0
if "message" not in ss:
    ss.message = f"I'm thinking of a number between {ss.low} and {ss.high}."

st.title("🎯 Guess the Number")

# --- Difficulty selector ---
DIFFICULTIES = {
    "Easy (1–50)": (1, 50),
    "Medium (1–100)": (1, 100),
    "Hard (1–500)": (1, 500),
}

def set_difficulty():
    low, high = DIFFICULTIES[ss.difficulty]

    # Clear the previous guess for the old input widget (optional but tidy)
    prev_key = f"guess_{ss.game_id}"
    ss.pop(prev_key, None)

    # Update range and bump game_id to force a fresh number_input instance
    ss.low, ss.high = low, high
    ss.game_id += 1
    ss.secret = random.randint(low, high)
    ss.attempts = 0
    ss.message = f"New game! I'm thinking of a number between {low} and {high}."
    # NOTE: No st.rerun() here; selectbox change already triggers a rerun.

st.selectbox(
    "Difficulty",
    list(DIFFICULTIES.keys()),
    index=1,                           # default to Medium
    key="difficulty",
    on_change=set_difficulty,
)

st.write(ss.message)

# --- Callback: runs when the input changes (press Enter) ---
def check_guess():
    key = f"guess_{ss.game_id}"
    g = ss.get(key, None)
    if g is None:
        return
    ss.attempts += 1
    if g < ss.secret:
        ss.message = "Too low! Try again."
    elif g > ss.secret:
        ss.message = "Too high! Try again."
    else:
        ss.message = (
            f"✅ Correct! The number was {ss.secret}. "
            f"You took {ss.attempts} {'try' if ss.attempts == 1 else 'tries'}."
        )

# Number input with a PER-GAME key so it resets after Play again/difficulty change
current_key = f"guess_{ss.game_id}"
st.number_input(
    "Your guess:",
    min_value=ss.low,
    max_value=ss.high,
    step=1,
    key=current_key,
    on_change=check_guess,
)

# --- Reset game ---
if st.button("Play again"):
    ss.game_id += 1
    ss.secret = random.randint(ss.low, ss.high)
    ss.attempts = 0
    ss.message = f"New game! I'm thinking of a number between {ss.low} and {ss.high}."
    # No st.rerun() needed; button interaction already reruns the script.

st.caption("Built with Streamlit in GitHub Codespaces")
