from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import random

world_boundary = 650.0    
grid_unit_size = 45.0   
boundary_height = 120.0    
field_of_view = 75.0      
near_clip = 0.5            
far_clip = 5000.0         
player_location = [0.0, 35.0, 0.0] 
player_rotation =5.0             
movement_velocity = 7.5            
rotation_speed = 1.0               

player_collision_radius = 25.0        

ground_Y = 0.0
localZ= -12.0  

active_projectiles = []         
projectileSize = 10.0            
projectileValocity = 20.0
bulletLifeTime = 550         

adversary_count = 5          
adversary_base_radius = 20.0
adversary_head_radius = 12.0
adversary_movement_speed = 0.5
adversaries = []                   
current_score = 0                 
remaining_lives = 5                 
missed_shots = 0                   
game_terminated = False             

viewer_height = 450.0              
viewer_angle = 135.0               
viewer_distance = 1100.0           
perspective_mode = False             
camera_tracking = False            

active_inputs = set()            
enhancement_active = False          
enhancement_rotation_speed = 1.0    
enhancement_fire_delay = 5          
last_fire_time = 0

animation_frame = 0                 

def convert_rotation_to_direction(rotation_degrees):
   
    angle_radians = math.radians(rotation_degrees)
    return [math.sin(angle_radians), 0.0, math.cos(angle_radians)]

def convertHumanWalking(rotation_degrees):
   
    angle_radians = math.radians(rotation_degrees)
    return [-math.sin(angle_radians), 0.0, math.cos(angle_radians)]


def convert_shootingDirection(rotation_degrees):
    
    if perspective_mode:
   
        angle_radians = math.radians(rotation_degrees)
        return [math.sin(angle_radians), 0.0, math.cos(angle_radians)]
    else:
        angle_radians = math.radians(rotation_degrees)
        return [-math.sin(angle_radians), 0.0, math.cos(angle_radians)]


def normalize_vector(vector):

    magnitude = math.sqrt(vector[0]*vector[0] + vector[1]*vector[1] + vector[2]*vector[2])
    if magnitude == 0:
        return [0.0, 0.0, 0.0]
    
    return [vector[0]/magnitude, vector[1]/magnitude, vector[2]/magnitude]

def calculate_distance(point_a, point_b):

    delta_x = point_a[0] - point_b[0]
    delta_y = point_a[1] - point_b[1]
    delta_z = point_a[2] - point_b[2]

    return math.sqrt(delta_x*delta_x + delta_y*delta_y + delta_z*delta_z)

def compute_angle_difference(angle_a, angle_b):
   
    difference = (angle_a - angle_b + 180.0) % 360.0 - 180.0
    return difference

def constrain_value(value, minimum, maximum):
    
    return max(minimum, min(maximum, value))

def create_rectangular_prism(width, height, depth):
  
    glPushMatrix()
    glScalef(width, height, depth)
    glutSolidCube(1.0)
    glPopMatrix()

def create_cylindrical_shape(radius, height, segment_count=24):

    glPushMatrix()
    glTranslatef(0.0, -height*0.5, 0.0)
    gluCylinder(gluNewQuadric(), radius, radius, height, segment_count, 1)
    glPopMatrix()

def create_spherical_shape(radius):
 
    gluSphere(gluNewQuadric(), radius, 24, 18)

