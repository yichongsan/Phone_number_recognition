from tkinter.filedialog import *
import cv2 as cv
import cv2
from PIL import Image, ImageGrab
import os
import tkinter
import tkinter.filedialog
import time
from PIL import ImageGrab,ImageTk
import pho_reg as pr
from tkinter.messagebox import askyesno
import numpy as np
from keras.models import *


class Application(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidget()
        self.master.protocol('WM_DELETE_WINDOW', self.closeWindow)

    def createWidget(self):

        self.f1 = Frame(root, bg="white")
        self.f1.place(relx=0, rely=0, relwidth=1, relheight=1)

        # self.f2 = Frame(self.f1, bg="white")
        # self.f2.place(relx=0.4, rely=0.08, relwidth=0.2, relheight=0.1)

        # 显示选择的文件
        self.show = Label(self.f1, font=("宋体", 12), bg="white")
        self.show.place(relx=0.1, rely=0.01, relwidth=0.8, relheight=0.03)

        # 显示识别后的手机号码
        # self.show_pho_num = Label(self.f1, font=("黑体", 18), bg="white")
        # self.show_pho_num.place(relx=0.3, rely=0.2, relwidth=0.4, relheight=0.03)

        # 四个个按钮
        Button(self.f1, text="选择图片", font=("黑体", 15), command=self.selectPic).place(relx=0.02, rely=0.08,
                                                                                                 relwidth=0.12,
                                                                                                 relheight=0.1)
        Button(self.f1, text="拍摄照片", font=("黑体", 15), command=self.capture).place(relx=0.02, rely=0.25,
                                                                                              relwidth=0.12,
                                                                                              relheight=0.05)

        self.btnQuit = Button(self.f1, text="退出",font=("黑体", 15), command=root.destroy).place(relx=0.02,rely=0.85,
                                                                                    relwidth=0.12,
                                                                                    relheight=0.1)

        self.sep = Button(self.f1,text="手动截取识别",font=("黑体",15),command=self.seperate).place(relx=0.02,rely=0.43,
                                                                                    relwidth=0.12,
                                                                                    relheight=0.1)

        self.btn_reg = Button(self.f1, text="自动识别", font=("黑体", 15))
        self.btn_reg["command"] = self.reg_pho
        self.btn_reg.place(relx=0.02, rely=0.6, relwidth=0.12, relheight=0.1)

        # 选择摄像头
        self.v1 = StringVar()
        self.v1.set("本地摄像头")
        self.om = OptionMenu(self.f1, self.v1, "USB摄像头", "本地摄像头")
        self.om["width"] = 10
        self.om.place(relx=0.02, rely=0.30, relwidth=0.12, relheight=0.05)

        # 显示输入图片
        self.label01 = Label(self.f1, text="显示输入图片", font=("宋体", 20), bg="GhostWhite")
        self.label01.place(relx=0.17, rely=0.08, relwidth=0.42, relheight=0.87)

        # 显示结果图片
        self.label02 = Label(self.f1, text="显示识别图片", font=("宋体", 20), bg="GhostWhite")
        self.label02.place(relx=0.60, rely=0.08, relwidth=0.35, relheight=0.45)

        self.label03 = Label(self.f1,text="显示识别的手机号",font=("宋体", 20), bg="GhostWhite")
        self.label03.place(relx=0.60, rely=0.57, relwidth=0.35, relheight=0.17)

        self.label04 = Label(self.f1, text="显示识别手动截取的手机号", font=("宋体", 20), bg="GhostWhite")
        self.label04.place(relx=0.60, rely=0.78, relwidth=0.35, relheight=0.17)

    def seperate(self):
        root1.deiconify()


    def selectPic(self):
        # 清空显示信息
        self.show["text"] = ""
        self.label03["text"] = ""
        # 显示选中的图片名字
        self.img_jpg = askopenfilename(title="上传文件", initialdir="E://gui/images", filetypes=[("图片文件", ".jpg")])
        self.img_gif = self.img_jpg.split('images')[0] + "/images/temp" + self.img_jpg.split('images')[1].split('.')[
            0] + ".gif"
        # print(self.img_gif)

        im = Image.open(self.img_jpg)
        if im.size[0] < im.size[1]:
            im = im.rotate(90)
        # print(im.size)
        im.save(self.img_gif)
        self.show["text"] = self.img_jpg
        # 显示选中的图片
        self.src_photo = PhotoImage(file=self.img_gif)
        self.label01["image"] = self.src_photo

    def capture(self):
        # print(self.v1.get())
        cap_flag = 0
        if self.v1.get() == "本地摄像头":  # 0
            cap_flag = 0
            print("调用本地摄像头进行拍摄")
        elif self.v1.get() == "USB摄像头":  # 1
            cap_flag = 1
            print("调用USB外置摄像头进行拍摄")

        cap = cv.VideoCapture(cap_flag)
        i = 0
        while True:
            ret, frame = cap.read()
            cv.imshow("capture", frame)
            k = cv.waitKey(1)
            if k == ord('b'):
                break
            elif k == ord('s'):
                i += 1
                pic_name_jpg = "./images/capture_" + time.strftime("%H-%M-%S", time.localtime()) + str(
                    i) + ".jpg"
                pic_name_gif = "./images/capture_" + time.strftime("%H-%M-%S", time.localtime()) + str(
                    i) + ".gif"
                self.img_jpg = pic_name_jpg
                self.img_gif = pic_name_gif
                cv.imwrite(pic_name_jpg, frame)
                break
        cap.release()
        cv.destroyAllWindows()
        # 转换格式
        im = Image.open(self.img_jpg)
        im.save(self.img_gif)
        # 显示选中的图片
        self.photo = PhotoImage(file=self.img_gif)
        self.label01["image"] = self.photo

    def reg_pho(self):
        self.crop_path, self.left_up_point = pr.preprocess(self.img_jpg)
        res, loc = pr.handwriting(self.crop_path)
        res = "手机号码：" + res
        self.label03["text"] = res
        self.label03["fg"] = "black"
        # print(res, loc)

        #红色矩形框
        self.rect_img_file = pr.drwaRect2(self.img_jpg, loc, self.left_up_point)

        im = Image.open(self.rect_img_file)
        self.img_rect_gif = self.rect_img_file.split(".")[0] + ".gif"
        im.save(self.img_rect_gif)
        # 显示选中的图片
        self.des_photo = PhotoImage(file=self.img_rect_gif)
        self.label02["image"] = self.des_photo

    def closeWindow(self):
        ans = askyesno(title='警告', message='关闭窗口吗？')
        if ans:
            self.del_file("./images/temp/")
            root.destroy()
        else:
            return

    def del_file(self, path):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                self.del_file(c_path)
            else:
                os.remove(c_path)
                print("正在删除文件：", c_path)



class FreeCapture():
    """ 用来显示全屏幕截图并响应二次截图的窗口类
    """
    def __init__(self, root1, img):
        # 变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        # 屏幕尺寸
        screenWidth = root1.winfo_screenwidth()
        screenHeight = root1.winfo_screenheight()
        # 创建顶级组件容器
        self.top = tkinter.Toplevel(root1, width=screenWidth, height=screenHeight)
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
            # fileName = tkinter.filedialog.asksaveasfilename(title='保存截图', filetypes=[('image', '*.jpg *.png')],
            #                                                 defaultextension='.png')
            #
            # if fileName:
            #     pic.save(fileName)
            pic.save('picture\\crop_pic.jpg')
            # 关闭当前窗口
            self.top.destroy()
            return pic

        self.canvas.bind('<B1-Motion>', onLeftButtonMove)  # 按下左键
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)  # 抬起左键
        # 让canvas充满窗口，并随窗口自动适应大小
        self.canvas.pack(fill=BOTH, expand=YES)


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

