import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import date

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="World Cup 2026 Challenge", layout="wide")

# --- DATABASE CONNECTION ---
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- APP DATA & LOOKUPS ---
groups = {
    "A": ["🇲🇽 Mexico", "🇿🇦 South Africa", "🇰🇷 South Korea", "🇨🇿 Czechia"],
    "B": ["🇨🇦 Canada", "🇧🇦 Bosnia and Herzegovina", "🇶🇦 Qatar", "🇨🇭 Switzerland"],
    "C": ["🇧🇷 Brazil", "🇲🇦 Morocco", "🇭🇹 Haiti", "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland"],
    "D": ["🇺🇸 United States", "🇵🇾 Paraguay", "🇦🇺 Australia", "🇹🇷 Türkiye"],
    "E": ["🇩🇪 Germany", "🇨🇼 Curaçao", "🇨🇮 Ivory Coast", "🇪🇨 Ecuador"],
    "F": ["🇳🇱 Netherlands", "🇯🇵 Japan", "🇸🇪 Sweden", "🇹🇳 Tunisia"],
    "G": ["🇧🇪 Belgium", "🇪🇬 Egypt", "🇮🇷 Iran", "🇳🇿 New Zealand"],
    "H": ["🇪🇸 Spain", "🇨🇻 Cape Verde", "🇸🇦 Saudi Arabia", "🇺🇾 Uruguay"],
    "I": ["🇫🇷 France", "🇸🇳 Senegal", "🇮🇶 Iraq", "🇳🇴 Norway"],
    "J": ["🇦🇷 Argentina", "🇩🇿 Algeria", "🇦🇹 Austria", "🇯🇴 Jordan"],
    "K": ["🇵🇹 Portugal", "🇨🇩 DR Congo", "🇺🇿 Uzbekistan", "🇨🇴 Colombia"],
    "L": ["🏴󠁧󠁢󠁥󠁮󠁧󠁿 England", "🇭🇷 Croatia", "🇬🇭 Ghana", "🇵🇦 Panama"],
}

