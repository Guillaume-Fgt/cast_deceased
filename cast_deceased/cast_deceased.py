from imdb import Cinemagoer
import streamlit as st
import concurrent.futures

LIMIT_ACTORS = 20
st.header("Are they dead?")

ia = Cinemagoer()

st.sidebar.header("Search your movie")
movie_search = st.sidebar.text_input("Search movie")
movie_list = ia.search_movie(movie_search, results=5)
if movie_list:
    movie_list.insert(0, "")  # we want empty value in selectbox to not trigger search
    movie_selected = st.sidebar.radio("select movie", movie_list)
    if movie_selected:
        movie = ia.search_movie(str(movie_selected))
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
    return {"death_date": death_date, "avatar": avatar}


try:
    # movie found
    movie_id = movie[0].movieID
except:
    # movie not found
    st.info("Enter a valid movie title")
else:
    # if try ok
    movie_details = ia.get_movie(movie_id, info="main")
    cast_list = movie_details["cast"][:LIMIT_ACTORS]

    header = st.container()
    with header:
        h1, h2 = st.columns(2)
        h1.image(movie_details["full-size cover url"], use_column_width=True)
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
