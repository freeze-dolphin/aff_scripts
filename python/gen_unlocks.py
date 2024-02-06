import json

p_unlocks = {"unlocks": []}


def append_unlock_info(_song_id, _rating_class):
    p_unlocks["unlocks"].append(
        {
            "songId": _song_id,
            "ratingClass": _rating_class,
            "conditions": [{"type": 5, "rating": 1000}],
        }
    )


with open(
        "songlist",
        "r",
) as f_sl:
    s_sl = f_sl.read()
    j_sl = json.loads(s_sl)

    j_songs = j_sl["songs"]
    for j_song in j_songs:
        song_id = j_song["id"]

        j_diffs = j_song["difficulties"]
        for j_diff in j_diffs:
            rating = j_diff["rating"]
            rating_class = j_diff["ratingClass"]

            if rating == -1:
                append_unlock_info(song_id, rating_class)

j_unlocks = json.dumps(p_unlocks, indent=4)

with open(
        "unlocks",
        "w",
) as f_unlocks:
    # print(j_unlocks)
    f_unlocks.write(j_unlocks)
