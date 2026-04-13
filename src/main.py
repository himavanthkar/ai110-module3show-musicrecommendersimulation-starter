"""
Command-line runner for the Music Recommender Simulation.
Loads songs, runs multiple user profiles, and prints ranked results.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop Fan": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "danceability": 0.80,
        "valence": 0.85,
        "acousticness": 0.10,
    },
    "Chill Lofi Listener": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "danceability": 0.58,
        "valence": 0.58,
        "acousticness": 0.80,
    },
    "Intense Rock Enthusiast": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.90,
        "danceability": 0.65,
        "valence": 0.45,
        "acousticness": 0.08,
    },
    "Sad Acoustic (Edge Case)": {
        "genre": "folk",
        "mood": "sad",
        "energy": 0.30,
        "danceability": 0.40,
        "valence": 0.30,
        "acousticness": 0.90,
    },
    "Conflicting: High Energy + Sad (Adversarial)": {
        "genre": "pop",
        "mood": "sad",
        "energy": 0.92,
        "danceability": 0.85,
        "valence": 0.15,
        "acousticness": 0.05,
    },
}


def print_recommendations(profile_name, prefs, recommendations):
    """Display a formatted recommendation block for one user profile."""
    print("=" * 70)
    print(f"  Profile: {profile_name}")
    print("-" * 70)
    pref_parts = [f"genre={prefs['genre']}", f"mood={prefs['mood']}",
                  f"energy={prefs.get('energy', 'N/A')}"]
    if "danceability" in prefs:
        pref_parts.append(f"dance={prefs['danceability']}")
    if "valence" in prefs:
        pref_parts.append(f"valence={prefs['valence']}")
    print(f"  Preferences: {', '.join(pref_parts)}")
    print("=" * 70)

    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  "
              f"|  Energy: {song['energy']}  |  Valence: {song['valence']}")
        print(f"       Score: {score:.2f}")
        print(f"       Why:   {explanation}")

    print("\n")


def main():
    songs = load_songs(os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv"))
    print(f"\n  Loaded songs: {len(songs)}\n")

    for name, prefs in PROFILES.items():
        results = recommend_songs(prefs, songs, k=5)
        print_recommendations(name, prefs, results)


if __name__ == "__main__":
    main()
