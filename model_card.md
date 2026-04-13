# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This system suggests 5 songs from a small catalog based on a user's preferred genre, mood, and numerical audio features (energy, danceability, valence, acousticness). It is designed for classroom exploration and learning about how content-based recommendation systems work. It is not intended for real production use, commercial music platforms, or any situation where the recommendations influence real listener behavior at scale.

**Not intended for:**
- Replacing a real streaming platform's algorithm
- Making claims about musical quality or cultural value
- Handling users with complex or evolving taste profiles

---

## 3. How the Model Works

The system compares each song in the catalog against a user's preferences using a weighted scoring approach:

1. It checks whether the song's genre matches the user's preferred genre — this is the strongest signal, worth up to 2 points.
2. It checks whether the mood matches — worth up to 1.5 points.
3. For numerical features (energy, danceability, valence, acousticness), it calculates how close the song's value is to the user's target. A perfect match gets the full points; a completely opposite value gets nearly zero. Energy closeness is weighted more heavily (1.5 max) than acousticness (0.5 max) because energy is a more perceptually obvious feature.

After every song gets a total score, the system sorts them from highest to lowest and returns the top 5. Each recommendation comes with a plain-language explanation of why it scored the way it did.

---

## 4. Data

The dataset contains **20 songs** stored in `data/songs.csv`. The starter template provided 10 songs; I added 10 more to improve genre and mood diversity.

**Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, edm, folk, r&b, funk

**Moods represented:** happy, chill, intense, relaxed, moody, focused, sad

The data reflects a mix of popular Western music styles. It under-represents non-Western genres (no K-pop, Afrobeat, reggaeton, classical, etc.), and the "mood" labels are subjective — I assigned them based on my own perception, which may not match every listener's experience.

---

## 5. Strengths

- **Transparent and explainable:** Every recommendation comes with a score breakdown, so you can trace exactly why a song was chosen. This is something most real recommenders don't offer.
- **Intuitive results for clear profiles:** When a user has a well-defined taste (e.g., "chill lofi" or "intense rock"), the top results consistently make sense and feel like a real playlist.
- **Simple to modify:** The weights can be adjusted easily to experiment with different prioritization strategies, making it a good learning tool.
- **No cold start problem for content-based matching:** Unlike collaborative filtering, this system doesn't need any prior listening history — just a preference profile.

---

## 6. Limitations and Bias

- **Genre dominance creates filter bubbles.** The 2.0 genre weight means a same-genre song with mediocre numerical match will almost always beat a different-genre song with a perfect numerical match. This prevents cross-genre discovery.
- **Binary matching is too rigid.** "Epic" and "intense" are treated as completely different moods, even though they share emotional overlap. Same for "indie pop" vs. "pop."
- **Small catalog amplifies imbalance.** Rock has 3 songs while folk has 1. A rock fan gets meaningful rankings; a folk fan gets one clear winner and then irrelevant filler.
- **No temporal or social context.** The system doesn't know if someone is at the gym, studying, or driving — contexts where the same person might want completely different music.
- **Western-centric data.** The entire catalog is Western music, so the system literally cannot serve users who prefer other musical traditions.
- **If this were a real product**, the genre bias could systematically under-expose emerging or minority genres, making it harder for new artists in underrepresented categories to reach listeners.

---

## 7. Evaluation

I tested the system with **five distinct user profiles:**

1. **High-Energy Pop Fan** — Wanted upbeat, danceable pop. Results: Sunrise City and Gym Hero at the top. Felt correct.
2. **Chill Lofi Listener** — Wanted relaxed, acoustic study music. Results: Library Rain and Midnight Coding. Exactly what I'd expect.
3. **Intense Rock Enthusiast** — Wanted driving, energetic rock. Results: Storm Runner, Velvet Thunder, Rebel Yell Remix. All three rock + intense tracks ranked 1-2-3. Strong performance.
4. **Sad Acoustic (Edge Case)** — Only one folk/sad song in the catalog. It ranked #1 (Autumn Letters) with a high score, but the rest of the list dropped off sharply, showing the dataset limitation.
5. **Adversarial: High Energy + Sad** — Conflicting preferences. The system compromised by prioritizing genre (pop) and energy over mood, pushing upbeat pop tracks to the top instead of sad songs. This revealed how the weight hierarchy resolves ambiguity.

I also ran two experiments:
- Doubling energy weight while halving genre: made results more cross-genre but less genre-coherent.
- Removing mood matching entirely: made recommendations technically accurate but emotionally incoherent.

I wrote unit tests (in `tests/test_recommender.py`) to verify that the OOP `Recommender` class returns songs sorted by score and that explanations are non-empty strings.

---

## 8. Future Work

- **Fuzzy mood matching:** Treat related moods (e.g., "epic" and "intense") as partial matches instead of binary yes/no.
- **Diversity penalty:** Penalize songs from the same artist or genre if they already appear in the top results, to prevent repetitive recommendations.
- **Collaborative filtering layer:** Simulate multiple users with listening histories and use "users like you also listened to…" logic alongside content matching.
- **Tempo-based scoring:** Use `tempo_bpm` as a scoring feature — useful for workout or driving playlists where BPM matters.
- **Larger, more diverse catalog:** Expand to 100+ songs across more genres and cultural traditions.

---

## 9. Personal Reflection

The most surprising thing was how the adversarial profile exposed the system's decision-making. When I gave it conflicting preferences (high energy + sad mood), I expected it to find some middle ground, but instead it basically ignored the mood and chased genre + energy. That made me realize that weight design isn't just a technical decision — it's a *values* decision about which user signals matter most.

Building this changed how I think about real music apps. When Spotify puts the same artist in my Discover Weekly three weeks in a row, I now understand it's probably because their genre signal is overwhelming everything else, just like my 2.0 weight does here. The algorithm isn't "stupid" — it's doing exactly what the weights tell it to, which might not be what the user actually wants.

I think human judgment still matters for the ambiguous cases — the "I want something new but not too different" moments that no scoring formula can capture. A good recommender should know when to follow the formula and when to take a creative risk. My system can't do that yet, but understanding why helped me appreciate the engineering challenge behind the apps I use every day.
