# This script is used to split the objects in the dataset to categories

import os
import shutil
import json
import random

class Nuscenes_Objects:
    
    def __init__(self, dataset_path, output_path = None):
        self.dataset_path = dataset_path
        self.output_path = output_path
        self.general_categories_id_dict = {
            1: "animal",
            2: "human.pedestrian.personal_mobility",
            3: "human.pedestrian.stroller",
            4: "human.pedestrian.wheelchair",
            5: "movable_object.debris",
            6: "movable_object.pushable_pullable",
            7: "static_object.bicycle_rack",
            8: "vehicle.emergency.ambulance",
            9: "vehicle.emergency.police",
            10: "movable_object.barrier",
            11: "vehicle.bicycle",
            12: "vehicle.bus.bendy",
            13: "vehicle.bus.rigid",
            14: "vehicle.car",
            15: "vehicle.construction",
            16: "vehicle.motorcycle",
            17: "human.pedestrian.adult",
            18: "human.pedestrian.child",
            19: "human.pedestrian.construction_worker",
            20: "human.pedestrian.police_officer",
            21: "movable_object.trafficcone",
            22: "vehicle.trailer",
            23: "vehicle.truck"
        }
        self.extracted_categories_dict = {
            'Pedestrian': [17, 18, 19, 20],
            'Bicycle': [11],
            'Bus': [12, 13],
            'Car': [14],
            'Motorcycle': [16],
            'Truck': [23],
            'Wheelchair': [4]
        }

        self.json_path = 'formatted_nuscenes.json'

    def get_category_filenames(self, category, max_objects=None):
        '''
        Get the filenames of the objects in a specific category
        '''
        filenames = []
        category_ids = self.extracted_categories_dict[category]

        for category_id in category_ids:
            obj_ids = self.get_obj_ids_by_type(self.general_categories_id_dict[category_id])
            random.shuffle(obj_ids)  # Shuffle the list of obj_ids
            for obj_id in obj_ids:
                filenames.append(obj_id)
                if max_objects is not None and len(filenames) == max_objects:
                    return filenames

        return filenames

    def get_obj_ids_by_type(self, obj_type):
        '''
        Get the object ids of a specific type
        '''
        obj_ids = []
        with open(self.json_path, 'r') as file:
            data = file.read()

            # Add commas between JSON objects
            data = data.replace('}{', '},{')
        

            
            # Parse the JSON data
            try:
                json_data = json.loads(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return []

            for obj in json_data:
                if obj['Type'] == obj_type:
                    obj_ids.append(f"{obj['Obj_id']:06d}.pcd")
        return obj_ids
    
    def extract_data(self, category, max_objects=None):
        '''
        Extract the objects in a specific category
        '''
        category_path = os.path.join(self.output_path, category)
        if os.path.exists(category_path):
            shutil.rmtree(category_path)
            
        os.makedirs(category_path)
        
        filenames = self.get_category_filenames(category, max_objects)
        if not filenames:
            print(f"No objects found in the category: {category}")
            return
        for filename in filenames:
            shutil.copy(os.path.join(self.dataset_path, filename), os.path.join(category_path, filename))

    
if __name__ == '__main__':
    dataset_path = '/mnt/c/Users/hussa/Downloads/extracted_objects/extracted_objects'
    output_path = 'extracted_categories'

    nuscenes_objects = Nuscenes_Objects(dataset_path, output_path)

    for category in nuscenes_objects.extracted_categories_dict.keys():
        nuscenes_objects.extract_data(category, max_objects=2500)