def render_game_environment():
    global world_boundary,grid_unit_size,boundary_height
   
    floor_level = 0.0
    grid_start = -world_boundary
    grid_end = world_boundary
    grid_tiles = int((world_boundary*2)//grid_unit_size) + 1 

    for grid_x in range(grid_tiles):
        x_start = grid_start + grid_x*grid_unit_size
        x_end = min(x_start + grid_unit_size, grid_end) 
        for grid_z in range(grid_tiles):
            z_start = grid_start + grid_z*grid_unit_size
            z_end = min(z_start + grid_unit_size, grid_end)
            if ((grid_x + grid_z) % 2) == 0:
                glColor3f(0.7, 0.5, 0.95)
            else:
                glColor3f(1, 1, 1)

            glBegin(GL_QUADS)
            glVertex3f(x_start, floor_level, z_start)
            glVertex3f(x_end, floor_level, z_start)
            glVertex3f(x_end, floor_level, z_end)
            glVertex3f(x_start, floor_level, z_end)
            glEnd()

    glColor3f(0.0, 1.0, 1.0);
    wall_thickness = 8.0

    glPushMatrix()
    glTranslatef(0.0, boundary_height*0.5, world_boundary)
    create_rectangular_prism(world_boundary*2.0, boundary_height, wall_thickness)
    glPopMatrix()

    glColor3f(1.0, 0.0, 0.0);

    glPushMatrix()
    glTranslatef(0.0, boundary_height*0.5, -world_boundary)
    create_rectangular_prism(world_boundary*2.0, boundary_height, wall_thickness)
    glPopMatrix()

    glColor3f(0.0, 0.0, 1.0);

    glPushMatrix()
    glTranslatef(+world_boundary, boundary_height*0.5, 0.0)
    create_rectangular_prism(wall_thickness, boundary_height, world_boundary*2.0)
    glPopMatrix()

    glColor3f(1.0, 0.5, 0.0); 

    glPushMatrix()
    glTranslatef(-world_boundary, boundary_height*0.5, 0.0)
    create_rectangular_prism(wall_thickness, boundary_height, world_boundary*2.0)
    glPopMatrix()

def _render_ground_clamp_translate():
    global ground_Y,localZ

    feet_world_y = player_location[1] + localZ

    if feet_world_y < ground_Y:
        glTranslatef(0.0, ground_Y - feet_world_y, 0.0)

def render_player_character():
   
    glPushMatrix()
    glTranslatef(player_location[0], player_location[1], player_location[2])

   
    _render_ground_clamp_translate()

    glRotatef(-90, 1, 0, 0)

    if game_terminated:
        glRotatef(25, 0, 0, 1)   
        glTranslatef(0, 0, -25)
    else:
        glRotatef(player_rotation, 0, 0, 1)

    # First-person view
    if perspective_mode and not game_terminated:
        arm_length = 35
        glColor3f(0.85, 0.75, 0.65)  

        # Right arm
        glPushMatrix()
        glTranslatef(-18, -12, 45)  
        glRotatef(-55, 0, 1, 0)      
        glRotatef(85, 1, 0, 0)       
        gluCylinder(gluNewQuadric(), 6, 3, arm_length, 18, 18)
        glPopMatrix()

        # Left arm 
        glPushMatrix()
        glTranslatef(18, -12, 45)   
        glRotatef(-55, 0, 1, 0)      
        glRotatef(85, 1, 0, 0)       
        gluCylinder(gluNewQuadric(), 6, 3, arm_length, 18, 18)
        glPopMatrix()

        # Weapon
        gun_barrel_len = 55
        glPushMatrix()
        glColor3f(0.4, 0.4, 0.4)
        glTranslatef(0, -12, 45)    
        glRotatef(-55, 0, 1, 0)    
        glRotatef(85, 1, 0, 0)       
        gluCylinder(gluNewQuadric(), 5, 2, gun_barrel_len, 14, 14)
        glPopMatrix()

    else:
        # Torso
        glPushMatrix()
        glColor3f(0.6, 0.8, 0.5)
        if game_terminated:
            glTranslatef(0, 0, 18)
            glScalef(1.6, 3.2, 0.9)
        else:
            glTranslatef(0, 0, 65)  
            glScalef(1.1, 1.6, 2.2)
        glutSolidCube(22)
        glPopMatrix()

        # Head
        glPushMatrix()
        glColor3f(0.1, 0.1, 0.1)
        if game_terminated:
            glTranslatef(12, 18, 22)
            glRotatef(-25, 0, 0, 1)
            glScalef(1.3, 1.3, 1.3)
        else:
            glTranslatef(0, 0, 100)
        gluSphere(gluNewQuadric(), 12, 22, 22)
        glPopMatrix()

        leg_length = 45
        glColor3f(0.2, 0.4, 0.8)

        #Left leg
        glPushMatrix()
        if game_terminated:
            glTranslatef(0, -28, 12)
            glRotatef(75, 0, 1, 0)
            glRotatef(25, 1, 0, 0)
        else:
            glTranslatef(0, -18, 35)
        glRotatef(180, 1, 0, 0)
        glTranslatef(0, -6, -6)
        gluCylinder(gluNewQuadric(), 8, 0, leg_length, 22, 22)
        glPopMatrix()

        # Right leg
        glPushMatrix()
        if game_terminated:
            glTranslatef(0, 28, 12)
            glRotatef(-75, 0, 1, 0)
            glRotatef(25, 1, 0, 0)
        else:
            glTranslatef(0, 18, 35)
        glRotatef(180, 1, 0, 0)
        glTranslatef(0, 6, -6)
        gluCylinder(gluNewQuadric(), 8, 0, leg_length, 22, 22)
        glPopMatrix()

        # Arms
        arm_length = 35
        glColor3f(0.85, 0.75, 0.65)

        # Right arm
        glPushMatrix()
        if game_terminated:
            glTranslatef(0, -32, 18)
            glRotatef(92, 0, 1, 0)
            glRotatef(-50, 1, 0, 0)
        else:
            glTranslatef(0, -22, 70)
            glRotatef(92, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 8, 3, arm_length, 22, 22)
        glPopMatrix()

        # Left arm
        glPushMatrix()
        if game_terminated:
            glTranslatef(0, 32, 18)
            glRotatef(92, 0, 1, 0)
            glRotatef(50, 1, 0, 0)
        else:
            glTranslatef(0, 22, 70)
            glRotatef(92, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 8, 3, arm_length, 22, 22)
        glPopMatrix()

        # Weapon
        gun_barrel_len = 45
        glPushMatrix()
        glColor3f(0.4, 0.4, 0.4)
        if game_terminated:
            glTranslatef(18, 0, 18)
            glRotatef(92, 0, 1, 0)
            glRotatef(35, 1, 0, 0)
        else:
            glTranslatef(0, 0, 70)  
            glRotatef(92, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 8, 2, gun_barrel_len, 12, 12)
        glPopMatrix()

    glPopMatrix()

def launch_projectile():
    global last_fire_time,bulletLifeTime

    if game_terminated:
        return
    direction_vector = convert_shootingDirection(player_rotation)

    if perspective_mode:
    
        gun_offset_x = 0.0
        gun_offset_y = -10.0  
        gun_offset_z = 40.0 
    else:
    
        gun_offset_x = 0.0
        gun_offset_y = 0.0   
        gun_offset_z = 70.0 
        
    spawn_x = player_location[0] + gun_offset_x + direction_vector[0]*(gun_offset_z+50.0 )  
    spawn_y = player_location[1] + gun_offset_y
    
    spawn_z = player_location[2] + gun_offset_z + direction_vector[2]*(gun_offset_z +50.0)
    
    if perspective_mode:
        active_projectiles.append({
            "position": [spawn_x, spawn_y, spawn_z],
            "direction": [direction_vector[0], 0.0, direction_vector[2]],
            "lifetime": bulletLifeTime
        })
    else:
        active_projectiles.append({
            "position": [spawn_x, spawn_y, spawn_z],
            "direction": [direction_vector[2], 0.0, direction_vector[0]],
            "lifetime": bulletLifeTime
        })

    last_fire_time = 0

def launch_targeted_projectile(target_position):
    global bulletLifeTime

    global last_fire_time
    if game_terminated:
        return
    
    target_vector = [target_position[0]-player_location[0], 0.0, target_position[2]-player_location[2]]

    normalized_direction = normalize_vector(target_vector)

  
    if perspective_mode:
      
        gun_offset_x = 0.0
        gun_offset_y = -10.0  
        gun_offset_z = 40.0  
    else:
   
        gun_offset_x = 0.0
        gun_offset_y = 0.0    
        gun_offset_z = 65.0   

    spawn_x = player_location[0] + gun_offset_x + normalized_direction[0]*(gun_offset_z + 50.0)  
    spawn_y = player_location[1] + gun_offset_y
    spawn_z = player_location[2] + gun_offset_z + normalized_direction[2]*(gun_offset_z + 50.0)
    active_projectiles.append({
        "position": [spawn_x, spawn_y, spawn_z],
        "direction": [normalized_direction[0], 0.0, normalized_direction[2]],
        "lifetime": bulletLifeTime,
        "guided": True
    })
    last_fire_time = 0

def render_projectile(projectile_data):
    global projectileSize

    glPushMatrix()
    glTranslatef(projectile_data["position"][0], projectile_data["position"][1], projectile_data["position"][2])
    glColor3f(1.0, 0.0, 0.0)  
    create_rectangular_prism(projectileSize, projectileSize, projectileSize)
    glPopMatrix()

def spawnEnemies():
    global world_boundary
   
    angle = random.random() * 2*math.pi
    radius = random.uniform(world_boundary*0.5, world_boundary*0.85)
    x_coordinate = math.cos(angle) * radius
    z_coordinate = math.sin(angle) * radius
    return {"position": [x_coordinate, 20.0, z_coordinate], "pulse_phase": random.random()*6.28}

def render_adversary(adversary_data):

    position = adversary_data["position"]
    pulse_scale = 1.0 + 0.15*math.sin(adversary_data["pulse_phase"])  
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    glScalef(pulse_scale, pulse_scale, pulse_scale)

    glColor3f(0.85, 0.2, 0.25)  
    create_spherical_shape(adversary_base_radius)

    glColor3f(0.0, 0.0, 0.0)  # Black head
    glTranslatef(0.0, adversary_base_radius + adversary_head_radius*0.8, 0.0)
    create_spherical_shape(adversary_head_radius)

    glPopMatrix()

def setup_interface_projection():

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

def restore_3d_projection():

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

def display_text_at_position(x_coord, y_coord, text_string):

    glRasterPos2f(x_coord, y_coord)
    for character in text_string:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))

