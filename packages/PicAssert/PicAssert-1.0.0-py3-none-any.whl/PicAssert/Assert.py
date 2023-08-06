"""
PicAssert图片断言工具：
anchor： 测码范晔
联系邮箱： 1538379200@qq.com
当前版本：v 1.0.0
通过图片拓展断言方式
PicAsssert会将图片在全局做一次模板匹配行为，当查找的图片大于或者等于设置的阈值的时候，程序将返回True，
当全局匹配的图片匹配度低于所设置的阈值时，程序将启动特征匹配模式，对前面相似度较近的区域进行截图，再次进行特征分析，
如果特征分析的结果判断为图片相似，程序将返回True，否则返回False
1.0.0添加图片定位点击功能
程序依赖 opencv、pillow 进行图片的处理

**使用说明**：
1、Assert类中设置一下 init_dpi，默认为(1920, 1080)以tuple或者list的形式，写上当前编写代码设备的分辨率，提升兼容性
2、PicAssert的Assert类，如果添加了driver，则识别为selenium操作，将使用selenium进行截图，代码可以无头模式运行，但为了提升稳定性，
  请将窗口设置为当前编写代码的设备的分辨率大小，设置selenium浏览器窗口大小代码为：
  dr.set_window_size(1920, 1080)
  Assert类中设置了max_window=True的选项时，会自动将浏览器大小放大为设置的init_dpi大小
  Assert类如果没有添加任何参数，则默认截取设备的全屏，可以在其他gui代码中运行，注意不能关闭当前显示的屏幕
3、使用图片断言会返回一个布尔值，True为找到当前图片，False为未找到图片
4、使用图片点击功能如不是无头模式，使用最大化浏览器或者设置浏览器为当前构建代码的设备分辨率尺寸，如果无头模式使用设置窗口大小为当前构建代码设备分辨率


**使用**
实例化Assert类：
ps = Assert()  # ps = Assert(driver=driver, init_dpi=(1920, 1080), max_window=True)
# 使用图像断言(assert_exist)
ps.assert_exist("./test.png", 0.7)
assert_exist有两个形参
第一个参数：pic_path  需要判断的图片保存路径
第二个参数：threshold  断言阈值，当前默认 0.7，可调制0到1的区间，1为100%，请尽量控制在0.6到0.9之间
# 使用图像搜索点击(assert_click)
ps.assert_click('img_4.png')
assert_click接受两个参数
第一个pic_path     需要进行搜索点击的图片
第二个hwnd         需要进行后台点击的窗口句柄


**使用流程**
assert_exist
1、正常编写代码，将需要断言的地方，使用工具(微信、QQ等)进行截图，截图尽量不会包含其他可变的干扰，将其保存在一个路径中
2、导入PicAssert包，实例化Assert类，使用assert_exist，传入前面截图路径
3、获取返回值
4、运行完成，将在项目目录下，新建一个.assert_cache文件夹，下面有success和fail文件夹，成功断言放在success中，失败在fail中，程序每次运行会清空缓存文件

assert_click
1、编写代码，使用工具进行截图(QQ、微信等)保存目标图片
2、使用assert_click，传入图片路径，如果是针对gui界面窗口，可以传入hwnd窗口句柄进行后台点击，窗口句柄可使用抓抓工具获取
3、获取返回值，返回值为计算的坐标地址，地址以分辨率大小为基准
4、运行完成，可在.项目assert_cache目录的click文件夹查看点击，点击的地方会标上红点

**selenium代码使用示例**
from SafeDriver.drivers import driver, option
import time
from PicAssert.Assert import Assert
dr = driver()
option.headless = True                                  # 设置selenium无头模式
dr.set_window_size(1920, 1080)                          # 设置selenium浏览器窗口大小
ps = Assert(dr, init_dpi=(1920, 1080), max_window=True)  # 实例化Assert类。并设置当前设备初始分辨率，设置max_window可不设置上述窗口大小
dr.get("https://www.baidu.com")
time.sleep(2)
# 图像断言
p1_res = ps.assert_exist(r"D:\test.png")     # ps.assert_exist(r"D:\test.png", 0.8)
if p1_res is True:
    print("图片存在")
else
    print("图片不存在")
# 图像搜索点击
p2_res = ps.assert_click(r'D:\test2.png')
print("当前点击位置：", p2_res)

**注意**
selenium未设置无头模式时，页面尺寸会略小于设定尺寸，但这种情况对于图像判断的影响并不是非常大，
在调试时，请注意无头模式和普通模式的数值设置
图片搜索点击，请务必保证界面是最大化运行的，不管是浏览器还是gui界面，gui界面请保持在窗口最前
"""
import warnings

