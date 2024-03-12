import dash
from dash import dcc
from dash import html
from dash import callback
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
from app.collect_images import umap_images
from app.umap_plot import umap_plotting
ui=umap_images()
from umap import UMAP
from sklearn.preprocessing import StandardScaler


# Initialize the Dash app
app = dash.Dash(__name__)


return_images = ui.collect_unsplash_images("textures")
for index, image in enumerate(return_images, start=1):
    print(f"{index}: {image}")

n_neighbors = 15
min_dist = 0.3

up=umap_plotting(return_images)

inp = input("Choose 1 for colour palettes or 2 for imagenet: ")
if inp == "1":
    colour_palettes = ui.get_colour_palettes(return_images)
    print(colour_palettes)
    up.plot_umap('colour palettes', colour_palettes, n_neighbors, min_dist)
    
elif inp == "2":
    imagenet_features = up.get_imagenet_features(return_images)
    up.plot_umap('imagenet', imagenet_features, n_neighbors, min_dist)    
else:
    print("You must choose between 1 or 2")

X_standard = StandardScaler().fit_transform(colour_palettes)

# Apply UMAP
# Note: You might need to tweak the parameters depending on your specific dataset
umap_3d = UMAP(n_components=3, random_state=42, n_neighbors=10, min_dist=0.1)
embedding_3d = umap_3d.fit_transform(X_standard)

hover_texts = [format(url) for url in return_images]
print(hover_texts)
# Assuming 'embedding_3d' is your UMAP results, 'color_palettes' are your colors, and 'image_urls' are your URLs
fig = go.Figure(data=[go.Scatter3d(
    x=embedding_3d[:, 0],
    y=embedding_3d[:, 1],
    z=embedding_3d[:, 2],
    mode='markers',
    marker=dict(
        size=5,
        color=[palette[0] for palette in colour_palettes],  # Use the first color in the palette for simplicity
        opacity=0.8,
    ),
    text=hover_texts,  # Use image URLs in an A tag as hover text
    hoverinfo='text'
)])

fig.update_layout(
    width=1000,  # Width of the figure in pixels
    height=1000,  # Height of the figure in pixels
    title_text='3D UMAP visualization of image color palettes',  # Optional: adds a title
    scene=dict(  # Adjusting the 3D scene
        xaxis_title='UMAP 1',  # Optional: adds a title to the X-axis
        yaxis_title='UMAP 2',  # Optional: adds a title to the Y-axis
        zaxis_title='UMAP 3'   # Optional: adds a title to the Z-axis
    )
)


# Define the layout of the app

app.layout = html.Div([
    # Wrapper div with flex display
    html.Div([
        # Graph component
        dcc.Graph(id='umap-3d-plot', figure=fig, style={'flex': '70%'}),  # Adjust the flex value as needed
        
        # Side panel for image and other info
        html.Div(id='side-panel', children=[
            html.Img(src='https://images.unsplash.com/photo-1583407723467-9b2d22504831?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NzI1NzB8MHwxfHNlYXJjaHwxM3x8dGV4dHVyZXN8ZW58MHx8fHwxNzEwMTU0NzkwfDA&ixlib=rb-4.0.3&q=80&w=400', id='image-display', style={'maxWidth': '100%', 'maxHeight': '100%'}),
            # Add other components as needed
        ], style={'flex': '30%', 'maxWidth': '30%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ], style={'display': 'flex', 'flexDirection': 'row'})  # This div uses flex display to arrange children side by side
], style={'width': '100%'}) 

@callback(
    #Output('image-links', 'children'),
    Output('image-display', 'src'),
    [Input('umap-3d-plot', 'clickData')]
)
def display_click_data(clickData):
    if clickData is None or 'points' not in clickData or len(clickData['points']) == 0:
        # No point clicked yet, could return a placeholder or keep the image source empty
        image_url=""
         
    else:
        # Assuming 'points' contains URLs in the 'hovertext', update this as per your data structure
        image_url = clickData['points'][0]['text']

    return image_url    

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)