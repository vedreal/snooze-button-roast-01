#!/usr/bin/env python3
"""Snooze Button Roast — make.fun entry.

Writes one line roasting an alarm clock that rings at 6 AM on a Saturday
morning to /output/entry.txt.

Judge's brief (in its published order, weights 5/4/3/2/1):
  1. Roasts an alarm clock that rings at 6 AM on a Saturday, in one line.
  2. Lands a real laugh: unexpected turn, punchline pays off in the last
     few words.
  3. Fresh angle: not the tired complaint about hating mornings, and not
     asking who invented it.
  4. Tight: every word earns its place, sayable out loud in one breath.
  5. Sharp, specific voice with concrete images, not vague grumbling.
"""

CANDIDATES = [
    # 1. The clock as the only employed thing in the house.
    "6 AM on a Saturday, and my alarm clock is already on its feet - "
    "the only thing in this house with a job, a schedule, and "
    "absolutely no friends.",
    # 2. The clock enjoys the sabotage.
    "My alarm clock rang at 6 AM on a Saturday like it had somewhere "
    "to be. It doesn't. It just enjoys ruining my one day of peace.",
    # 3. Mistaken for a fire drill.
    "Saturday, 6 AM: the alarm goes off, and for one glorious second "
    "I think it's a fire drill. Nope - just my clock, auditioning "
    "for a job as my enemy.",
    # 4. Rooster comparison, with a farm-decent twist.
    "The alarm clock rang at 6 AM on Saturday, proud as a rooster, "
    "except a rooster at least has the decency to live on a farm.",
    # 5. The house-on-fire misdirect.
    "At 6 AM on Saturday my alarm clock screamed like the house was "
    "on fire. The only thing burning was my weekend.",
    # 6. One setting: maximum betrayal.
    "My alarm clock has one setting: 6 AM, Saturday, maximum "
    "betrayal. It even snoozes itself just to watch me suffer twice.",
    # 7. A bird that read the calendar and chose violence.
    "Six in the morning, Saturday, and the alarm clock is chirping "
    "like a bird that read my calendar and chose violence.",
    # 8. The smug clock that waited all week.
    "The alarm clock rang at 6 AM on Saturday and I swear it sounded "
    "smug, like it had been waiting all week for this exact moment.",
    # 9. Tiny drill sergeant who missed the memo.
    "Saturday, 6 AM: my alarm clock went off like a tiny drill "
    "sergeant who missed the memo that the war is over and it's the "
    "weekend.",
    # 10. National emergency.
    "My alarm clock rang at 6 AM on a Saturday - the one morning I "
    "planned to sleep in - and it treated it like a national "
    "emergency.",
]

# Scores per candidate on the judge's five criteria (0-5 each), in the
# brief's order: on-subject, laugh, freshness, tightness, voice.
# Weights: 5, 4, 3, 2, 1 (max 75).
WEIGHTS = (5, 4, 3, 2, 1)

SCORES = {
    # 1: on-subject, strong closing list, fresh "only employed thing"
    # angle, tight, concrete (job/schedule/friends).
    1: (5, 4, 4, 4, 4),
    # 2: on-subject, "it just enjoys ruining" is a good turn, but the
    # "ruining my peace" line is a familiar complaint shape.
    2: (5, 3, 3, 4, 3),
    # 3: fire-drill misdirect is fun, but "job as my enemy" lands soft
    # and the line runs long.
    3: (5, 3, 3, 2, 3),
    # 4: rooster image is concrete and the farm punchline is fresh, but
    # the middle sags a little.
    4: (5, 4, 4, 3, 4),
    # 5: house-on-fire misdirect, punchline in the last words ("my
    # weekend"), fresh, tight, concrete.
    5: (5, 5, 4, 5, 4),
    # 6: "maximum betrayal" is punchy, but "watch me suffer twice" is
    # close to plain grumbling and the snooze logic is muddled.
    6: (5, 3, 3, 3, 3),
    # 7: "read my calendar and chose violence" is the freshest, most
    # specific image of the set; short and sayable in one breath.
    7: (5, 4, 5, 5, 5),
    # 8: "sounded smug" is a nice voice, but the joke is mostly
    # "it waited all week" - a familiar personification.
    8: (5, 3, 2, 4, 3),
    # 9: drill-sergeant image is concrete and the "war is over"
    # punchline lands last; slightly long.
    9: (5, 4, 4, 3, 4),
    # 10: "national emergency" is a decent closer, but the setup is
    # plain and the turn is mild.
    10: (5, 3, 2, 4, 3),
}


def total_score(scores):
    """Weighted total out of 75."""
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def rank_candidates():
    """Rank candidates best-first by weighted score, then by length."""
    ranked = []
    for i, text in enumerate(CANDIDATES, start=1):
        ranked.append((total_score(SCORES[i]), -len(text), i, text))
    ranked.sort(reverse=True)
    return ranked


def pick_winner():
    """Pick the winning line.

    Candidates 5 and 7 tie at 71/75. The tie-break is length: candidate 5
    is shorter (110 vs 115 chars), and its punchline ("my weekend") lands
    in the very last words, which the judge's second criterion rewards
    explicitly. Winner: candidate 5.
    """
    ranked = rank_candidates()
    _total, _neglen, idx, text = ranked[0]
    return idx, text


def validate(text):
    """Gate: UTF-8 text, 1-200 characters, single line, not only whitespace."""
    assert isinstance(text, str)
    text.encode("utf-8")
    assert 1 <= len(text) <= 200, f"length {len(text)} outside 1-200"
    assert text.strip(), "entry is only whitespace"
    assert "\n" not in text.strip(), "entry must be a single line"
    return True


def main():
    idx, text = pick_winner()
    validate(text)
    import os

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"winner: candidate {idx} ({len(text)} chars)")
    print(text)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "rank":
        for total, _neglen, idx, text in rank_candidates():
            print(f"{idx:2d} [{total:2d}/75] ({len(text)} chars) {text}")
    else:
        main()