team_facts = {
    "🇲🇽 Mexico": {"rank": 15, "players": "Edson Álvarez, Santiago Giménez", "last_wc": "Group Stage"},
    "🇿🇦 South Africa": {"rank": 60, "players": "Percy Tau, Ronwen Williams", "last_wc": "Did Not Qualify"},
    "🇰🇷 South Korea": {"rank": 25, "players": "Son Heung-min, Kim Min-jae", "last_wc": "Round of 16"},
    "🇨🇿 Czechia": {"rank": 41, "players": "Tomáš Souček, Patrik Schick", "last_wc": "Did Not Qualify"},
    "🇨🇦 Canada": {"rank": 30, "players": "Alphonso Davies, Jonathan David", "last_wc": "Group Stage"},
    "🇧🇦 Bosnia and Herzegovina": {"rank": 65, "players": "Edin Džeko, Miralem Pjanić", "last_wc": "Did Not Qualify"},
    "🇶🇦 Qatar": {"rank": 55, "players": "Akram Afif, Almoez Ali", "last_wc": "Group Stage"},
    "🇨🇭 Switzerland": {"rank": 19, "players": "Granit Xhaka, Manuel Akanji", "last_wc": "Round of 16"},
    "🇧🇷 Brazil": {"rank": 6, "players": "Vinícius Júnior, Raphinha", "last_wc": "Quarterfinals"},
    "🇲🇦 Morocco": {"rank": 8, "players": "Achraf Hakimi, Yassine Bounou", "last_wc": "Fourth Place"},
    "🇭🇹 Haiti": {"rank": 83, "players": "Frantzdy Pierrot, Duckens Nazon", "last_wc": "Did Not Qualify"},
    "🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland": {"rank": 43, "players": "Andrew Robertson, Scott McTominay", "last_wc": "Did Not Qualify"},
    "🇺🇸 United States": {"rank": 16, "players": "Christian Pulisic, Weston McKennie", "last_wc": "Round of 16"},
    "🇵🇾 Paraguay": {"rank": 40, "players": "Miguel Almirón, Julio Enciso", "last_wc": "Did Not Qualify"},
    "🇦🇺 Australia": {"rank": 27, "players": "Mathew Ryan, Harry Souttar", "last_wc": "Round of 16"},
    "🇹🇷 Türkiye": {"rank": 22, "players": "Hakan Çalhanoğlu, Arda Güler", "last_wc": "Did Not Qualify"},
    "🇩🇪 Germany": {"rank": 10, "players": "Jamal Musiala, Florian Wirtz", "last_wc": "Group Stage"},
    "🇨🇼 Curaçao": {"rank": 82, "players": "Leandro Bacuna, Vurnon Anita", "last_wc": "Did Not Qualify"},
    "🇨🇮 Ivory Coast": {"rank": 34, "players": "Franck Kessié, Sébastien Haller", "last_wc": "Did Not Qualify"},
    "🇪🇨 Ecuador": {"rank": 23, "players": "Moisés Caicedo, Pervis Estupiñán", "last_wc": "Group Stage"},
    "🇳🇱 Netherlands": {"rank": 7, "players": "Virgil van Dijk, Xavi Simons", "last_wc": "Quarterfinals"},
    "🇯🇵 Japan": {"rank": 18, "players": "Kaoru Mitoma, Wataru Endo", "last_wc": "Round of 16"},
    "🇸🇪 Sweden": {"rank": 38, "players": "Alexander Isak, Dejan Kulusevski", "last_wc": "Did Not Qualify"},
    "🇹🇳 Tunisia": {"rank": 44, "players": "Ellyes Skhiri, Aïssa Laïdouni", "last_wc": "Group Stage"},
    "🇧🇪 Belgium": {"rank": 9, "players": "Kevin De Bruyne, Jérémy Doku", "last_wc": "Group Stage"},
    "🇪🇬 Egypt": {"rank": 29, "players": "Mohamed Salah, Omar Marmoush", "last_wc": "Did Not Qualify"},
    "🇮🇷 Iran": {"rank": 21, "players": "Mehdi Taremi, Sardar Azmoun", "last_wc": "Group Stage"},
    "🇳🇿 New Zealand": {"rank": 85, "players": "Chris Wood, Liberato Cacace", "last_wc": "Did Not Qualify"},
    "🇪🇸 Spain": {"rank": 2, "players": "Rodri, Lamine Yamal", "last_wc": "Round of 16"},
    "🇨🇻 Cape Verde": {"rank": 69, "players": "Ryan Mendes, Bebé", "last_wc": "Did Not Qualify"},
    "🇸🇦 Saudi Arabia": {"rank": 61, "players": "Salem Al-Dawsari, Firas Al-Buraikan", "last_wc": "Group Stage"},
    "🇺🇾 Uruguay": {"rank": 17, "players": "Federico Valverde, Darwin Núñez", "last_wc": "Group Stage"},
    "🇫🇷 France": {"rank": 1, "players": "Kylian Mbappé, Ousmane Dembélé", "last_wc": "Runner-Up"},
    "🇸🇳 Senegal": {"rank": 14, "players": "Sadio Mané, Kalidou Koulibaly", "last_wc": "Round of 16"},
    "🇮🇶 Iraq": {"rank": 57, "players": "Aymen Hussein, Ali Jasim", "last_wc": "Did Not Qualify"},
    "🇳🇴 Norway": {"rank": 31, "players": "Erling Haaland, Martin Ødegaard", "last_wc": "Did Not Qualify"},
    "🇦🇷 Argentina": {"rank": 3, "players": "Lionel Messi, Julian Alvarez", "last_wc": "Champions"},
    "🇩🇿 Algeria": {"rank": 28, "players": "Riyad Mahrez, Ismaël Bennacer", "last_wc": "Did Not Qualify"},
    "🇦🇹 Austria": {"rank": 24, "players": "David Alaba, Marcel Sabitzer", "last_wc": "Did Not Qualify"},
    "🇯🇴 Jordan": {"rank": 63, "players": "Musa Al-Taamari, Yazan Al-Naimat", "last_wc": "Did Not Qualify"},
    "🇵🇹 Portugal": {"rank": 5, "players": "Bruno Fernandes, Bernardo Silva", "last_wc": "Quarterfinals"},
    "🇨🇩 DR Congo": {"rank": 46, "players": "Chancel Mbemba, Yoane Wissa", "last_wc": "Did Not Qualify"},
    "🇺🇿 Uzbekistan": {"rank": 50, "players": "Eldor Shomurodov, Abbosbek Fayzullaev", "last_wc": "Did Not Qualify"},
    "🇨🇴 Colombia": {"rank": 13, "players": "Luis Díaz, James Rodríguez", "last_wc": "Did Not Qualify"},
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 England": {"rank": 4, "players": "Harry Kane, Jude Bellingham", "last_wc": "Quarterfinals"},
    "🇭🇷 Croatia": {"rank": 11, "players": "Luka Modrić, Joško Gvardiol", "last_wc": "Third Place"},
    "🇬🇭 Ghana": {"rank": 67, "players": "Mohammed Kudus, Thomas Partey", "last_wc": "Group Stage"},
    "🇵🇦 Panama": {"rank": 33, "players": "Adalberto Carrasquilla, José Fajardo", "last_wc": "Did Not Qualify"},
}