def render_game_interface():

    setup_interface_projection()
    glColor3f(1, 1, 1)  # White text
    display_text_at_position(0.02, 0.96, f"Player Life Remaining: {remaining_lives}")
    display_text_at_position(0.02, 0.93, f"Game Score: {current_score}")
    display_text_at_position(0.02, 0.90, f"Player Bullet Missed: {missed_shots}")

    if game_terminated:
        glColor3f(1, 0.4, 0.4) 
        display_text_at_position(0.32, 0.52, "GAME OVER — press R to restart")
    restore_3d_projection()

def configure_viewport():
    global field_of_view,near_clip,far_clip

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    window_width = max(1, glutGet(GLUT_WINDOW_WIDTH))
    window_height = max(1, glutGet(GLUT_WINDOW_HEIGHT))
    gluPerspective(field_of_view, window_width/window_height, near_clip, far_clip)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if perspective_mode:

        direction_vector = convert_rotation_to_direction(player_rotation)
        up_vector = [0, 1, 0]

        base_camera_height = 58.0

        if camera_tracking:

            camera_position = [
                player_location[0], 
                player_location[1] + base_camera_height, 
                player_location[2]  
            ]

            look_ahead_distance = 150.0
            look_at_position = [
                player_location[0] + direction_vector[0]*look_ahead_distance,
                camera_position[1],
                player_location[2] + direction_vector[2]*look_ahead_distance
            ]

        else:

            camera_position = [
                player_location[0], 
                player_location[1] + base_camera_height, 
                player_location[2]  
            ]
         
            look_ahead_distance = 100.0
            look_at_position = [
                player_location[0] + direction_vector[0] * look_ahead_distance,  
                camera_position[1],  
                player_location[2] + direction_vector[2] * look_ahead_distance  
            ]
        gluLookAt(
            camera_position[0], camera_position[1], camera_position[2],
            look_at_position[0], look_at_position[1], look_at_position[2],
            up_vector[0], up_vector[1], up_vector[2]
        )
    else:
        camera_x = math.sin(math.radians(viewer_angle)) * viewer_distance
        camera_z = math.cos(math.radians(viewer_angle)) * viewer_distance
        camera_position = [camera_x, viewer_height, camera_z]
        target_position = [0.0, 0.0, 0.0]
        gluLookAt(
            camera_position[0], camera_position[1], camera_position[2],
            target_position[0], target_position[1], target_position[2],
            0, 1, 0
        )


