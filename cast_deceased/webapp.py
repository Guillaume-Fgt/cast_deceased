import streamlit as st
import concurrent.futures
from cast_deceased.utils import search_movie, get_movie, actor_details


def main():
    LIMIT_ACTORS = 20
    st.header("Are they dead?")

    st.sidebar.header("Tools")
    movie_search = st.sidebar.text_input("Search movie")
    movie_list = search_movie(movie_search, 10)
    movie_ID = []
    movie_title = []
    for movie in movie_list:
        movie_ID.append(movie.movieID)
        try:
            movie_title.append(str(movie) + " " + str(movie["year"]))
        except:
            movie_title.append(str(movie))
    movie_selected = st.sidebar.radio("Select movie", [""] + movie_title)
    for index, movie in enumerate(movie_title):
        if movie == movie_selected:
            movie_id = str(movie_ID[index])

    alive = 0

    try:
        movie_details = get_movie(movie_id)
    except:
        # movie not found
        st.info("Enter a valid movie title")
    else:
        # if try ok

        cast_list = movie_details["cast"][:LIMIT_ACTORS]

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
                        f"Director: {director}, {actor_details(director)['death_date']}"
                    )
            except:
                h2.markdown("No director found")
            h2.metric(
                label=f"Total actor (limited to {LIMIT_ACTORS})", value=len(cast_list)
            )

        # MultiThreading. Using map instead submit to keep actor order.
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(actor_details, cast_list)

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
