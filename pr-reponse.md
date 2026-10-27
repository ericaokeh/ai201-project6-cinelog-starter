# PR Response Doc — CineLog Watchlist Feature

## AI Usage
I used AI to explain the existing Flask, SQLAlchemy, service, route, and test code while implementing the watchlist feature. I asked: "What counterargument would a careful code reviewer raise against this position? What tradeoff am I not acknowledging?" about my decision to make watchlists public by default. The counterargument was that users may expect their watchlists to be private, so public visibility should be intentional and clearly communicated. As a result, I kept `public=True` for social discovery but documented the privacy tradeoff and the need for a future visibility control. AI also helped me understand test failures, identify missing fixtures, and improve the wording of my PR responses.

## Comment 1 — Rename
**What I did:**
I renamed save_to_watchlist() to add_to_watchlist() to match the existing add_to_collection() naming pattern. There were two call sites: the function definition in services/watchlist_service.py and the import plus call in routes/watchlist/watchlist.py (POST /watchlist/<user_id>/add). Both now use add_to_watchlist.
**How I verified:**
I ran `grep -rn "save_to_watchlist" --include='*.py' .` across the whole repo (routes/, services/, tests/, app.py) and it returned 0 matches. The test file imports add_to_watchlist directly, so the full test suite passing confirms nothing still references the old name.

## Comment 2 — Deduplication
**What I did:**
I followed the add_to_collection() pattern: the service queries for an existing entry using both user_id and film_id. If one is found, it raises AlreadyInWatchlistError before creating another row.
**How I verified:**
I ran the duplicate-entry test and confirmed the second add raises AlreadyInWatchlistError and leaves one database row.

## Comment 3 — Missing test
**What I did:**
I added test_add_to_watchlist_nonexistent_film_raises, modeled on test_add_to_collection_nonexistent_film_raises in tests/test_collection.py. It passes a well-formed UUID (00000000-0000-0000-0000-000000000000) that is not in the Film table and checks that add_to_watchlist raises FilmNotFoundError instead of a database integrity error.
**How I verified:**
I ran the nonexistent-film test and confirmed it passed with FilmNotFoundError.

## Comment 4 — Default visibility
**My position:**
I chose to make watchlists public by default with public = True.
**Reasoning:**
Public watchlists can help users discover films through other people’s lists, see what their friends or favorite users are watching, and get ideas for what to add next. This makes the watchlist useful as a social discovery feature from the beginning.
**Tradeoff acknowledged:**
The tradeoff is that users’ watchlists are visible unless the visibility setting is changed. If private watchlists are added later, the application should provide a clear way for users to change this setting and explain the visibility behavior.

## Comment 5 — Sort order
**My position:**
I chose date-added order. CineLog users are likely to open a watchlist to see what they most recently saved, so new ideas appear first instead of being hidden in an alphabetical list.
**Reasoning:**
Watchlists are planning tools, so the most recently saved films are the most relevant for the user’s next viewing choice.
**Engagement with reviewer's point:**
I agree with the maintainer that most users want to see what they added recently. The service uses WatchlistEntry.date_added.desc() to implement that behavior.

## Comment 6 — Rebase
**What conflicted:**
The rebase had conflicts in the model, watchlist files, PR response, and test. The main issue was integer IDs versus UUID string IDs.
**How I resolved it:**
I kept main's UUID version of models.py (Film.id and WatchlistEntry.film_id are String(36) UUIDs), the newer watchlist code, my PR response, and the test. I then updated the watchlist service and route so film_id is documented and handled as a UUID string instead of an int (commit: `fix: update watchlist film IDs to UUID format after main refactor`).
**How I verified no conflict remains:**
I removed the conflict markers, staged the files, and completed the rebase. The history is linear (no merge commits), the watchlist files pass a Python compile check, and the full test suite passes using UUID film IDs.

## Stretch — Second test
**What I did:**
I added test_get_watchlist_returns_newest_first, modeled on test_get_collection_returns_newest_first. It adds "Alien" five days ago and "Blade Runner" today, then checks get_watchlist returns ["Blade Runner", "Alien"].
**Why this edge case:**
The sort order was changed during review (Comment 5), and nothing tested it. I picked titles where alphabetical order and date order disagree, so the test fails if the query ever goes back to Film.title.asc(). I confirmed this by temporarily switching the sort back and watching the test fail.

## PR Description
Added a watchlist feature that lets users add films and view their saved films.

The service checks that a film exists and prevents the same user from adding the same film more than once. Duplicate requests return a conflict error, and invalid film IDs raise FilmNotFoundError.

**Design decisions:**
- **Default visibility: public.** Watchlists are public by default so other users can discover films through each other's lists.
- **Sort order: date added, newest first.** Users usually open their watchlist to find what they saved most recently, so new additions appear at the top instead of being buried alphabetically.

**How to test manually:**
1. Run `python seed.py`, then start the app with `python app.py` (http://localhost:5000).
2. Pick a real user ID and two film IDs from the seeded database.
3. `POST /watchlist/<user_id>/add` with body `{"film_id": "<film_id>"}` and confirm a 201 response.
4. Send the same request again and confirm a 409 response.
5. Send `{"film_id": "00000000-0000-0000-0000-000000000000"}` and confirm a 404 response.
6. Add the second film, then `GET /watchlist/<user_id>` and confirm the second film is listed first.

Automated tests (`python -m pytest -q`) cover the successful add, the duplicate add, a nonexistent film, and newest-first sorting.
