import streamlit as st
import pandas as pd

# Title and description
st.title("Phoenix Suns Roster 2024")
st.write("View and manage the 2024 Phoenix Suns roster and statistics.")

# Predefined Phoenix Suns roster data
default_roster = [
    {"Name": "Kevin Durant", "Position": "Forward", "Height": "6'10", "Weight (lbs)": 240, 
     "Games Played": 50, "Points Per Game": 29.1, "Rebounds Per Game": 7.3, "Assists Per Game": 5.0},
    {"Name": "Devin Booker", "Position": "Guard", "Height": "6'5", "Weight (lbs)": 206, 
     "Games Played": 55, "Points Per Game": 27.0, "Rebounds Per Game": 4.5, "Assists Per Game": 6.8},
    {"Name": "Bradley Beal", "Position": "Guard", "Height": "6'4", "Weight (lbs)": 207, 
     "Games Played": 40, "Points Per Game": 23.2, "Rebounds Per Game": 3.9, "Assists Per Game": 5.4},
    {"Name": "Deandre Ayton", "Position": "Center", "Height": "6'11", "Weight (lbs)": 250, 
     "Games Played": 60, "Points Per Game": 18.5, "Rebounds Per Game": 10.2, "Assists Per Game": 1.8},
]

# Load roster into session state
if "roster" not in st.session_state:
    st.session_state["roster"] = default_roster

# Sidebar: Add or update a player
st.sidebar.header("Add/Update Player")
with st.sidebar.form("player_form"):
    name = st.text_input("Player Name")
    position = st.selectbox("Position", ["Guard", "Forward", "Center"])
    height = st.text_input("Height (e.g., 6'5)")
    weight = st.number_input("Weight (lbs)", min_value=100, max_value=350, step=1)
    games_played = st.number_input("Games Played", min_value=0, step=1)
    points_per_game = st.number_input("Points Per Game", min_value=0.0, step=0.1)
    rebounds_per_game = st.number_input("Rebounds Per Game", min_value=0.0, step=0.1)
    assists_per_game = st.number_input("Assists Per Game", min_value=0.0, step=0.1)

    # Submit button
    submitted = st.form_submit_button("Add/Update Player")
    if submitted:
        # Check if the player already exists
        existing_player = next((p for p in st.session_state["roster"] if p["Name"].lower() == name.lower()), None)
        player_data = {
            "Name": name,
            "Position": position,
            "Height": height,
            "Weight (lbs)": weight,
            "Games Played": games_played,
            "Points Per Game": points_per_game,
            "Rebounds Per Game": rebounds_per_game,
            "Assists Per Game": assists_per_game,
        }
        if existing_player:
            # Update player data
            st.session_state["roster"] = [
                player_data if p["Name"].lower() == name.lower() else p
                for p in st.session_state["roster"]
            ]
            st.success(f"Updated player: {name}")
        else:
            # Add new player
            st.session_state["roster"].append(player_data)
            st.success(f"Added new player: {name}")

# Main Section: Display Roster
st.header("Phoenix Suns Roster")
if st.session_state["roster"]:
    roster_df = pd.DataFrame(st.session_state["roster"])
    st.dataframe(roster_df)
else:
    st.write("No players in the roster yet.")

# Save roster as CSV
st.sidebar.markdown("---")
if st.session_state["roster"]:
    st.sidebar.download_button(
        label="Download Roster as CSV",
        data=pd.DataFrame(st.session_state["roster"]).to_csv(index=False),
        file_name="phoenix_suns_roster_2024.csv",
        mime="text/csv",
    )

