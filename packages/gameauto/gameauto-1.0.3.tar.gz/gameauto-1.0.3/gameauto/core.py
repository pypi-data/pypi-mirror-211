import time
import random
import numpy as np

from minidevice import MiniDevice
from .images import find_image_color,find_image

def random_number(bbox):
    """
    Generates a random coordinate within a given rectangular boundary.

    Args:
        bbox: A tuple containing four values (x_min, y_min, x_max, y_max),
            representing the rectangular boundary. The coordinates should satisfy
            he condition that x_min < x_max and y_min < y_max.

    Returns:
        A tuple containing two integers (x, y), which represent the randomly
        generated coordinates within the given rectangular boundary.

    Raises:
        None.
    """
    x_min, y_min, x_max, y_max = bbox

    # Compute the center point of the rectangular boundary
    center_x, center_y = (x_min + x_max) / 2, (y_min + y_max) / 2

    # Compute the standard deviation of the rectangular boundary
    std_x, std_y = (x_max - x_min) / 6, (y_max - y_min) / 6

    # Generate random coordinates until a valid coordinate is found
    while True:
        x, y = np.random.normal(center_x, std_x), np.random.normal(center_y, std_y)
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return round(x), round(y)

def xywh2xyxy(region):
    """[x,y,w,h] to [xmin,ymin,xmax,ymax]

    Args:
        region (array): [x,y,w,h]

    Returns:
        array: [xmin,ymin,xmax,ymax]
    """
    return [region[0], region[1], region[0] + region[2], region[1] + region[3]]

def xyxy2xywh(region):
    """[xmin,ymin,xmax,ymax] to [x,y,w,h] 

    Args:
        region (array): [xmin,ymin,xmax,ymax]

    Returns:
        array: [x,y,w,h]
    """
    return [region[0], region[1], region[2] - region[0]  , region[3] - region[1]]


class Core (MiniDevice):
    def __init__(self, device):
        super().__init__(device)
    
    def miniFindImage(
        self,
        template_path,
        target_path,
        region=None,
        threshold=0.8,
        is_color=False,
        color_threshold=30,
        is_click=False,
    ):
        """找图函数示例，建议重写

        Args:
            - template_path (Str/Mat): 图像地址或者opencv格式的图像 小图
            - target_path (Str/Mat): 图像地址或者opencv格式的图像 大图
            - region (list, optional): 模板匹配的区域左上角和右下角两点坐标[Xmin,Ymin,Xmax,Ymax]. Defaults to None.
            - threshold (float, optional): 图像相似度. Defaults to 0.8.
            - is_color (bool, optional): 是否匹配图像颜色. Defaults to False.
            - color_threshold (int, optional): 颜色相似度. Defaults to 30.
            - is_click (bool, optional): 是否点击图像. Defaults to False.

        Returns:
            list/None: 图像所在区域[Xmin,Ymin,Xmax,Ymax]
        """
        if is_color:
            res = find_image_color(
                template_path, target_path, region, threshold, True, color_threshold
            )
        else:
            res = find_image(template_path, target_path, region, threshold)

        if res:
            if is_click:
                self.miniRandomClick(xywh2xyxy(res))
            return xywh2xyxy(res)
        else:
            return None
        
    def miniRandomClick(self, region, point=None, method=1):
        """随机点击 同样建议重写

        Args:
            - region (array): [x_min, y_min, x_max, y_max]
            - point (tuple, optional): 坐标点. Defaults to None.
            - method (int, optional): 1:范围随机点击需传入region 2:定点点击. Defaults to 1.
        """
        p = [0, 0]
        if region != None:
            p[0], p[1] = random_number(region)

        if method == 2 and point != None:
            p[0], p[1] = point
            self.miniPress(p[0], p[1], random.randint(80, 150))
        else:
            i = abs(np.random.normal(0, 30))
            if i > 90:
                self.miniSmlMove(
                    p[0],
                    p[1],
                    p[0] + random.randint(0, 3),
                    p[1] + random.randint(0, 3),
                    time=random.randint(200, 350),
                )
                # print("滑动")
            elif i > 60:
                self.miniPress(p[0], p[1], random.randint(300, 600))
                # print(f"长按{p}")
            else:
                self.miniPress(p[0], p[1], random.randint(80, 150))
                # print(f"点击{p}")
        time.sleep(random.randint(80, 120) / 1000)

    def miniSmlMove(self, qx, qy, zx, zy, time=500):
        """三次贝塞尔曲线滑动 同样建议重写

        Args:
            - qx (int): 起点
            - qy (int): 
            - zx (int): 终点
            - zy (int): 
            - time (int, optional): 滑动时长. Defaults to 500.
        """
        slidingPath = []
        point = [
            {"x": qx, "y": qy},
            {"x": random.randint(qx - 100, qx + 100), "y": random.randint(qy, qy + 50)},
            {"x": random.randint(zx - 100, zx + 100), "y": random.randint(zy, zy + 50)},
            {"x": zx, "y": zy},
        ]
        cx = 3.0 * (point[1]["x"] - point[0]["x"])
        bx = 3.0 * (point[2]["x"] - point[1]["x"]) - cx
        ax = point[3]["x"] - point[0]["x"] - cx - bx
        cy = 3.0 * (point[1]["y"] - point[0]["y"])
        by = 3.0 * (point[2]["y"] - point[1]["y"]) - cy
        ay = point[3]["y"] - point[0]["y"] - cy - by
        t_values = np.arange(0, 1, 0.08)
        t_squared = t_values * t_values
        t_cubed = t_squared * t_values
        x_values = ax * t_cubed + bx * t_squared + cx * t_values + point[0]["x"]
        y_values = ay * t_cubed + by * t_squared + cy * t_values + point[0]["y"]
        slidingPath.extend([(int(x), int(y)) for x, y in zip(x_values, y_values)])
        self.miniSwipe(slidingPath, duration=time)