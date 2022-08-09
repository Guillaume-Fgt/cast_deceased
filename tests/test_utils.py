from cast_deceased.utils import (
    IMDbBase,
    connect,
    search_movie,
    get_movie,
    actor_details,
)
import pytest


@pytest.fixture
def create_connection() -> IMDbBase:
    return connect()


def test_connect(create_connection) -> None:
    assert isinstance(create_connection, IMDbBase)


def test_search_movie(create_connection) -> None:
    search = search_movie(create_connection, "Goodfellas", 10)
    assert len(search) == 10


def test_get_movie(create_connection) -> None:
    movie_detail = get_movie(create_connection, "0099685")
    assert movie_detail["title"] == "Goodfellas"


def test_actor_details(create_connection) -> None:
    movie_detail = get_movie(create_connection, "0099685")
    cast = movie_detail["cast"][0]
    actor = actor_details(create_connection, cast)
    assert len(actor) == 2
