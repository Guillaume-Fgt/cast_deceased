import streamlit as st
import concurrent.futures
from cast_deceased.utils import (
    connect,
    search_movie,
    get_movie,
    actor_details,
    set_title,
)
import itertools


def main() -> None:
    LIMIT_ACTORS = 20
    st.header("Are they dead?")
    st.sidebar.header("Tools")
    movie_search = st.sidebar.text_input("Search movie")

    ia_connection = connect()
    movie_list = search_movie(ia_connection, movie_search, 10)
    movie_dict = {set_title(movie): movie.movieID for movie in movie_list}

    movie_selected = st.sidebar.radio(
        label="Select movie", options=[""] + list(movie_dict.keys())
    )

    try:
        movie_id = movie_dict[movie_selected]
    except KeyError:
        st.info("Enter a valid movie title")
    else:
        movie_details = get_movie(ia_connection, movie_id)
        alive = 0

        try:
            cast_list = movie_details["cast"][:LIMIT_ACTORS]
        except KeyError:
            cast_list = []
            st.info("No cast avalaible for this movie")

        header = st.container()
        with header:
            h1, h2 = st.columns(2)
            try:
                h1.image(movie_details["full-size cover url"], use_column_width=True)
            except KeyError:
                h1.text("No poster")
            h2.markdown(f'Year: {movie_details["year"]}')
            try:
                for director in movie_details["director"]:
                    h2.markdown(
                        f"Director: {director}, {actor_details(ia_connection,director)['death_date']}"
                    )
            except KeyError:
                h2.markdown("No director found")
            h2.metric(
                label=f"Total actor (limited to {LIMIT_ACTORS})", value=len(cast_list)
            )

        # MultiThreading. Using map instead submit to keep actor order.
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(
                actor_details, itertools.repeat(ia_connection), cast_list
            )

        list_avatar = []
        list_death = []
        for result in results:
            list_avatar.append(result["avatar"])
            list_death.append(result["death_date"])

        st.image(list_avatar, width=67, caption=cast_list)

        cast = st.container()
        with cast:
            col1, col2 = st.columns(2)

            col1.subheader("Name")
            col2.subheader("Death date")

            # actor names
            [col1.markdown(actor) for actor in cast_list]

            for date in list_death:
                if date == "Alive":
                    alive += 1
                    col2.markdown(date)
                else:
                    col2.markdown(f":skull_and_crossbones: {date}")

        with header:
            h2.metric(label="Alive", value=alive)
            h2.metric(label="Deceased", value=len(cast_list) - alive)


if __name__ == "__name__":
    main()
