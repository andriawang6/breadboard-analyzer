# Breadboard Bakery
## Freshly baked schematics for your breadboard!
Users upload an image of their wired breadboard, and Breadboard Bakery generates a schematic representing the logic circuit.
## Sample Schematic Output
<img src="https://github.com/user-attachments/assets/8e684a01-59b0-4476-912f-9c1b7e9873ef" width=500>

# 🍞 Inspiration
As computer science and computer engineering students at Georgia Tech, we often work with breadboards when prototyping. We can debug code relatively easily by adding print statements and using debuggers that are conveniently built into modern IDEs, but breadboards are much more difficult to debug. In hopes of solving this issue, we created a breadboard analyzer that converts wires and chips into an organized visual schematic.
# 🍞 What it does
Users upload an image of their wired breadboard, and Breadboard Bakery generates a schematic representing the logic circuit.
# 🍞 How we built it
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
# 🍞 Challenges we ran into
While working on computer vision image processing, we ran into the challenge of not properly detecting all the wires on the breadboard. Often, the program would detect parts of a wire or would detect the holes of the breadboard as wires. To resolve these issues, we refined our wire-detection algorithms by  improving the pre-processing and constraining the edge detection to minimum and maximum widths and lengths. This helped us differentiate the wires from the holes.

Developing the logic processing was challenging because of the sheer quantity and variety of data we had to store in order to have enough information about the circuit to generate the schematics. We spent a majority of this time diagramming the situation and experimenting with what data structures would allow us to store the information in an organized way for efficient processing. To develop the logic expression generation algorithm, we traced several circuits in many different ways to figure out a feasible strategy that would work with our data structure. By the time we finished analyzing the system, it only took a couple of hours to write and debug the code, since we already developed detailed pseudocode and well-defined test cases.

Another challenge we encountered was integrating the various components of our application: image processing, logic generation, and UI. Although we thoroughly tested each part individually, it was challenging to make them work together to generate and display schematics. To pinpoint the issues, we worked backwards through each layer, and we identified that some pieces of data that we were passing into certain methods were missing or incorrectly formatted. After ensuring that all components were communicating properly, we were able to receive the image from the user, process the image, pass it to the logic and schematic generation algorithm, and display the resulting schematic on the web application.
# 🍞 Accomplishments we're proud of
Overall, we are proud of what we accomplished to process breadboard images, identify circuit components, and create a visual schematic. Each of these steps were intimidating at first, whether it was fine-tuning computer vision algorithms, developing a custom data structure and graph algorithm, or setting up a server to connect the back and front ends.

Breadboard Bakery is a complex application that involves several discrete yet interdependent stages of processing, and we are also proud of the work we put in during the ideation and planning stage. Analyzing the problem carefully allowed us to break it down into coherent components, delegate tasks according to our strengths and interests, and work collaboratively to integrate the components smoothly. 
# 🍞 What we learned
During the process of creating Breadboard Bakery, we worked with many technologies that we had little to no prior experience with. We learned how to use OpenCV to use computer vision to process images, and we learned how to use Flask to create a backend framework that can interface with a frontend. We also learned how to integrate these with a visually appealing and easy-to-use user interface. 
# 🍞 What's next for Breadboard Bakery
In the future, we hope to continue enhancing Breadboard Bakery to support complex breadboard components, such as resistors and memory components, and analyze more intricate circuits, such as state machines. 

# 🍞 Meet Brioche, the owner of Breadboard Bakery!
<img src="https://github.com/user-attachments/assets/460f5748-9eee-4769-b88a-8629f226c2e1" width="400">


