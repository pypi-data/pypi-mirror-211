"""
This class is in charge of analyzing the elements (i.e. form, color, etc.).
"""
from vid2info.inference.configs.constants import ACCEPTABLE, FAILED_ON
from vid2info.utils.quality_checker import QualityChecker
from vid2info.inference.config import SEGMENTATION_INFO, POLYGON_XY, CLASS_NAME
from vid2info.state.element_state.constants import FORM

import cv2
import numpy as np

class ElementAnalysis:
    def __init__(self, element_info: dict, frame: np.ndarray = None, quality_checker: QualityChecker | None = None):
        """
        Initialize the ElementAnalysis.

        :param element_state: ElementState. The element state to analyze.
        """
        self.quality_checker = quality_checker
        self.info = {
            FORM: self.analyze_form(element_info=element_info)
        }

    def analyze_form(self, element_info: dict) -> dict[str, float]:
        """
        Analyze the form of the element.

        :param element_info: dict. The information of the element.
        :return: dict[str, float]. The form of the element. Containing the following keys: ('circularity', 'ellipse_major_axis', 'ellipse_shorter_axis')
        """
        # Get the polygon in image coordinates (for taking aspect ratio into account), as a numpy array of shape (N, 2)
        polygon_xy = element_info[SEGMENTATION_INFO][POLYGON_XY]
        assert type(polygon_xy) == np.ndarray, f'Expected polygon_xy to be a numpy array. Got {type(polygon_xy)} instead.'

        # Using cv2.contourArea to find the area of the polygon
        area = cv2.contourArea(polygon_xy)

        # Using cv2.arcLength to find the perimeter of the polygon
        perimeter = cv2.arcLength(polygon_xy, True)

        # Calculating the circularity using the formula 4π(Area)/(perimeter^2)
        circularity = None if perimeter == 0 else 4 * np.pi * area / (perimeter ** 2)

        # Using cv2.fitEllipse to fit an ellipse to the polygon and get its major and minor axis lengths
        # Please note that the function cv2.fitEllipse will fail if the polygon has fewer than 5 points.
        if len(polygon_xy) >= 5:
            (x, y), (major_axis, minor_axis), angle = cv2.fitEllipse(polygon_xy)
        else:
            major_axis = minor_axis = angle = None

        # Return the circularity and axis lengths
        form =  {
            'circularity': circularity,
            'ellipse_major_axis': major_axis,
            'ellipse_minor_axis': minor_axis,
            'ellipse_minor_to_major_ratio': minor_axis / major_axis if major_axis != 0 else None, # Avoid division by zero
            'ellipse_angle': angle
        }

        form[ACCEPTABLE], form[FAILED_ON] = self.quality_checker.check(values=form, class_name=element_info[CLASS_NAME])

        return form


