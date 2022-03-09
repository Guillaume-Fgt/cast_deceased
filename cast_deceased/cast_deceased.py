from imdb import Cinemagoer
import streamlit as st
import concurrent.futures


st.header("Are they dead?")

ia = Cinemagoer()

movie_search = st.sidebar.text_input("Movie title")
movie = ia.search_movie(movie_search)

alive = 0


def actor_details(actor):
    actor_info = ia.get_person(actor.personID, info="biography")
    try:
        return f':skull_and_crossbones: {actor_info["death date"]}'
    except:
        return "Alive"


try:
    # movie found
    movie_id = movie[0].movieID
except:
    # movie not found
    st.info("Enter a valid movie title")
else:
    # if try ok
    movie_details = ia.get_movie(movie_id, info="main")
    cast_list = movie_details["cast"]

    header = st.container()
    with header:
        h1, h2 = st.columns(2)
        h1.image(movie_details["full-size cover url"], use_column_width=True)
        h2.markdown(f'Year: {movie_details["year"]}')
        try:
            for director in movie_details["director"]:
                h2.markdown(f"Director: {director}, {actor_details(director)}")
        except:
            h2.markdown("No director found")
        h2.metric(label="Total actor", value=len(cast_list))

    cast = st.container()
    with cast:
        col1, col2 = st.columns(2)
        col1.subheader("Name")
        col2.subheader("Death date")

        # actor names
        [col1.markdown(actor) for actor in movie_details["cast"]]

        # MultiThreading. Using map instead submit to keep actor order.
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(actor_details, cast_list)

            for result in results:
                col2.markdown(result)
                if result == "Alive":
                    alive += 1
    with header:
        h2.metric(label="Alive", value=alive)
        h2.metric(label="Deceased", value=len(cast_list) - alive)
# for actor in movie_details["cast"]:
#     print(f"processing actor n°{list_num}")
#     actor_info = ia.get_person(actor.personID, info="biography")
#     try:
#         death_date.append(int(actor_info["death date"][:4]))
#         dead += 1
#     except:
#         alive += 1
#     list_num += 1
# death_date.sort()
# print(dead, alive, len(death_date), death_date)

# # print(movie_details['cast'])
# actor = ia.get_person('0000008', info='biography')
# print(actor.keys())
