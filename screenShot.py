# -*- codeing = utf-8 -*-
# @Time : 2021/5/9 15:01
# @Author : ZY
# @File : screenShot.py
# Software : PyCharm
"""
tkinter实现屏幕截图
源地址：https://blog.csdn.net/chengqiuming/article/details/78601078
在Linux上pip install pyscreenshot，然后把from PIL import imagegrab改成import pyscreenshot as ImageGrab，其他无需改动
"""
import os
import cv2
import tkinter
import tkinter.filedialog
import time
from PIL import ImageGrab


# import pyscreenshot as ImageGrab

class FreeCapture():
    """ 用来显示全屏幕截图并响应二次截图的窗口类
    """

    def __init__(self, root11, img):
        # 变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        # 屏幕尺寸
        screenWidth = root11.winfo_screenwidth()
        screenHeight = root11.winfo_screenheight()
        # 创建顶级组件容器
        self.top = tkinter.Toplevel(root11, width=screenWidth, height=screenHeight)
        # 不显示最大化、最小化按钮
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top, bg='white', width=screenWidth, height=screenHeight)
        # 显示全屏截图，在全屏截图上进行区域截图
        self.image = tkinter.PhotoImage(file=img)
        self.canvas.create_image(screenWidth // 2, screenHeight // 2, image=self.image)

        self.lastDraw = None

        # 鼠标左键按下的位置
        def onLeftButtonDown(event):
            self.X.set(event.x)
            self.Y.set(event.y)
            # 开始截图
            self.sel = True

        self.canvas.bind('<Button-1>', onLeftButtonDown)

        def onLeftButtonMove(event):
            # 鼠标左键移动，显示选取的区域
            if not self.sel:
                return
            try:  # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(self.lastDraw)
            except Exception as e:
                pass
            self.lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='green')

        def onLeftButtonUp(event):
            # 获取鼠标左键抬起的位置，保存区域截图
            self.sel = False
            try:
                self.canvas.delete(self.lastDraw)
            except Exception as e:
                pass

            time.sleep(0.5)
            # 考虑鼠标左键从右下方按下而从左上方抬起的截图
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            pic = ImageGrab.grab((left + 1, top + 1, right, bottom))
            # 弹出保存截图对话框
            #
            # fileName = tkinter.filedialog.asksaveasfilename(title='保存截图', filetypes=[('image', '*.jpg *.png')],
            #                                                 defaultextension='.png')
            #
            # if fileName:
            #     pic.save(fileName)
            # pic.save('E:\\picture2\\crop_pic.jpg')

            # 关闭当前窗口
            self.top.destroy()

        self.canvas.bind('<B1-Motion>', onLeftButtonMove)  # 按下左键
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)  # 抬起左键
        # 让canvas充满窗口，并随窗口自动适应大小
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)


def screenShot():
    """ 自由截屏的函数 (button按钮的事件)
    """
    #    print("test")
    root1.state('icon')  # 最小化主窗体
    time.sleep(0.2)
    im = ImageGrab.grab()
    # 暂存全屏截图
    im.save('temp.png')
    im.close()
    # 进行自由截屏
    w = FreeCapture(root1, 'temp.png')
    button_screenShot.wait_window(w.top)
    # 截图结束，恢复主窗口，并删除temp.png文件
    root1.state('normal')
    os.remove('temp.png')


####
root1 = tkinter.Tk()
root1.title('自由截屏')
# 指定窗口的大小
root1.geometry('200x200')
# 不允许改变窗口大小
root1.resizable(False, False)

# ================== 布置截屏按钮 ====================================
button_screenShot = tkinter.Button(root1, text='截屏', command=screenShot)
button_screenShot.place(relx=0.25, rely=0.25, relwidth=0.5, relheight=0.5)
# ================== 完 =============================================

try:
    # root1.withdraw()
    root1.mainloop()
except:
    root1.destroy()