# --- AUTHENTICATION STATE ---
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
    st.session_state["username"] = None
    st.session_state["is_admin"] = False

# --- LOGIN / SIGNUP LOGIC ---
if not st.session_state["user_id"]:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # PAGE-SPECIFIC IMAGE: LOGIN
        st.image("login.jpg", width="stretch")
        st.title("World Cup 2026 Bracket Challenge")
        
        st.write("Enter your username to log in or create a new profile.")

        # Wrapping the inputs in a form automatically enables the "Enter" key
        with st.form("login_form"):
            username = st.text_input("Username").strip()

            # Side-by-side buttons
            c1, c2 = st.columns(2)
            with c1:
                # The first submit button in a form is the default for the Enter key
                login_btn = st.form_submit_button("Log In", type="primary", width="stretch")
            with c2:
                signup_btn = st.form_submit_button("Create Account", width="stretch")

            # Logic executed if "Log In" is clicked OR "Enter" is pressed
            if login_btn:
                if username:
                    res = supabase.table("profiles").select("*").eq("username", username).execute()
                    if res.data:
                        st.session_state["user_id"] = res.data[0]["user_id"]
                        st.session_state["username"] = res.data[0]["username"]
                        st.session_state["is_admin"] = res.data[0]["is_admin"]
                        st.rerun()
                    else:
                        st.error("User not found. Check your spelling or create an account.")
                else:
                    st.warning("Please enter a username.")
                    
            # Logic executed only if "Create Account" is explicitly clicked
            if signup_btn:
                if username:
                    try:
                        # ⬇️ FIX: Removed the "password" field entirely!
                        res = supabase.table("profiles").insert({"username": username}).execute()
                        st.success("Account created! Click 'Log In' to enter.")
                    except Exception as e:
                        st.error(f"Database Error: {e}") 
                else:
                    st.warning("Please enter a username.")
    st.stop()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    # Small generic logo for the sidebar
    st.image("logo.jpg", width=100)
    st.write(f"Logged in as: **{st.session_state['username']}**")
    
    pages = ["📊 Leaderboard", "📝 Group Picks", "🏆 Knockout Bracket"]
    if st.session_state["is_admin"]:
        pages.append("⚙️ Admin Panel")
    
    current_page = st.sidebar.radio("Navigation", pages)
    
    if st.button("Log Out"):
        st.session_state["user_id"] = None
        st.rerun()

    st.sidebar.divider()

    # --- SCOUTING REPORT ---
    if current_page in ["📝 Group Picks", "🏆 Knockout Bracket"]:
        st.sidebar.header("📋 Team Scouting Report")
        all_teams = sorted([team for sublist in groups.values() for team in sublist])
        scout_selection = st.sidebar.selectbox("Lookup a team:", all_teams)
        
        if scout_selection in team_facts:
            f = team_facts[scout_selection]
            st.sidebar.markdown(f"### {scout_selection}")
            st.sidebar.markdown(f"**🌍 World Rank:** {f['rank']}")
            st.sidebar.markdown(f"**⭐ Notable Players:** {f['players']}")
            st.sidebar.markdown(f"**🔙 2022 Finish:** {f['last_wc']}")

# --- MAIN APP ROUTING ---

# 1. LEADERBOARD
if current_page == "📊 Leaderboard":
    st.image("leaderboard.jpg", width="stretch")
    st.title("Tournament Leaderboard")
    
    res = supabase.table("leaderboard").select("*").execute()
    
    if res.data:
        df = pd.DataFrame(res.data)
        
        # 1. Sort the dataframe so 1st place is at the top
        df = df.sort_values(by="total_score", ascending=False).reset_index(drop=True)
        
        # 2. Insert a clean 1, 2, 3 Rank column
        df.insert(0, "Rank", range(1, len(df) + 1))
        
        # 3. Add a visual indicator for the logged-in user
        current_user = st.session_state["username"]
        df["username"] = df["username"].apply(
            lambda x: f"👤 {x} (You)" if x == current_user else x
        )
        
        # 4. Render the beautified dataframe
        st.dataframe(
            df,
            column_config={
                "Rank": st.column_config.NumberColumn(
                    "Rank",
                    help="Current standing"
                ),
                "username": st.column_config.TextColumn(
                    "Manager"
                ),
                "rank_points": st.column_config.NumberColumn(
                    "Group Stage - Order", 
                    help="Points earned for predicting the exact 1st-4th finish in a group",
                    format="%d pts"
                ),
                "advancement_points": st.column_config.NumberColumn(
                    "Group Stage - Advancing", 
                    help="Points earned for correctly picking 3rd place teams that advance",
                    format="%d pts"
                ),
                "knockout_points": st.column_config.NumberColumn(
                    "Knockout Round Points", 
                    format="%d pts"
                ),
                "total_score": st.column_config.NumberColumn(
                    "Total Score 🏆", 
                    help="Combined score from all rounds",
                    format="%d pts"
                ),
            },
            hide_index=True, 
            width="stretch"
        )
    else:
        st.info("No scores calculated yet. Check back once matches start!")