def detect_nearest_adversary_in_cone():

    best_adversary_index = -1
    closest_distance = 1e9

    for adversary_index, adversary in enumerate(adversaries):
        distance = calculate_distance(player_location, adversary["position"]) or 1.0
        direction_vector = [adversary["position"][0]-player_location[0], 0.0, adversary["position"][2]-player_location[2]]
        bearing_angle = math.degrees(math.atan2(direction_vector[0], direction_vector[2]))

        if abs(compute_angle_difference(player_rotation, bearing_angle)) < 15.0: 
            if distance < closest_distance:
                closest_distance = distance
                best_adversary_index = adversary_index
    return best_adversary_index

def execute_enhancement_system():

    global player_rotation, last_fire_time

    if game_terminated or not enhancement_active or not adversaries:
        return

    best_adversary_index = -1
    minimum_distance = 1e9
    for adversary_index, adversary in enumerate(adversaries):
        distance = calculate_distance(player_location, adversary["position"]) or 1.0
        if distance < minimum_distance:
            minimum_distance = distance
            best_adversary_index = adversary_index

    if best_adversary_index == -1:
        return

    target_adversary = adversaries[best_adversary_index]["position"]

    direction_vector = [target_adversary[0]-player_location[0], 0.0, target_adversary[2]-player_location[2]]
    target_rotation = math.degrees(math.atan2(direction_vector[0], direction_vector[2]))

    rotation_difference = compute_angle_difference(target_rotation, player_rotation)
    rotation_step = enhancement_rotation_speed * 1.8  

    if abs(rotation_difference) <= rotation_step:
        player_rotation = target_rotation
    else:
        player_rotation = (player_rotation + rotation_step if rotation_difference > 0 else player_rotation - rotation_step) % 360.0

    if abs(compute_angle_difference(target_rotation, player_rotation)) < 2.5 and last_fire_time > enhancement_fire_delay:
        launch_targeted_projectile(target_adversary)

