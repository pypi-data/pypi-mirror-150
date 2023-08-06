"""
# PicAssert图片断言工具：
anchor： 测码范晔
联系邮箱： 1538379200@qq.com
当前版本：v 1.3.1
通过图片拓展断言方式
> assert_exist会将图片在全局做一次模板匹配行为，当查找的图片大于或者等于设置的阈值的时候，程序将返回True，
当全局匹配的图片匹配度低于所设置的阈值时，程序将启动特征匹配模式，对前面相似度较近的区域进行截图，再次进行特征分析，
如果特征分析的结果判断为图片相似，程序将返回True，否则返回False
assert_click图片点击返回一个分辨率的坐标点

## 参数
1、Assert类参数
    driver:                 传入的selenium.webdriver.Chrome的实例，传入则视为操作web端而非gui，不填写默认当前gui界面
    lock_conf:              是否锁定配置文件输入，设置为True则从配置文件读取配置，在其他设备运行增加兼容性(需要先运行生成配置文件)
2、Assert().assert_exist()方法参数
    pic_path(str):          需要进行断言的图片路径，有传入driver则默认作用浏览器
    threshold(float|int):   整数或者浮点数，断言的判断阈值，0~1之间，默认0.7
3、Assert().assert_click()方法参数
    pic_path(str):          需要点击的目标图片，传入图片的路径，有传入driver默认作用浏览器
    hwnd(str):              字符串形式，应用于GUI界面，填写当前窗口的句柄，填写可以默认使用后台鼠标点击，不移动当前鼠标指针(传入driver的浏览器默认不用传入)

## 使用示例
```pycon
from PicAssert.Assert import Assert
from SafeDriver.drivers import driver, option


dr = driver()
ps = Assert(driver=dr, lock_conf=True)
res1 = ps.assert_exist(r'D:\test.png')
if res1 is True:
    print("找到图片")
else:
    print("未找到")
res2 = ps.assert_click(r'D:\test2.png')
print("当前点击坐标点：", res2)
```
## 其他说明即注意事项
1、因为不同设备的分辨率尺寸，很难做到完全的兼容使用，目前建议在本机进行操作
2、浏览器运行，现在暂时不增加无头模式的运行兼容，因为其截图和设备尺寸的兼容现在没有很好的方法解决
3、点击和断言的结果，都可以在.assert_cache文件夹中查看图片结果，断言成功为其passed文件夹，失败为failed文件夹，点击为click
    断言用红色方框标明断言的区域，click用红色点标明点击的位置
4、因为考虑后续可能会加入其他功能和更改，为了保证后续更新代码能正常运行，所以已设定需要以键值对形式传入参数
"""
import warnings
import cv2
from pathlib import Path
import os
import shutil
from typing import Union
import numpy as np
import win32api, win32con, win32gui, win32print
from PIL import ImageGrab
import time
import configparser
from selenium.webdriver.common.action_chains import ActionChains


