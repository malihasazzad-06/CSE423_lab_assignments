# CSE423_lab_assignments

#**CSE423 Computer Graphics Lab Assignment 1**

This project is the implementation of **CSE423 Computer Graphics Lab Assignment 1** using **Python OpenGL (GLUT)**. It focuses on creating interactive 2D graphics and animations using basic OpenGL primitives, along with keyboard and mouse event handling. The entire solution is written in a single Python file following the given constraints.

The project includes two main tasks. In **Task 1 (House in Rainfall)**, a house is drawn using only `GL_POINTS`, `GL_LINES`, and `GL_TRIANGLES`, with animated rainfall falling continuously. The left and right arrow keys gradually bend the direction of rain, while additional keys control a day/night transition by changing the background from dark to light and vice versa, ensuring proper visibility of all scene elements. In **Task 2 (Amazing Box)**, a bounded box simulation is created where right mouse clicks generate randomly colored moving points that travel diagonally and bounce off walls. The up and down arrow keys adjust the speed of all points, left click toggles a blinking effect, and the spacebar freezes or unfreezes all movement and interactions.

Overall, this **Assignment 1** demonstrates core computer graphics concepts such as primitive drawing, animation, collision detection, and real-time interaction. It also improves understanding of event-driven programming using OpenGL, making the system fully interactive and dynamic within a constrained graphical environment.

# **CSE423 – Lab 02: Midpoint Line Drawing & Game Project**

This project is part of **CSE423 Computer Graphics Lab 02**, focusing on the implementation of the **Midpoint Line Drawing Algorithm** and its application in a simple 2D game.

The first part involves implementing the midpoint line drawing algorithm using only **GL_POINTS**. The algorithm efficiently draws lines using integer arithmetic and handles all 8 zones by converting coordinates to Zone 0, applying the algorithm, and mapping results back to the original zone. This improves performance compared to DDA by avoiding floating-point calculations.

The second part is a game called **“Catch the Diamonds!”**. In this game, a catcher moves horizontally using arrow keys to catch falling diamonds. Each successful catch increases the score, while missing a diamond ends the game. The game includes restart, pause/play, and exit buttons drawn using midpoint lines. A special **cheat mode** (activated by ‘C’) allows automatic catching of diamonds. Collision detection is handled using AABB logic, and gameplay speed increases over time for difficulty scaling.

The project strictly uses OpenGL primitives and reinforces concepts of line drawing, animation, and interactive game design.


 #**CSE423 Lab 03: OpenGL 3D Introduction and Transformation**.
 
 It focuses on understanding **3D graphics in PyOpenGL** and how objects are controlled in a 3D world using **translation, rotation, scaling, and perspective projection (gluPerspective, gluLookAt)**. It also explains how camera positioning and viewing direction work in a 3D environment.

The main task is to build a 3D game called **Bullet Frenzy**. The game includes a **player character (sphere, cylinder, cuboid), 5 enemy spheres, and a grid floor with boundaries**. The player can move the gun using **W/S (forward/backward)** and rotate using **A/D keys**, and shoot bullets using the **mouse click**. Enemies continuously move toward the player and respawn when hit.

The game also includes **camera controls (arrow keys + first/third person toggle)**, **cheat mode (C key auto-aim and auto-shoot)**, and **auto-follow mode (V key)**. The game ends when **lives reach 0 or 10 bullets are missed**, and can be restarted with **R key**.

