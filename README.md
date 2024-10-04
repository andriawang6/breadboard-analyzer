# Breadboard Bakery
## Freshly baked schematics for your breadboard!
Users upload an image of their wired breadboard, and Breadboard Bakery generates a schematic representing the logic circuit.
## Sample Schematic Output
<img src="https://github.com/user-attachments/assets/8e684a01-59b0-4476-912f-9c1b7e9873ef" width=500>

## Backend
### 1. Image Processing
Breadboards are used to prototype electrical circuits and experimental designs for electronics. The perforated plastic casing has a uniform grid of holes. Each of the outer edges has two vertical lines that are electrically connected—one rail supplies power (VCC), and the other connects to ground (GND). The two halves of the board are not connected, but all holes that are in the same horizontal row on the same side are connected electrically and carry the same signal.

A chip has two columns of pins, and each pin corresponds to either an input or an output of a logic gate. Each type of chip has a datasheet, which specifies what each pin corresponds to. For example 1A and 1B could be the input pins to an AND gate, and 1Y would be the output pin.  Wires are used to connect these inputs and outputs to create complex logic expressions.

Our first step was to preprocess the image by detecting the breadboard from the image and isolating it from the background surface. After converting the image to grayscale, applying a blur, and skewing the image, we could consistently detect the corners of the breadboard and crop the image to display only the board. This preprocessing step allowed us to segment the grid,  use contour detection to identify the chips, and apply edge detection to detect the wires. Finally, we could extract a set of wires represented by their endpoint coordinates, and a set of chips with their corresponding pin coordinates.

### 2. Logic Analysis
The next task was to transform the computer vision data into information about the logic expression represented by the breadboard.

All points in a row on a side are electrically connected, so we realized that we could abstract each coordinate to its row & side. Then, we could determine which rows were connected to gate pins by looking up the serial numbers of the chips on the user’s board with manufacturer datasheets. We could also determine which wires are connected to which gates, noting that if a wire endpoint is not connected to a chip, then it must be either an input or an output to the entire system. These observations allowed us to convert the coordinate endpoints to meaningful mappings. For example, we could determine that an input A goes into a NOT gate, and the output of the NOT gate goes into an AND gate.

We used this set of mappings to generate a logical expression, such as ((A*B)’+C)’=D. Because of the properties of the logic circuits our web application analyzes, we could interpret this data set as a directed acyclic graph. We developed a modified depth-first search to process these logical connections in a way that generated complete logical expressions.

### 3. Flask
A Flask API connects the backend and the frontend, allowing users to upload photos of their own breadboards. We set up POST requests to receive image data and chip serial numbers and GET requests to send back generated information about the circuit and the schematic. The Flask server runs the image processing and schematic generation code and sends the SVG to the frontend to display.
## Frontend
We used React to create a web application that allows users to upload an image of their breadboard. The website returns a cropped image of the breadboard after scaling and dewarping in OpenCV and prompts the user to select the type of each chip (NOT, AND, OR, etc.). Once the user submits their chip information, the schematic is generated and displayed as an image. The web app page features Brioche, the head baker at Breadboard Bakery.

# Meet Brioche, the owner of Breadboard Bakery!
<img src="https://github.com/user-attachments/assets/460f5748-9eee-4769-b88a-8629f226c2e1" width="400">


