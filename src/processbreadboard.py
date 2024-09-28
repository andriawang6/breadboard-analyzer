import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_filter(image):
    """
    Define a 5X5 kernel and apply the filter to gray scale image
    Args:
        image: np.array

    Returns:
        filtered: np.array

    """
    blurred =  cv2.blur(image, (30, 30))
    gray = cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY)
    kernel = np.ones((5, 5), np.float32) / 15
    filtered = cv2.filter2D(gray, -1, kernel)
    # plt.imshow(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
    # plt.title('Filtered Image')
    # plt.show()
    return filtered

def apply_threshold(filtered):
    """
    Apply OTSU threshold

    Args:
        filtered: np.array

    Returns:
        thresh: np.array

    """
    ret, thresh = cv2.threshold(filtered, 250, 255, cv2.THRESH_OTSU)
    # plt.imshow(cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB))
    # plt.title('After applying OTSU threshold')
    # plt.show()
    return thresh

def detect_contour(img, image_shape):
    """

    Args:
        img: np.array()
        image_shape: tuple

    Returns:
        canvas: np.array()
        cnt: list

    """
    canvas = np.zeros(image_shape, np.uint8)
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    cv2.drawContours(canvas, cnt, -1, (0, 255, 255), 3)
    # plt.title('Largest Contour')
    # plt.imshow(canvas)
    # plt.show()

    return canvas, cnt

