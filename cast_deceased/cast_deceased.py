from imdb import Cinemagoer
import streamlit as st
import concurrent.futures


st.header("Are they dead?")

ia = Cinemagoer()

movie_search = st.sidebar.text_input("Movie title")
movie = ia.search_movie(movie_search)

alive = 0


def actor_details(actor):
    # return death date and avatar for a given actor ID
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
    return [f":skull_and_crossbones: {death_date}", avatar]


try:
    # movie found
    movie_id = movie[0].movieID
except:
    # movie not found
    st.info("Enter a valid movie title")
else:
    # if try ok
    movie_details = ia.get_movie(movie_id, info="main")
    cast_list = movie_details["cast"][:20]

    header = st.container()
    with header:
        h1, h2 = st.columns(2)
        h1.image(movie_details["full-size cover url"], use_column_width=True)
        h2.markdown(f'Year: {movie_details["year"]}')
        try:
            for director in movie_details["director"]:
                h2.markdown(f"Director: {director}, {actor_details(director)[0]}")
        except:
            h2.markdown("No director found")
        h2.metric(label="Total actor (limited to 20)", value=len(cast_list))

    # MultiThreading. Using map instead submit to keep actor order.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(actor_details, cast_list)

        list_avatar = []
        list_death = []
        for result in results:
            list_avatar.append(result[1])
            list_death.append(result[0])

        st.image(list_avatar, width=67, caption=cast_list)

    cast = st.container()
    with cast:
        col1, col2 = st.columns(2)

        col1.subheader("Name")
        col2.subheader("Death date")

        # actor names
        [col1.markdown(actor) for actor in cast_list]

        for date in list_death:
            col2.markdown(date)
            if date == "Alive":
                alive += 1

    with header:
        h2.metric(label="Alive", value=alive)
        h2.metric(label="Deceased", value=len(cast_list) - alive)
