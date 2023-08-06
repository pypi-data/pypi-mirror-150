"""
This would contain all the functionality from google cloud that has to do with analysing an image to get
metadata
"""
import os

from Config.settings import BASE_DIR, value_serp_api_key, ocr_space_api_key, tldr_key
from google.cloud import vision

## Set google application credentials
google_service_key_path = os.path.join(BASE_DIR, 'general_input', 'service_keys', 'bloverse-image-staging-c4559b844a06.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=google_service_key_path

def generate_bbox_from_google_vertices(image_width, image_length, vertices):

    x_list = []
    y_list = []
    for vert in vertices:
        x_perc = vert[0]
        y_perc = vert[1]
        x_axis = int(x_perc*image_width)
        y_axis = int(y_perc*image_length)
        x_list.append(x_axis)
        y_list.append(y_axis)

    x0 = min(x_list)
    y0 = min(y_list)
    x1 = max(x_list)
    y1 = max(y_list)
    object_bbox = [x0,y0,x1,y1]
    
    obj_width = int(x1-x0)
    obj_height = int(y1-y0)
    obj_area = int(obj_width*obj_height)
    img_area = int(image_width*image_length)
    obj_perc = round(obj_area/img_area,2)
    
    return object_bbox, obj_perc

def get_image_objects_from_google(path, image_width, image_length):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    # Generate the object dict
    image_object_dict = {}
    count = 1

    for object_ in objects:
        vertices = [] # first index is x and the second is y
        for vertex in object_.bounding_poly.normalized_vertices:
            vertices.append([vertex.x, vertex.y])
            
        object_bbox, obj_perc = generate_bbox_from_google_vertices(image_width, image_length, vertices)
        
        object_dict = {
            'type' : object_.name,
            'confidence' : object_.score,
            'object_bbox' : object_bbox,
            'obj_perc' : obj_perc
        }
        object_name = 'object_%s' % count
        image_object_dict.update({object_name:object_dict})
        count += 1
    
    return image_object_dict