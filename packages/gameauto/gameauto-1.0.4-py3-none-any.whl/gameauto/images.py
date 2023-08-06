import cv2
import ncnn
from ncnn.utils.objects import Detect_Object

def compare_color(image, point, color, tolerance=0):
    """
    比较某一图像中某点的颜色值是否和传入颜色参数值相等。

    参数：
    - image: 图像 Mat格式
    - point: 坐标点 Point[x,y]
    - color: 需要比较的颜色值，例如 "#FF0000" 表示红色
    - tolerance: 允许的颜色差异程度

    返回值：
    - 如果传入的颜色值和指定点的颜色值相等，返回 True,否则返回 False。
    """
    # 将颜色值转换为 RGB 分量值
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    pixel_color = image[point[1], point[0]]
    # 比较颜色值
    if (
        abs(pixel_color[2] - r) <= tolerance
        and abs(pixel_color[1] - g) <= tolerance
        and abs(pixel_color[0] - b) <= tolerance
    ):
        return True
    else:
        return False


def get_color(image, point):
    """
    获取图像中指定位置的颜色值，并将其转换为 16 进制格式。

    参数：
    - image:图像 Mat格式
    - point [x,y] 坐标点

    返回值：
    - 该点的颜色值，格式为 "#RRGGBB"
    """
    # 获取指定点的颜色值（BGR 格式）
    pixel_color = image[point[1], point[0]]
    # 将 BGR 格式转换为 RGB 格式
    rgb_color = pixel_color[::-1]
    # 将 RGB 分量值转换为 16 进制格式
    hex_color = "#{:02X}{:02X}{:02X}".format(rgb_color[0], rgb_color[1], rgb_color[2])
    return hex_color


def find_color(image, color, region=None, tolerance=0):
    # 设置查找区域
    if region is not None:
        x_min, y_min, x_max, y_max = region
        image = image[y_min:y_max, x_min:x_max]
    for x in range(image.shape[1]):
        for y in range(image.shape[0]):
            # 将颜色值转换为 RGB 分量值
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            pixel_color = image[y, x]
            # 比较颜色值
            if (
                abs(pixel_color[2] - r) <= tolerance
                and abs(pixel_color[1] - g) <= tolerance
                and abs(pixel_color[0] - b) <= tolerance
            ):
                return x, y
    return None


def find_image(template_path, target_path, region=None, threshold=0.8,flag=cv2.IMREAD_COLOR):
    """灰度找图

    Args:
        params: 一个字典，包含以下参数：

            - template_path: 模板图像的路径/cv2格式

                - target_path: 目标图像的路径/cv2格式

                - region: 指定在目标图像中查找的区域,格式为(x_min, y_min, x_max, y_max),默认为None表示查找整张图片

                - threshold: 相似度的阈值,取值为0~1之间,默认为0

                - flag:图像读取方式

        Returns:
            一个包含4个元素的元组(x, y,w,h),表示查找到的最相似部分在目标图像中的左上角坐标,如果未找到则返回None
    """
    # 读取模板图像和目标图像
    template = (
        cv2.imread(template_path, flag)
        if isinstance(template_path, str)
        else template_path
    )

    target = (
        cv2.imread(target_path, flag) if isinstance(target_path, str) else target_path
    )
    # 设置查找区域
    if region is not None:
        x_min, y_min, x_max, y_max = region
        target = target[y_min:y_max, x_min:x_max]
    # 匹配模板图像
    res = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    # 选择相似度最高的一个结果
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < threshold:
        return None
    # 转换坐标系
    if region is not None:
        max_loc = (max_loc[0] + x_min, max_loc[1] + y_min)
    # 返回匹配结果
    return [max_loc[0], max_loc[1], template.shape[1], template.shape[0]]


def find_image_color(
    template_path,
    target_path,
    region=None,
    threshold=0.8,
    is_color=False,
    color_threshold=30,
):
    """找图进阶含找色

    Args:
        template_path (_type_): _description_
        target_path (_type_): _description_
        region (_type_): _description_
        threshold (float, optional): _description_. Defaults to 0.8.
        is_color (bool, optional): _description_. Defaults to False.
        color_threshold (int, optional): _description_. Defaults to 30.

    Returns:
        _type_: _description_
    """
    flag = cv2.IMREAD_COLOR
    # 读取模板图像和目标图像
    template = (
        cv2.imread(template_path, flag)
        if isinstance(template_path, str)
        else template_path
    )

    target = (
        cv2.imread(target_path, flag) if isinstance(target_path, str) else target_path
    )

    res = find_image(template, target, region, threshold)

    if res:
        if is_color:
            if (
                find_color(
                    target,
                    get_color(template, [0, 0]),
                    [res[0], res[1], res[0] + 10, res[0] + 10],
                    color_threshold,
                )
                is None
            ):
                return None
        return res
    else:
        return None


