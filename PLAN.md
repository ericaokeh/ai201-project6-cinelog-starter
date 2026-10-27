# Watchlist Plan

## Goal
Add a watchlist feature that lets a CineLog user save films for later and retrieve them in the order they were added.

## Files and actions
1. Update models.py with WatchlistEntry, using the same UUID film ID type as Film.
2. Implement add_to_watchlist() and get_watchlist() in services/watchlist_service.py.
3. Add GET and POST watchlist routes and map service errors to HTTP responses.
4. Add service tests for a successful add, duplicate add, and nonexistent film ID.
5. Update the PR response and verify the code with pytest and Python compilation.

## Inputs and outputs
The add service takes a user ID and film ID and returns a WatchlistEntry or raises FilmNotFoundError or AlreadyInWatchlistError. The list service takes a user ID and returns film dictionaries with date_added and public metadata. The POST endpoint accepts a JSON body containing film_id and returns JSON with HTTP 201 on success.

## Risks and unknowns
The WatchlistEntry film_id type must match Film.id after the UUID refactor. Duplicate requests must be rejected before insertion and should return HTTP 409 through the route. The test fixtures must create an isolated database so tests do not affect the local SQLite database.

## Edge cases
- A nonexistent film ID must raise FilmNotFoundError and must not insert a row.
- Adding the same film twice for one user must raise AlreadyInWatchlistError and leave one row.
- A request without film_id must return HTTP 400.
- A user with no watchlist entries must receive an empty list.