# 2. GROUP PICKS
elif current_page == "📝 Group Picks":
    st.image("groups.jpg", width="stretch")
    st.title("Group Stage Predictions")
    
    # Define the lock date (Locks at midnight as June 11th turns into June 12th)
    group_lock_date = date(2026, 6, 12) 
    # Use st.session_state["is_admin"] so you (the commissioner) can always bypass the lock if needed
    is_group_locked = date.today() >= group_lock_date and not st.session_state.get("is_admin", False)
    
    # Fetch existing user picks
    existing_gp = supabase.table("group_predictions").select("*").eq("user_id", st.session_state["user_id"]).execute()
    saved_group_picks = {(r["group_name"], r["predicted_rank"]): r["team_name"] for r in existing_gp.data}
    saved_wildcards = [r["team_name"] for r in existing_gp.data if r.get("is_advancing_bonus")]

    def get_saved_index(group, rank, team_list):
        saved = saved_group_picks.get((group, rank))
        return team_list.index(saved) if saved in team_list else rank - 1

    # --- MODE 1: EDITING (Before Deadline) ---
    # --- MODE 1: EDITING (Before Deadline) ---
    if not is_group_locked:
        st.info("🕒 Picks lock at the end of the day on **June 11th**.")
        
        # ⬇️ FIX: Removed the st.form wrapper so the page updates instantly!
        user_picks = {}
        third_place_teams = []
        cols = st.columns(3)
        for i, (g_name, teams) in enumerate(groups.items()):
            col = cols[i % 3]
            with col:
                st.markdown(f"#### Group {g_name}")
                # Because we use 'key', Streamlit remembers the user's choice even when the page reloads
                p1 = st.selectbox("1st", teams, index=get_saved_index(g_name, 1, teams), key=f"g{g_name}_1")
                p2 = st.selectbox("2nd", teams, index=get_saved_index(g_name, 2, teams), key=f"g{g_name}_2")
                p3 = st.selectbox("3rd", teams, index=get_saved_index(g_name, 3, teams), key=f"g{g_name}_3")
                p4 = st.selectbox("4th", teams, index=get_saved_index(g_name, 4, teams), key=f"g{g_name}_4")
                user_picks[g_name] = [p1, p2, p3, p4]
                third_place_teams.append(p3)

        st.divider()
        st.subheader("🔥 Wildcard Bonus")
        st.write("Select the 8 third-place teams you believe will advance to the knockout stage.")
        
        # This will now update instantly whenever a 3rd place pick changes above!
        valid_wildcards = [t for t in saved_wildcards if t in third_place_teams]
        bonus_advancers = st.multiselect("Select 8 to advance:", options=third_place_teams, default=valid_wildcards)

        # ⬇️ FIX: Swapped st.form_submit_button for a standard st.button
        if st.button("Lock In All Group Picks", type="primary", use_container_width=True):
            errors = []
            if len(bonus_advancers) != 8:
                errors.append(f"Wildcards: Selected {len(bonus_advancers)}/8 required.")
            for g, picks in user_picks.items():
                if len(set(picks)) != 4:
                    dupes = ", ".join(set([t for t in picks if picks.count(t) > 1]))
                    errors.append(f"Group {g}: '{dupes}' selected multiple times.")
            
            if errors:
                st.error("Please fix issues before saving:")
                for e in errors: st.warning(e)
            else:
                with st.spinner("Saving..."):
                    supabase.table("group_predictions").delete().eq("user_id", st.session_state["user_id"]).execute()
                    payload = []
                    for g, picks in user_picks.items():
                        for idx, team in enumerate(picks):
                            payload.append({
                                "user_id": st.session_state["user_id"], "group_name": g, 
                                "team_name": team, "predicted_rank": idx+1,
                                "is_advancing_bonus": (idx+1 == 3 and team in bonus_advancers)
                            })
                    supabase.table("group_predictions").insert(payload).execute()
                    st.toast("Group stage picks successfully locked in! 🏆", icon="✅")

    # --- MODE 2: GRADING SCORECARD (After Deadline) ---
    else:
        st.warning("🔒 Group Stage picks are locked! Here is how your predictions are holding up.")
        
        # 1. Fetch the actual results from the database to grade the user
        actual_res = supabase.table("actual_results").select("*").execute()
        actual_ranks = {(r["group_name"], r["actual_rank"]): r["team_name"] for r in actual_res.data}

        cols = st.columns(3)
        for i, (g_name, teams) in enumerate(groups.items()):
            col = cols[i % 3]
            with col:
                st.markdown(f"#### Group {g_name}")
                with st.container(border=True): # Wraps each group in a neat card
                    for rank in range(1, 5):
                        # What did the user guess?
                        user_pick = saved_group_picks.get((g_name, rank), "No pick saved")
                        
                        # What was the real result?
                        real_team = actual_ranks.get((g_name, rank))
                        
                        # Grading Logic
                        if real_team is None:
                            # The group hasn't finished playing yet, show a neutral gray/blue box
                            st.info(f"**{rank}.** {user_pick}")
                        elif user_pick == real_team:
                            # Exact match! Show a green box
                            st.success(f"**{rank}.** {user_pick} ✅")
                        else:
                            # Wrong pick! Show a red box and tell them who actually took that spot
                            st.error(f"**{rank}.** ~~{user_pick}~~ *(Real: {real_team})* ❌")

