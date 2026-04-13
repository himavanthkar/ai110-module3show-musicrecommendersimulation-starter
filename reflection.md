# Reflection: Profile Comparisons and Observations

## Profile-by-Profile Comparison

### High-Energy Pop Fan vs. Chill Lofi Listener

These two profiles are near-opposites, and the results reflect that clearly. The Pop Fan's top 5 are all high-energy, high-valence tracks with strong danceability (Sunrise City, Gym Hero, Neon Jungle). The Lofi Listener's top 5 are low-energy, high-acousticness tracks (Library Rain, Midnight Coding, Focus Flow). There is **zero overlap** between the two lists, which makes sense — these users want fundamentally different listening experiences. The system correctly separates them because genre and energy are so different between the two profiles.

### Intense Rock Enthusiast vs. High-Energy Pop Fan

Both profiles want high energy, but one wants rock and the other wants pop. The top results are completely different — Storm Runner vs. Sunrise City — which shows that the genre weight (2.0) is doing its job of separating genres even when the numerical features are similar. However, if I dropped the genre weight to 0.5, I'd expect these two profiles to start sharing recommendations, since both users want energy around 0.85–0.90.

### Sad Acoustic (Edge Case) vs. Chill Lofi Listener

Both want calm, low-energy music, but with different emotional tones (sad vs. chill). The Sad Acoustic profile gets "Autumn Letters" (folk, sad) at the top while the Lofi profile gets "Library Rain" (lofi, chill). The interesting part is that the Sad Acoustic profile's list drops off quickly after #1 — from 7.43 down to 5.04 — because there's only one folk/sad song in the catalog. The Lofi profile has a much smoother top 5 because there are three lofi tracks available. This shows how dataset size directly affects recommendation quality for niche tastes.

### Adversarial Profile vs. Everyone Else

The adversarial profile (pop + sad + high energy) is the most revealing test. It asks for a combination that barely exists in music — high-energy sad pop. The system resolves the conflict by leaning on genre (pop gets +2.0) and energy (high match gets ~1.5), which together outweigh the mood bonus (+1.5). So "Gym Hero" (pop, intense, 0.93 energy) beats "Broken Records" (indie pop, sad, 0.45 energy) even though Broken Records matches the "sad" mood perfectly. This tells me: **when preferences conflict, the heaviest weight wins, and the lighter features get sacrificed.** A smarter system might detect the conflict and ask the user to clarify.

### Intense Rock vs. Sad Acoustic

These profiles share almost nothing — different genre, different mood, opposite energy levels. The Rock profile gets all three rock/intense songs in its top 3. The Sad Acoustic profile gets folk in #1 and then a scattered mix. The complete separation here validates that the scoring function can differentiate between very different user types.

---

## What Surprised Me

1. **The "Gym Hero" problem.** Gym Hero (pop, intense, 0.93 energy) kept appearing in multiple profiles — it showed up for the Pop Fan (#2) and the Adversarial profile (#1). Its high energy and danceability scores give it baseline points against many profiles, even when the mood doesn't match. In a real product, this would be the song that gets over-recommended.

2. **Edge cases expose dataset gaps.** The Sad Acoustic profile revealed that with only 1 folk song, the system runs out of good recommendations quickly. After the #1 pick, the rest of the list is just "least bad" options that don't really match.

3. **Mood matters more than I expected.** When I removed the mood check in my experiment, the results felt technically correct but emotionally wrong — like a playlist that sounds right on paper but you'd skip through in practice.

---

## What I Learned About the Engineering Process

I used AI tools to help brainstorm the initial scoring weights and to generate additional CSV song data. This saved time on the mechanical parts, but I had to manually verify and adjust things — for example, the initial weight suggestion treated all features equally, which produced mushy results where genre didn't matter enough. I ended up settling on the 2.0 / 1.5 / 1.5 / 1.0 / 1.0 / 0.5 hierarchy after running all five profiles and checking whether the top results matched my musical intuition.

The biggest lesson is that recommendation systems aren't just math problems — they're design decisions about what matters. Choosing to weight genre at 2.0 is a bet that genre is the strongest predictor of taste, and that assumption shapes everything downstream. If I'm wrong about that for a particular user, the whole recommendation list falls apart.
