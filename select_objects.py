import os
import shutil
import random
import open3d as o3d


def visualize_pcd(pcd_path):
    '''
    Visualize a point cloud file
    '''
    pcd = o3d.io.read_point_cloud(pcd_path)
    
    def close_window(vis):
        print("Enter key pressed. Closing window.")
        vis.close()
        return False

    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window(window_name=os.path.basename(pcd_path))
    vis.add_geometry(pcd)
    
  
    vis.register_key_callback(257, close_window)
    
    
    vis.run()
    vis.destroy_window()

def select_objects(category, output_path, max_objects=1000):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    category_source_path = os.path.join('extracted_categories', category)
    if not os.path.exists(category_source_path):
        print(f"Category {category} does not exist.")
        return
    
    category_destination_path = os.path.join(output_path, category)
    if not os.path.exists(category_destination_path):
        os.makedirs(category_destination_path)

    visited_files = set([f for f in os.listdir(category_destination_path) if f.endswith('.pcd')])

    visualize_pcd_folder_randomly(category_source_path, category_destination_path, max_objects, visited_files)
    


def visualize_pcd_folder_randomly(folder_path, output_path,  max_objects=1000, visited_files=None):
    # Get list of .pcd files in the folder
    pcd_files = [f for f in os.listdir(folder_path) if f.endswith('.pcd')]
    random.shuffle(pcd_files)
    
    if not visited_files:
        visited_files = set()

    while len(visited_files) < max_objects:
        file_name = pcd_files[random.randint(0, len(pcd_files) - 1)]
        if file_name in visited_files:
            continue
        
        visited_files.add(file_name)
        file_path = os.path.join(folder_path, file_name)
        
        # Load and visualize the PCD file
        visualize_pcd(file_path)
        
        # Prompt user for input
        user_input = input(f"File {file_name} viewed. Press 'y' to accept or 'n' to skip or 'q' to quit: ").strip().lower()
        
        if user_input == 'y':
            shutil.copy(os.path.join(folder_path, file_name), output_path)
        elif user_input == 'q':
            print("Quitting the program.")
            break
        else:
            print("Skipping to next file.")
        print(f'Number of files visited: {len(visited_files)}')


if __name__ == '__main__':
    output_path = 'dataset'
    category = 'Pedestrian'

    select_objects(category, output_path, max_objects=1000)
