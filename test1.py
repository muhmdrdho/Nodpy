
from streamlit_folium import re
from index_lib import *

st.set_page_config(page_title="Nodpy", layout="wide", initial_sidebar_state="auto")
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
#Sidebar
st.sidebar.image('app/assets/logo/Nodpy2.png')
with st.sidebar:
    selected = option_menu("Main Menu",["Preacquisition", "Interpretation", "About"],
                            icons=["file","compass","megaphone"],
                            menu_icon="cast",
                            default_index=0
                            )

df_map = pd.read_csv("app/assets/data/Geology+Jambi4.csv")
df_map1 = df_map[["SYMBOLS","IDX_FORMATION"]]
state_geo = "app/assets/data/Geology+Jambi.geojson"
geojson = gpd.read_file(state_geo)
geojson_states = list(geojson.SYMBOLS.values)
final_df = geojson.merge(df_map, on="SYMBOLS")

    
uploader = st.sidebar.file_uploader('Choose your file')

if selected == "Preacquisition":
    
    

    #Preacquisition Title
    pre_title = st.title("Preacquisition")

    #Main part of preacquisition map
    pre_map = folium.Map(tiles='StamenTerrain',location=[-1.609972, 103.607254], zoom_start=6)
    
    #base tile map
    Esri_Satellite = folium.TileLayer(
                                                        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                                                        attr = 'Esri',
                                                        name = 'Esri Satellite',
                                                        overlay = True,
                                                        control = True
                                                        ).add_to(pre_map)
    Google_Satellite_Hybrid =  folium.TileLayer(
                                                        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
                                                        attr = 'Google',
                                                        name = 'Google Satellite',
                                                        overlay = True,
                                                        control = True
                                                         ).add_to(pre_map)
    Google_Terrain = folium.TileLayer(
                                                        tiles = 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
                                                        attr = 'Google',
                                                        name = 'Google Terrain',
                                                        overlay = True,
                                                        control = True
                                                        ).add_to(pre_map)
    Google_Satellite = folium.TileLayer(
                                                        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                                                        attr = 'Google',
                                                        name = 'Google Satellite',
                                                        overlay = True,
                                                        control = True
                                                        ).add_to(pre_map)
    Google_Maps = folium.TileLayer(
                                                        tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                                                        attr = 'Google',
                                                        name = 'Google Maps',
                                                        overlay = True,
                                                        control = True
                                                        ).add_to(pre_map)
    #Layer control
    folium.LayerControl().add_to(pre_map)
    
    #Fullscreeen
    plugins.Fullscreen().add_to(pre_map)

    #Locate Control
    plugins.LocateControl().add_to(pre_map)
     #Locate Control
            
            
            #Cursor Postion
    fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(pre_map)
            
            #Add the draw 
    plugins.Draw(export=True, filename='data.geojson', position='topleft', draw_options=None, edit_options=None).add_to(pre_map)
            
            #Measure Control
    plugins.MeasureControl(position='topright', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(pre_map)

    upload_pre = st.file_uploader("choose your file")
    if upload_pre is not None :
        data_pre = pd.read_csv(upload_pre)
        coordinate_data = data_pre
        coordinate_data = coordinate_data.dropna(subset=['Latitude'])
        coordinate_data = coordinate_data.dropna(subset=['Longitude'])
        for i in range(len(coordinate_data)):
            folium.Marker(location=[coordinate_data.iloc[i]['Latitude'], coordinate_data.iloc[i]['Longitude']]).add_to(pre_map)
    
    col0, col1 = st.columns(2)
    
    with col0:
        folium_static(pre_map)

    with col1:
        Main_Geology = folium.Map(tiles='StamenTerrain',location=[-1.609972, 103.607254], zoom_start=6)
        Geology_colormap = cm.LinearColormap(colors=['darkblue','blue','cyan','yellow','orange','red'])
        Geology_Map = folium.Choropleth(geo_data=final_df,
                                        data=final_df,
                                        columns=["IDX_FORMATION", "IDX_FORMATIONX"],
                                        key_on='feature.properties.IDX_FORMATION',
                                        fill_color='Paired',
                                        nan_fill_color='White',
                                        line_opacity=0,
                                        fill_opacity=1,
                                        ).add_to(Main_Geology)
        style_function = lambda x: {
                                                'fillColor':'#ffffff',
                                                 'color':'#000000',
                                                 'fillOpacity': 0,
                                                 'weight': 0
                                                }
        highlight_function = lambda x: {
                                                     'fillColor':'#000000',
                                                     'color':'#000000',
                                                     'fillOpacity':0,
                                                     'weight':0
                                                    } 
        hoover = folium.features.GeoJson(
                                                        data = final_df,
                                                        style_function=style_function,
                                                        control=False,
                                                        highlight_function=highlight_function,
                                                        tooltip= folium.features.GeoJsonTooltip(
                                                                fields=['NAME_x','CLASS_LITH_y'],
                                                                aliases=['FORMATION','LITOLOGY'],
                                                                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")

                                                        )
                                                    )
        Main_Geology.add_child(hoover)

        folium_static(Main_Geology)

    #Place of the map
    
            
#Interpretation page
if selected == "Interpretation":

    #title
    data_field_title = st.title("Interpretation")

    #tabs
    dash, file_view = st.tabs(["Dashboard","File View"])
    with dash:


        if uploader is not None:
            
            #Initialization data
            data = pd.read_csv(uploader)
            
            #Initialization map data
            

            
            #Main part Interpretation Map
            sample_map = folium.Map(tiles='StamenTerrain',location=[-1.609972, 103.607254], zoom_start=6)
            
            #Base tile Interpretation Map
            Esri_Satellite = folium.TileLayer(
                                                        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                                                        attr = 'Esri',
                                                        name = 'Esri Satellite',
                                                        overlay = True,
                                                        control = True
                                                        ).add_to(sample_map)
            Google_Satellite_Hybrid =  folium.TileLayer(
                                                        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
                                                        attr = 'Google',
                                                        name = 'Google Satellite',
                                                        overlay = True,
                                                        control = True
                                                         ).add_to(sample_map)
            Google_Terrain = folium.TileLayer(
                                                        tiles = 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
                                                        attr = 'Google',
                                                        name = 'Google Terrain',
                                                        overlay = True,
                                                        control = True
                                                        ).add_to(sample_map)
            Google_Satellite = folium.TileLayer(
                                                        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                                                        attr = 'Google',
                                                        name = 'Google Satellite',
                                                        overlay = True,
                                                        control = True
                                                        ).add_to(sample_map)
            Google_Maps = folium.TileLayer(
                                                        tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                                                        attr = 'Google',
                                                        name = 'Google Maps',
                                                        overlay = True,
                                                        control = True
                                                        ).add_to(sample_map)
            
            #Layer Control
            folium.LayerControl().add_to(sample_map)
            
            #Fullscreen
            plugins.Fullscreen().add_to(sample_map)
            
            #Locate Control
            plugins.LocateControl().add_to(sample_map)
            
            #Cursor Postion
            fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
            plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(sample_map)
            
            #Add the draw 
            plugins.Draw(export=True, filename='data.geojson', position='topleft', draw_options=None, edit_options=None).add_to(sample_map)
            
            #Measure Control
            plugins.MeasureControl(position='topright', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(sample_map)



            #Marker of the map
            coordinate_data = data
            coordinate_data = coordinate_data.dropna(subset=['Latitude'])
            coordinate_data = coordinate_data.dropna(subset=['Longitude'])
            for i in range(len(coordinate_data)):
                folium.Marker(location=[coordinate_data.iloc[i]['Latitude'], coordinate_data.iloc[i]['Longitude']]).add_to(sample_map)

            #Geology Map

            #Main part of geology map
            Main_Geology = folium.Map(tiles='StamenTerrain',location=[-1.609972, 103.607254], zoom_start=6)
            Geology_colormap = cm.LinearColormap(colors=['darkblue','blue','cyan','yellow','orange','red'])
            #Geology choropleth map
            Geology_Map = folium.Choropleth(geo_data=final_df,
                                        data=final_df,
                                        columns=["IDX_FORMATION", "IDX_FORMATIONX"],
                                        key_on='feature.properties.IDX_FORMATION',
                                        fill_color='Paired',
                                        nan_fill_color='White',
                                        line_opacity=0,
                                        fill_opacity=1,
                                        ).add_to(Main_Geology)

            #Pop up, tooltips of Geology Choropleth map
            style_function = lambda x: {
                                                'fillColor':'#ffffff',
                                                 'color':'#000000',
                                                 'fillOpacity': 0,
                                                 'weight': 0
                                                }
            highlight_function = lambda x: {
                                                     'fillColor':'#000000',
                                                     'color':'#000000',
                                                     'fillOpacity':0,
                                                     'weight':0
                                                    } 
            hoover = folium.features.GeoJson(
                                                        data = final_df,
                                                        style_function=style_function,
                                                        control=False,
                                                        highlight_function=highlight_function,
                                                        tooltip= folium.features.GeoJsonTooltip(
                                                                fields=['NAME_x','FORMATION_x'],
                                                                aliases=['NAME','FORMATION'],
                                                                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")

                                                        )
                                                    )
            Main_Geology.add_child(hoover)

            #Marker of geology map based on coordinate data
            for i in range(len(coordinate_data)):
                folium.Marker(location=[coordinate_data.iloc[i]['Latitude'], coordinate_data.iloc[i]['Longitude']]).add_to(Main_Geology)
    
    
            with st.expander('MapBox'):
                
                with st.container():
                    cols1, cols2 = st.columns(2)

                    with cols1:
                        folium_static(sample_map, width=600)
                    
                
                    with cols2:
                        folium_static(Main_Geology, width=600)



    #input
            filein = data  
            ncolours=12 
            colourscheme='Spectral_r' 
    #Resistivity
            rhos_min = filein['Resistivity'].min()
            rhos_max = filein['Resistivity'].max()
            

            clevels_res = np.logspace(np.log10(np.min(rhos_min)),np.log10(np.max(rhos_max)),num=ncolours)
            fig, axes_res = plt.subplots( nrows=2, sharex=False, squeeze=True, sharey=True)

            for ax in axes_res:
                x=filein['X']
                z=filein['Depth']
                rho=filein['Resistivity']
                triang = mpl.tri.Triangulation(x, z)
                mask = mpl.tri.TriAnalyzer(triang).get_flat_tri_mask()
                triang.set_mask(mask)
   
    
    #plt.tricontourf(triang,rho,levels=clevels, cmap=colourscheme)
    #cc=ax.tricontourf(triang,rho,levels=clevels, cmap=colourscheme)
                cc=ax.tricontourf(triang,rho,levels=clevels_res, norm=mpl.colors.LogNorm(vmin=rhos_min, vmax=rhos_max), cmap=colourscheme)
                ax.set_ylim(min(z)-2, max(z)+2)
                ax.set_xlim(0, max(x)+5)
                axes_res[0].set_visible(False)

            

            clabels=[]
            for c in clevels_res: 
                clabels.append('%d' % c) 
            thecbar=fig.colorbar(cc, ax=axes_res,ticks=clevels_res, orientation="horizontal")
            thecbar.ax.set_xticklabels(clabels, rotation=45)

       #Conductivity
            cond_min = filein['Cond'].min()
            cond_max = filein['Cond'].max()
            

            clevels_cond = np.logspace(np.log10(np.min(cond_min)),np.log10(np.max(cond_max)),num=ncolours)
            fig_cond, axes_cond = plt.subplots( nrows=2, sharex=False, squeeze=True, sharey=True)

            for ax in axes_cond:
                x=filein['X']
                z=filein['Depth']
                rho=filein['Cond']
                triang = mpl.tri.Triangulation(x, z)
                mask = mpl.tri.TriAnalyzer(triang).get_flat_tri_mask()
                triang.set_mask(mask)
   
    
    #plt.tricontourf(triang,rho,levels=clevels, cmap=colourscheme)
    #cc=ax.tricontourf(triang,rho,levels=clevels, cmap=colourscheme)
                cc_cond=ax.tricontourf(triang,rho,levels=clevels_cond, norm=mpl.colors.LogNorm(vmin=cond_min, vmax=cond_max), cmap=colourscheme)
                ax.set_ylim(min(z)-2, max(z)+2)
                ax.set_xlim(0, max(x)+5)
                axes_cond[0].set_visible(False)

            

            clabels=[]
            for c in clevels_cond: 
                clabels.append('%2.4f' % c) 
            thecbar=fig.colorbar(cc_cond, ax=axes_cond,ticks=clevels_cond, orientation="horizontal")
            thecbar.ax.set_xticklabels(clabels, rotation=45)

            with dash:
                cols = st.columns(2)
                with cols[0]:
                    st.markdown("""
                                    <h3>Resistivity</h3>
                    """, unsafe_allow_html=True)
                    #fig_html = mpld3.fig_to_html(fig)
                    #components.html(fig_html)

                    st.pyplot(fig)

                with cols[1]:
                    st.markdown("""
                                    <h3>Conductivity</h3>
                    """, unsafe_allow_html=True)
                    #fig_html = mpld3.fig_to_html(fig)
                    #components.html(fig_html)

                    st.pyplot(fig_cond)

            datum_file = data
            datum_file_x = datum_file["X"]
            datum_file_y = datum_file["Depth"]


            datum_fig, ax = plt.subplots()
            ax.plot(datum_file_x, datum_file_y ,"o")

            
            res_value = data
            res_value_x = res_value['X']
            res_value_y = res_value['Resistivity']

            res_value_fig, ax_res = plt.subplots()
            ax_res.plot(res_value_x, res_value_y)
            
            
            
            
    
        
        
            with file_view:
                cols = st.columns(2)
                with cols[0]:
                    st.markdown("""
                                    <h3>Datum View</h3>
                    """, unsafe_allow_html=True)
                    st.pyplot(datum_fig)
                    #fig_html = mpld3.fig_to_html(datum_fig)
                    #components.html(fig_html, height=600)
                with cols[1]:
                    

                    st.markdown("""
                                    <h3>Data</h3>
                    """, unsafe_allow_html=True)
                    data_view = AgGrid(dataframe=data, fit_columns_on_grid_load=True)
                
            
            

