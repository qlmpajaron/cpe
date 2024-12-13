import streamlit as st
import pandas as pd

# Title and description
st.title("Phoenix Suns Roster 2024")
st.write("Welcome to the 2024 Phoenix Suns Roster App. Manage player stats, view details, and save changes!")

# CSV file to save/load data
csv_file = "phoenix_suns_roster_2024.csv"

# Load Roster from CSV
try:
    # Attempt to read the existing CSV
    roster_df = pd.read_csv(csv_file)
    st.session_state["roster"] = roster_df.to_dict("records")
except FileNotFoundError:
    # Handle if CSV doesn't exist
    st.session_state["roster"] = []

# Sidebar for adding/updating players
st.sidebar.header("Add/Update Player")
with st.sidebar.form("player_form"):
    name = st.text_input("Player Name")
    position = st.selectbox("Position", ["Guard", "Forward", "Center"])
    height = st.text_input("Height (e.g., 6'5\")")
    weight = st.number_input("Weight (lbs)", min_value=100, max_value=350, step=1)
    games_played = st.number_input("Games Played", min_value=0, step=1)
    points_per_game = st.number_input("Points Per Game", min_value=0.0, step=0.1)
    rebounds_per_game = st.number_input("Rebounds Per Game", min_value=0.0, step=0.1)
    assists_per_game = st.number_input("Assists Per Game", min_value=0.0, step=0.1)

    submitted = st.form_submit_button("Add/Update Player")
    if submitted:
        # Create player data dictionary
        player_data = {
            "Name": name,
            "Position": position,
            "Height": height,
            "Weight (lbs)": weight,
            "Games Played": games_played,
            "Points Per Game": points_per_game,
            "Rebounds Per Game": rebounds_per_game,
            "Assists Per Game": assists_per_game
        }

        # Check if player already exists in the list
        existing_player = next(
            (p for p in st.session_state["roster"] if p["Name"].lower() == name.lower()), None
        )
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

# Main Section: Display the full roster
st.header("Phoenix Suns Roster")
if st.session_state["roster"]:
    # Convert the session state to DataFrame for display
    roster_df = pd.DataFrame(st.session_state["roster"])
    st.dataframe(roster_df)
else:
    st.write("No players added yet. Use the sidebar to add players.")

# Save Roster Button
if st.session_state["roster"]:
    if st.sidebar.button("Save Roster to CSV"):
        # Save roster to CSV
        pd.DataFrame(st.session_state["roster"]).to_csv(csv_file, index=False)
        st.sidebar.success("Roster saved successfully!")

# Download Button for CSV
st.sidebar.download_button(
    label="Download Roster as CSV",
    data=pd.DataFrame(st.session_state["roster"]).to_csv(index=False),
    file_name="phoenix_suns_roster_2024.csv",
    mime="text/csv"
)
