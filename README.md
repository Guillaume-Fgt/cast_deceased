Search a movie name, select between 10 results and see how many actors of the cast are still alived.

* Webapp: Streamlit
* Data: Cinemagoer
* Optimisation: use ThreadPoolExecutor to make request concurrently 

limitations:
by default, I limited the number of actors to 20. You can change the value in webapp.py

![Animation](https://user-images.githubusercontent.com/66461774/157872863-db265110-2d97-4c00-9066-8f0eedc881fe.gif)

# How to use it:

clone the repo:
```
git clone https://github.com/Guillaume-Fgt/cast_deceased.git
```
Navigate to the clone directory and use [uv] to run the main file:
```
uv run main.py
```