def update_projectile_positions():
    global projectileSize,projectileValocity
  
    global active_projectiles, current_score, missed_shots,world_boundary
    surviving_projectiles = []

    for projectile in active_projectiles:

        if projectile.get("guided") and enhancement_active and adversaries:
           
            closest_adversary_index = 0
            minimum_distance = 1e9
            for adversary_index, adversary in enumerate(adversaries):
                distance = calculate_distance(projectile["position"], adversary["position"]) or 1.0
                if distance < minimum_distance:
                    minimum_distance = distance
                    closest_adversary_index = adversary_index

            target_adversary = adversaries[closest_adversary_index]["position"]
            target_vector = [target_adversary[0]-projectile["position"][0], 0.0, target_adversary[2]-projectile["position"][2]]
            normalized_target = normalize_vector(target_vector)

            steering_factor = 0.4
            projectile["direction"][0] = (1-steering_factor)*projectile["direction"][0] + steering_factor*normalized_target[0]
            projectile["direction"][2] = (1-steering_factor)*projectile["direction"][2] + steering_factor*normalized_target[2]

            normalized_direction = normalize_vector([projectile["direction"][0], 0.0, projectile["direction"][2]])
            projectile["direction"][0], projectile["direction"][2] = normalized_direction[0], normalized_direction[2]

        projectile["position"][0] += projectile["direction"][0]*projectileValocity
        projectile["position"][1] += projectile["direction"][1]*projectileValocity
        projectile["position"][2] += projectile["direction"][2]*projectileValocity
        projectile["lifetime"] -= 1

        if (abs(projectile["position"][0]) > world_boundary or
            abs(projectile["position"][2]) > world_boundary or
            projectile["lifetime"] <= 0):
            missed_shots += 1
            continue

        collision_detected = False
        for adversary_index, adversary in enumerate(adversaries):
            delta_x = projectile["position"][0] - adversary["position"][0]
            delta_z = projectile["position"][2] - adversary["position"][2]
            if math.hypot(delta_x, delta_z) < (adversary_base_radius + projectileSize*0.7):
                current_score += 2
                adversaries[adversary_index] = spawnEnemies()
                collision_detected = True
                break

        if not collision_detected:
            surviving_projectiles.append(projectile)

    active_projectiles = surviving_projectiles

def update_adversary_positions():

    for adversary in adversaries:

        direction_to_player = [player_location[0]-adversary["position"][0], 0.0, player_location[2]-adversary["position"][2]]
        normalized_direction = normalize_vector(direction_to_player)

        adversary["position"][0] += normalized_direction[0]*adversary_movement_speed
        adversary["position"][2] += normalized_direction[2]*adversary_movement_speed
        adversary["pulse_phase"] += 0.15

def check_player_collision():
    global player_collision_radius

    global remaining_lives, game_terminated
    for adversary_index, adversary in enumerate(adversaries):
        if calculate_distance(player_location, adversary["position"]) < (player_collision_radius + adversary_base_radius*0.6):
            remaining_lives -= 1
            adversaries[adversary_index] = spawnEnemies()
            if remaining_lives <= 0:
                terminate_game()
            break