def readImgArr(imgPathArr):
    """读取图像并返回cv2图像字典

    Args:
        imgPathArr (array): 图像路径数组

    Returns:
        dict: cv2图像字典
    """
    imgArr = {}
    for imgPath in imgPathArr:
        imgArr[imgPath.split("/")[-1].split(".")[0]] = cv2.imread(imgPath)
    return imgArr


class YoloV3:
    def __init__(
        self,
        param_path:str,
        bin_path:str,
        class_names:list,
        tiny=False,
        num_threads=1,
        use_gpu=False,
    ):
        """ncnn加载yolov3模型

        Args:
            - param_path (str): yolov3模型param地址
            - bin_path (str): yolov3模型bin地址
            - class_names (list): 类名列表
            - tiny (bool, optional): 是否启用tiny模型. Defaults to False.
            - num_threads (int, optional): 启用线程数量. Defaults to 1.
            - use_gpu (bool, optional): 是否启用gpu计算 Defaults to False.
        """
        target_size = 416 if tiny else 608
        self.target_size = target_size
        self.num_threads = num_threads
        self.use_gpu = use_gpu

        self.mean_vals = []
        self.norm_vals = [1 / 255.0, 1 / 255.0, 1 / 255.0]

        self.net = ncnn.Net()
        self.net.opt.use_vulkan_compute = self.use_gpu
        self.net.opt.num_threads = self.num_threads

        self.net.load_param(param_path)
        self.net.load_model(bin_path)

        self.class_names = class_names

    def __del__(self):
        self.net = None

    def __call__(self, img):
        img_h = img.shape[0]
        img_w = img.shape[1]

        mat_in = ncnn.Mat.from_pixels_resize(
            img,
            ncnn.Mat.PixelType.PIXEL_BGR2RGB,
            img.shape[1],
            img.shape[0],
            self.target_size,
            self.target_size,
        )
        mat_in.substract_mean_normalize(self.mean_vals, self.norm_vals)

        ex = self.net.create_extractor()
        ex.input("data", mat_in)

        ret, mat_out = ex.extract("output")

        objects = []

        for i in range(mat_out.h):
            values = mat_out.row(i)

            obj = Detect_Object()
            obj.label = values[0]
            obj.prob = values[1]
            obj.rect.x = values[2] * img_w
            obj.rect.y = values[3] * img_h
            obj.rect.w = values[4] * img_w - obj.rect.x
            obj.rect.h = values[5] * img_h - obj.rect.y

            objects.append(obj)

        return objects


def yolo_filter(class_name: str, class_names: list, objects: list, min_prob=0.0):
    """模型计算结果筛选

    Args:
        - class_name (str): 筛选的类名
        - class_names (list): 模型类名列表
        - objects (list): 模型计算返回的结果
        - min_prob (float, optional): 结果置信度阈值. Defaults to 0.0.

    Returns:
        - list: objects
            - object:
                - rect.x 左上角横坐标
                - rect.y 左上角纵坐标   
                - rect.w 区域宽
                - rect.h 区域高
                - prob  置信度
                - label 类名
    """
    yoloResult = []
    for obj in objects:
        if obj.prob < min_prob:
            continue
        if class_names[int(obj.label)] == class_name:
            yoloResult.append(obj)
    return yoloResult

if __name__ == "__main__":
    m = cv2.imread("screenshotemulator-5554.png")
    #加载模型
    net = YoloV3(
        param_path="yolov3-tiny_6700-opt.param",
        bin_path="yolov3-tiny-opt.bin",
        #类名此处记得将第一个元素留空,所有元素往后一个(ncnn的问题好像是(有空改改))
        class_names=["", "exp", "hd", "jb"],
        num_threads=4,
        use_gpu=True,
    )
    #输入mat格式图像进行计算
    objects = net(m)
    #过滤结果
    yolo_filter("exp",net.class_names,objects,0.8)
    # draw_detection_objects(m, net.class_names, objects)