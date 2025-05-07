
import streamlit as st
import random
import matplotlib.pyplot as plt

def simulate_grape_game(total_grapes, grapes_eaten, poison_grapes=1):
    grapes = ['poison'] * poison_grapes + ['safe'] * (total_grapes - poison_grapes)
    random.shuffle(grapes)
    chosen_grapes = random.sample(grapes, grapes_eaten)
    if 'poison' in chosen_grapes:
        return False, 0
    else:
        return True, grapes_eaten * 100_000

st.title("Grape Gamble Simulator")
st.markdown("Simulate your odds in a deadly game of chance. One grape is poison. The others are worth $100,000 each.")

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

# Run single simulation
if st.button("Eat the Grapes!"):
    survived, reward = simulate_grape_game(total_grapes, grapes_eaten, poison_grapes)
    if survived:
        st.success(f"You survived and earned ${reward:,}!")
    else:
        st.error("You ate the poison grape. You died!")

# Advanced simulation
st.markdown("---")
st.subheader("Advanced Simulation and Risk Analysis")

if st.button("Run 1,000 Simulations"):
    outcomes = []
    survival_count = 0
    for _ in range(1000):
        survived, reward = simulate_grape_game(total_grapes, grapes_eaten, poison_grapes)
        outcomes.append(reward)
        if survived:
            survival_count += 1

    survival_rate = survival_count / 1000
    expected_value = sum(outcomes) / 1000

    st.info(f"✅ Survival rate: **{survival_rate * 100:.1f}%**")
    st.info(f"💰 Expected value: **${expected_value:,.2f}**")

    # Risk meter
    st.subheader("Danger Level")
    if survival_rate > 0.9:
        st.success("🟢 Low Risk")
    elif survival_rate > 0.5:
        st.warning("🟡 Medium Risk")
    else:
        st.error("🔴 High Risk")

    # Histogram
    st.subheader("Survival Outcomes Histogram")
    fig, ax = plt.subplots()
    ax.hist(outcomes, bins=20, color='skyblue', edgecolor='black')
    ax.set_title("Distribution of Rewards Over 1,000 Trials")
    ax.set_xlabel("Reward ($)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
