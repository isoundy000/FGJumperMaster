'''
测试从文件中读取图片并标注 保存标注文件

'''
import cv2
import numpy
from SampleLabel import SampleLabel
from  glob import glob
import os

save_path = "./samples/label/"
label_filename = "./samples/label/labels.txt"

slabel = SampleLabel(save_path, label_filename)

# 获取图片列表
img_path_list = glob('samples/unlabel/*.png')
# 生成迭代器
img_path_iter = iter(img_path_list)

# 提取文件名
def getImgName(img_path):
    # 'samples/unlabel/2018-01-25-22-19-42.png' ->  '2018-01-25-22-19-42.png'
    return img_path.split('/')[-1]

def nextImg(img_path_iter, slabel):
    '''
        使用迭代器， 遍历数组
    '''
    try:

        img_path = next(img_path_iter)
        img_name = getImgName(img_path)
        print("迭代至图片")
        print(img_path)

        img = cv2.imread(img_path)
        # 确认图片是否成功读入
        if img is None:
            return False
        else:
            slabel.updateImg(img, img_name=img_name)
            
            # 读入就将原来 unlabel的文件删除
            os.remove(img_path)
        return True
    except StopIteration:
        print("遍历结束")
        return False

# 初始读入第一个
nextImg(img_path_iter, slabel)
while True:
    keyValue = cv2.waitKey(0)
    # slabel.responseToKeyEvent(k, img=img)

    if keyValue == ord('e'):
        print('销毁窗口并保存')
        slabel.onDestroy()
        break

    elif keyValue == ord('n'):
        print("跳过，下一张图片")
        if not nextImg(img_path_iter, slabel):
            # 如果获取失败， 退出
            break
        
    elif keyValue == ord('j'):
        print("跳")
        # 这个涉及到ADB 这个程序里不实现。
        print("Jump")

    elif keyValue == ord('c'):
        print("取消标注")
        # update frame
        slabel.updateImg(slabel.img)

    elif keyValue == ord('s'):
        print("保存")
        if slabel.isMarkDone():
            slabel.saveImg()
            slabel.saveLabelInfo()
            slabel.printProcessOnCanvas("Save Done")
        
            # 自动载入下一张图片
            if not nextImg(img_path_iter, slabel):
                # 如果获取失败， 退出
                break
        else:
            # 标注未完成， 无法保存
            slabel.printProcessOnCanvas("Error: mark undone, could not save")


    elif keyValue == ord('h'):

            print('''
            标注工具-帮助菜单
            ==================================
            键盘 n - next 下一张图片
            键盘 c - cancel 撤销标注
            键盘 s - save 保存
            键盘 j - jump 跳跃
            键盘 h - help 帮助菜单
            键盘 e - exit 保存标记并退出系统
            ''')