def terminate_game():
    global game_terminated
    game_terminated = True

def reset_game_state():

    global current_score, remaining_lives, missed_shots, game_terminated
    global player_location, player_rotation, active_projectiles, adversaries, camera_tracking,perspective_mode

    current_score = 0
    remaining_lives = 5
    missed_shots = 0
    game_terminated = False
    perspective_mode = False
    player_location = [0.0, 35.0, 0.0]
    player_rotation = 0.0
    active_projectiles.clear()
    camera_tracking = False  
    adversaries.clear()
    for i in range(adversary_count):
        adversaries.append(spawnEnemies())


def render_scene():

    glClearColor(0.05, 0.06, 0.08, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    configure_viewport()
    render_game_environment()

    for adversary in adversaries:
        render_adversary(adversary)

    render_player_character()

    for projectile in active_projectiles:
        render_projectile(projectile)

    render_game_interface()
    glutSwapBuffers()

def enforce_ground(pos):
    global ground_Y,localZ

    feet_y = pos[1] + localZ
    if feet_y < ground_Y:
        pos[1] += (ground_Y - feet_y)

def update_game_state():
    global world_boundary,player_collision_radius

    global animation_frame, last_fire_time, missed_shots, player_location, player_rotation

    if game_terminated:
        glutPostRedisplay()
        return

    if b'w' in active_inputs:

        direction_vector = convertHumanWalking(player_rotation)

        player_location[0] += direction_vector[2] * movement_velocity 
        player_location[2] += direction_vector[0] * movement_velocity  

    if b's' in active_inputs:

        direction_vector = convertHumanWalking(player_rotation)
       
        player_location[0] -= direction_vector[2] * movement_velocity  
        player_location[2] -= direction_vector[0] * movement_velocity  
        
    if b'a' in active_inputs:

        player_rotation = (player_rotation + rotation_speed) % 360.0

    if b'd' in active_inputs:
        player_rotation = (player_rotation - rotation_speed) % 360.0

    player_location[0] = constrain_value(player_location[0], -world_boundary+player_collision_radius, world_boundary-player_collision_radius)
    player_location[2] = constrain_value(player_location[2], -world_boundary+player_collision_radius, world_boundary-player_collision_radius)

    enforce_ground(player_location)

    if enhancement_active:
        execute_enhancement_system()

    update_projectile_positions()
    update_adversary_positions()
    check_player_collision()

    if missed_shots >= 10:
        terminate_game()

    animation_frame += 1
    last_fire_time += 1
    glutPostRedisplay()

def handle_key_press(key, x, y):

    global enhancement_active, camera_tracking

    if key in (b'\x1b', b'q'):  
        glutLeaveMainLoop()
        return
    if key == b'c':
        enhancement_active = not enhancement_active
        
        if not enhancement_active:
            camera_tracking = False
    elif key == b'v':

        camera_tracking = not camera_tracking
    elif key == b'r':
        reset_game_state()
    else:
        active_inputs.add(key)

def handle_key_release(key, x, y):

    if key in active_inputs:
        active_inputs.remove(key)

def handle_special_keys(key, x, y):

    global viewer_height, viewer_angle

    if key == GLUT_KEY_UP:
        viewer_height += 10.0
    elif key == GLUT_KEY_DOWN:
        viewer_height -= 10.0
        viewer_height = constrain_value(viewer_height, 100.0, 3000.0)
    elif key == GLUT_KEY_LEFT:
        viewer_angle += 3.0
    elif key == GLUT_KEY_RIGHT:
        viewer_angle -= 3.0

def handle_mouse_input(button, state, x, y):

    global perspective_mode

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        launch_projectile()
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        perspective_mode = not perspective_mode

def initialize_game_systems():

    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    adversaries.clear()
    for i in range(adversary_count):
        adversaries.append(spawnEnemies())

def main():

    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1200, 800)
    glutCreateWindow(b"Maro Guli koro cheat")

    initialize_game_systems()

    glutDisplayFunc(render_scene)
    glutIdleFunc(update_game_state)
    glutKeyboardFunc(handle_key_press)
    glutKeyboardUpFunc(handle_key_release)
    glutSpecialFunc(handle_special_keys)
    glutMouseFunc(handle_mouse_input)

    glutMainLoop()

if __name__ == "__main__":
    main()