def detect_corners_from_contour(canvas, cnt):
    """
    Detecting corner points form contours using cv2.approxPolyDP()
    Args:
        canvas: np.array()
        cnt: list

    Returns:
        approx_corners: list

    """
    epsilon = 0.02 * cv2.arcLength(cnt, True)
    approx_corners = cv2.approxPolyDP(cnt, epsilon, True)
    cv2.drawContours(canvas, approx_corners, -1, (255, 255, 0), 10)
    approx_corners = sorted(np.concatenate(approx_corners).tolist())
    # print('\nThe corner points are ...\n')
    for index, c in enumerate(approx_corners):
        character = chr(65 + index)
        # print(character, ':', c)
        cv2.putText(canvas, character, tuple(c), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Rearranging the order of the corner points
    approx_corners = [approx_corners[i] for i in [1, 3, 0, 2]]

    # plt.imshow(canvas)
    # plt.title('Corner Points: Douglas-Peucker')
    # plt.show()
    return approx_corners    


def get_destination_points(corners):
    """
    -Get destination points from corners of warped images
    -Approximating height and width of the rectangle: we take maximum of the 2 widths and 2 heights

    Args:
        corners: list

    Returns:
        destination_corners: list
        height: int
        width: int

    """

    w1 = np.sqrt((corners[0][0] - corners[1][0]) ** 2 + (corners[0][1] - corners[1][1]) ** 2)
    w2 = np.sqrt((corners[2][0] - corners[3][0]) ** 2 + (corners[2][1] - corners[3][1]) ** 2)
    w = max(int(w1), int(w2))

    h1 = np.sqrt((corners[0][0] - corners[2][0]) ** 2 + (corners[0][1] - corners[2][1]) ** 2)
    h2 = np.sqrt((corners[1][0] - corners[3][0]) ** 2 + (corners[1][1] - corners[3][1]) ** 2)
    h = max(int(h1), int(h2))

    destination_corners = np.float32([(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)])

    # print('\nThe destination points are: \n')
    # for index, c in enumerate(destination_corners):
    #     character = chr(65 + index) + "'"
    #     print(character, ':', c)

    # print('\nThe approximated height and width of the original image is: \n', (h, w))
    return destination_corners, h, w

def unwarp(img, src, dst):
    """
    Args:
        img: np.array
        src: list
        dst: list

    Returns:
        un_warped: np.array

    """
    h, w = img.shape[:2]
    H, _ = cv2.findHomography(src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0)
    # print('\nThe homography matrix is: \n', H)
    un_warped = cv2.warpPerspective(img, H, (w, h), flags=cv2.INTER_LINEAR)

    # plot

    # f, (ax2) = plt.subplots(1, figsize=(15, 8))
    # f.subplots_adjust(hspace=.2, wspace=.05)
    # ax1.imshow(img)
    # ax1.set_title('Original Image')

    x = [src[0][0], src[2][0], src[3][0], src[1][0], src[0][0]]
    y = [src[0][1], src[2][1], src[3][1], src[1][1], src[0][1]]

    # ax2.imshow(img)
    # ax2.plot(x, y, color='yellow', linewidth=3)
    # ax2.set_ylim([h, 0])
    # ax2.set_xlim([0, w])
    # ax2.set_title('Target Area')

    # plt.show()
    return un_warped

def show_grid(image, dimensions, color):
    h, w, _ = image.shape
    rows, cols = dimensions
    dy, dx = h / rows, w / cols

    # draw vertical lines
    for x in np.linspace(start=dx, stop=w-dx, num=cols-1):
        x = int(round(x))
        cv2.line(image, (x, 0), (x, h), color, thickness=3)

    # draw horizontal lines
    for y in np.linspace(start=dy, stop=h-dy, num=rows-1):
        y = int(round(y))
        cv2.line(image, (0, y), (w, y), color, thickness=3)

def crop_grids(image):
    """
    Skew correction using homography and corner detection using contour points.
    Returns: None
    """
    # Read and display the original image

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # plt.imshow(image)
    # plt.title('Original Image')
    # plt.show()

    # Apply filtering and thresholding
    filtered_image = apply_filter(image)
    threshold_image = apply_threshold(filtered_image)

    # Detect contours and corners
    cnv, largest_contour = detect_contour(threshold_image, image.shape)
    rect = cv2.boundingRect(largest_contour)
    x,y,w,h = rect
    cv2.rectangle(threshold_image,(x,y),(x+w,y+h),(255,0,0),2)

    # Show result
    # plt.imshow(threshold_image)
    # plt.show()

    corners = detect_corners_from_contour(cnv, largest_contour)

    # Get destination points and perform unwarping
    destination_points, h, w = get_destination_points(corners)
    un_warped = unwarp(image, np.float32(corners), destination_points)

    # Crop the unwarped image
    cropped = un_warped[0:h, 0:w]

    #percentage offsets
    starty = (int)(h * 0.015)
    endy = (int)(h * 0.982)

    startx = (int)(w * 0.22)
    endx = (int)(w * 0.46)

    centeroffset = (int)(w*0.32)

    left_crop = cropped[starty:endy, startx:endx]
    #show_grid(left_crop, (63, 5), (255, 0, 0))

    # plt.imshow(left_crop)
    # plt.title('left crop')
    # plt.show()

    right_crop = cropped[starty:endy, startx+centeroffset:endx+centeroffset]
    #show_grid(right_crop, (63, 5), (255, 0, 0))

    cropped = cropped[starty:endy, 0:w]

    # plt.imshow(right_crop)
    # plt.title('right crop')

    # # Display the plots
    # plt.show()
    return cropped, left_crop, right_crop

def detect_chips(image):
    chips = []

    filtered_image = apply_filter(image)
    threshold_image = apply_threshold(filtered_image)
    contours, _ = cv2.findContours(threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    im_shape = image.shape
    for c in contours:
        rect = cv2.boundingRect(c)
        #ignores too small or bounding the entire breadboard
        if rect[2] < 80 or rect[3] < 80 or (rect[2] * rect[3])/(image.shape[0] * image.shape[1]) > 0.9: continue
        x,y,w,h = rect
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)

        #assign
        pin_7_row = int((y+h)/(im_shape[0]/63)) - 1
        chips.append([""])
        for i in range(1, 15):
            if i <= 7:
                chips[len(chips) - 1].append((4, pin_7_row-(7 - i)))
            else:
                chips[len(chips) - 1].append((5, pin_7_row-(i-7-1)))
        #print(chips[len(chips) - 1])
            

    # Show result
    # plt.imshow(image)
    # plt.show()
    return chips


def detect_wires(image, side, min_width=20, max_width=100, min_length=200, max_length=10000):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 30, 100)
    
    # Apply dilation (optional, adjust kernel size if needed)
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    
    # Find contours on dilated edges
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    im_shape = image.shape

    endpoints = []
    
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        length = cv2.arcLength(c, True)
        
        # Check for bounding box dimensions and contour length
        if min_width <= w <= max_width and min_length <= length <= max_length:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            #handles left and right side coords
            offset = 5 if side == "right" else 0

            point1 = ((int((x)/(im_shape[1]/5) + offset)), (int((y)/(im_shape[0]/63))))
            point2 = ((int((x)/(im_shape[1]/5) + offset)), (int((y+h)/(im_shape[0]/63))))

            if point1[0] == 4 or point1[0] == 5: continue
            endpoints.append([point1, point2])
    
    # Show the final image with detected wires
    # plt.imshow(image)
    # plt.show()

    return endpoints


def process_image(image_path):
    breadboard_image = cv2.imread(image_path)
    cropped, left_crop, right_crop = crop_grids(breadboard_image)
    
    # Analyze both left and right crops and get wire endpoints
    endpoints = [*detect_wires(left_crop, "left"), *detect_wires(right_crop, "right")]

    chips = detect_chips(cropped)

    return chips


# if __name__ == '__main__':
#     breadboard_image = cv2.imread('../images/breadboard16.jpg')
#     cropped, left_crop, right_crop = crop_grids(breadboard_image)
    
#     # Analyze both left and right crops and get wire endpoints
#     endpoints = [*detect_wires(left_crop, "left"), *detect_wires(right_crop, "right")]
#     print("endpoints", endpoints)

    # chips = detect_chips(cropped)
    # print("chips", chips)