import cv2
from PIL import ImageGrab, Image
from pathlib import Path
import os
import shutil
from typing import Union
import numpy as np
import win32api, win32con, win32gui, win32print
import time
from selenium.webdriver.common.action_chains import ActionChains


class Assert:
    __pic_width = 0
    __pic_height = 0

    def __init__(self, driver=None, init_dpi: Union[tuple, list] = (1920, 1080), max_window: bool = False):
        self.__driver = driver
        self.__init_dpi = init_dpi
        self.__max_window = max_window
        if (self.__max_window is True) and (self.__driver is not None):
            self.__driver.set_window_size(*init_dpi)
            self.__driver.set_window_position(0, 0)
        cache_path = Path.cwd().resolve() / '.assert-cache'
        success_path = cache_path / 'success'
        fail_path = cache_path / 'fail'
        click_path = cache_path / 'click'
        shutil.rmtree(cache_path, ignore_errors=True)
        cache_path.mkdir(exist_ok=True)
        success_path.mkdir(exist_ok=True)
        fail_path.mkdir(exist_ok=True)
        click_path.mkdir(exist_ok=True)
        self.__cache_path = os.fspath(cache_path)
        self.__seccess_path = os.fspath(success_path)
        self.__fail_path = os.fspath(fail_path)
        self.__click_path = os.fspath(click_path)
        self.__width, height = self.__ScaledResolution()
        self.__dpi_h, v = self.__GetResolution()
        self.__size_scale = self.__dpi_h / self.__width
        if type(self.__init_dpi) not in (list, tuple):
            raise TypeError("初始分辨率应为list或者tuple类型，且值类型应该为int")

    def __get_shot(self) -> str:
        """
        获取当前页面的截图，如果设置了driver，将使用selenium的截图方法
        :return: 图片路径名称
        """
        now_time = time.strftime("%Y%m%d%H%M%S")
        filename = "PICASSERT-" + now_time + ".png"
        filename = self.__cache_path + '/' + filename
        if not self.__driver:
            all_screen = ImageGrab.grab()  # 全屏截图
            all_screen.save(filename)
        else:
            self.__driver.get_screenshot_as_file(filename)
        image = Image.open(filename)
        x, y = image.size
        if self.__pic_width != x and self.__pic_height != y:  # 设置图片缩放比例，已设置则略过
            self.__pic_width = x
            self.__pic_height = y
            if self.__init_dpi[0] != self.__pic_width:
                self.__scale = self.__init_dpi[0] / self.__pic_width
            else:
                self.__scale = 1
        return filename

    def __GetResolution(self):
        """
        获取目前设置屏幕的分辨率
        :return: 屏幕宽、高
        """
        hDC = win32gui.GetDC(0)  # 获取整个屏幕的上下文环境的句柄，为空获取整个
        width = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
        height = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
        return width, height

    def __ScaledResolution(self):
        """
        获取的屏幕原始大小
        :return: 屏幕宽、高
        """
        width = win32api.GetSystemMetrics(0)  # 获取宽
        height = win32api.GetSystemMetrics(1)  # 获取高
        return width, height

    def assert_exist(self, pic_path: str, threshold: Union[int, float] = 0.7) -> Union[bool, None]:
        """
        进行图片匹配，判断是否存在此图片
        程序将先进行模板匹配，找到截图对应的区域，如果匹配值小于设定的阈值，程序会将最接近的区域进行截图，重新进行特征点匹配，也小于0.1才返回False
        匹配成功图片保存在.assert-cache/success中
        失败保存在.assert-cache/fail中
        :param pic_path: 当前需要进行匹配的图片
        :param threshold: 阈值，0~1区间
        :return: bool
        """
        pic_cache_path = self.__get_shot()
        try:
            picname_color = cv2.imread(pic_cache_path)
            picname = cv2.cvtColor(picname_color, cv2.COLOR_RGB2GRAY)
            tmp = cv2.imread(pic_path, 0)
            w, h = tmp.shape[::-1]
            w = int(w / self.__scale)  # 图像缩放
            h = int(h / self.__scale)
            tmp = cv2.resize(tmp, (w, h))
            res = cv2.matchTemplate(picname, tmp, cv2.TM_CCOEFF_NORMED)  # 模板匹配
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            cv2.rectangle(picname_color, (max_loc), (max_loc[0] + w, max_loc[1] + h), (0, 0, 255), 3)  # 图片框体绘制
            checkpic = pic_path.replace("\\", '/').split('/')[-1]
            if max_val > threshold:
                cv2.imwrite(self.__seccess_path + "/" + "OK-" + checkpic, picname_color)
                return True
            else:
                # 以下为暴力匹配模式
                try:
                    picname_cut = picname[max_loc[1]:max_loc[1] + h, max_loc[0]:max_loc[0] + w]  # 最佳匹配点局部截图
                    orb = cv2.ORB_create()
                    kp1, des1 = orb.detectAndCompute(tmp, None)  # 计算特征点和描述子
                    kp2, des2 = orb.detectAndCompute(picname_cut, None)
                    bf = cv2.BFMatcher(cv2.NORM_HAMMING)  # 通过汉明距离计算特征点距离
                    matchs = bf.knnMatch(des1, trainDescriptors=des2, k=2)  # knn计算，1个匹配两个相似点
                    # 以0.75做阈值计算最合理的匹配点
                    good_match = [x for x, y in matchs if x.distance < 0.75 * y.distance]
                    sim = len(good_match) / len(matchs)
                    if sim >= 0.1:
                        cv2.imwrite(self.__seccess_path + "/" + "OK-" + checkpic, picname_color)
                        return True
                    else:
                        cv2.imwrite(self.__fail_path + "/" + "Fail-" + checkpic, picname_color)
                        return False
                except RuntimeError:
                    cv2.imwrite(self.__fail_path + "/" + "Fail-" + checkpic, picname_color)
                    return False
        except Exception as e:
            print("程序运行出错：", e)
        finally:
            Path(pic_cache_path).unlink(missing_ok=True)

    def assert_click(self, pic_path: str, hwnd: Union[str, None] = None) -> Union[tuple, None]:
        """
        通过图片查找坐标点进行点击，如果传入hwnd默认使用后台鼠标点击，
        hwnd代表窗口句柄，可以使用抓抓工具抓取需要的句柄传入，传入driver此项不用传入
        有driver状态下默认是进行网页操作，使用selenium进行坐标点击操作，操作不控制鼠标
        未传入driver默认为窗口gui界面操作，对于整个屏幕进行操作，此时屏幕需要放在界面对顶端，最好最大化显示
        :param pic_path: 需要查找点击的位置截图
        :param hwnd: 窗口的句柄，如果填写则默认使用后台鼠标点击，填写了传入了driver请不要填写此项
        :return: 当前函数运行计算的坐标，此坐标为以分辨率为基准的坐标点，失败返回None
        """
        shot_pic = self.__get_shot()
        try:
            tmp = cv2.imread(pic_path, 0)
            source = cv2.imread(shot_pic)
            tx, ty = tmp.shape[::-1]
            source_gray = cv2.cvtColor(source, cv2.COLOR_RGB2GRAY)
            # tx = int(tx / self.__scale)
            # ty = int(ty / self.__scale)
            # tmp = cv2.resize(tmp, (tx, ty))
            res = cv2.matchTemplate(source_gray, tmp, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            right_x = max_loc[0] + tx
            right_y = max_loc[1] + ty
            center_x = int(np.median((max_loc[0], right_x)))
            center_y = int(np.median((max_loc[1], right_y)))
            center_pos_dpi = (center_x, center_y)
            pic_color = cv2.circle(source, center_pos_dpi, 10, (0, 0, 255), 10)
            picname = pic_path.replace("\\", '/').split('/')[-1]
            cv2.imwrite(self.__click_path + '/' + 'Click-' + picname, pic_color)
            center_pos = (np.array(center_pos_dpi) / self.__size_scale).astype(int)
            if self.__driver is None:
                if hwnd is None:
                    win32api.SetCursorPos(center_pos)
                    time.sleep(0.5)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                else:
                    long_pos = win32api.MAKELONG(int(center_pos[0]), int(center_pos[1]))  # 转换坐标格式
                    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_pos)  # 按下左键
                    time.sleep(0.1)
                    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_pos)
            else:
                ActionChains(self.__driver).move_by_offset(*center_pos).click().perform()
                ActionChains(self.__driver).move_by_offset(-center_pos[0], -center_pos[1]).perform()
            return center_pos_dpi
        except RuntimeError as e:
            print("图片点击运行错误：", e)
        # finally:
        #     Path(shot_pic).unlink(missing_ok=True)
