import matplotlib.pyplot as plt, geopandas as gpd
from sklearn.preprocessing import MinMaxScaler

def plot_points_shape_file(shape_file, list_values, list_longitude, list_latitude, title):
    scaler = MinMaxScaler(feature_range=(50,1000))
    list_final = scaler.fit_transform([[i] for i in (list_values)])
    gdf = gpd.read_file(shape_file)
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.axis('off')
    for i in range(len(list_values)):
        plt.scatter(x=[list_longitude[i]], y=[list_latitude[i]], s=list_final[i])
    plt.title(title)
    plt.tight_layout()
    gdf.plot(facecolor="none",ax=ax, legend=True, linewidth=1, edgecolor='black')