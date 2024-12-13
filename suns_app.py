import streamlit as st
import pandas as pd

# Title and description
st.title("Phoenix Suns Roster 2024")
st.write("Manage the 2024 Phoenix Suns roster, add players, and export data to a CSV file.")

# Load roster from a CSV file
csv_file = "phoenix_suns_roster_2024.csv"
try:
    # Read the existing CSV file
    roster_df = pd.read_csv(csv_file)
    st.session_state["roster"] = roster_df.to_dict("records")
except FileNotFoundError:
    # If the file doesn't exist, start with an empty roster
    st.session_state["roster"] = []

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
        # Add or update the player in the roster
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
        # Check if the player already exists
        existing_player = next((p for p in st.session_state["roster"] if p["Name"].lower() == name.lower()), None)
        if existing_player:
            # Update the existing player
            st.session_state["roster"] = [
                player_data if p["Name"].lower() == name.lower() else p
                for p in st.session_state["roster"]
            ]
            st.success(f"Updated player: {name}")
        else:
            # Add new player
            st.session_state["roster"].append(player_data)
            st.success(f"Added new player: {name}")

# Main Section: Display the roster
st.header("Phoenix Suns Roster")
if st.session_state["roster"]:
    roster_df = pd.DataFrame(st.session_state["roster"])
    st.dataframe(roster_df)
else:
    st.write("No players in the roster yet. Use the sidebar to add players.")

# Sidebar: Save data back to CSV
if st.session_state["roster"]:
    if st.sidebar.button("Save Roster to CSV"):
        pd.DataFrame(st.session_state["roster"]).to_csv(csv_file, index=False)
        st.sidebar.success(f"Roster saved to {csv_file}")

# Sidebar: Download roster as CSV
st.sidebar.download_button(
    label="Download Roster as CSV",
    data=pd.DataFrame(st.session_state["roster"]).to_csv(index=False),
    file_name="phoenix_suns_roster_2024.csv",
    mime="text/csv",
)
