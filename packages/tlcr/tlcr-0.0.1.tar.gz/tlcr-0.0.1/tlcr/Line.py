import numpy as np
import cv2


class Line:
    def __init__(self, coords):
        self.__pts = np.array(coords, np.int32).reshape((- 1, 1, 2))
        self.__rect = cv2.boundingRect(self.__pts)
        self.__mask = None
        self.__count_mask_pixels = 0
        self.__color = (255, 255, 255)
        self.__final_size = (256, 256)
        self.__final_orig_size = (256, 256, 3)

    def __get_mask(self, shape):
        if self.__mask is not None:
            return self.__mask
        self.__mask = np.full((shape[0], shape[1]), 0, dtype=np.uint8)
        cv2.fillPoly(self.__mask, [self.__pts], self.__color)
        x, y, w, h = self.__rect
        self.__mask = self.__mask[y:y + h, x:x + w]
        self.__count_mask_pixels = cv2.countNonZero(self.__mask)
        return self.__mask

    def get_dataset_images(self, orig_image, res_image):
        return self.get_image(orig_image), self.get_image(res_image, False)

    def get_image(self, image, orig=True):
        mask = self.__get_mask(image.shape)
        x, y, w, h = self.__rect
        orig_crop = image[y:y + h, x:x + w]
        final_image = np.full(self.__final_orig_size if orig is True else self.__final_size, 0, dtype=np.uint8)
        final_image[0:h, 0:w] = cv2.bitwise_or(orig_crop, orig_crop, mask=mask)
        return final_image

    def get_tlcr(self, image):
        return cv2.sumElems(image)[0] / self.__count_mask_pixels

    def sum_elems_optimized(self, mask):
        pixels = np.argwhere(mask == 255)
        x_dict = {}
        x_values = []
        for coords in pixels:
            if str(coords[1]) not in x_dict:
                x_dict[str(coords[1])] = []
                x_values.append(coords[1])
            x_dict[str(coords[1])].append(coords[0])
        x_values.sort()
        x_bound, y_bound, _, _ = self.__rect
        new_pts = []
        for i in range(4):
            new_pts.append([self.__pts[i][0][0] - x_bound, self.__pts[i][0][1] - y_bound])

        #sort new_points
        new_pts.sort(key=lambda x: x[1])

        if new_pts[0][0] > new_pts[1][0]:
            self.swap_positions(new_pts, 0, 1)

        if new_pts[2][0] > new_pts[3][0]:
            self.swap_positions(new_pts, 2, 3)

        height_min = [0, 0]
        pixel_stripes = []
        pixel_stripes.append([])
        for i in range(new_pts[2][0], new_pts[3][0] + 1):
            popped = x_dict[str(i)].pop()
            pixel_stripes[0].append([i, popped])
            if i == new_pts[2][0]:
                height_min[0] = popped - 1
            elif i == new_pts[3][0]:
                height_min[1] = popped - 1

        reached_checkpoint = False
        met_height_value = []
        met_height_value.append(False)
        met_height_value.append(False)
        stripe_ind = 0
        while not reached_checkpoint:
            met_height_value[0] = False
            met_height_value[1] = False
            stripe_ind += 1
            for x in x_values:
                if len(x_dict[str(x)]) > 0:
                    if (x == new_pts[0][0] and x_dict[str(x)][len(x_dict[str(x)]) - 1] == new_pts[0][1])\
                            or (x == new_pts[1][0] and x_dict[str(x)][len(x_dict[str(x)]) - 1] == new_pts[1][1]):
                        reached_checkpoint = True

                    if height_min[0] == x_dict[str(x)][len(x_dict[str(x)]) - 1] and not met_height_value[0]:
                        pixel_stripes.append([])
                        met_height_value[0] = True
                        height_min[0] -= 1

                    if height_min[1] == x_dict[str(x)][len(x_dict[str(x)]) - 1] and not met_height_value[1]:
                        met_height_value[1] = True
                        height_min[1] -= 1

                    if met_height_value[0] and not (met_height_value[1] and height_min[1] > x_dict[str(x)][len(x_dict[str(x)]) - 1]):
                        popped = x_dict[str(x)].pop()
                        pixel_stripes[stripe_ind].append([x, popped])

        print(f'Length of 0 stripe is {len(pixel_stripes[0])}, length of {len(pixel_stripes) - 1} stripe is {len(pixel_stripes[len(pixel_stripes) - 1])}')

        return pixel_stripes

    def swap_positions(self, list, pos1, pos2):
        list[pos1], list[pos2] = list[pos2], list[pos1]
        return list
