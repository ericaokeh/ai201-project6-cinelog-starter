# PR Response Doc — CineLog Watchlist Feature

## AI Usage
I used AI to explain the existing Flask, SQLAlchemy, service, route, and test code while implementing the watchlist feature. I asked: "What counterargument would a careful code reviewer raise against this position? What tradeoff am I not acknowledging?" about my decision to make watchlists public by default. The counterargument was that users may expect their watchlists to be private, so public visibility should be intentional and clearly communicated. As a result, I kept `public=True` for social discovery but documented the privacy tradeoff and the need for a future visibility control. AI also helped me understand test failures, identify missing fixtures, and improve the wording of my PR responses.

## Comment 1 — Rename
**What I did:**
I renamed save_to_watchlist() to add_to_watchlist() to match the existing add_to_collection() naming pattern. I checked the watchlist route and service call sites to make sure they use the new name.
**How I verified:**
I searched the watchlist route and service for save_to_watchlist references and confirmed the call now uses add_to_watchlist.

## Comment 2 — Deduplication
**What I did:**
I followed the add_to_collection() pattern: the service queries for an existing entry using both user_id and film_id. If one is found, it raises AlreadyInWatchlistError before creating another row.
**How I verified:**
I ran the duplicate-entry test and confirmed the second add raises AlreadyInWatchlistError and leaves one database row.

## Comment 3 — Missing test
**What I did:**
I modeled the test on the nonexistent-film collection test. It passes an ID that is not in the Film table and checks that FilmNotFoundError is raised before a database insert is attempted.
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
I kept the UUID version, the newer watchlist code, my PR response, and the test.
**How I verified no conflict remains:**
I removed the conflict markers, staged the files, and completed the rebase. The watchlist files also passed a Python compile check.

## PR Description
Added a watchlist feature that lets users add films and view their saved films.

The service checks that a film exists and prevents the same user from adding the same film more than once. Duplicate requests return a conflict error, and invalid film IDs raise FilmNotFoundError. Watchlists are public by default to support film discovery, and films are sorted by the date they were added, newest first.

To manually test the feature, seed the database, start the Flask app, then use a real user ID and film ID. Send POST /watchlist/<user_id>/add once and confirm a 201 response. Send the same request again and confirm a 409 response. Send an invalid film ID and confirm a 404 response. Finally, send GET /watchlist/<user_id> and confirm the films are returned newest first. Automated tests cover the successful add, duplicate add, and nonexistent film cases.
