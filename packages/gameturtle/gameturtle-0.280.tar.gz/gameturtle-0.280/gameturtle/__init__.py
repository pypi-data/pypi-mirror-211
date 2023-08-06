"""
   gameturtle.py   
   0.279版对0.273版进行了微调，主要是group和grab两个函数。
   增加了把RGB颜色三元组转换成以#开头的颜色转换函数，如(255,0,0)转换为#ff0000
   同时微调了pencolor命令。解决了不接收RGB三元组作为颜色报错问题。
   去掉了is_chinese函数，直接算字符的字节数，让single2multitext更加精准。
   新增了Key和Mouse类，进键盘和鼠标按键进行按键检测。
   增加了out_canvas的别名collide_edge
   新增make_rect，make_ellispe函数，用于生成矩形图和椭圆图，还有make_circle和make_square函数。
   新增replace_color替换颜色函数，角色的write命令，circle命令。
   新增pixelate像素化图形函数，mozaic马赛克图像处理函数。
   从tkinter.message模块导入了所有显示信息的命令对话框。
   single2multitext函数把gb2312改成了utf-8
"""
__author__ = '李兴球'
__date__ = '2023/06/01'
__blog__ = 'www.lixingqiu.com'
__version__ = 0.280

import os
import time
import math
import numpy as np
from random import randint
from tkinter import Tk,Canvas
from tkinter.messagebox import *
from moviepy.editor import ImageSequenceClip
from PIL import Image,ImageTk,ImageGrab,ImageOps,ImageDraw,ImageColor,ImageFont,ImageSequence


def replace_color(im,source,dest):
    """颜色替换函数，把source颜色换成dest颜色
       im：pillow图形对象,
       soucrce: 将要换的颜色值，如[255,0,0,255]为红色
       dest：目标颜色值，如[0,0,0,0]即透明色
       返回pillow图形对象，要求numpy模块和pillow模块支持
    """
    if isinstance(source,str):
        source = ImageColor.getrgb(source)
        source = source[0],source[1],source[2],255
    if isinstance(dest,str):
        dest = ImageColor.getrgb(dest)
        dest = dest[0],dest[1],dest[2],255
    
    im = im.convert("RGBA")
    im = np.array(im)
    mask = np.all(im==source,axis=-1) # 返回所有source颜色逻辑阵列
    im[mask] = dest
    return Image.fromarray(im)

def _rgbcolor2str( color):
     """把RGB三元组颜色转换成#开头的颜色字符串表示法，如(255,0,0)转换成#ff0000
     """
     try:
        r, g, b = color
     except (TypeError, ValueError):
        print("bad color arguments: %s" % str(color))
     return "#%02x%02x%02x" % (r, g, b)

def random_color():
    r = randint(0,255)
    g = randint(0,255)
    b = randint(0,255)
    return _rgbcolor2str((r,g,b))

def make_rect(fill='white',width=50,height=50,thickness=2,outline='black'):
    """生成矩形图"""
    if fill=='random' or fill=='rnd':fill = random_color()
    im = Image.new("RGBA",(width,height),fill)
    draw = ImageDraw.Draw(im, "RGBA")
    draw.rectangle([0,0,width-1,height-1],fill=fill,outline=outline,width=thickness)
    return im

def make_square(fill='white',length=50,thickness=2,outline='black'):
    return make_rect(fill=fill,width=length,height=length,
                     thickness=thickness,outline=outline)

def make_ellipse(fill='white',width=50,height=50,thickness=2,outline='black'):
    """生成椭圆形图"""
    if fill=='random' or fill=='rnd':fill = random_color()        
    im = Image.new("RGBA",(width,height))    
    draw = ImageDraw.Draw(im, "RGBA")    
    draw.ellipse([0,0,width-1,height-1],fill=fill,outline=outline,width=thickness)
    return im

def make_circle(fill='white',radius=25,thickness=2,outline='black'):
    w = radius * 2
    return make_ellipse(fill=fill,width=w,height=w,
                        thickness=thickness,outline=outline)

def make_polygon(fill='white',points=[(0,0),(50,0),(0,50)],thickness=2,outline='black'):
    """下一个版本"""
    pass

def make_cross(fill='white',length=20,thickness=2,outline='black'):
    """下一个版本"""
    pass

def make_triangle(fill='white',length=20,thickness=2,outline='black'):
    """下一个版本"""
    pass

 
def center_window(win):
    """
       居中显示窗口函数
    """
    win.update_idletasks()
    width = win.winfo_width()   # 自己的宽度
    height = win.winfo_height() # 自己的高度
    # 下面是获取屏幕中心点距离左上角win宽高分别一半时的那个坐标.
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

Tk.center = center_window                         # 给Tk类新增center方法

def single2multitext(line,length):
    """line：字符串,length:每行的字母长度，注意一个汉字占两个位"""
    txtbiao = []
    start = 0
    index = 0
    # w是一个计数器，记录当前行字母数(一个汉字算两个字母)是否超出length
    w = 0                                               
    current_line_length = 0
    while index < len(line):       
        w = w + len(bytes(line[index],'utf-8'))             # 根据字节长度决定位数3个字节一个汉字,所以写length90的话一行显示30汉字 
        current_line_length += 1
        if w>= length or line[index]=='\n':
            if line[index]=='\n':  current_line_length -= 1      # 不加入换行符
            txtbiao.append(line[start:start+current_line_length]) # current_line_length是动态的。
            start += current_line_length
            if line[index]=='\n':start+= 1
            w = 0
            current_line_length = 0
        index += 1
    txtbiao.append(line[start:])
    return "\n".join(txtbiao)            # 返回多行文本

def draw_rnd_rect(width,height,radius,bg='white'):
    """这是用来画圆角矩形的"""
    bgcolor = (0,0,0,0)
    im = Image.new("RGBA", (width, height), bgcolor)
    draw = ImageDraw.Draw(im, "RGBA")

    draw.rounded_rectangle((00, 0, width, height), radius,width=4,
                           outline=(200,200,220,255),fill=bg)
    start = 2*radius + 4
    end = 3 * radius -4 
    # 画缺口，以bg色填充一个矩形区域
    draw.line((start,height-3,end,height-3),width=4,fill=bg)
    
    return im

