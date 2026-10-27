# PR Response Doc — CineLog Watchlist Feature

## AI Usage
I used AI to explain the existing Flask, SQLAlchemy, service, route, and test code while implementing the watchlist feature. I asked: "What counterargument would a careful code reviewer raise against this position? What tradeoff am I not acknowledging?" about my decision to make watchlists public by default. The counterargument was that users may expect their watchlists to be private, so public visibility should be intentional and clearly communicated. As a result, I kept `public=True` for social discovery but documented the privacy tradeoff and the need for a future visibility control. AI also helped me understand test failures, identify missing fixtures, and improve the wording of my PR responses.

## Comment 1 — Rename
**What I did:**
I just changed it to match the "add" rather than save
**How I verified:**
running tesst

## Comment 2 — Deduplication
**What I did:**
I used the existing value to check if the ideal user + movie was inside the database, If it is, then the existing error function called ALreadywatchlisterror is raissed. The custom exception already existed and I just added it. 
**How I verified:**
running tests 

## Comment 3 — Missing test
**What I did:**
Added a test that created an esception error in case a non-valid id was imputted to add to the watchlist. This raises an exception instead of database error.  
**How I verified:**
running test in pytest

## Comment 4 — Default visibility
**My position:**
I chose to make watchlists public by default with public = True.
**Reasoning:**
Public watchlists can help users discover films through other people’s lists, see what their friends or favorite users are watching, and get ideas for what to add next. This makes the watchlist useful as a social discovery feature from the beginning.
**Tradeoff acknowledged:**
The tradeoff is that users’ watchlists are visible unless the visibility setting is changed. If private watchlists are added later, the application should provide a clear way for users to change this setting and explain the visibility behavior.

## Comment 5 — Sort order
**My position:**
I agree, timeing can give better idea of when films are reviewed, released and even bring attention to marketing. 
**Reasoning:**
Timing gives more context about what was just recently watched. 
**Engagement with reviewer's point:**
I agree, great point with the recent view

## Comment 6 — Rebase
**What conflicted:**
**How I resolved it:**
**How I verified no conflict remains:**

## PR Description
<!-- Written at the end — feature overview, design decisions, manual testing steps -->
