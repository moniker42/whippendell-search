import streamlit as st
import pandas as pd

# --- 1. SETTINGS & PASSWORD ---
PASSWORD = "poshcheddar"  # <--- Change this to your team's password

st.set_page_config(page_title="Whippendell Secret Finder", layout="wide")

# This function handles the "Login" state
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("🔒 Restricted Access")
        user_input = st.text_input("Enter Team Password:", type="password")
        if st.button("Unlock"):
            if user_input == PASSWORD:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Incorrect password.")
        return False
    return True

# --- 2. MAIN APP ---
if check_password():
    st.title("🌲 Whippendell Wood W3W Search")
    st.write("Welcome, Team! Search our private database of 240,400 squares.")

    @st.cache_data
    def load_data():
        # Using low_memory=False helps with larger CSV files
        return pd.read_csv("Whippendell_W3W_List.csv")

    df = load_data()

    # Search Interface
    query = st.text_input("Search for a word or coordinate fragment:", "")

    if query:
        # Search the 'Words' column (case-insensitive)
        results = df[df['Words'].str.contains(query.lower(), na=False)].copy()
        
        if not results.empty:
            # Create a Google Maps link for every result
            # Using the 'f' string to format the URL correctly
            results['Map Link'] = results.apply(
                lambda x: f"https://www.google.com/maps?q={x['Latitude']},{x['Longitude']}", 
                axis=1
            )
            
            st.success(f"Found {len(results)} matches!")
            
            # Display results in a clean table with clickable links
            st.dataframe(
                results,
                column_config={
                    "Latitude": st.column_config.NumberColumn(format="%.6f"),
                    "Longitude": st.column_config.NumberColumn(format="%.6f"),
                    "Map Link": st.column_config.LinkColumn("View on Google Maps")
                },
                hide_index=True,
                use_container_width=True
            )
        else:
            st.warning("No squares found containing that word.")
    
    # Sidebar Logout
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()