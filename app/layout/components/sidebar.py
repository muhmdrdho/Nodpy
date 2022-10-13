from index_lib import *


with st.sidebar:
    selected = option_menu("Main Menu", ["Data Field","Explore"],
                                        icons=["data", "compass"],
                                        menu_icon="cast",
                                        default_index=0
                            )