import sys
from streamlit import cli as stcli
import streamlit as st
from cast_deceased import webapp


if __name__ == "__main__":
    if st._is_running_with_streamlit:
        webapp.main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
