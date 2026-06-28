import os
import requests
from supabase import create_client, Client

# --- 1. INITIALIZE SUPABASE ---
# In GitHub Actions, we use os.environ to pull the secrets securely
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: Supabase credentials not found in environment variables.")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. FETCH MATCH DATA ---
def fetch_real_world_results():
    print("Fetching real-world match data from Supabase...")
    
    # ⬇️ FIX: Pointing to your existing table!
    group_res = supabase.table("actual_results").select("*").execute()
    real_group_data = group_res.data
    
    ko_res = supabase.table("actual_knockout_results").select("*").execute()
    real_knockout_data = ko_res.data
    
    return real_group_data, real_knockout_data


# --- 3. SCORING ENGINE ---
def calculate_and_update_leaderboard(group_results, knockout_results):
    """
    Pulls user predictions, compares them against real results, calculates scores,
    and updates the leaderboard table in Supabase.
    """
    print("Calculating leaderboard scores...")

    # 1. Create easy lookup dictionaries from the real-world results
    actual_advancing_teams = [row["team_name"] for row in group_results if row["actually_advanced"]]
    actual_team_ranks = {row["team_name"]: row["actual_rank"] for row in group_results}
    actual_knockout_winners = {row["match_id"]: row["actual_winner"] for row in knockout_results}

    # 2. Fetch all users and their predictions from Supabase
    users_res = supabase.table("profiles").select("user_id, username").execute()
    group_preds_res = supabase.table("group_predictions").select("*").execute()
    knockout_preds_res = supabase.table("knockout_predictions").select("*").execute()
    
    users = users_res.data
    group_preds = group_preds_res.data
    knockout_preds = knockout_preds_res.data

    leaderboard_payload = []

    # 3. Calculate scores for each user
    for user in users:
        user_id = user["user_id"]
        username = user["username"]
        
        advancement_points = 0
        rank_points = 0
        knockout_points = 0
        
        # Filter predictions for this specific user
        user_group_preds = [p for p in group_preds if p["user_id"] == user_id]
        user_ko_preds = [p for p in knockout_preds if p["user_id"] == user_id]
        
        # --- GROUP STAGE SCORING ---
        for pred in user_group_preds:
            team = pred["team_name"]
            pred_rank = pred["predicted_rank"]
            is_wildcard = pred.get("is_advancing_bonus", False)
            
            # Did the user predict them to move on?
            predicted_to_advance = (pred_rank in [1, 2]) or is_wildcard
            # Did they actually move on?
            actually_advanced = team in actual_advancing_teams
            
            if team in actual_team_ranks:
                real_rank = actual_team_ranks[team]
                
                # Condition A: Perfect Rank Match (2 Points)
                if pred_rank == real_rank:
                    rank_points += 2
                    
                # Condition B: Safety Net Match (1 Point)
                elif predicted_to_advance and actually_advanced:
                    advancement_points += 1
                    
        # --- KNOCKOUT STAGE SCORING ---
        for pred in user_ko_preds:
            match_id = pred["match_id"]
            pred_winner = pred["predicted_winner"]
            
            if match_id in actual_knockout_winners:
                if pred_winner == actual_knockout_winners[match_id]:
                    # You can add logic later to weight later rounds higher (e.g., Final = 10 pts)
                    knockout_points += 3 # Standard points per correct knockout pick
                    
        total_score = advancement_points + rank_points + knockout_points
        
        # 4. Prepare the payload for this user
        leaderboard_payload.append({
            "user_id": user_id,
            "username": username,
            "advancement_points": advancement_points,
            "rank_points": rank_points,
            "knockout_points": knockout_points,
            "total_score": total_score
        })
        
    # 5. Push the updated leaderboard back to Supabase
    if leaderboard_payload:
        print(f"Pushing updated scores for {len(leaderboard_payload)} users to Supabase...")
        supabase.table("leaderboard").upsert(leaderboard_payload, on_conflict="user_id").execute()
        print("Leaderboard update complete.")


# --- 4. MASTER UPDATE ROUTINE ---
def update_database():
    # Step 1: Get the data
    group_results, knockout_results = fetch_real_world_results()
    
    # Step 2 (Optional): If you have tables to store actual results, update them here
    # supabase.table("actual_results").upsert(group_results).execute()
    # supabase.table("actual_knockout_results").upsert(knockout_results).execute()
    
    # Step 3: Run the scoring engine
    calculate_and_update_leaderboard(group_results, knockout_results)


if __name__ == "__main__":
    print("Starting automated World Cup updater...")
    try:
        update_database()
        print("✅ Successfully updated all match results and recalculated the leaderboard!")
    except Exception as e:
        print(f"❌ Error during update: {e}")