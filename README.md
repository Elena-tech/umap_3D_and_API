## Installation

Before you begin, it's recommended to create a new virtual environment for this project. This helps keep dependencies required by different projects separate by creating isolated environments for them.

1. **Create a Virtual Environment:**
   
   - For **Windows**, open your command prompt and run:
     ```
     python -m venv venv
     ```
   
   - For **macOS/Linux**, open your terminal and run:
     ```
     python3 -m venv venv
     ```
   Replace `venv` with the name you want to give to your virtual environment.

2. **Activate the Virtual Environment:**
   
   - On **Windows**, execute:
     ```
     .\venv\Scripts\activate
     ```
   
   - On **macOS/Linux**, use:
     ```
     source .venv/bin/activate
     ```
   After activation, your command line should show the name of your virtual environment, indicating that it is currently active. From now on, any Python or pip commands will use the versions in the virtual environment, not the global ones.

3. **Clone the repository:**

git clone https://your-repository-url.git
cd your-repository-directory

4. **Install the required Python packages:**
Inside the activated virtual environment, install the project dependencies by running:
pip install -r requirements.txt

## Requirements

This project requires Python 3.x and the following Python libraries:

- umap-learn==0.5.3 
- opencv-python 
- scikit-image 
- seaborn
- plotly
- dash
- python-dotenv
- requests
- pillow
- tensorflow

## Usage

To run the application locally, execute the following command from the root directory of the project:

python main.py

Navigate to `http://127.0.0.1:8051/` (or the port you've configured) in your web browser to view the app.


## Project Structure

- `app.py`: Main Python script to launch the Dash app.
- `/app`: Directory containing modular components of the app, such as image collection and UMAP plotting utilities.
  - `collect_images.py`: Module for fetching images based on queries.
  - `umap_plot.py`: Module for performing UMAP dimensionality reduction and plotting.
- `requirements.txt`: File listing the project's dependencies for easy installation via pip.

### Interacting with the Application

Once the application is running, you'll see a 3D UMAP visualization of images based on your chosen criteria (e.g., textures, colors). Here's how to interact with it:

- **Explore the 3D Plot**: Use your mouse to rotate, zoom in, and zoom out of the 3D scatter plot. This will help you get different perspectives of the data clustering.
- **View Images**: Click on any dot (point) within the scatter plot to view the corresponding image. Upon clicking, the image will be displayed in a side panel or designated area within the app.
- **Navigate Through Images**: Continue clicking on different points to explore various images that are clustered together in the 3D space. This allows you to visually analyze how similar images are grouped based on the UMAP algorithm.


## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your proposed changes. For major changes, please open an issue first to discuss what you would like to change.