def _draw_small_bubble(width,height,radius,bg='white'):
    """这是用来画说话泡泡下面的小泡泡的"""
    bgcolor = (0,0,0,0)
    im = Image.new("RGBA", (width, height), bgcolor)
    draw = ImageDraw.Draw(im, "RGBA")
    xy = [2*radius,-radius//2,3*radius,radius//2]
    start = 0
    end = 180
    draw.chord(xy,start,end,outline=(200,200,220,255),fill=bg,width=3)
    xy = [1.75*radius,radius//2,2.5*radius,1.25*radius]
    draw.ellipse(xy,outline=(200,200,220,255),width=3,fill=bg)

    xy = [1.25*radius,radius,1.75*radius,1.5*radius]
    draw.ellipse(xy,outline=(200,200,220,255),width=3,fill=bg)

    start = 2*radius + 3
    end = 3 * radius -3 
    # 画缺口，以bg色填充一个矩形区域
    draw.line((start,0,end,0),width=6,fill=bg)    

    return im

def splice_image(im1,im2,mode='v'):
    """上下或左右拼接两张图片
       im1,im2是pillow图形对象，
       mode是模式，mode='v'则是上下拼接
       mode='h',是左右拼接模式。
    """
    w1,h1 = im1.size
    w2,h2 = im2.size    
    if mode=='v':
        w = max(w1,w2)
        h = h1 + h2
        x,y = 0,h1                    # 下面这个图的粘贴坐标
    elif mode=='h':
        w = w1 + w2
        h = max(h1,h2)
        x,y = w1,0                    # 右边这图的粘贴坐标 
    im = Image.new("RGBA", (w, h), (0,0,0,0))

    im.paste(im1,(0,0))               # 在im上贴上im1,上或左
    im.paste(im2,(x,y))               # 在im上贴上im2,下或右
    return im
spliceimage = splice_image

def _make_say_bubble(s,margin,radius,bg='white',fg='black',fz=14):
    """生成说话泡泡图"""    
    if len(s)<6:s = s + ' ' * (6-len(s))
    s = single2multitext(s,24)                           # 24是一行的字母数(一汉字为两字母数)
    txtimg = txt2image(s,fontsize=fz,color=fg,bgcolor=bg)# 文本转多行图象
    width = txtimg.width + margin*2                      # 说话泡泡的宽度
    height = txtimg.height + margin * 2                  # 说话泡泡上面矩形的高度
    im1 = draw_rnd_rect(width,height,radius,bg=bg)       # 说话泡泡上面的圆角矩形
    im2 = _draw_small_bubble(width,28,radius,bg=bg)      # 说话泡泡下面的“小泡泡”   
    bubble = splice_image(im1,im2)                       # 拼接图片‘说话泡泡’
    # 填充白色，这是由于用arc画的是空心的，无法填充为白色，所以拼接后用下面的命令再次填充
    xy = radius*2.5,height+radius//3
    ImageDraw.floodfill(bubble, xy, ImageColor.getrgb(bg), thresh=50)
    bubble_right = bubble.transpose(Image.FLIP_LEFT_RIGHT)# 左右翻转 
    bubble_right.paste(txtimg,(margin,margin))           # 把文字贴粘到‘说话泡泡里'
    bubble.paste(txtimg,(margin,margin))           # 把文字贴粘到‘说话泡泡里'
    
    return bubble,bubble_right                     # 返回左右说话泡泡

   
def makegif(images,filename=None,duration=200,quality=65,ext='.png',loop=False):
   """合帧
      images: 列表或者一个路径。如果是列表，则里面的是用图形对象。如果是路径，则是一个字符串而已
      filename: 输出的gif文件名
      duration: 每帧播放的毫秒时间
      quality: 压缩质量，只对jpg格式的图形有效，即模式为RGB
      ext: 如果images是一个文件夹路径，那么这个参数才有效，否则忽略，表示扩展名。
      loop：生成的gif图是否循环播放。
      注意path下面的文件名要是这样的:0.png,1.png,2.png....。
    """
   if isinstance(images,(list,tuple)):
        frames = images
   else:                                          # 否则认为是一个路径
       amounts = len([ image for image in os.listdir(images) if os.path.splitext(image)[-1] == ext ])
       images = [ images + os.sep + str(i) + ext for i in range(0,amounts)]
       frames = [Image.open(frame) for frame in images]

   pic = frames[0]
   if filename==None:filename=str(time.time()) + ".gif"
   pic.save(filename, save_all=True,append_images=frames[1:],
            optimize=True,quality=quality,duration=duration,loop=loop)

def makevideo(images,filename=None,fps=30, durations=None, with_mask=True, ismask=False, load_images=False):
    """images:是一个列表,列表中是pillow图形对象,或者是一个文件夹路径名"""
    if isinstance(images,list):
        images = [np.array(im) for im in images]
    clip = ImageSequenceClip(images, fps=fps,durations=durations,with_mask=with_mask,ismask=ismask,load_images=load_images)
    if filename:
        clip.write_videofile(filename, fps=fps)
    else:
        return clip
    
def txt2images(string,width=480,height=360,background=None,margin=68,fontsize=18,
               fontfile="simkai.ttf",fgcolor=(150,200,200,255),bgcolor=(0,0,0,0),compress=False):
    
    """文本转逐帧图像,string:字符串，width:宽度，height:高度,background:背景图或颜色,
       margin:边距，fontsize:字体大小，fgcolor:字的颜色，bgcolor:背景色

    """
    if background == None:
       base = Image.new("RGBA",(width,height),bgcolor)  # 新建图形
    else:
       base = Image.open(background)
       base = base.convert("RGBA")
       
    width,height = size = base.size

    fnt = ImageFont.truetype(fontfile,fontsize)
      
    txt = Image.new("RGBA",size,(0,0,0,0))            # 新建空白图像.
    d = ImageDraw.Draw(txt)
    
    x = margin
    y = margin
    frames = []                                       # 空列表
    index = 0
    amount = len(string)
    w,h = d.textsize('',font=fnt,spacing=18)          # 仅用来生成初始w,h
    while True:         
          char = string[index]
          if char=='\n':                              # 如果是换行
             y = y + h*1.4                            # 那么y坐标下移
             x = margin - w                           # x坐标定位，注意减了w                 
          else:
             w,h = d.textsize(char,font=fnt,spacing=18)
             if x + w > width - margin:                 # 超过最右边界则换行或结束循环
                 if  y + h > height - margin:
                     break
                 else:
                     y = y + h*1.4
                     x = margin    
             d.text((x,y),char,font=fnt,fill=fgcolor)   # 在txt图形上写字         
             out = Image.alpha_composite(base, txt)     # 合成
             if compress : out =  out.convert('RGB')
             frames.append(out)                         # 写一个字后就保存
          index = index + 1
          if index == amount :break
          x = x + w
    return  frames

def splitgif(imagepath):
    """拆帧，返回帧图形对象列表和图形对象本身(以便使用im.info字典查询信息)"""
    frames = []
    ext = os.path.splitext(imagepath)[-1]
    ext = ext.lower()
    im = Image.open(imagepath)
    if ext == '.gif' or '.webp':                 # 如果是gif/webp扩展名则拆帧        
        for frame in ImageSequence.Iterator(im):
            frames.append(frame.copy())
    else:
        frames.append(im)
    return frames,im
        
def txt2image(txt,fontfile="simkai.ttf",fontsize=64,
              color=(255,0,0,255),stroke=None,bgcolor=(0,0,0,0)):
    """
        文本转图像实用函数,支持多行文本,默认为楷体,返回pillow图形对象。
        txt：文本        
        fontfile:ttf字体文件
        fontsize:字体大小
        color:颜色,通过写alpha值可支持半透明图形。如设定color=(0,0,255,127)蓝色透明字
        stroke：二元组，第一个值是一个整数，第二个值为描边颜色
    """    
    windowsdir = os.environ.get('WINDIR')
    try:
       fnt = ImageFont.truetype(fontfile,fontsize)
    except:
       fontfile = 'msyh.ttc'                      # win10的微软雅黑为ttc
       p = windowsdir + os.sep + 'fonts' + os.sep + fontfile
       fnt = ImageFont.truetype(p,fontsize)
    
    size = fnt.getsize(txt)                       # 获取文本的宽高

    pic = Image.new('RGBA', size,color=bgcolor)
    d = ImageDraw.Draw(pic)
    if stroke == None:
       size = d.multiline_textsize(text=txt, font=fnt,spacing=4)
    else:
       size = d.multiline_textsize(text=txt, font=fnt,spacing=4,stroke_width=stroke[0])
    w,h = size
    size = w,h+4
    pic = pic.resize(size)                        # 根据多行文本尺寸重调图形
    d = ImageDraw.Draw(pic)                       # 重新生成绘图对象
    
    if stroke == None:
        d.multiline_text((0,0),txt,font=fnt,fill=color)
    else:
        d.multiline_text((0,0),txt,font=fnt,fill=color,stroke_width=stroke[0], stroke_fill=stroke[1])
        
    return pic

def turtleimage(color='green'):
    """画海龟图形,返回图形"""
    size = (49,37)                 # 海龟图的分辨率
    cors = ((48.0, 18.0), (44.0, 22.0), (36.0, 20.0), (30.0, 26.0),
            (34.0, 32.0), (32.0, 36.0), (26.0, 30.0), (18.0, 32.0),
            (10.0, 28.0), (4.0, 34.0), (0.0, 30.0), (6.0, 26.0),
            (2.0, 18.0), (6.0, 10.0), (0.0, 6.0), (4.0, 2.0),
            (10.0, 8.0), (18.0, 4.0), (26.0, 6.0), (32.0, 0.0),
            (34.0, 4.0), (30.0, 10.0), (36.0, 16.0), (44.0, 14.0))
    
    im = Image.new("RGBA",size)
    d  = ImageDraw.Draw(im)
    d.polygon(cors,fill=color)
    return im

def _find_pixels(im_array,pixel,ignore_alpha=True):
    """im_array：二维像素阵列
       pixel：RGBA三或四元组或列表
       ignore_alpha:：是否忽略alpha通道
       返回行列号集合。
    """
    if ignore_alpha:
        im_array = im_array[:,:,:3]
        pixel = pixel[:3]
    pixel = np.array(list(pixel),dtype=np.uint8)
    rows,cols = np.where(np.all(im_array==pixel, axis=-1))
    rc = set(zip(rows,cols))
    return rc
    
def _make_croped_area(overlaped,rectangle):
    """
       overlapped是rectangle上面的一个子矩形。
       但它们的坐标都是相对于画布坐标系的。
       这个函数返回overlaped相对于rectangle左上角坐标的待剪裁区域。
       overlaped:Rect对象，
       rectangle:Rect对象，
       返回left,top,right,bottom，相对于rectangle的
    """
    left = overlaped.left - rectangle.left
    top = overlaped.top - rectangle.top
    right = left + overlaped.width
    bottom = top + overlaped.height
    return left,top,right,bottom

def _make_mask(image,area):
    """
       image:pillow图形对象
       area:图形对象上的一个区域(left,top,right,bottom)
    """
    im = image.crop(area)          # 根据area剪裁图形
    im_array = np.array(im)        # 转换成二维阵列
    mask = im_array[:,:,3] > 127   # 大于127的值变成1，否则变为0
    mask.dtype=np.uint8            # 类型转换
    return mask,im_array           # 返回mask和图形的二维数组

# 给画布增加一个方法，用来获取鼠标指针在画布的坐标
def _mouse_pos(self):    
     """获取鼠标指针的坐标，相对于画布的"""
     root = self.winfo_toplevel()
     mx = self.winfo_pointerx() - root.winfo_rootx() - self.winfo_x()
     my = self.winfo_pointery() - root.winfo_rooty() - self.winfo_y()
     return mx,my
Canvas.mouse_pos = _mouse_pos
Canvas.mouse_position = _mouse_pos
Canvas.mousepos = _mouse_pos
Canvas.mouseposition = _mouse_pos

# 给画布增加一个方法，用来截图
def _grab(self,margin=2):
    """截画布为图形对象，margin是边距"""
    root = self.winfo_toplevel()    
    x = root.winfo_rootx() + self.winfo_x()        
    y = root.winfo_rooty() + self.winfo_y()
    width = self.cget('width')
    height = self.cget('height')
    right = x + int(width)
    bottom = y + int(height)
    size = (x+margin,y+margin,right-margin,bottom-margin)
    self.update()
    im = ImageGrab.grab(size)
    return im        
Canvas.grab = _grab

# 给画布增加一个方法，用来获取画布中心点坐标
def _center(self):
    width = self.cget('width')
    height = self.cget('height')    
    w = int(width)
    h = int(height)
    return w/2,h/2
Canvas.center = _center

def group(canvas,tag):
    """在画布中查找标签为tag的所有角色，返回角色列表"""
    items = canvas.find_withtag(tag)  # 在画布上查找标签为tag的item  
    sprites = list(map(lambda i:Sprite.sprites[i],items))
    return sprites
Canvas.group = group
Canvas.listen = Canvas.focus_force                             # 定义别名
class Rect:
    """
    操作矩形的类，有left,top,right,bottom,width和height属性。
    有collidepoint，isintersect用来判断两个矩形是否相交的方法，
    overlap方法用来返回和另一个矩形的重叠区域，也用一个矩形表示。
    还有contain包含方法，用来判断一个矩形是否完全包含另一个矩形。 
    """
    def __init__(self, x,y,w,h):
        """
        x,y,w,h：最左x坐标，最顶y坐标，宽度，高度
        """
        self.resize(x,y,w,h)

        self.raw_left = x                # 原始x坐标
        self.raw_top = y                 # 原始y坐标
        self.raw_right = x + w           
        self.raw_bottom = y + h 
        self.raw_width = w
        self.raw_height = h
        
    def resize(self,x,y,w,h):
        self.left = x                    # 左上角x坐标
        self.top = y                     # 左上角y坐标
        self.width = w                   # 矩形宽度
        self.height = h                  # 矩形高度
        self.right = x + w               # 矩形右下角x坐标
        self.bottom = y + h              # 矩形右下角y坐标
        
    def collidepoint(self, x,y):
        """
        测试一个点是否在矩形内，在边界上也算。
        """
        c1 = (x >= self.left) and  (x <= self.right) # 在左右之间
        c2 = (y >= self.top) and (y <= self.bottom)  # 在上下之间
        return  c1 and  c2             # 两个条件同时成立则返回真 

    def isintersect(self, other):
        """
        测试是否和另一个矩形有重叠区域。
        """
        if self.left > other.right: return False
        if self.right < other.left: return False
        if self.bottom < other.top: return False
        if self.top > other.bottom: return False
        return True 

    def overlap(self, other):
        """
        返回和另一个矩形的重叠区域。
        """
        left = max((self.left, other.left))
        bottom = min((self.bottom, other.bottom))    # 两个矩形更大的bottom值
        right = min((self.right, other.right))
        top = max((self.top, other.top))             # 两个矩形更小的top        
        if (right - left)>=1 and (bottom-top)>=1 :
            return Rect(left,top,right-left,bottom-top)
        else:
            return None

    def contain(self, other):
        """
        如果other这个矩形包含在self内，则返回真。
        """
        if other.left >= self.left and other.right <= self.right:
            if other.top >= self.top and other.bottom <= self.bottom:
                return True
        return False

    def move(self,dx,dy):
        """
           在水平和垂直方向移动矩形分别为dx和dy个单位
        """
        self.left = self.left + dx
        self.top = self.top + dy
        
        self.right = self.left + self.width
        self.bottom = self.top + self.height

    def scale(self,scalew,scaleh=None,pos='center'):
        """缩放矩形，pos缩放的中心点，它有2个值，分别是:
           lefttop,center。
           scalew：横向缩放因子，为一个小数。
           scaleh：纵向缩放因子，为一个小数。
        """
        if scaleh == None:scaleh = scalew
        left = self.raw_left             # 记录最左x坐标
        top = self.raw_top               # 记录最顶y坐标
        right = self.raw_right           # 记录最右x坐标 
        bottom = self.raw_bottom         # 记录最下y坐标
        new_width = self.raw_width * scalew   # 新宽度
        new_height = self.raw_height * scaleh # 新高度
        if pos == 'lefttop' or pos == 'topleft':
            self.resize(left,top,new_width,new_height)                 
        elif pos == 'center' or pos=='' or pos==None:
            dw = self.raw_width - new_width  
            dh = self.raw_height - new_height 
            left = left + dw/2
            top = top + dh /2
            self.resize(left,top,new_width,new_height)
            
    def cross_left(self):
        """矩形内十字架左部"""
        if self.width < 3 or self.height <3:return self
        top = self.top + self.height//3
        w = self.width//3
        h = self.height//3        
        return Rect(self.left,top,w,h)        
        
    def cross_right(self):
        """矩形内十字架右部"""
        if self.width < 3 or self.height <3:return self
        left = self.left + self.width * 2 //3
        top = self.top + self.height//3
        w = self.width//3 
        h = self.height//3  
        return Rect(left,top,w,h)        
        
    def cross_top(self):
        """矩形内十字架上部"""
        if self.width < 3 or self.height <3:return self
        left = self.left + self.width//3
        w = self.width//3
        h = self.height//3 
        return Rect(left,self.top,w,h)

    def cross_bottom(self):
        """矩形内十字架下部"""
        if self.width < 3 or self.height <3:return self
        left = self.left + self.width//3
        top = self.top + self.height * 2//3
        w = self.width//3
        h = self.height//3     
        return Rect(left,top,w,h)
    
    def __repr__(self):
        """把自己显示为供解释器更好读的方式"""
        return "%s(left:%s,top:%s,width:%s,height:%s)@%d" % \
               (self.__class__.__name__, self.left, self.top, \
                self.width, self.height ,id(self))
    
class Sprite:
    sprites = {}                               # 所有item:角色字典
    def __init__(self,canvas,frames=None,pos=None,visible=True,heading=0,tag='sprite'):
        """
           canvas：海龟所在的画布
           frames：用Image.open打开的图形列表。
           pos：坐标
           visible：可见性，True或者Faslse。
           heading：初始方向
           tag：标签用于分组，值为字符串，或者数据为字符串的元组。
        """    
        self._canvas = canvas                   # 画布
        self._root = self._canvas.winfo_toplevel()
        canvas.update()                         # 更新一下，要不然获取不到宽高
        self._cv_width = self.canvas_width()        # 画布边框这里应该是获取
        self._cv_height = self.canvas_height()       
        self.item = self._canvas.create_image((0,0),image='',tags=tag) # 一个图形对象
        Sprite.sprites[self.item] = self    # 把自己存在所有角色字典中
        # 说话泡泡配置
        self._bubble_right =  self._canvas.create_image((0,0),image='',anchor='se')
        self._bubble_left = self._canvas.create_image((0,0),image='',anchor='sw')
        
        self._current_bubble = ''
        self._saying = False                    # 描述是否正在说话中的逻辑变量
        self._saypic_right = ''
        self._saypic_left = ''
        
        self._pendown = False                   # 落笔为否
        self._pensize = 2                       # 画笔线宽
        self._pencolor = 'blue'                 # 画笔颜色
        self._fillcolor = 'yellow'              # 填充颜色
        self._fillpath = [] 
        self._bubble = None                     # 说话泡泡项目号
        if pos==None:                           # 不写坐标，默认为画布中间
            pos = self._cv_width/2,self._cv_height/2             

        if not visible:
            self.hide()                        # 如果不可见，则调用hide方法
        else:
            self._visible = True
        self._heading = heading                 # 初始朝向        
        self._stretchfactor = [1,1]             # 造型的伸展因子
        self._rotationstyle = 0                # 旋转模式0:all around, 1:left-right,2:no(don't rotate),
        # 如果frames为空，下面的方法会加载内置的海龟图做为角色的造型 
        self._loadshapes(frames)                # 加载frames造型列表,frames是pillow图形对象        
        
        self.goto(pos) 
        self._lineitems = []                    # 保存线条项目id
        self._fillitems = []                    # 保存填充项目id
        self._dotitems = []                     # 打的每个圆点项目id
        self._circleitems = []                  # 打的每个空心圆项目id
        self._writeitems = []                   # 写字项目id列表
        self._stampitems = []                   # 保存图章列表
        self._stampimages = []                  # 保存图章的PhotoImage造型列表(原因是需要全局引用)
        self._alive = True                      # 描述是否活着的逻辑变量
        

    def canvas_width(self):
        """返回角色所在的画布宽度，设置宽度直接用canvas.config(width=400)"""
        return int(self._canvas.config('width')[-1])
    def canvas_height(self):
        """返回角色所在的画布高度，设置宽度直接用canvas.config(height=400)"""
        return int(self._canvas.config('height')[-1])
        
    def setrotmode(self,mode=1):
        """设置旋转模式，默认为左右翻转:)。
           mode:值为0表示角色将会360度旋转,1表示只会左右翻转，2表示不旋转 
        """
        if mode in (0,1,2,360):
           self._rotationstyle = mode
           self._process_shape()                # 在造型列表中修改造型
           self._setshape()                     # 还需要重新设定造型并显示造型

    def getrotmode(self):
        """得到旋转模式"""
        return self._rotationstyle

    def shapesize(self,width=None,length=None):
        """角色变形，设定伸展因子
           width：以角色前进方向为准的造型的横向伸展因子
           length：以角色前进方向为准的造型的纵向伸展因子
           如果一个参数也不写，则返回伸展因子列表。
        """
        if width==None and length==None:
            return self._stretchfactor
        elif width!=None and length==None:
            length = width
        self._stretchfactor = [width,length]
        self._process_shape()
        self._setshape()                        # 设置造型         
        
    def pencolor(self,*args):
        if args:                              # 如果有参数
            if len(args)==1:                  # 有一个参数认为是字符串或元组
                if isinstance(args[0],str):                    
                    self._pencolor = args[0]
                else:
                    self._pencolor = _rgbcolor2str(*args)
            elif len(args)>1:
                self._pencolor = _rgbcolor2str(args)
        else:
            return  self._pencolor
        
    def fillcolor(self,*args):
        if args:                              # 如果有参数
            if len(args)==1:                  # 有一个参数认为是字符串或元组                
               if isinstance(args[0],str):
                    self._fillcolor = args[0]
               else:
                    self._fillcolor = _rgbcolor2str(*args)
                    
            elif len(args)>1:
                self._fillcolor = _rgbcolor2str(args)
        else:
            return  self._fillcolor
        
    def color(self,*args):
        if args:
            l = len(args)
            if l == 1:
                self._pencolor = self._fillcolor = args[0]
            elif l == 2:
                self._pencolor ,self._fillcolor = args
            elif l == 3:
                self._pencolor = self._fillcolor = _rgbcolor2str(args)
        else:
            return self._pencolor, self._fillcolor
        

    def pendown(self):
        """落笔，别名是down"""
        self._pendown = True

    def penup(self):
        """抬笔，别名是up或者pu"""
        self._pendown = False

    def pensize(self,w=None):
        """设定或返回线宽"""
        if w==None:
            return self._pensize
        self._pensize = w

    def dot(self,diameter=None,color=None):
        """打圆点"""
        if diameter==None:diameter=2
        if color==None:color=self._pencolor
        radius = diameter/2
        x,y = self.position()
        x0,y0 = x - radius,y - radius
        x1,y1 = x + radius,y + radius
        item = self._canvas.create_oval(x0,y0,x1,y1,fill=color,width=0)
        self._dotitems.append(item)
        self._canvas.tag_raise(self.item)
        return item
    
    def circle(self,radius=None,color=None):
        """以角色为圆心画圆形"""
        if radius==None:radius=2
        if color==None:color=self._pencolor
        x,y = self.position()
        x0,y0 = x - radius,y - radius
        x1,y1 = x + radius,y + radius
        item = self._canvas.create_oval(x0,y0,x1,y1,fill='',
                                        outline=color,width=self._pensize)
        self._circleitems.append(item)
        self._canvas.tag_raise(self.item)
        return item
    
        
    def _getrect(self):
        """
          获取当前造型的矩形,
          返回Rect(left,top,width,height)对象
        """
        w,h = self._current_shape.size    # 造型宽高
        x,y = self.pos()                  # 中心点坐标
        left = int(x) - int(w/2) 
        top = int(y) - int(h/2)
        return Rect(left,top,w,h)
    
    def _cross_left(self):
        """获取角色十字架左部分矩形"""
        r = self._getrect()
        return r.cross_left()
    
    def _cross_right(self):
        """获取角色十字架右部分矩形"""
        r = self._getrect()
        return r.cross_right()

    def _cross_top(self):
        """获取角色十字架上部分矩形"""
        r = self._getrect()
        return r.cross_top()
    
    def _cross_bottom(self):
        """获取角色十字架下部分矩形"""
        r = self._getrect()
        return r.cross_bottom()
    
    def rect_overlap(self,other,area=None):
        """和另一个角色的矩形碰撞，两个角色要在同一画布上。
           返回相对于画布的重叠区域。
        """
        if self._canvas != other._canvas:return None
        if self._visible == False or other._visible == False:return None
        if area==None:
            self._rect = self._getrect()
        elif area =='left':
            self._rect = self._cross_left()
        elif area =='right':
            self._rect = self._cross_right()
        elif area =='top':
            self._rect = self._cross_top()
        elif area =='bottom':
            self._rect = self._cross_bottom()

        other._rect = other._getrect()
        r = self._rect.overlap(other._rect)
        return r       
    
    def left_collide(self,other):
        """自己的左边区域和另一个角色，或者另一种颜色的碰撞。
           other：角色或者颜色，如果是角色，返回矩形重叠区域，
           如果是颜色，返回的和每个角色的(array,im_a,im_b,r)信息。
        """
        if isinstance(other,Sprite):          # 如果other是Sprite对象
            return self.rect_overlap(other,area='left')
        elif isinstance(other,(tuple,list,str)):  # 如果是序列则认为是颜色
            return self.collide_color(color=other,area='left')
    
    def right_collide(self,other):
        """自己的右边区域和另一个角色，或者另一种颜色的碰撞。
           other：角色或者颜色，如果是角色，返回矩形重叠区域，
           如果是颜色，返回的和每个角色的(array,im_a,im_b,r)信息。
        """
        if isinstance(other,Sprite):
            return self.rect_overlap(other,area='right')
        elif isinstance(other,(tuple,list,str)):  # 如果是序列则认为是颜色
            return self.collide_color(color=other,area='right')
    
    def top_collide(self,other):
        """自己的上边区域和另一个角色，或者另一种颜色的碰撞。
           other：角色或者颜色，如果是角色，返回矩形重叠区域，
           如果是颜色，返回的和每个角色的(array,im_a,im_b,r)信息。
        """
        if isinstance(other,Sprite):
            return self.rect_overlap(other,area='top')
        elif isinstance(other,(tuple,list,str)):  # 如果是序列则认为是颜色
            return self.collide_color(color=other,area='top')
    
    def bottom_collide(self,other):
        """自己的下边区域和另一个角色，或者另一种颜色的碰撞。
           other：角色或者颜色，如果是角色，返回矩形重叠区域，
           如果是颜色，返回的和每个角色的(array,im_a,im_b,r)信息。
        """
        if isinstance(other,Sprite):
            return self.rect_overlap(other,area='bottom')
        elif isinstance(other,(tuple,list,str)):  # 如果是序列则认为是颜色            
            return self.collide_color(color=other,area='bottom')
    
    def _pixels_overlapped(self,other):
        """
           和另一个角色的像素重叠检测，两个角色要在同一画布上。
           返回空或者重叠区域所有像素点的行列号及两图形分别的重叠子图array。
        """
        r = self.rect_overlap(other)        
        if not r : return None
        r_a = _make_croped_area(r,self._rect)  # 返回在self图上的待剪区域
        r_b = _make_croped_area(r,other._rect) # 返回在other图上的待剪区域
        mask_a,im_a = _make_mask(self._current_shape,r_a)  # 剪后形成mask_a
        mask_b,im_b = _make_mask(other._current_shape,r_b)
        mask = mask_a  + mask_b                # 最终所需要的mask  
        overlapped = np.argwhere(mask == 2)    # 所有像素重叠点的行列号
        
        if overlapped.size > 0:
            return overlapped,im_a,im_b,r,other # im_a和im_b都是numpy array 
        else:
            return None
            
    def _first_overlapped_pixel(self,other,ignore_alpha=True):
        """和另一个角色的像素重叠检测，两个角色要在同一画布上。
           返回第一个重叠点相对于画布的坐标和在两张图片上相应点的像素值。
        """
        result = self._pixels_overlapped(other)
        if not result : return False
        overlapped_pixels,im_a,im_b,r,other = result           
        top,left = overlapped_pixels[0]       # 第一个点的行列号          
        x = left + r.left                     # 相对于画布的x坐标
        y = top + r.top                       # 相对于画布的y坐标
        p1 = im_a[top,left]
        p2 = im_b[top,left]
        if ignore_alpha:
            p1 = p1[:3]
            p2 = p2[:3]
        return x,y,tuple(p1),tuple(p2)  # 注意只返回第一个点

    def near(self,other,distance):
        """通过距离进行的‘碰撞检测’
           self和other的距离小于或者等于distance则认为发生碰撞,
           适合于圆形角色。
        """
        return self.distance(other) <= distance
        
    def collide(self,other,mode='pixel', ignore_alpha=True,distance=None):
        """和另一个角色的碰撞检测方法，可以用矩形，像素级与距离三种模式
           other：Sprite对象
           mode：碰撞检测的模式，pixel为像素级，rect为矩形，distance为距离
           ignore_alpha：是否忽略alpha通道
           
           根据mode返回不同的值
        """
        if mode == 'pixel':
            return self._first_overlapped_pixel(other,ignore_alpha=ignore_alpha)
        elif mode == 'rect':
            return self.rect_overlap(other)
        elif mode == 'distance':
            if distance == None:
                distance = self._rect.width
            return self.near(other,distance)

    def _overlapped_items(self,area=None):
        """
           查找自己的矩形区域，或者部分矩形区域的画布items。
           area的值为left,top,right,bottom，用于区分基于十字架模型的碰撞区域。
           返回item集合。
        """
        if area==None:
           a,b,c,d = self._canvas.bbox(self.item) # 注意和自定义的_getrect返回的矩形的区别
        else:
            if area=="left":
               r = self._cross_left()  # 这里返回的是自己定义的Rect对象              
            if area=="right":
               r = self._cross_right()
            if area=="top":
               r = self._cross_top()
            if area=="bottom":
               r = self._cross_bottom()
            a,b,c,d = r.left,r.top,r.left + r.width,r.top + r.height            

        items = set(self._canvas.find_overlapping(a,b,c,d))
        items.remove(self.item)             # 移除自己
        return items        
        
    def collide_tag(self,tag=None,area=None,pixel=True):
        """根据area找出重叠的item，然后检测item是否对应角色。
           再调用_pixels_overlapped和每个角色进行检测，看有没有发生像素级重叠。
           有则返回和其它所有角色发生的像素等信息。
           tag参数用于分组。area的值为left,top,right,bottom，
           用于区分基于十字架模型的碰撞区域。
           pixel参数用来决定是否还要进一步进行像素级检测。
        """            
        items = self._overlapped_items(area=area) # left,top,right,bottom        
        if tag != None:    # 相应标签的角色才会检测
            items = items.intersection(set(self._canvas.find_withtag(tag))) 
         
        others = [Sprite.sprites.get(item) for item in items] # item对应的角色
        others = list(filter(bool,others))                    # 去掉None,(不是角色) 
        if not others:return False                            # 没有碰到其它角色

        if pixel==False:return others          # 如果pixel为假，返回所有找到的角色
        # 下面的results是一个个的(array,im_a,im_b,r,ot)，每个array是和角色的所有碰撞点       
        results = [self._pixels_overlapped(other) for other in others]       
        results = filter(bool,results)   # 把没有发生像素级碰撞的过滤掉
        results = list(results)
        return results
        
    def collide_color(self,color,ignore_alpha=True,area=None):
        """对所有重叠的角色进行像素极检测，           。 
           在下面中rets解包的array、im_a和im_b及r解释分别如下:
           array：重叠区域所有碰撞点的行列号
           im_a：重叠区域转换成numpy数组的主碰方图像
           im_b：重叠区域转换成numpy数组的被碰方图像
           返回所碰到的角色列表。
        """
        results = self.collide_tag(area=area)        
        if not results:return False
        if isinstance(color,str):color = ImageColor.getrgb(color) # 0.23版增加
        if len(color)==3 : ignore_alpha=True
        sprites = []                                       # 待返回的角色列表 
        for rets in results:
            array,im_a,im_b ,r ,ot= rets
            others = _find_pixels(im_b,color,ignore_alpha) # 查找像素
            
            array = list(array)
            array = set(map(tuple,array))
            if array.intersection(others): sprites.append(ot)       
        return sprites
    
    def color_collide_color(self,color1,color2,ignore_alpha=True):
        """自己上面的颜色碰到其它角色们上的颜色
           返回所碰到的角色列表。
        """
        results = self.collide_tag()        
        if not results:return False
        if isinstance(color1,str):color1 = ImageColor.getrgb(color1) # 0.23版增加                
        if isinstance(color2,str):color2 = ImageColor.getrgb(color2) # 0.23版增加        if len(color1)==3 or len(color2)==3 : ignore_alpha=True
        sprites = []                                       # 待返回的角色列表 
        for rets in results:
            array,im_a,im_b ,r ,ot = rets            
            selfs = _find_pixels(im_a,color1,ignore_alpha) # 找到像素的行列号
            others = _find_pixels(im_b,color2,ignore_alpha)# 找到像素的行列号
            array = list(array)
            array = set(map(tuple,array))
            
            if array.intersection(selfs) and array.intersection(others):
                  if selfs.intersection(others):sprites.append(ot)         
        return sprites
        
    def color_collide_other_color(self,selfcolor,other,
                                  othercolor,ignore_alpha=True):
        """自己上面的颜色碰到单个角色上面的颜色的碰撞检测。
           selfcolor：自己图形区域的像素点值，RGBA四元组，alpha通道忽略则是三元组，下同。
           other：其它角色。
           othercolor：其它角色上面的像素点值，RGBA四元组。
           ignore_alpha：是否忽略透明通道，默认为忽略。
           返回真或者假。
        """
        if isinstance(selfcolor,str):selfcolor = ImageColor.getrgb(selfcolor) # 0.23版增加
        if isinstance(othercolor,str):othercolor = ImageColor.getrgb(othercolor) # 0.23版增加
        if len(selfcolor)==3 or len(othercolor)==3:
            ignore_alpha = True            
        
        result = self._pixels_overlapped(other)  # 测试是否发生像素级重叠
        if not result : return False
        array,im_a,im_b ,r,other = result

        selfs = _find_pixels(im_a,selfcolor,ignore_alpha)
        others = _find_pixels(im_b,othercolor,ignore_alpha)

        # 如果有相同的行列号，说明这个点的两种颜色发生“碰撞”
        if selfs.intersection(others):
            return True
        else:
            return False
        
    def _loadshapes(self,frames):
        """加载造型列表"""
        if frames == None:                              # 如果是空则画个海龟
            frames = [turtleimage('green')]
                      
        if not isinstance(frames,(list,tuple)):frames = [frames]
        frames = [im.convert("RGBA") for im in frames]  # 转换成RGBA模式
        self._raw_shapes = [im.copy() for im in frames] # 保留原始造型(用于图像处理)
       
        self._shapes = [im.copy() for im in frames]     # 当前的造型列表
        self._shape_amounts = len(self._shapes)         # 造型数量
        self._shapeindex = 0                            # 当前造型索引号
        self._current_shape = self._shapes[self._shapeindex] # 当前造型       
        self._process_shape()                           # 根据方向，伸展因子处理当前造型
        self._setshape()                                # 设置造型
        
    def randomshape(self):
        """随机选择一个造型"""
        r = randint(0,self._shape_amounts-1)
        self._shapeindex = r
        self._setshape()
        
    def setindex(self,index):
        """指定造型索引号"""       
        self._shapeindex = index
        self._setshape()
        
    def shapeamounts(self):
        return self._shape_amounts
    
    def nextshape(self):
        """下一个造型"""
        self._shapeindex += 1                       # 索引号加1
        self._shapeindex %= self._shape_amounts     # 对数量求余
        self._process_shape()
        self._setshape()                            # 配置造型            

    def previousshape(self):
        """上一个造型"""       
        self._shapeindex -= 1                       # 索引号加1
        self._shapeindex %= self._shape_amounts     # 对数量求余
        self._process_shape()
        self._setshape()                            # 配置造型

    def _setshape(self):
        """设置造型"""
        self._current_shape = self._shapes[self._shapeindex]
        self._rect = self._getrect()                # 换造型后要修改自己的矩形  
        self._PhotoImage = ImageTk.PhotoImage(self._current_shape)
        self._canvas.itemconfig(self.item,image=self._PhotoImage)        
        self._bubble_reconfig()                      # 重新配置说话泡泡(异步执行说话的时候)
        
    def _process_shape(self):
        """当前造型图形处理"""
        rawshape = self._raw_shapes[self._shapeindex] # 取出原始造型
         
        w,h = rawshape.size    
        newwidth = int(w * self._stretchfactor[1])
        newheight = int(h * self._stretchfactor[0])
        size = (newwidth,newheight)
        rawshape  = rawshape.resize(size,Image.ANTIALIAS)

        if self._rotationstyle==0 or self._rotationstyle==360: # 360度旋转
           self._current_shape = rawshape.rotate(-self.heading(),expand=1)# 旋转后的原始造型
        elif self._rotationstyle==1:                          # 左右翻转
            if self._heading>90 and self._heading<270:
                self._current_shape = ImageOps.mirror(rawshape)
            else:
                self._current_shape = rawshape
        elif self._rotationstyle==2:                          # 不旋转 
            self._current_shape = rawshape
        
        self._shapes[self._shapeindex] = self._current_shape   # 写回造型列表       
        
    def setheading(self,angle):
        """设置朝向，y轴向下，向右转,方向值增加"""
        self._heading = angle
        self._heading = self._heading % 360
        self._process_shape()
        self._setshape()
        self._bubble_reconfig()                      # 重新配置说话泡泡(异步执行说话的时候)
        
    def right(self,a):
        """向右旋转一定的角度，y轴向下，所以角度值增加"""
        self._heading += a
        self.setheading(self._heading)        

    def left(self,a):
        """向左旋转一定的角度，y轴向下，所以角度值减少"""
        self.right(-a)

    def heading(self):
        """返回方向值"""
        return self._heading

    def towards(self,x,y=None):
        """朝向某个坐标"""
        if y == None:      # 如果y是空值，把x当成有两个数值的坐标或角色            
            if isinstance(x,Sprite):
                x,y = self._canvas.coords(x.item)
            else:                    # 否则认为x是一个元组
                x,y = x
        dx,dy = x - self.xcor(),y - self.ycor()
        angle = round(math.atan2(dy, dx)*180.0/math.pi, 10)            
        self.setheading(angle)

    def distance(self, x, y=None):
        """到某点或个角色的距离"""
        if y == None:
            # 如果它是Sprite实例的话，取它的x,y坐标
            if isinstance(x,Sprite):
                x,y = self._canvas.coords(x.item)
            else:                    # 否则认为x是一个元组
                x,y = x
        a,b = self._canvas.coords(self.item)
        dx = a - x
        dy = b - y
        return math.sqrt(dx*dx + dy*dy)        

    def goto(self,x,y=None):
        pos = self._canvas.coords(self.item)
        if y==None:                    # 如果y是None，把x当成有两个数据的序列
            x,y = x
        self._canvas.coords(self.item,x,y)
        self._canvas.tag_raise(self.item)
        if len(self._fillpath)>0:
            self._fillpath.append(self._canvas.coords(self.item))
        self._bubble_reconfig()                      # 重新配置说话泡泡(异步执行说话的时候)
        self._drawline(pos,(x,y))

    def position(self):
        """返回(x,y)坐标"""
        return self._canvas.coords(self.item)

    def xcor(self):
        """返回x坐标"""
        return self._canvas.coords(self.item)[0]
    
    def ycor(self):
        """返回y坐标"""
        return self._canvas.coords(self.item)[1]

    def setx(self,newx):
        """设置x坐标"""
        x,y = self._canvas.coords(self.item)
        self._canvas.coords(self.item,newx,y)
        self._canvas.tag_raise(self.item)
        if len(self._fillpath)>0:
            self._fillpath.append(self._canvas.coords(self.item))

        self._bubble_reconfig()                      # 重新配置说话泡泡(异步执行说话的时候)
        self._drawline((x,y),(newx,y))
        
    def sety(self,newy):
        """设置y坐标"""
        x,y = self._canvas.coords(self.item)
        self._canvas.coords(self.item,x,newy)
        self._canvas.tag_raise(self.item)
        if len(self._fillpath)>0:
            self._fillpath.append(self._canvas.coords(self.item))

        self._bubble_reconfig()                      # 重新配置说话泡泡(异步执行说话的时候)
        self._drawline((x,y),(x,newy))

    def addx(self,dx):
        """增加x坐标的值为dx"""
        x,y = self._canvas.coords(self.item)
        self._canvas.coords(self.item,x+dx,y)
        self._canvas.tag_raise(self.item)
        if len(self._fillpath)>0:
            self._fillpath.append(self._canvas.coords(self.item))

        self._bubble_reconfig()                      # 重新配置说话泡泡(异步执行说话的时候)
        self._drawline((x,y),(x+dx,y))
        
    def addy(self,dy):
        """增加y坐标的值为dy"""
        x,y = self._canvas.coords(self.item)
        self._canvas.coords(self.item,x,y+dy)
        self._canvas.tag_raise(self.item)
        if len(self._fillpath)>0:
            self._fillpath.append(self._canvas.coords(self.item))

        self._bubble_reconfig()                      # 重新配置说话泡泡(异步执行说话的时候)
        self._drawline((x,y),(x,y+dy))  
        
    def forward(self,distance):
        """前进distance距离"""
        start = self._canvas.coords(self.item)       # 开始坐标
        r = math.radians(self._heading)              # 转换成弧度单位
        dx = distance * math.cos(r)                  # 计算需要前进的水平距离
        dy = distance * math.sin(r)                  # 计算需要前进的垂直距离
        self._canvas.move(self.item,dx,dy)           # 移动角色
        self._canvas.tag_raise(self.item)
        end  = self._canvas.coords(self.item)        # 终点坐标
        if len(self._fillpath)>0:
            self._fillpath.append(end)

        self._bubble_reconfig()                      # 重新配置说话泡泡(异步执行说话的时候)
        self._drawline(start,end)                    # 画线条     
            
    def backward(self,distance):
        """倒退"""
        self.forward(-distance)

    def _drawline(self,start,end):
        """画线"""
        if self._pendown:
            i = self._canvas.create_line(*start,*end,fill=self._pencolor,
                                         width=self._pensize,cap='round')
            self._canvas.tag_raise(self.item)
            self._lineitems.append(i)
     
    def hide(self):
        """隐藏"""
        self._visible=False            # 描述角色是否可见的逻辑变量
        self._canvas.itemconfig(self.item,state='hidden')
        self._bubble_reconfig()                      # 重新配置说话泡泡(异步执行说话的时候)
        self._canvas.update()

    def show(self):
        """显示"""
        self._visible=True
        self._canvas.itemconfig(self.item,state='normal')
        self._bubble_reconfig()                      # 重新配置说话泡泡(异步执行说话的时候)
        self._canvas.update()

    def isvisible(self):
        return self._visible

    def stamp(self):
        """盖图章"""
        pos = self.position()
        current_shape = self._shapes[self._shapeindex]
        phim = ImageTk.PhotoImage(current_shape)       
        item = self._canvas.create_image(pos,image=phim)
        self._canvas.tag_raise(self.item)
        self._canvas.update()
        self._stampitems.append(item)
        self._stampimages.append(phim)
        return item
    
    def clearstamp(self, stampid):
        """清除一个图章
        """
        if stampid in self._stampitems:
            self._canvas.delete(stampid)
            index = self._stampitems.index(stampid) # 根据编号求所在索引号
            self._stampitems.remove(stampid)
            self._stampimages.pop(index)            # 弹出对应索引的图章造型 
            self._canvas.update()
            
    def clearstamps(self, n=None):
        """清除多个图章
        """
        if n is None:
            toDelete = self._stampitems[:]
        elif n >= 0:
            toDelete = self._stampitems[:n]
        else:
            toDelete = self._stampitems[n:]
        [self.clearstamp(item) for item in toDelete]        
        
    def clear(self):
        """清除所画线条，图章，圆点，空心圆形，填充块，说话泡泡"""
        [self._canvas.delete(item) for item in self._lineitems]
        self._lineitems = []
        self.clearstamps()
        [self._canvas.delete(item) for item in self._fillitems]
        self._fillitems=[]
        [self._canvas.delete(item) for item in self._dotitems]
        self._dotitems = []
        [self._canvas.delete(item) for item in self._circleitems]
        self._circleitems = []
        [self._canvas.delete(item) for item in self._writeitems]
        self._writeitems = []

        self._fillpath = []
        self._end_say()                        # 清除说话泡泡

    def home(self):
        """到画布中央,别名为center"""
        pos = self._canvas.coords(self.item)   # 记录原先坐标
        x = self.canvas_width()//2
        y = self.canvas_height()//2
        self.goto(x,y)
        self.setheading(0)
        self._bubble_reconfig()                # 重新配置说话泡泡
        self._drawline(pos,(x,y))        

    def reset(self):
        self.clear()
        self.home()

    def kill(self):
        self.clear()
        Sprite.sprites.pop(self.item)
        self._canvas.delete(self.item)
        self._alive = False            # 死了
        
    def is_alive(self):
        return self._alive

    def out_canvas(self):
        """超出画布区域的范围"""
        x,y = self.position()
        if x >=self.canvas_width() or x <=0 or \
           y >=self.canvas_height() or y<=0:
            return True
        else:
            return False
        
    def ondrag(self, fun, num=1, add=None):
        """
        绑定鼠标按钮的移动事件到海龟，fun函数要有两个整数参数，用来接收鼠标指针坐标，
        默认是左键(num=1)。最简单的用法就是t.ondrag(t.goto)，这样可拖动海龟。
        """
        if fun is None:
            self._canvas.tag_unbind(self.item, "<Button%s-Motion>" % num)
        else:
            def eventfun(event):
                try:                   
                    fun(event.x, event.y)
                except Exception:
                    pass
            self._canvas.tag_bind(self.item, "<Button%s-Motion>" % num, eventfun, add)    

    def _head_west(self):
       """辅助函数，朝东还是朝西,如果朝西，则返回真，否则返回假"""
       h = self.heading()
       return h > 90 and h < 270

    def _end_say(self):
       
       self._canvas.itemconfig(self._bubble_right,image='')
       self._canvas.itemconfig(self._bubble_left,image='')
       self._saying = False
       self._current_bubble = None

    def _bubble_xy(self):
        """说话泡泡的坐标,以左下或右下为它的坐标"""
        r = self._getrect()
        xy = self.xcor(),r.top-5
        return xy
      
    def _bubble_reconfig(self):
       if self._saying==False:return
       if self._visible == False:
           self._canvas.itemconfig(self._bubble_right,image=self._saypic_right,anchor='se',state='hidden')
           self._canvas.itemconfig(self._bubble_left,image=self._saypic_left,anchor='sw',state='hidden')
           return
       if self._head_west():
          self._canvas.itemconfig(self._bubble_right,image=self._saypic_right,anchor='se',state='normal')
          self._canvas.itemconfig(self._bubble_left,image=self._saypic_left,anchor='sw',state='hidden')
          self._current_bubble = self._bubble_right
       else:
          self._canvas.itemconfig(self._bubble_right,image=self._saypic_right,anchor='se',state='hidden')
          self._canvas.itemconfig(self._bubble_left,image=self._saypic_left,anchor='sw',state='normal')
          self._current_bubble = self._bubble_left
       x,y = self._bubble_xy()          # 泡泡坐标
       self._canvas.coords(self._current_bubble,x,y)
       self._canvas.tag_raise(self._current_bubble)
       
    def say(self,words,second,wait=True,bg='white',fz=14,fg='black'):
        if self._saying:return 
        self._saying = True                     # 说话正在进行
        words = str(words)
        bubble_left,bubble_right = _make_say_bubble(words,16,18,bg=bg,fz=fz,fg=fg)  # 返回pillow图形对象18是margion,20是圆角矩形半径
        
        self._saypic_left = ImageTk.PhotoImage(bubble_left)
        self._saypic_right = ImageTk.PhotoImage(bubble_right)    
        self._bubble_reconfig()        
        
        self._saytime = second                  # 记录说话泡泡要显示的时间
        self._saystart  = time.time()           # 说话起始时间
        if wait==False:
           self._canvas.after(int(second*1000),self._end_say) # 一定时间后结束说话泡泡显示
        else:
           while time.time() - self._saystart < self._saytime:
              self._canvas.update()
           self._end_say()

    def set_tag(self,tag):
          """设定标签,tag可能是字符串或者包括字符串的元组"""
          self._canvas.itemconfig(self.item,tags=tag)

    def get_tag(self):
          """返回角色的标签"""
          return self._canvas.gettags(self.item)
    def add_tag(self,tag):
         """添加标签"""
         self._canvas.addtag(tag,'withtag',self.item)
         
    def delete_tag(self,tag):
         """删除标签"""
         self._canvas.dtag(self.item,tag)

    def begin_fill(self):
        """开始填充"""
        if not self._fillpath:          # 如果填充路径没有，则创建一个空的多边形对象
            self.currentfillitem = self._canvas.create_polygon((0, 0, 0, 0, 0, 0), fill="", outline="")
            self._fillpath = [self._canvas.coords(self.item)]
            self._fillitems.append(self.currentfillitem) # 保存当前的填充项目id以便以后删除
            
    def end_fill(self):
        if len(self._fillpath) > 2:
            cl = []
            for x, y in self._fillpath:
               cl.append(x)
               cl.append(y)
            self._canvas.coords(self.currentfillitem, *cl)
            self._canvas.itemconfig(self.currentfillitem,fill=self._fillcolor)
            self_fillpath = []
            
    def write(self, txt,align='center', font=('',14,'normal'),angle=0):
        """在画布上写文本"""
        x, y = self._canvas.coords(self.item)
        
        anchor = {"left":"sw", "center":"s", "right":"se" }
        item = self._canvas.create_text(x, y, text=txt, anchor=anchor[align],
                                        fill=self._pencolor, font=font,angle=angle)
        self._writeitems.append(item)
        self._canvas.tag_raise(self.item)
        return item
    
        
    # 定义别名
    alive = is_alive
    settag = set_tag
    gettag = get_tag
    addtag = add_tag
    deletetag = delete_tag
    isalive =is_alive
    up = penup
    down = pendown
    pd = pendown
    pu = penup
    width = pensize
    center = home
    fd = forward
    rt = right
    lt = left
    seth = setheading
    setposition = goto
    setpos = goto
    pos = position
    bk = backward
    back = backward
    next_shape = nextshape
    next_costume = nextshape
    nextcostume = nextshape    
    previous_shape = previousshape
    last_shape = previousshape
    lastshape = previousshape
    lastcostume = previousshape
    last_costume = previousshape
    ccc = color_collide_color
    ccoc = color_collide_other_color
    shape = _loadshapes
    rotationmode = setrotmode
    randomcostume = randomshape
    ht = hide
    hideturtle = hide
    st = show
    showturtle = show
    out_of_canvas = out_canvas
    collide_edge = out_canvas               # 定义碰到边
    
def setalpha(rawim,a):
    """
       设置图形对象非透明点的alpha通道值,rawim是一个pillow图形对象
    """
    im = rawim.copy()
    r, g, b, alpha = im.split()                # 分离r,g,b,a通道
    alpha = alpha.point(lambda i: i>0 and a)   # 把非透明点的alpha值换成a
    im.putalpha(alpha)                      # 替换im的alpha通道
    return im

def pixelate(im,k):
    """像素化图形"""
    k = abs(k)
    if k==0:return im
    k = min(k,99)
    k = max(1,k)    
    width = im.width
    size = int(width * ((100-k)/500))
    size = max(1,size)
    imgSmall = im.resize((size,size),resample=Image.BILINEAR)   
    result = imgSmall.resize(im.size,Image.NEAREST)
    return result

def mozaic(im,k):
    """对图像进行马赛克处理,im是pillow图形对象"""
    k = abs(k)
    if k==0 or k==1:return im
    k = 1/k
    w,h = im.size
    new_w,new_h = int(w*k),int(h*k)
    new_w = max(1,new_w)
    new_h = max(1,new_h)
    rows = h//new_h                    # 行数
    cols = w//new_w                    # 列数
    if cols>1:
        im_small = im.resize((new_w,new_h))# 小图像
        im_small = np.array(im_small)        
        # 水平连接
        arrh = np.hstack((im_small, im_small))
        for _ in range(cols-2):
            arrh = np.hstack((arrh, im_small))
        # 垂直连接    
        arrv = np.vstack((arrh, arrh))
        for _ in range(rows-2):
            arrv = np.vstack((arrv, arrh))
        return Image.fromarray(arrv)
    else:
        return im
    
class Key:
    def __init__(self,cv,key=None):
        self.cv = cv
        self._key = key
        self._operation=[]
        self.event = None
        self.bind()
        
    def bind(self):
        if self._key==None: 
           self.cv.bind(f'<KeyPress>',self._press)  
           self.cv.bind(f'<KeyRelease>',self._release)
        else:
           self.cv.bind(f'<KeyPress-{self._key}>',self._press)  
           self.cv.bind(f'<KeyRelease-{self._key}>',self._release)  
        
    def unbind(self):        
        self.event = None
        if self._key==None:
            self.cv.unbind(f'<KeyPress>')  
            self.cv.unbind(f'<KeyRelease>')
        else:             
            self.cv.unbind(f'<KeyPress-{self._key}>')  
            self.cv.unbind(f'<KeyRelease-{self._key}>') 
        
    def isdownup(self):
         """是否按下并弹起键盘按键"""
         if len(self._operation)<2:return
         if self._operation[-1]=='up' and self._operation[-2]=='down':
              self._operation.clear()
              return True
         
    def _press(self,event):
        self._operation.clear()
        self._operation.append('down')
        self.event = event

    def _release(self,event):
        self._operation.append('up')
        self.event = event

    def down(self):
        """是否按下某键"""
        if len(self._operation)>0:
            return self._operation[-1]=='down'
        else:
            return False          
    isdown = down 

class Mouse:
    def __init__(self,cv,number=1):
      self.cv = cv
      self._number = number
      self.event = None
      self._operation = []
      self.bind()

    def bind(self):
       self.cv.bind(f"<ButtonPress-{self._number}>",self._press)
       self.cv.bind(f"<ButtonRelease-{self._number}>",self._release)
      
    def unbind(self):
        self.event = None
        self.status = None
        self._operation.clear()
        self.cv.unbind(f'<ButtonPress-{self._number}>')  
        self.cv.unbind(f'<ButtonRelease-{self._number}>')
        
    def isdownup(self):
         """是否按下并弹起鼠标键"""
         if len(self._operation)<2:return
         if self._operation[-1]=='up' and self._operation[-2]=='down':
              self._operation.clear()
              return True
          
    def _press(self,event):
       self._operation.clear()
       self._operation.append('down')
       self.event = event
      
    def _release(self,event):
       self._operation.append('up')
       self.event = event
         
    def down(self):
        """是否按下"""
        if len(self._operation)>0:
            return self._operation[-1]=='down'
        else:
            return False  
    isdown = down 
     
class Clock:
    """控制fps的时钟Clock类"""
    def __init__(self):
       self._old_start_time = time.perf_counter()
       self._start_time = time.perf_counter()

    def tick(self,fps=0):
        """返回每帧逝去的时间，如果fps不为0，则会等待直到时间大于1/fps"""
        end_time = time.perf_counter()
        elapsed_time = end_time - self._start_time

        if fps!=0:
            step = 1/fps
            if elapsed_time < step:  # 如果逝去的时间小于step则等待
               time.sleep(step - elapsed_time)
            
        self._old_start_time = self._start_time
        self._start_time = time.perf_counter()
        return time.perf_counter() - self._old_start_time
    
    def getfps(self):
        """得到fps"""
        t = time.perf_counter() - self._old_start_time
        return round(1/t,2)
    
if __name__ == "__main__":
     
     root = Tk()
     cv = Canvas()
     cv.pack()
     
     showinfo("Hello", "你好,世界")
     
     circle = Sprite(cv,make_ellipse())
     circle.goto(250,200)
     
     rect = Sprite(cv,make_rect())
     rect.goto(100,100)
     
     turtle = Sprite(cv)
     c = (123,45,22)
     
     turtle.color(255,0,255)
        
     turtle.fillcolor('red')

     turtle.write('中华人民共和国',font=('黑体',12,'underline'),angle=45)
     
     turtle.begin_fill()
     turtle.goto(100,100)
     turtle.goto(100,200)
     turtle.addx(100)     
     turtle.end_fill()
     turtle.fd(100)
     turtle.dot(20)
     turtle.addy(-100)
     turtle.circle(30)

     a = askyesno("gameturtle","要关闭窗口吗?")
     if a :root.destroy()
     root.mainloop()