# 3. KNOCKOUT BRACKET
elif current_page == "🏆 Knockout Bracket":
    st.image("knockout.jpg", width="stretch")
    
    # Define the lock date (Locks at midnight as June 28th turns into June 29th)
    knockout_lock_date = date(2026, 6, 29)
    is_knockout_locked = date.today() >= knockout_lock_date and not st.session_state.get("is_admin", False)
    
    # Fetch existing knockout picks
    existing_ko = supabase.table("knockout_predictions").select("*").eq("user_id", st.session_state["user_id"]).execute()
    saved_ko_picks = {r["match_id"]: r["predicted_winner"] for r in existing_ko.data}

    # 🚀 NEW: Fetch live matchups dynamically from your new table
    matchups_res = supabase.table("official_matchups").select("*").execute()
    matchups = {m["match_id"]: [m["team_1"], m["team_2"]] for m in matchups_res.data}

    def get_ko_index(match_id, options_list):
        saved = saved_ko_picks.get(match_id)
        return options_list.index(saved) if saved in options_list else 0

    # --- MODE 1: EDITING (Before Deadline) ---
    if not is_knockout_locked:
        st.title("Knockout Stage Predictions")
        st.info("🕒 Bracket locks at the end of the day on **June 28th**.")
        st.write("Select the winner of each matchup to build your path to the final.")
        
        with st.form("knockout_form", border=False): 
            
            st.markdown("### Round of 32")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                with st.container(border=True): m1 = st.selectbox("⚽ Match 1", matchups[1], index=get_ko_index(1, matchups[1]), key="km1")
                with st.container(border=True): m2 = st.selectbox("⚽ Match 2", matchups[2], index=get_ko_index(2, matchups[2]), key="km2")
                with st.container(border=True): m3 = st.selectbox("⚽ Match 3", matchups[3], index=get_ko_index(3, matchups[3]), key="km3")
                with st.container(border=True): m4 = st.selectbox("⚽ Match 4", matchups[4], index=get_ko_index(4, matchups[4]), key="km4")
            with c2:
                with st.container(border=True): m5 = st.selectbox("⚽ Match 5", matchups[5], index=get_ko_index(5, matchups[5]), key="km5")
                with st.container(border=True): m6 = st.selectbox("⚽ Match 6", matchups[6], index=get_ko_index(6, matchups[6]), key="km6")
                with st.container(border=True): m7 = st.selectbox("⚽ Match 7", matchups[7], index=get_ko_index(7, matchups[7]), key="km7")
                with st.container(border=True): m8 = st.selectbox("⚽ Match 8", matchups[8], index=get_ko_index(8, matchups[8]), key="km8")
            with c3:
                with st.container(border=True): m9 = st.selectbox("⚽ Match 9", matchups[9], index=get_ko_index(9, matchups[9]), key="km9")
                with st.container(border=True): m10 = st.selectbox("⚽ Match 10", matchups[10], index=get_ko_index(10, matchups[10]), key="km10")
                with st.container(border=True): m11 = st.selectbox("⚽ Match 11", matchups[11], index=get_ko_index(11, matchups[11]), key="km11")
                with st.container(border=True): m12 = st.selectbox("⚽ Match 12", matchups[12], index=get_ko_index(12, matchups[12]), key="km12")
            with c4:
                with st.container(border=True): m13 = st.selectbox("⚽ Match 13", matchups[13], index=get_ko_index(13, matchups[13]), key="km13")
                with st.container(border=True): m14 = st.selectbox("⚽ Match 14", matchups[14], index=get_ko_index(14, matchups[14]), key="km14")
                with st.container(border=True): m15 = st.selectbox("⚽ Match 15", matchups[15], index=get_ko_index(15, matchups[15]), key="km15")
                with st.container(border=True): m16 = st.selectbox("⚽ Match 16", matchups[16], index=get_ko_index(16, matchups[16]), key="km16")

            st.divider()
            
            st.markdown("### Round of 16")
            r16c1, r16c2, r16c3, r16c4 = st.columns(4)
            with r16c1:
                with st.container(border=True): m17 = st.selectbox("🔥 Match 17", [m1, m2], index=get_ko_index(17, [m1, m2]), key="km17")
                with st.container(border=True): m18 = st.selectbox("🔥 Match 18", [m3, m4], index=get_ko_index(18, [m3, m4]), key="km18")
            with r16c2:
                with st.container(border=True): m19 = st.selectbox("🔥 Match 19", [m5, m6], index=get_ko_index(19, [m5, m6]), key="km19")
                with st.container(border=True): m20 = st.selectbox("🔥 Match 20", [m7, m8], index=get_ko_index(20, [m7, m8]), key="km20")
            with r16c3:
                with st.container(border=True): m21 = st.selectbox("🔥 Match 21", [m9, m10], index=get_ko_index(21, [m9, m10]), key="km21")
                with st.container(border=True): m22 = st.selectbox("🔥 Match 22", [m11, m12], index=get_ko_index(22, [m11, m12]), key="km22")
            with r16c4:
                with st.container(border=True): m23 = st.selectbox("🔥 Match 23", [m13, m14], index=get_ko_index(23, [m13, m14]), key="km23")
                with st.container(border=True): m24 = st.selectbox("🔥 Match 24", [m15, m16], index=get_ko_index(24, [m15, m16]), key="km24")

            st.divider()
            
            st.markdown("### Quarterfinals")
            qfc1, qfc2 = st.columns(2)
            with qfc1:
                with st.container(border=True): m25 = st.selectbox("⚡ Match 25", [m17, m18], index=get_ko_index(25, [m17, m18]), key="km25")
                with st.container(border=True): m26 = st.selectbox("⚡ Match 26", [m19, m20], index=get_ko_index(26, [m19, m20]), key="km26")
            with qfc2:
                with st.container(border=True): m27 = st.selectbox("⚡ Match 27", [m21, m22], index=get_ko_index(27, [m21, m22]), key="km27")
                with st.container(border=True): m28 = st.selectbox("⚡ Match 28", [m23, m24], index=get_ko_index(28, [m23, m24]), key="km28")

            st.divider()
            
            sf1, sf2 = st.columns(2)
            with sf1:
                st.markdown("### Semifinals")
                with st.container(border=True): m29 = st.selectbox("🌟 Match 29", [m25, m26], index=get_ko_index(29, [m25, m26]), key="km29")
                with st.container(border=True): m30 = st.selectbox("🌟 Match 30", [m27, m28], index=get_ko_index(30, [m27, m28]), key="km30")
            
            with sf2:
                st.markdown("### 🏆 World Cup Final")
                st.write("Pick your ultimate champion:")
                with st.container(border=True): 
                    m31 = st.selectbox("🥇 Champion", [m29, m30], index=get_ko_index(31, [m29, m30]), key="km31", label_visibility="collapsed")
                
                st.markdown("<br>", unsafe_allow_html=True)
                submit_bracket = st.form_submit_button("Lock In Full Bracket", type="primary", use_container_width=True)

            if submit_bracket:
                winners = [m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,m22,m23,m24,m25,m26,m27,m28,m29,m30,m31]
                
                with st.spinner("Securing your bracket..."):
                    supabase.table("knockout_predictions").delete().eq("user_id", st.session_state["user_id"]).execute()
                    payload = [{"user_id": st.session_state["user_id"], "match_id": i+1, "predicted_winner": w} for i, w in enumerate(winners)]
                    supabase.table("knockout_predictions").insert(payload).execute()
                
                st.toast(f"Knockout bracket locked! {m31} to win it all! 🚀", icon="✅")
                st.balloons()

    # --- MODE 2: GRADING SCORECARD (After Deadline) ---
    else:
        st.title("Knockout Stage Scorecard")
        st.warning("🔒 The bracket is locked! Watch how your picks unfold below.")
        
        # 1. Fetch the actual results from the database
        actual_ko_res = supabase.table("actual_knockout_results").select("*").execute()
        actual_ko = {r["match_id"]: r["actual_winner"] for r in actual_ko_res.data}
        
        # 2. Helper function to render a color-coded match card
        def render_grading_card(match_id, emoji="⚽"):
            user_pick = saved_ko_picks.get(match_id, "No pick saved")
            real_winner = actual_ko.get(match_id)
            
            with st.container(border=True):
                if real_winner is None:
                    # Match hasn't been played yet
                    st.info(f"{emoji} **M{match_id}:** {user_pick}")
                elif user_pick == real_winner:
                    # Correct pick!
                    st.success(f"{emoji} **M{match_id}:** {user_pick} ✅")
                else:
                    # Incorrect pick!
                    st.error(f"{emoji} **M{match_id}:** ~~{user_pick}~~ *(Real: {real_winner})* ❌")

        # 3. Layout the Scorecard Grid
        st.markdown("### Round of 32")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            for i in range(1, 5): render_grading_card(i)
        with c2:
            for i in range(5, 9): render_grading_card(i)
        with c3:
            for i in range(9, 13): render_grading_card(i)
        with c4:
            for i in range(13, 17): render_grading_card(i)
            
        st.divider()
        st.markdown("### Round of 16")
        r16c1, r16c2, r16c3, r16c4 = st.columns(4)
        with r16c1:
            for i in range(17, 19): render_grading_card(i, "🔥")
        with r16c2:
            for i in range(19, 21): render_grading_card(i, "🔥")
        with r16c3:
            for i in range(21, 23): render_grading_card(i, "🔥")
        with r16c4:
            for i in range(23, 25): render_grading_card(i, "🔥")

        st.divider()
        st.markdown("### Quarterfinals")
        qfc1, qfc2 = st.columns(2)
        with qfc1:
            for i in range(25, 27): render_grading_card(i, "⚡")
        with qfc2:
            for i in range(27, 29): render_grading_card(i, "⚡")

        st.divider()
        sf1, sf2 = st.columns(2)
        with sf1:
            st.markdown("### Semifinals")
            for i in range(29, 31): render_grading_card(i, "🌟")
        with sf2:
            st.markdown("### 🏆 World Cup Final")
            render_grading_card(31, "🥇")

