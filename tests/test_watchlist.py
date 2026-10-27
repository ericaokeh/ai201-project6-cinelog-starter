import pytest
from app import create_app, db
from models import Film, User, WatchlistEntry
from services.collection_service import FilmNotFoundError
from services.watchlist_service import (
    AlreadyInWatchlistError,
    add_to_watchlist,
)


@pytest.fixture
def app():
    app = create_app(config={
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def sample_user(app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def sample_film(app):
    with app.app_context():
        film = Film(title="Paddington 2", year=2017, genre="Comedy")
        db.session.add(film)
        db.session.commit()
        return film.id


def test_add_to_watchlist_creates_entry(app, sample_user, sample_film):
    with app.app_context():
        entry = add_to_watchlist(user_id=sample_user, film_id=sample_film)

        assert entry.user_id == sample_user
        assert entry.film_id == sample_film
        assert WatchlistEntry.query.count() == 1


def test_add_to_watchlist_duplicate_raises(app, sample_user, sample_film):
    with app.app_context():
        add_to_watchlist(user_id=sample_user, film_id=sample_film)

        with pytest.raises(AlreadyInWatchlistError):
            add_to_watchlist(user_id=sample_user, film_id=sample_film)

        assert WatchlistEntry.query.count() == 1


def test_add_to_watchlist_nonexistent_film_raises(app, sample_user):
    """
    Adding a film_id that doesn't exist in the database should raise
    FilmNotFoundError, not a database integrity error.
    """
    with app.app_context():
        fake_film_id = "00000000-0000-0000-0000-000000000000"

        with pytest.raises(FilmNotFoundError):
            add_to_watchlist(user_id=sample_user, film_id=fake_film_id)
