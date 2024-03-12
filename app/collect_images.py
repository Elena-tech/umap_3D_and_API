import cv2
import os 
import requests
from skimage import io
from sklearn.cluster import KMeans
import numpy as np
from skimage import color
from dotenv import load_dotenv


class umap_images:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('CLIENT_ID') #getting a key and printing it 
        self.api_url = os.getenv('API_URL') #getting a key and printing it 
        
        self.images=[]
        print(self.client_id)
        print(self.api_url)

    def collect_unsplash_images(self,query, max_pages=20):
        images = []
        page = 1

        while page < max_pages:
            params = {
                "query": query,
                "client_id": self.client_id,
                "per_page": 30,  
                "page": page
            }
            response = requests.get(self.api_url, params=params)
            if response.status_code == 200:
                data = response.json()['results']
                if not data:
                    break  # No more images available
                for item in data:
                    images.append(item['urls']['small']) #so we dont need to resize it on the future 

            else:
                print(f"Failed to fetch data from Unsplash: HTTP {response.status_code}")
                break
            page += 1
        
        print(f'Finished collecting {len(images)} images.')
        return images

    def resize_image(self,image):
        height, width = image.shape[:2]
        max_height = 200
        max_width = 200

        # only shrink if img is bigger than required
        if max_height < height or max_width < width:
            # get scaling factor
            scaling_factor = max_height / float(height)
            if max_width/float(width) < scaling_factor:
                scaling_factor = max_width / float(width)
            # resize image
            resized_image = cv2.resize(image, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

        return resized_image

    def get_colour_palettes(self,image_data):
        colour_palettes = []

        for image in image_data:
            image = io.imread(image)
            image = self.resize_image(image)
            image = image.reshape((image.shape[1]*image.shape[0],3))

            kmeans = KMeans(n_clusters=5).fit(image)
            labels = kmeans.labels_
            labels=list(labels)
            centroid = kmeans.cluster_centers_

            percent = []
            for i in range(len(centroid)):
                j = labels.count(i)
                j = j/(len(labels))
                percent.append(j)

            rgb = np.array(centroid/255)

            percent_idx = np.array(percent).argsort()
            rgb_sorted = rgb[percent_idx[::-1]]

            colour_palettes.append(rgb_sorted)

        lab = color.rgb2lab(colour_palettes)
        X = [lab_palette.flatten() for lab_palette in lab]

        return X
