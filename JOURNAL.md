# Project Journal

## Check-in 1

I selected the watchlist feature because it is a focused change that builds on the existing collection service. The main tasks were to understand the User, Film, and WatchlistEntry models, implement the service and routes, prevent duplicate entries, and add tests for invalid IDs and duplicate requests.

The main risk was the branch containing an older integer film ID while main had moved to UUID string IDs. I planned to resolve that by matching WatchlistEntry.film_id to Film.id and then rebasing the feature branch onto main.

## Check-in 2

The watchlist feature is implemented on feature/watchlist. It adds endpoints for viewing a user's watchlist and adding a film, rejects duplicate entries, returns a clear error for nonexistent film IDs, defaults watchlists to public, and sorts entries newest first.

Tests created or modified: tests/test_watchlist.py. The tests cover a successful add, a duplicate add, and a nonexistent film ID. I also verified the watchlist route and service compile successfully.

Branch: feature/watchlist
PR: https://github.com/codepath/ai201-project6-cinelog-starter/pull/1
PathReview issue: TODO: replace this with the live PathReview issue URL before submission

Self-review:
- [x] make check passes
- [x] make test-unit passes

## Reflection

Reviewer feedback was received on the watchlist rename, duplicate handling, missing test, default visibility, sort order, and rebase. I documented the response to each comment in pr-reponse.md and updated the code or documentation where needed.

The hardest part was resolving the rebase conflicts caused by the change from integer film IDs to UUID strings. I learned that a feature branch must be kept aligned with the current model contract on main, not only with the code that existed when the feature began.

Working in this codebase taught me to trace behavior across routes, services, models, and tests. For example, the route converts service exceptions into HTTP responses while the service owns duplicate and missing-film rules.

AI helped me understand unfamiliar SQLAlchemy queries, identify the missing pytest fixtures, and challenge the public-by-default visibility decision. It fell short when the environment was missing dependencies and when Git history became confusing, so I verified repository state with Git commands.

If I started over, I would make smaller conventional commits, avoid committing generated files, and rebase earlier before the branch history became difficult to resolve.

I am most proud of making duplicate watchlist additions safe and adding a test that confirms invalid film IDs raise a clear application exception instead of reaching the database.
