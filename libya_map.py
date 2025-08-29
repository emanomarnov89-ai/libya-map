import geopandas as gpd
import folium

shapefile_path = r"C:\Users\user\Downloads\lby_adm_unosat_lbsc_20180507_SHP\lby_adm_unosat_lbsc_20180507_shp\lby_admbnda_adm2_unosat_lbsc_20180507.shp"
gdf = gpd.read_file(shapefile_path)

# الحل الأفضل: حذف أعمدة التواريخ قبل العرض
gdf = gdf.drop(columns=[col for col in ['date', 'validOn', 'validTo'] if col in gdf.columns])

# البديل: تحويل أي تاريخ لسلسلة نصية
for col in gdf.columns:
    if gdf[col].dtype.name.startswith('datetime'):
        gdf[col] = gdf[col].astype(str)

m = folium.Map(location=[26.3, 17.2], zoom_start=6, control_scale=True)

folium.GeoJson(
    gdf,
    style_function=lambda feature: {
        'fillColor': '#%06x' % (hash(feature['properties']['ADM2_EN']) & 0xFFFFFF),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7,
    },
    tooltip=folium.GeoJsonTooltip(fields=['ADM2_EN'], aliases=['البلدية:'])
).add_to(m)

m.save("libya_map.html")
print("تم حفظ الخريطة باسم libya_map.html")
