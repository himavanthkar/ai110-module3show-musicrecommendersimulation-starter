# Music Recommender Simulation — VibeFinder 1.0

A content-based music recommendation engine that scores and ranks songs based on how closely they match a listener's taste profile. Built to simulate how platforms like Spotify and YouTube Music turn raw song attributes into personalized playlists.

The system reads a catalog of 20 songs from a CSV file, takes a user's preferences (genre, mood, energy, danceability, valence, acousticness), and produces a ranked list of the top 5 songs with a full breakdown of *why* each song was chosen.

---

## How The System Works

### How Real Platforms Do It

Streaming platforms usually combine two approaches:

- **Collaborative filtering** looks at millions of other users who share similar listening patterns and recommends tracks they enjoyed. It's great for discovery but needs a huge amount of behavioral data.
- **Content-based filtering** ignores other users entirely. Instead it compares the *attributes of songs themselves* (tempo, energy, mood, genre) against a user profile. If you keep listening to high-energy pop, it finds more high-energy pop.

Spotify and YouTube actually layer both methods together, plus natural-language analysis of how people describe music online. My simulation focuses only on the content-based side to keep things transparent and explainable.

### What VibeFinder Uses

Each **Song** object carries these attributes:

| Field | Type | Description |
|---|---|---|
| `genre` | string | Music genre (pop, rock, lofi, edm, etc.) |
| `mood` | string | Emotional tone (happy, chill, intense, sad, etc.) |
| `energy` | 0.0–1.0 | How energetic / active the track feels |
| `danceability` | 0.0–1.0 | How suitable the track is for dancing |
| `valence` | 0.0–1.0 | How positive / cheerful the track sounds |
| `acousticness` | 0.0–1.0 | How acoustic (vs. electronic) the production is |
| `tempo_bpm` | int | Beats per minute |

Each **UserProfile** stores:

- `genre` — preferred genre
- `mood` — preferred mood
- `energy`, `danceability`, `valence`, `acousticness` — target numerical values

### Algorithm Recipe (Scoring Rule)

For every song in the catalog, the system computes a relevance score:

| Rule | Max Points | Logic |
|---|---|---|
| Genre match | **+2.0** | Exact match between song and user genre |
| Mood match | **+1.5** | Exact match between song and user mood |
| Energy similarity | **+1.5** | `(1 − |song_energy − target_energy|) × 1.5` |
| Danceability similarity | **+1.0** | `(1 − |song_dance − target_dance|) × 1.0` |
| Valence similarity | **+1.0** | `(1 − |song_valence − target_valence|) × 1.0` |
| Acousticness similarity | **+0.5** | `(1 − |song_acoustic − target_acoustic|) × 0.5` |

**Maximum possible score: ~7.5 points.**

Genre gets the heaviest weight because it's the strongest signal for musical preference — a rock fan rarely wants lofi suggestions even if the energy levels are identical. Mood is second because it captures the *context* (working out vs. studying). The numerical features fine-tune rankings within those buckets.

### Ranking Rule

After every song gets a score, the system sorts them highest-to-lowest and returns the top *k* (default 5). That sorted list is the final recommendation.

### Data Flow

```
User Preferences (genre, mood, energy, ...)
       │
       ▼
┌──────────────────────────────┐
│  Load all songs from CSV     │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  For each song:              │
│    score_song(prefs, song)   │
│    → (numeric score, reasons)│
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Sort by score descending    │
│  Return top K with reasons   │
└──────────────────────────────┘
```

---

## Getting Started

### Setup

1. Clone this repo and `cd` into it.

