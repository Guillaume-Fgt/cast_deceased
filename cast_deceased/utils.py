from imdb import Cinemagoer
import streamlit as st

"""
Functions used in the backend to search movie and actors infos
"""


def connect():
    # create an instance of an imdb object
    return Cinemagoer()


@st.cache
def search_movie(movie, nbr_result: int):
    # search list of movies corresponding to a title
    ia = connect()
    list = ia.search_movie(movie, results=nbr_result)
    return list


@st.cache
def get_movie(movie):
    # search movie details corresponding to a movie ID
    ia = connect()
    list = ia.get_movie(movie, info="main")
    return list


def actor_details(actor):
    # return death date and avatar for a given actor ID
    ia = connect()
    actor_info = ia.get_person(actor.personID, info="biography")
    # check if death date exists
    try:
        death_date = actor_info["death date"]
    except:
        death_date = "Alive"
    # check if avatar exists
    try:
        avatar = actor_info["headshot"]
    except:
        avatar = "ressources/avatar.jpg"
    return {"death_date": death_date, "avatar": avatar}
