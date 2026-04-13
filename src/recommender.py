import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        """Compute a numeric relevance score for one song."""
        score = 0.0

        if song.genre == user.favorite_genre:
            score += 2.0
        if song.mood == user.favorite_mood:
            score += 1.5

        energy_gap = abs(song.energy - user.target_energy)
        score += (1.0 - energy_gap) * 1.5

        if user.likes_acoustic:
            score += song.acousticness * 0.5
        else:
            score += (1.0 - song.acousticness) * 0.5

        score += song.danceability * 0.5
        score += song.valence * 0.5

        return round(score, 2)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs sorted by relevance score (highest first)."""
        scored = sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable breakdown of why a song was recommended."""
        parts = []

        if song.genre == user.favorite_genre:
            parts.append(f"genre match '{song.genre}' (+2.0)")
        if song.mood == user.favorite_mood:
            parts.append(f"mood match '{song.mood}' (+1.5)")

        energy_gap = abs(song.energy - user.target_energy)
        energy_pts = round((1.0 - energy_gap) * 1.5, 2)
        parts.append(f"energy similarity (+{energy_pts})")

        if user.likes_acoustic:
            ac_pts = round(song.acousticness * 0.5, 2)
            parts.append(f"acousticness bonus (+{ac_pts})")
        else:
            ac_pts = round((1.0 - song.acousticness) * 0.5, 2)
            parts.append(f"low-acousticness bonus (+{ac_pts})")

        parts.append(f"danceability (+{round(song.danceability * 0.5, 2)})")
        parts.append(f"valence (+{round(song.valence * 0.5, 2)})")

        total = self._score(user, song)
        return f"Score {total}: " + ", ".join(parts)


# ── Functional helpers used by src/main.py ───────────────────────────────────

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"].strip().lower(),
                "mood": row["mood"].strip().lower(),
                "energy": float(row["energy"]),
                "tempo_bpm": int(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences, returning (score, reasons)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs.get("mood", "").lower():
        score += 1.5
        reasons.append("mood match (+1.5)")

    if "energy" in user_prefs:
        energy_gap = abs(song["energy"] - user_prefs["energy"])
        energy_pts = round((1.0 - energy_gap) * 1.5, 2)
        score += energy_pts
        reasons.append(f"energy similarity (+{energy_pts})")

    if "danceability" in user_prefs:
        dance_gap = abs(song["danceability"] - user_prefs["danceability"])
        dance_pts = round((1.0 - dance_gap) * 1.0, 2)
        score += dance_pts
        reasons.append(f"danceability similarity (+{dance_pts})")

    if "valence" in user_prefs:
        val_gap = abs(song["valence"] - user_prefs["valence"])
        val_pts = round((1.0 - val_gap) * 1.0, 2)
        score += val_pts
        reasons.append(f"valence similarity (+{val_pts})")

    if "acousticness" in user_prefs:
        ac_gap = abs(song["acousticness"] - user_prefs["acousticness"])
        ac_pts = round((1.0 - ac_gap) * 0.5, 2)
        score += ac_pts
        reasons.append(f"acousticness similarity (+{ac_pts})")

    score = round(score, 2)
    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by relevance and return the top k with explanations."""
    scored = []
    for song in songs:
        pts, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, pts, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
