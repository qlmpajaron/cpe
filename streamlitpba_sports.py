import streamlit as st
import pandas as pd

# Title and description
st.title("PBA Basketball Players 2023-2024")
st.write("A simple application to represent PBA basketball players and their statistics.")

# Initialize a placeholder for players' data
if "players_data" not in st.session_state:
    st.session_state["players_data"] = []

# Sidebar: Add a new player
st.sidebar.header("Add a New Player")
with st.sidebar.form("player_form"):
    name = st.text_input("Player Name")
    team = st.text_input("Team")
    position = st.selectbox("Position", ["Guard", "Forward", "Center"])
    height = st.text_input("Height (e.g., 6'3)")
    weight = st.number_input("Weight (lbs)", min_value=100, max_value=300, step=1)
    games_played = st.number_input("Games Played", min_value=0, step=1)
    points_per_game = st.number_input("Points Per Game", min_value=0.0, step=0.1)
    rebounds_per_game = st.number_input("Rebounds Per Game", min_value=0.0, step=0.1)
    assists_per_game = st.number_input("Assists Per Game", min_value=0.0, step=0.1)
    steals_per_game = st.number_input("Steals Per Game", min_value=0.0, step=0.1)
    blocks_per_game = st.number_input("Blocks Per Game", min_value=0.0, step=0.1)

    # Submit button
    submitted = st.form_submit_button("Add Player")
    if submitted:
        # Append the new player's data
        st.session_state["players_data"].append({
            "Name": name,
            "Team": team,
            "Position": position,
            "Height": height,
            "Weight (lbs)": weight,
            "Games Played": games_played,
            "Points Per Game": points_per_game,
            "Rebounds Per Game": rebounds_per_game,
            "Assists Per Game": assists_per_game,
            "Steals Per Game": steals_per_game,
            "Blocks Per Game": blocks_per_game,
        })
        st.success(f"Player {name} added!")

# Main Section: Display Players Data
st.header("PBA Players 2023-2024")
if st.session_state["players_data"]:
    # Convert the data to a DataFrame for display
    players_df = pd.DataFrame(st.session_state["players_data"])
    st.dataframe(players_df)
else:
    st.write("No players added yet. Use the sidebar to add players.")

# Optional: Download players' data as a CSV
st.sidebar.markdown("---")
if st.session_state["players_data"]:
    st.sidebar.download_button(
        label="Download Player Data as CSV",
        data=pd.DataFrame(st.session_state["players_data"]).to_csv(index=False),
        file_name="pba_players_2023_2024.csv",
        mime="text/csv",
    )