def show():
    global photo
    path='picture\\crop_pic.jpg'
    photo = ImageTk.PhotoImage(file=path)
    app.label02["image"]=photo
    # img_label = Label(root, imag=photo)
    # img_label.place(relx=0.65, rely=0.08, relwidth=0.35, relheight=0.5)
    # img_path = 'E:\\picture2\\crop_pic.jpg'
    # img_open=Image.open()
    image_path=os.path.abspath(path)
    return image_path

def recognition():
    recognition_model = load_model('model/verification_mode_23.h5', compile=False)
    CHARS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    CHARS_DICT = {char: i for i, char in enumerate(CHARS)}
    results = ''
    image_path='./picture/crop_pic.jpg'
    # 用 cv2 读取图片
    img = cv2.imread(image_path)
    img = cv2.resize(img, (164, 48))
    # img.show()
    # 定义一个的矩阵， 1：代表图片数量（因为我们一次识别一张）；164：代表图片宽度；
    # 48：代表图片高度；3：代表图片通道数
    X = np.zeros((1, 164, 48, 3), dtype=np.uint8)
    # 旋转图片
    x_temp = img.transpose(1, 0, 2)
    # 把旋转的图片赋值给 X
    X[0] = np.array(x_temp)
    # 预测
    y_pred = recognition_model.predict(X)
    # y_pred 的值是这种格式[3, 4, 63, 45, 7, 34, 46] 这种就是 CHARS 的下标
    y_pred = y_pred[:, 2:, :]
    # 下面代码就是把 y_pred 的值变为验证码值
    table_pred = y_pred.reshape(-1, len(CHARS) + 1)
    res = table_pred.argmax(axis=1)
    for i, one in enumerate(res):
        if one < len(CHARS) and (i == 0 or (one != res[i - 1])):
            results += CHARS[one]

    app.label04["text"]=results
    # print("手机号：" + results)
    # return results

if __name__ == '__main__':
    root = Tk()
    root.geometry("1800x900+5+5")
    root.title("快递单中的手写体电话号码识别系统")
    root["bg"] = "white"
    app = Application(master=root)
    ####
    root1 = Toplevel()
    root1.title('自由截屏')

    # 指定窗口的大小
    root1.geometry('100x80')
    # 不允许改变窗口大小
    root1.resizable(False, False)

    # ================== 布置截屏按钮 ====================================
    button_screenShot = Button(root1, text='截屏', command=screenShot)
    button_screenShot.pack()

    button_showCropImg=Button(root1,text='显示图片',command=show)
    button_showCropImg.pack()
    # label_Img=Label(root,text='显示图片')

    button_rec=Button(root1, text='识别', command=recognition)
    button_rec.pack()


    # ================== 完 =============================================
    root1.withdraw()
    root1.mainloop()
    root.mainloop()
