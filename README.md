# Read the Play

**Can you read the play like a coach?**
A fan experience for the Spengler Cup, built by Team AwArt for the SIC Data-hack 2026 (ThinkSport × Spengler Cup Davos).

## The idea

Most fans see the goal, not the decision behind it. *Read the Play* shows a key moment of the game and asks the fan to judge the player's decision, like a coach. Then the data reveals what really happened.

1. **Watch** a real game clip, with the key player highlighted. Newcomers get a second view, zoomed in and in slow motion.
2. **Vote:** Bad, Neutral, Good or Exceptional.
3. **The reveal**, step by step:
   - how the other fans voted;
   - **decision time:** how long the player had to decide, compared with how long the fan took to vote;
   - **what the player saw:** the tracking view with all 12 players, the pressure and the open space. Fans can tap any player to explore more data;
   - **what came next:** the shot, its speed and its chance of becoming a goal (xG).
4. **The expert's verdict** at the final whistle, points, levels and a card to share.

Available in English, French and German.

## How the data drives it

The prototype uses Wisehockey tracking and event data:

- **Decision time:** time between the player receiving the puck (`PuckControl` event) and his pass or shot.
- **Pressure and space:** distance to the nearest opponent, from the positions of all players at that moment.
- **The 2D replay:** positions of the 12 players over time, interpolated between events.
- **The outcome:** shot speed and expected goals (xG) from the event data.

## Data and confidentiality

The challenge data is confidential and is **not** in this repository.

- `data/sample-sequence.js` contains **invented sample data** with the same structure, so the prototype runs out of the box.
- To use real data, run `scripts/extract_sequence.py` on the challenge files. It writes `private/sequence.js`, which overrides the sample data and is ignored by git.
- The game clip is loaded from `private/clip.mp4` (not committed). Without it, the app falls back to the 2D tracking replay.

## Run it

Open `index.html` through any static web server, for example:

```bash
python -m http.server 8000
# then open http://localhost:8000
```

No build step and no backend.

## Team

Team AwArt: Michael Rohrer, Vili Bénain, Casper Thiriet (EHC Basel), Serge Pelletier.
Built on the experience of [AwArt](https://awart.one), live fan voting for sports clubs.