class Assert:
    def __init__(self, *, driver=None, lock_conf=False):
        self.__driver = driver
        self.__lock_conf = lock_conf
        conf = configparser.ConfigParser()
        base_path = Path(__file__).cwd().resolve()
        self.__cache_path = base_path / '.assert_cache'
        self.__pass_path = self.__cache_path / 'passed'
        self.__fail_path = self.__cache_path / 'failed'
        self.__click_path = self.__cache_path / 'click'
        self.__conf_file = base_path / 'dev_conf.ini'
        shutil.rmtree(self.__cache_path, ignore_errors=True)
        self.__cache_path.mkdir(exist_ok=True)
        self.__pass_path.mkdir(exist_ok=True)
        self.__fail_path.mkdir(exist_ok=True)
        self.__click_path.mkdir(exist_ok=True)
        self.__cache_path = os.fspath(self.__cache_path)
        self.__pass_path = os.fspath(self.__pass_path)
        self.__fail_path = os.fspath(self.__fail_path)
        self.__click_path = os.fspath(self.__click_path)
        if lock_conf is False:
            h, v = self.__get_dpi()
            width, height = self.__get_size()
            self.__conf_file.unlink(missing_ok=True)
            self.__conf_file.touch(exist_ok=True)
            conf.add_section("resolution")
            conf['resolution']['width'] = str(h)
            conf['resolution']['height'] = str(v)
            conf.add_section("screensize")
            conf["screensize"]["width"] = str(width)
            conf["screensize"]["height"] = str(height)
            conf.add_section("scale")
            self.__scale = h / width
            self.__change_scale = 1
            conf["scale"]["scale"] = str(self.__scale)
            with open(self.__conf_file, 'w') as f:
                conf.write(f)
        else:
            if self.__conf_file.exists():
                conf.read(self.__conf_file)
                h, v = self.__get_dpi()
                width, height = self.__get_size()
                origin_h = conf["resolution"]["width"]
                self.__scale = h / width
                self.__change_scale = int(origin_h) / h
            else:
                raise FileExistsError("作为参考的 dev_conf.ini 文件不存在")
        if self.__driver:
            headless = self.__driver.execute_script("return window.navigator.userAgent")
            if 'headless' in headless.lower():
                warnings.warn("当前与无头模式不能很好兼容，请尽量不要使用无头模式运行", Warning)
            self.__driver.maximize_window()

    def __get_dpi(self):
        hdc = win32gui.GetDC(0)
        dev_h = win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES)
        dev_v = win32print.GetDeviceCaps(hdc, win32con.DESKTOPVERTRES)
        return dev_h, dev_v

    def __get_size(self):
        width = win32api.GetSystemMetrics(0)
        height = win32api.GetSystemMetrics(1)
        return width, height

    def __get_shot(self):
        time_now = time.strftime('%Y%m%d%H%M%S')
        shot_pic_path = self.__cache_path + '/' + time_now + '.png'
        if self.__driver is None:
            pic = ImageGrab.grab()
            pic.save(shot_pic_path)
        else:
            self.__driver.get_screenshot_as_file(shot_pic_path)
        return shot_pic_path

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
            picname = cv2.cvtColor(picname_color, cv2.COLOR_RGB2GRAY)  # 转换灰度图
            tmp = cv2.imread(pic_path, 0)
            w, h = tmp.shape[::-1]  # 获取维度即尺寸
            w = int(w / self.__change_scale)  # 图像缩放
            h = int(h / self.__change_scale)
            tmp = cv2.resize(tmp, (w, h))
            res = cv2.matchTemplate(picname, tmp, cv2.TM_CCOEFF_NORMED)  # 模板匹配
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 获取匹配值
            cv2.rectangle(picname_color, (max_loc), (max_loc[0] + w, max_loc[1] + h), (0, 0, 255), 3)  # 图片框体绘制
            checkpic = pic_path.replace("\\", '/').split('/')[-1]
            if max_val > threshold:
                cv2.imwrite(self.__pass_path + "/" + "OK-" + checkpic, picname_color)
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
                        cv2.imwrite(self.__pass_path + "/" + "OK-" + checkpic, picname_color)
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
            tx = int(tx / self.__change_scale)
            ty = int(ty / self.__change_scale)
            tmp = cv2.resize(tmp, (tx, ty))
            source_gray = cv2.cvtColor(source, cv2.COLOR_RGB2GRAY)
            res = cv2.matchTemplate(source_gray, tmp, cv2.TM_CCOEFF_NORMED)  # 模板匹配
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 获取模板匹配值
            right_x = max_loc[0] + tx
            right_y = max_loc[1] + ty
            center_x = int(np.median((max_loc[0], right_x)))  # 计算中心点坐标
            center_y = int(np.median((max_loc[1], right_y)))
            center_pos_dpi = (center_x, center_y)
            pic_color = cv2.circle(source, center_pos_dpi, 10, (0, 0, 255), 10)  # 图像标注
            picname = pic_path.replace("\\", '/').split('/')[-1]
            cv2.imwrite(self.__click_path + '/' + 'Click-' + picname, pic_color)
            center_pos = (np.array(center_pos_dpi) / self.__scale).astype(int)  # 中心点坐标数值转换
            if self.__driver is None:
                if hwnd is None:
                    # 鼠标前台点击
                    win32api.SetCursorPos(center_pos)
                    time.sleep(0.5)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                else:
                    # 鼠标后台点击
                    long_pos = win32api.MAKELONG(int(center_pos[0]), int(center_pos[1]))  # 转换坐标格式
                    win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_pos)  # 按下左键
                    time.sleep(0.1)
                    win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_pos)
            else:
                # selenium坐标点点击
                ActionChains(self.__driver).move_by_offset(*center_pos).click().perform()
                ActionChains(self.__driver).move_by_offset(-center_pos[0], -center_pos[1]).perform()
            return center_pos_dpi
        except RuntimeError as e:
            print("图片点击运行错误：", e)
        finally:
            Path(shot_pic).unlink(missing_ok=True)
        