import cv2
import numpy as np
from PIL import Image


def analyze_filter(image):
    """
    Analyzes a filter photograph and estimates
    the number of visible particles and filter loading.
    """

    # Convert PIL image to NumPy array
    img = np.array(image)

    # Convert RGB to OpenCV format
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Make a copy for drawing results
    output = img.copy()

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Reduce small image noise
    blurred = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    # Detect darker particles
    _, threshold = cv2.threshold(
        blurred,
        150,
        255,
        cv2.THRESH_BINARY_INV
    )

    # Clean small noise
    kernel = np.ones(
        (3, 3),
        np.uint8
    )

    cleaned = cv2.morphologyEx(
        threshold,
        cv2.MORPH_OPEN,
        kernel
    )

    # Find particle shapes
    contours, _ = cv2.findContours(
        cleaned,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    particle_count = 0
    total_particle_area = 0

    # Examine each detected object
    for contour in contours:

        area = cv2.contourArea(contour)

        # Ignore extremely tiny objects
        # and extremely large objects
        if 20 < area < 5000:

            particle_count += 1

            total_particle_area += area

            x, y, w, h = cv2.boundingRect(contour)

            # Draw a box around detected particle
            cv2.rectangle(
                output,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # Label particle
            cv2.putText(
                output,
                str(particle_count),
                (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1
            )

    # Calculate filter area
    image_area = gray.shape[0] * gray.shape[1]

    # Estimate percentage of image occupied by particles
    loading = (
        total_particle_area / image_area
    ) * 100

    # Convert this to a simple prototype loading scale
    # for the school demonstration.
    filter_loading = min(
        100,
        loading * 20
    )

    filter_loading = round(
        filter_loading,
        1
    )

    # Convert result back to RGB
    output = cv2.cvtColor(
        output,
        cv2.COLOR_BGR2RGB
    )

    return output, particle_count, filter_loading
