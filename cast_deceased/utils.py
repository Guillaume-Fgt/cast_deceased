from imdb import Cinemagoer, IMDbBase, Movie, Person

"""
Functions used in the backend to search movie and actors infos
"""


def connect() -> IMDbBase:
    # create an instance of an imdb object
    return Cinemagoer()


def search_movie(
    connection: IMDbBase, movie: str, nbr_result: int
) -> list[Movie.Movie]:
    # search list of movies corresponding to a title
    return connection.search_movie(movie, results=nbr_result)


def get_movie(connection: IMDbBase, movie_id: str) -> Movie.Movie:
    # search movie details corresponding to a movie ID
    return connection.get_movie(movie_id, info="main")


def actor_details(connection: IMDbBase, actor: Person.Person) -> dict[str, str]:
    """return death date and avatar for a given actor ID"""
    actor_info = connection.get_person(actor.personID, info="biography")
    death_date = actor_info.get("death date")
    if not death_date:
        death_date = "Alive"
    avatar = actor_info.get("headshot")
    if not avatar:
        avatar = "ressources/avatar.jpg"
    return {"death_date": death_date, "avatar": avatar}


def set_title(movie: Movie.Movie) -> str:
    """generate a movie title handling possible missing year key"""
    try:
        movie_title = str(movie) + " " + str(movie["year"])
    except KeyError:
        movie_title = str(movie)
    return movie_title
