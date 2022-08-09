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
    list = connection.search_movie(movie, results=nbr_result)
    return list


def get_movie(connection: IMDbBase, movie) -> Movie.Movie:
    # search movie details corresponding to a movie ID
    list = connection.get_movie(movie, info="main")
    return list


def actor_details(connection: IMDbBase, actor: Person.Person) -> dict[str, str]:
    # return death date and avatar for a given actor ID
    actor_info = connection.get_person(actor.personID, info="biography")
    # check if death date exists
    try:
        death_date = actor_info["death date"]
    except KeyError:
        death_date = "Alive"
    # check if avatar exists
    try:
        avatar = actor_info["headshot"]
    except KeyError:
        avatar = "ressources/avatar.jpg"
    return {"death_date": death_date, "avatar": avatar}


def set_title(movie: Movie.Movie) -> str:
    """generate a movie title handling possible missing year key"""
    try:
        movie_title = str(movie) + " " + str(movie["year"])
    except KeyError:
        movie_title = str(movie)
    return movie_title
