
import streamlit as st
import random
import matplotlib.pyplot as plt

def simulate_grape_game(total_grapes, grapes_eaten, poison_grapes=1, diminishing_returns=False):
    grapes = ['poison'] * poison_grapes + ['safe'] * (total_grapes - poison_grapes)
    random.shuffle(grapes)
    chosen_grapes = random.sample(grapes, grapes_eaten)
    if 'poison' in chosen_grapes:
        return False, 0
    else:
        if diminishing_returns:
            # Example: First grape = $100k, each additional grape = $10k less
            payout = 0
            for i in range(grapes_eaten):
                payout += max(0, 100_000 - i * 10_000)
            return True, payout
        else:
            return True, grapes_eaten * 100_000

st.title("Grape Gamble Simulator")
st.markdown("Simulate your odds in a deadly game of chance. One grape is poison. The others are worth $100,000 each—unless diminishing returns are enabled.")

st.subheader("Game Settings")

# Dual input: total grapes
col1, col2 = st.columns(2)
with col1:
    total_grapes_input = st.number_input("Total number of grapes (type)", min_value=2, max_value=1000, value=10, step=1)
with col2:
    total_grapes = st.slider("Total number of grapes (slider)", 2, 1000, value=total_grapes_input, step=1)

# Dual input: poison grapes
col3, col4 = st.columns(2)
with col3:
    poison_grapes_input = st.number_input("Poison grapes (type)", min_value=1, max_value=total_grapes - 1, value=1, step=1)
with col4:
    poison_grapes = st.slider("Poison grapes (slider)", 1, total_grapes - 1, value=poison_grapes_input, step=1)

# Dual input: grapes eaten
col5, col6 = st.columns(2)
with col5:
    grapes_eaten_input = st.number_input("Number of grapes to eat (type)", min_value=1, max_value=total_grapes, value=1, step=1)
with col6:
    grapes_eaten = st.slider("Number of grapes to eat (slider)", 1, total_grapes, value=grapes_eaten_input, step=1)

# Rounds & Options
st.subheader("Simulation Options")
rounds = st.number_input("Number of rounds to simulate", min_value=1, max_value=100, value=1, step=1)
diminishing = st.toggle("Enable diminishing returns", value=False)

# Single simulation over multiple rounds
if st.button("Play Rounds"):
    total_reward = 0
    for i in range(int(rounds)):
        survived, reward = simulate_grape_game(total_grapes, grapes_eaten, poison_grapes, diminishing)
        if not survived:
            st.error(f"💀 You died in round {i + 1}. Final reward: ${total_reward:,}")
            break
        total_reward += reward
    else:
        st.success(f"🏆 You survived all {int(rounds)} rounds! Total reward: ${total_reward:,}")

# Batch simulation for statistics
st.markdown("---")
st.subheader("Advanced Simulation and Risk Analysis")

if st.button("Run 1,000 Simulations"):
    outcomes = []
    survival_count = 0
    for _ in range(1000):
        total_reward = 0
        for i in range(int(rounds)):
            survived, reward = simulate_grape_game(total_grapes, grapes_eaten, poison_grapes, diminishing)
            if not survived:
                total_reward = 0
                break
            total_reward += reward
        if total_reward > 0:
            survival_count += 1
        outcomes.append(total_reward)

    survival_rate = survival_count / 1000
    expected_value = sum(outcomes) / 1000

    st.info(f"✅ Survival rate over {int(rounds)} rounds: **{survival_rate * 100:.1f}%**")
    st.info(f"💰 Expected value: **${expected_value:,.2f}**")

    st.subheader("Danger Level")
    if survival_rate > 0.9:
        st.success("🟢 Low Risk")
    elif survival_rate > 0.5:
        st.warning("🟡 Medium Risk")
    else:
        st.error("🔴 High Risk")

    st.subheader("Reward Distribution (Histogram)")
    fig, ax = plt.subplots()
    ax.hist(outcomes, bins=20, color='skyblue', edgecolor='black')
    ax.set_title("Distribution of Total Rewards Over 1,000 Trials")
    ax.set_xlabel("Total Reward ($)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