2. Create a virtual environment (optional but recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the recommender:

```bash
python3 src/main.py
```

### Running Tests

```bash
pytest tests/ -v
```

---

## Sample Output

### High-Energy Pop Fan

```
======================================================================
  Profile: High-Energy Pop Fan
----------------------------------------------------------------------
  Preferences: genre=pop, mood=happy, energy=0.85, dance=0.8, valence=0.85
======================================================================

  #1  Sunrise City  —  Neon Echo
       Genre: pop  |  Mood: happy  |  Energy: 0.82  |  Valence: 0.84
       Score: 7.40
       Why:   genre match (+2.0), mood match (+1.5), energy similarity (+1.46),
              danceability similarity (+0.99), valence similarity (+0.99),
              acousticness similarity (+0.46)
```

### Chill Lofi Listener

```
  #1  Library Rain  —  Paper Lanterns
       Genre: lofi  |  Mood: chill  |  Energy: 0.35  |  Valence: 0.6
       Score: 7.41
       Why:   genre match (+2.0), mood match (+1.5), energy similarity (+1.46),
              danceability similarity (+1.0), valence similarity (+0.98),
              acousticness similarity (+0.47)
```

### Intense Rock Enthusiast

```
  #1  Storm Runner  —  Voltline
       Genre: rock  |  Mood: intense  |  Energy: 0.91  |  Valence: 0.48
       Score: 7.43
       Why:   genre match (+2.0), mood match (+1.5), energy similarity (+1.48),
              danceability similarity (+0.99), valence similarity (+0.97),
              acousticness similarity (+0.49)
```

### Sad Acoustic (Edge Case)

```
  #1  Autumn Letters  —  Clara Moon
       Genre: folk  |  Mood: sad  |  Energy: 0.3  |  Valence: 0.35
       Score: 7.43
       Why:   genre match (+2.0), mood match (+1.5), energy similarity (+1.5),
              danceability similarity (+1.0), valence similarity (+0.95),
              acousticness similarity (+0.48)
```

### Adversarial: High Energy + Sad

```
  #1  Gym Hero  —  Max Pulse
       Genre: pop  |  Mood: intense  |  Energy: 0.93  |  Valence: 0.77
       Score: 5.33
       Why:   genre match (+2.0), energy similarity (+1.48),
              danceability similarity (+0.97), valence similarity (+0.38),
              acousticness similarity (+0.5)
```

This adversarial profile is interesting — the user wants pop + sad + high energy, which is a contradictory combination. The system compromises by favoring genre + energy over mood, pushing "Gym Hero" (pop, intense, 0.93 energy) to the top even though it doesn't match "sad" at all. This exposes how the scoring weights resolve conflicts.

---

## Experiments I Tried

### Experiment 1: Doubled Energy Weight, Halved Genre Weight

I changed the genre weight from 2.0 to 1.0 and energy similarity multiplier from 1.5 to 3.0. The results shifted noticeably:

- For the Rock Enthusiast, "Bass Cathedral" (EDM, energy 0.95) jumped into the top 2 because the energy match was now worth more than the genre match.
- For the Pop Fan, "Neon Jungle" (EDM) overtook "Gym Hero" (pop) because its energy was closer to the target.
- The recommendations became less genre-focused and more about energy alignment, which made the output feel less like "genre radio" and more like a workout playlist.

**Takeaway:** Genre weight acts as a "stay in your lane" control. Lowering it increases cross-genre discovery but also increases the chance of irrelevant results.

### Experiment 2: Removed Mood Check

I commented out the mood matching logic entirely. The impact:

- For the Chill Lofi profile, "Focus Flow" (mood: focused) jumped up because without the mood bonus, it was only competing on genre + numerical features — and its energy was very close.
- The Sad Acoustic profile started recommending ambient tracks alongside folk because there was no mood penalty for "chill" vs. "sad."
- Overall the rankings felt less emotionally coherent. Songs were technically similar but didn't "feel" right as a playlist.

**Takeaway:** Mood matching is critical for emotional coherence. Without it, the system optimizes for sound characteristics but ignores the listening context.

---

## Limitations and Risks

- **Tiny catalog (20 songs):** Some genres only have 1–2 representatives, so the system can't provide much variety for niche tastes.
- **Binary genre/mood matching:** "Epic" and "intense" feel related, but get zero match credit. A fuzzy matching approach would be more realistic.
- **No listening history:** Real recommenders learn from skips, replays, and playlist additions. This system has no feedback loop.
- **Dataset imbalance:** Rock and lofi have 3+ entries each while folk, funk, and r&b have only 1. The system inherently has more options for some genres.
- **No lyrics or language understanding:** A Spanish ballad and an English ballad get the same treatment if their numbers match.
- **Filter bubble risk:** Because genre is weighted so heavily, a user who says "pop" will almost never see a jazz or ambient track, even if it perfectly matches their energy and mood.

---

## Reflection

Read and complete the [`model_card.md`](model_card.md) for the full Model Card.

Building this recommender taught me that the gap between "simple math" and "feels like a real recommendation" is surprisingly small. A weighted scoring function with just six features produces results that genuinely make sense — when I ran the Chill Lofi profile, the top results were exactly what I'd pick for a study session.

But I also saw how easily the system creates filter bubbles. The genre weight (2.0 points) is so dominant that it drowns out everything else for borderline cases. A user who likes folk will never discover that "Rainy Jazz Cafe" might be perfect for them, because jazz ≠ folk and that's a 2-point penalty that numerical similarity can't overcome. In real products this compounds over time: you listen to more of what the system shows you, which reinforces the system's confidence that you only want that genre.

I used AI assistance to help brainstorm the initial scoring formula and to generate additional song data for the CSV, but I manually adjusted the weights after testing showed the first version was too energy-dominant. The AI suggestion of equal weights across all features sounded reasonable in theory, but when I ran it, genre became meaningless and the results felt random. That taught me that designing an algorithm isn't just math — it's about understanding which features actually matter to human listeners.

If I had more time I'd add collaborative filtering using simulated listening histories, implement fuzzy mood matching (so "epic" and "intense" get partial credit), and build a diversity penalty that prevents the same artist from appearing twice in the top 5.