# 4. ADMIN PANEL
elif current_page == "⚙️ Admin Panel":
    st.title("Admin Control Panel")
    st.info("Logged in with Admin Privileges.")
    
    users_res = supabase.table("profiles").select("*").execute()
    
    if users_res.data:
        user_list = {u["username"]: u["user_id"] for u in users_res.data}
        
        target_user = st.selectbox(
            "Which user do you want to manage?", 
            list(user_list.keys()), 
            key="admin_user_select"
        )
        target_id = user_list[target_user]

        # --- SECTION 1: EDIT SPECIFIC PICKS ---
        st.markdown("### 🛠️ Edit User Picks")
        st.write(f"Modify specific rankings or bracket winners for **{target_user}**.")
        
        edit_type = st.radio("What are we fixing?", ["Group Stage", "Knockout Bracket"], horizontal=True)

        if edit_type == "Group Stage":
            current_gp = supabase.table("group_predictions").select("*").eq("user_id", target_id).execute()
            lookup = {(r['group_name'], r['predicted_rank']): r['team_name'] for r in current_gp.data}
            saved_wildcards = [r["team_name"] for r in current_gp.data if r.get("is_advancing_bonus")]

            def get_admin_index(g_name, rank, team_list):
                current_team = lookup.get((g_name, rank))
                return team_list.index(current_team) if current_team in team_list else rank-1

            edited_user_picks = {}
            third_place_teams = []
            cols = st.columns(3)
            
            for index, (group_name, teams) in enumerate(groups.items()):
                col = cols[index % 3]
                with col:
                    st.markdown(f"**Group {group_name}**")
                    # ⬇️ FIX: Added target_user to the keys to force Streamlit to refresh the dropdowns
                    p1 = st.selectbox("1st", teams, index=get_admin_index(group_name, 1, teams), key=f"adm_{target_user}_{group_name}_1")
                    p2 = st.selectbox("2nd", teams, index=get_admin_index(group_name, 2, teams), key=f"adm_{target_user}_{group_name}_2")
                    p3 = st.selectbox("3rd", teams, index=get_admin_index(group_name, 3, teams), key=f"adm_{target_user}_{group_name}_3")
                    p4 = st.selectbox("4th", teams, index=get_admin_index(group_name, 4, teams), key=f"adm_{target_user}_{group_name}_4")
                    edited_user_picks[group_name] = [p1, p2, p3, p4]
                    third_place_teams.append(p3)

            st.divider()
            
            st.subheader("🔥 Edit Wildcards")
            valid_wildcards = [t for t in saved_wildcards if t in third_place_teams]
            bonus_advancers = st.multiselect(
                f"Select {target_user}'s 8 advancing 3rd place teams:", 
                options=third_place_teams, 
                default=valid_wildcards,
                key=f"admin_{target_user}_wildcard_select" # Dynamic key here too
            )

            if st.button(f"Save Group Edits for {target_user}", type="primary", use_container_width=True):
                errors = []
                if len(bonus_advancers) != 8:
                    errors.append(f"Wildcards: Selected {len(bonus_advancers)}/8 required.")
                for g, p in edited_user_picks.items():
                    if len(set(p)) != 4:
                        errors.append(f"Duplicate teams in Group {g}!")
                        
                if errors:
                    for e in errors: st.error(e)
                else:
                    supabase.table("group_predictions").delete().eq("user_id", target_id).execute()
                    new_payload = []
                    for g, p in edited_user_picks.items():
                        for i, team in enumerate(p):
                            new_payload.append({
                                "user_id": target_id, 
                                "group_name": g, 
                                "team_name": team, 
                                "predicted_rank": i+1, 
                                "is_advancing_bonus": (i+1 == 3 and team in bonus_advancers)
                            })
                    supabase.table("group_predictions").insert(new_payload).execute()
                    st.toast(f"Successfully updated Group Stage for {target_user}!", icon="✅")

        else:
            current_kp = supabase.table("knockout_predictions").select("*").eq("user_id", target_id).execute()
            kp_lookup = {r['match_id']: r['predicted_winner'] for r in current_kp.data}

            with st.form("admin_edit_knockout_form"):
                st.write("Edit individual match winners (Match 1-31)")
                new_kp_winners = {}
                
                c1, c2, c3, c4 = st.columns(4)
                for m_id in range(1, 32):
                    current_winner = kp_lookup.get(m_id, "")
                    
                    if m_id <= 8: col = c1
                    elif m_id <= 16: col = c2
                    elif m_id <= 24: col = c3
                    else: col = c4
                    
                    with col:
                        # ⬇️ FIX: Added target_user to the knockout keys as well
                        new_kp_winners[m_id] = st.text_input(f"Match {m_id}", value=current_winner, key=f"adm_{target_user}_m_{m_id}")
                
                if st.form_submit_button(f"Save Knockout Edits for {target_user}", type="primary"):
                    supabase.table("knockout_predictions").delete().eq("user_id", target_id).execute()
                    kp_payload = [{"user_id": target_id, "match_id": m, "predicted_winner": w} for m, w in new_kp_winners.items()]
                    supabase.table("knockout_predictions").insert(kp_payload).execute()
                    st.toast(f"Knockout winners updated for {target_user}!", icon="✅")

        st.divider()

        # --- SECTION 2: CLEAR/RESET PICKS ---
        st.markdown("### 📝 Clear/Reset Picks")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Wipe ALL Group Picks for {target_user}"):
                supabase.table("group_predictions").delete().eq("user_id", target_id).execute()
                st.success(f"Wiped group picks for {target_user}.")
        with col2:
            if st.button(f"Wipe ALL Knockout Picks for {target_user}"):
                supabase.table("knockout_predictions").delete().eq("user_id", target_id).execute()
                st.success(f"Wiped knockout bracket for {target_user}.")

        st.divider()

        # --- SECTION 3: DANGER ZONE ---
        st.markdown("### 🚨 Danger Zone")
        st.warning("This action is irreversible. It will delete the user profile and all associated data.")
        if st.button(f"DELETE ENTIRE ACCOUNT: {target_user}", type="primary"):
            supabase.table("knockout_predictions").delete().eq("user_id", target_id).execute()
            supabase.table("group_predictions").delete().eq("user_id", target_id).execute()
            supabase.table("leaderboard").delete().eq("user_id", target_id).execute()
            supabase.table("profiles").delete().eq("user_id", target_id).execute()
            st.success(f"Deleted {target_user}.")
            st.rerun()
            
    else:
        st.write("No users found in the database.")