try:
    from PySide.QtGui import *
    from PySide.QtCore import *
    ISPYSIDE1 = True
except:
    raise ImportError('Cannot load PySide1.')
try:
    import nt
except:
    raise Exception('Windows, ReactOS or Wine is required.')
import sys
import ctypes
try:
    import winreg
except:
    import _winreg as winreg
from ctypes.wintypes import MSG, POINT, RECT


__all__ = ['CustomizedWindow', 'BlurWindow']


class LOGFONT(ctypes.Structure):
    _fields_ = [
    ('lfHeight', ctypes.c_long),
    ('lfWidth', ctypes.c_long),
    ('lfEscapement', ctypes.c_long),
    ('lfOrientation', ctypes.c_long),
    ('lfWeight', ctypes.c_long),
    ('lfItalic', ctypes.c_byte),
    ('lfUnderline', ctypes.c_byte),
    ('lfStrikeOut', ctypes.c_byte),
    ('lfCharSet', ctypes.c_byte),
    ('lfOutPrecision', ctypes.c_byte),
    ('lfClipPrecision', ctypes.c_byte),
    ('lfQuality', ctypes.c_byte),
    ('lfPitchAndFamily', ctypes.c_byte),
    ('lfFaceName', ctypes.c_wchar * 32)]


class NONCLIENTMETRICS(ctypes.Structure):
    _fields_ = [
    ('cbSize', ctypes.c_ulong),
    ('iBorderWidth', ctypes.c_int),
    ('iScrollWidth', ctypes.c_int),
    ('iScrollHeight', ctypes.c_int),
    ('iCaptionWidth', ctypes.c_int),
    ('iCaptionHeight', ctypes.c_int),
    ('lfCaptionFont', LOGFONT),
    ('iSmCaptionWidth', ctypes.c_int),
    ('iSmCaptionHeight', ctypes.c_int),
    ('lfSmCaptionFont', LOGFONT),
    ('iMenuWidth', ctypes.c_int),
    ('iMenuHeight', ctypes.c_int),
    ('lfMenuFont', LOGFONT),
    ('lfStatusFont', LOGFONT),
    ('lfMessageFont', LOGFONT),
    ('iPaddedBorderWidth', ctypes.c_int),]


class NCCALCSIZE_PARAMS(ctypes.Structure):
    _fields_ = [('rgrc', RECT * 3),
                ('lppos', ctypes.POINTER(ctypes.c_void_p))]


class WindowCompositionAttribute(ctypes.Structure):
    _fields_ = [("Attribute", ctypes.c_int), ("Data", ctypes.POINTER(ctypes.c_int)), ("SizeOfData", ctypes.c_size_t)]


class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [("AccentState", ctypes.c_uint), ("AccentFlags", ctypes.c_uint), ("GradientColor", ctypes.c_uint),
        ("AnimationId", ctypes.c_uint)]


class DWM_BLURBEHIND(ctypes.Structure):
    _fields_ = [('dwFlags', ctypes.c_ulong), ('fEnable', ctypes.c_long),
        ('hRgnBlur', ctypes.c_void_p), ('fTransitionOnMaximized', ctypes.c_long)]


class MARGINS(ctypes.Structure):
    _fields_ = [("cxLeftWidth", ctypes.c_int), ("cxRightWidth", ctypes.c_int), ("cyTopHeight", ctypes.c_int),
                ("cyBottomHeight", ctypes.c_int)]


class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [("Attribute", ctypes.c_ulong), ("Data", ctypes.POINTER(ACCENT_POLICY)),
        ("SizeOfData", ctypes.c_ulong)]


class Win10BlurEffect:
    def __init__(self):
        self.WCA_ACCENT_POLICY = 19
        self.ACCENT_ENABLE_BLURBEHIND = 3
        self.ACCENT_ENABLE_ACRYLICBLURBEHIND = 4
        self.SetWindowCompositionAttribute = ctypes.windll.user32.SetWindowCompositionAttribute
        self.accentPolicy = ACCENT_POLICY()
        self.winCompAttrData = WINDOWCOMPOSITIONATTRIBDATA()
        self.winCompAttrData.Attribute = self.WCA_ACCENT_POLICY
        self.winCompAttrData.SizeOfData = ctypes.sizeof(self.accentPolicy)
        self.winCompAttrData.Data = ctypes.pointer(self.accentPolicy)
    def setAeroEffect(self, hWnd, gradientColor='01000000', isEnableShadow=True, animationId=0):
        gradientColor = ctypes.c_ulong(int(gradientColor, base=16))
        animationId = ctypes.c_ulong(animationId)
        accentFlags = ctypes.c_ulong(0x20 | 0x40 | 0x80 | 0x100 | 0x200) if isEnableShadow else ctypes.c_ulong(0)
        self.accentPolicy.AccentState = self.ACCENT_ENABLE_BLURBEHIND
        self.accentPolicy.GradientColor = gradientColor
        self.accentPolicy.AccentFlags = accentFlags
        self.accentPolicy.AnimationId = animationId
        code = self.SetWindowCompositionAttribute(hWnd, ctypes.byref(self.winCompAttrData))
        return code
    def setAcrylicEffect(self, hWnd, gradientColor='01000000', isEnableShadow=True, animationId=0):
        gradientColor = ctypes.c_ulong(int(gradientColor, base=16))
        animationId = ctypes.c_ulong(animationId)
        accentFlags = ctypes.c_ulong(0x20 | 0x40 | 0x80 | 0x100) if isEnableShadow else ctypes.c_ulong(0)
        self.accentPolicy.AccentState = self.ACCENT_ENABLE_ACRYLICBLURBEHIND
        self.accentPolicy.GradientColor = gradientColor
        self.accentPolicy.AccentFlags = accentFlags
        self.accentPolicy.AnimationId = animationId
        code = self.SetWindowCompositionAttribute(hWnd, ctypes.byref(self.winCompAttrData))
        return code


class MenuButton(QAbstractButton):
    def __init__(self, parent):
        super(MenuButton, self).__init__(parent)
        self.isminsizebutton, self.ismaxsizebutton, self.isclosebutton = map(isinstance, [self] * 3, [MinSizeButton, MaxSizeButton, CloseButton])
        self.parent = parent
        self.setFocusPolicy(Qt.NoFocus)
        self.backgroundcolour = Qt.transparent
    def paintEvent(self, *args):
        width, height = self.width(), self.height()
        parent = self.parent
        dpi, realdpi = parent.dpi, parent.realdpi
        isdarktheme = parent.isdarktheme
        isactivewindow = parent.isActiveWindow()
        ismaximized = ctypes.windll.user32.IsZoomed(parent.hwnd)
        painter, path = QPainter(self), QPainterPath()
        painter.setBrush(self.backgroundcolour)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())
        painter.setBrush(Qt.NoBrush)
        if isdarktheme: pen = QPen(Qt.white) if isactivewindow else QPen(QColor(155, 155, 155))
        else: pen = QPen(Qt.black) if isactivewindow else QPen(QColor(99, 99, 99))
        penwidth = int(1.35 * dpi / 96.0)
        pen.setWidth(penwidth)
        painter.setPen(pen)
        if realdpi >= 143: painter.setRenderHint(QPainter.Antialiasing)
        if self.isminsizebutton:
            path.moveTo(int(0.391 * width), int(0.500 * height))
            path.lineTo(int(0.609 * width), int(0.500 * height))
        elif self.ismaxsizebutton:
            if ismaximized:
                path.moveTo(int(0.402 * width), int(0.406 * height))
                path.lineTo(int(0.559 * width), int(0.406 * height))
                path.lineTo(int(0.559 * width), int(0.656 * height))
                path.lineTo(int(0.402 * width), int(0.656 * height))
                path.lineTo(int(0.402 * width), int(0.406 * height))
                path.moveTo(int(0.441 * width), int(0.344 * height))
                path.lineTo(int(0.598 * width), int(0.344 * height))
                path.lineTo(int(0.598 * width), int(0.594 * height))
            else:
                path.moveTo(int(0.402 * width), int(0.344 * height))
                path.lineTo(int(0.598 * width), int(0.344 * height))
                path.lineTo(int(0.598 * width), int(0.656 * height))
                path.lineTo(int(0.402 * width), int(0.656 * height))
                path.lineTo(int(0.402 * width), int(0.344 * height))
        elif self.isclosebutton:
            path.moveTo(int(0.402 * width), int(0.344 * height))
            path.lineTo(int(0.598 * width), int(0.656 * height))
            path.moveTo(int(0.598 * width), int(0.344 * height))
            path.lineTo(int(0.402 * width), int(0.656 * height))
        painter.drawPath(path)


class MinSizeButton(MenuButton):
    def __init__(self, *args):
        super(MinSizeButton, self).__init__(*args)


class MaxSizeButton(MenuButton):
    def __init__(self, *args):
        super(MaxSizeButton, self).__init__(*args)


class CloseButton(MenuButton):
    def __init__(self, *args):
        super(CloseButton, self).__init__(*args)


class SystemLabel(QAbstractButton):
    def __init__(self, parent):
        super(SystemLabel, self).__init__(parent)
        self.istitlebar, self.isclientarealabel, self.istitletextlabel, self.istitleiconlabel = map(isinstance, [self] * 4, [TitleBar, ClientAreaLabel, TitleTextLabel, TitleIconLabel])
        self.parent = parent
        self.setFocusPolicy(Qt.NoFocus)
        self.backgroundcolour = Qt.transparent
        self.draw = True
    def paintEvent(self, *args):
        parent = self.parent
        isdarktheme = parent.isdarktheme
        isblurwindow = parent.isblurwindow
        isaeroenabled = parent.isaeroenabled
        isactivewindow = parent.isActiveWindow()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        backgroundcolour = Qt.transparent
        if self.istitlebar:
            if isblurwindow:
                if self.draw:
                    backgroundcolour = QLinearGradient(0, 0, 0, self.height())
                    if isaeroenabled: list(map(backgroundcolour.setColorAt, [0, 1], [QColor(0, 0, 0, 107), QColor(0, 0, 0, 197)])) if isdarktheme else list(map(backgroundcolour.setColorAt, [0, 1], [QColor(255, 255, 255, 107), QColor(255, 255, 255, 197)]))
                    else: list(map(backgroundcolour.setColorAt, [0, 1], [QColor(38, 38, 38), QColor(0, 0, 0)])) if isdarktheme else list(map(backgroundcolour.setColorAt, [0, 1], [QColor(217, 217, 217), QColor(255, 255, 255)]))
                else:
                    if isaeroenabled: backgroundcolour = QColor(0, 0, 0, 127) if isdarktheme else QColor(255, 255, 255, 127)
                    else: backgroundcolour = QColor(20, 20, 20) if isdarktheme else QColor(235, 235, 235)
            else: backgroundcolour = QColor(0, 0, 0) if isdarktheme else QColor(255, 255, 255)
        elif self.isclientarealabel:
            if isblurwindow:
                if isaeroenabled: backgroundcolour = QColor(0, 0, 0, 127) if isdarktheme else QColor(255, 255, 255, 127)
                else: backgroundcolour = QColor(20, 20, 20) if isdarktheme else QColor(235, 235, 235)
            else: backgroundcolour = QColor(0, 0, 0) if isdarktheme else QColor(255, 255, 255)
        elif self.istitletextlabel:
            if isdarktheme: pen = QPen(Qt.white) if isactivewindow else QPen(QColor(155, 155, 155))
            else: pen = QPen(Qt.black) if isactivewindow else QPen(QColor(99, 99, 99))
            painter.setBrush(Qt.NoBrush)
            painter.setPen(pen)
            font = QFont(parent.captionfont)
            font.setPixelSize(parent.title_font_size)
            painter.setFont(font)
            if self.draw: painter.drawText(self.rect(), Qt.AlignVCenter, parent.windowTitle())
        elif self.istitleiconlabel:
            pixmap = parent.windowIcon().pixmap(self.width(), self.height())
            if self.draw: painter.drawPixmap(0, 0, pixmap)
        painter.setBrush(backgroundcolour)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())


class TitleBar(SystemLabel):
    def __init__(self, *args):
        super(TitleBar, self).__init__(*args)


class ClientAreaLabel(SystemLabel):
    def __init__(self, *args):
        super(ClientAreaLabel, self).__init__(*args)


class TitleTextLabel(SystemLabel):
    def __init__(self, *args):
        super(TitleTextLabel, self).__init__(*args)


class TitleIconLabel(SystemLabel):
    def __init__(self, *args):
        super(TitleIconLabel, self).__init__(*args)


def isAeroEnabled():
    try:
        pfEnabled = ctypes.c_uint()
        ctypes.windll.dwmapi.DwmIsCompositionEnabled(ctypes.byref(pfEnabled))
        return pfEnabled.value
    except: return 0


def isdarktheme():
    try:
        value = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize'), 'AppsUseLightTheme')[0]
    except: return False
    if value: return False
    else: return True


def pyside1_hwnd(winId):
    try:
        ctypes.pythonapi.PyCapsule_GetPointer.restype = ctypes.c_void_p
        ctypes.pythonapi.PyCapsule_GetPointer.argtypes = [ctypes.py_object, ctypes.c_char_p]
        hwnd = ctypes.pythonapi.PyCapsule_GetPointer(winId, None)
    except ValueError:
        ctypes.pythonapi.PyCObject_AsVoidPtr.restype = ctypes.c_void_p
        ctypes.pythonapi.PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
        hwnd = ctypes.pythonapi.PyCObject_AsVoidPtr(winId)
    return hwnd


def gethwnd(window):
    hwnd = window.winId()
    if type(hwnd) != int:
        try: hwnd = int(hwnd)
        except: hwnd = pyside1_hwnd(hwnd)
    return hwnd


def getdpiforwindow_winapi(hwnd):
    try:
        dpi_x = ctypes.c_uint()
        dpi_y = ctypes.c_uint()
        monitor_handle = ctypes.windll.user32.MonitorFromWindow(hwnd, 2)
        ctypes.windll.shcore.GetDpiForMonitor(monitor_handle, 0, ctypes.byref(dpi_x), ctypes.byref(dpi_y))
        dpi = dpi_x.value
    except:
        if hasattr(ctypes.windll.user32, 'IsProcessDPIAware'):
            if ctypes.windll.user32.IsProcessDPIAware():
                hDC = ctypes.windll.user32.GetDC(None)
                dpi = ctypes.windll.gdi32.GetDeviceCaps(hDC, 88)
                ctypes.windll.user32.ReleaseDC(None, hDC)
            else: dpi = 96
        else: dpi = 96
    return dpi


def getautohidetaskbarposition():
    SPI_GETWORKAREA = 0x30
    primaryscreenrect = RECT()
    GetSystemMetrics = ctypes.windll.user32.GetSystemMetrics
    FindWindowA = ctypes.windll.user32.FindWindowA
    GetWindowRect = ctypes.windll.user32.GetWindowRect
    primaryscreenwidth = GetSystemMetrics(0)
    primaryscreenheight = GetSystemMetrics(1)
    primaryscreenrect.left = 0
    primaryscreenrect.top = 0
    primaryscreenrect.right = primaryscreenwidth
    primaryscreenrect.bottom = primaryscreenheight
    if primaryscreenwidth != primaryscreenrect.right - primaryscreenrect.left or primaryscreenheight != primaryscreenrect.bottom - primaryscreenrect.top: return 4
    taskbar_hwnd = FindWindowA(b'Shell_TrayWnd', None)
    if not taskbar_hwnd: return 4
    taskbar_rect = RECT()
    GetWindowRect(taskbar_hwnd, ctypes.byref(taskbar_rect))
    if taskbar_rect.left < primaryscreenrect.left and taskbar_rect.top == primaryscreenrect.top and taskbar_rect.right != primaryscreenrect.right and taskbar_rect.bottom == primaryscreenrect.bottom: return 0
    elif taskbar_rect.left == primaryscreenrect.left and taskbar_rect.top < primaryscreenrect.top and taskbar_rect.right == primaryscreenrect.right and taskbar_rect.bottom != primaryscreenrect.bottom: return 1
    elif taskbar_rect.left != primaryscreenrect.left and taskbar_rect.top == primaryscreenrect.top and taskbar_rect.right > primaryscreenrect.right and taskbar_rect.bottom == primaryscreenrect.bottom: return 2
    elif taskbar_rect.left == primaryscreenrect.left and taskbar_rect.top != primaryscreenrect.top and taskbar_rect.right == primaryscreenrect.right and taskbar_rect.bottom > primaryscreenrect.bottom: return 3
    else: return 4
    

def getcaptionfont():
    result = NONCLIENTMETRICS()
    result.cbSize = ctypes.sizeof(NONCLIENTMETRICS)
    ctypes.windll.user32.SystemParametersInfoW(0x29, ctypes.sizeof(NONCLIENTMETRICS), ctypes.byref(result), 0)
    captionfont = result.lfCaptionFont.lfFaceName
    return captionfont


class SplashScreen(QSplashScreen):
    def __init__(self, parent):
        super(SplashScreen, self).__init__()
        self.hwnd = gethwnd(self)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        dpi = parent.dpi
        screen = QGuiApplication.primaryScreen().geometry()
        self.resize(*[500 * dpi / 96.0] * 2)
        self.move(screen.width() // 2 - self.width() // 2, screen.height() // 2 - self.height() // 2)
        self.mainlabel = QLabel(self)
        backgroundcolour = '#B3000000' if parent.isdarktheme else '#B3FFFFFF'
        shadowcolour = '#7F7F7F'
        self.mainlabel.setStyleSheet('background: %s; border-radius: %d' % (backgroundcolour, int(20 * dpi / 96.0)))
        self.mainlabel.resize(self.width() - int(50 * dpi / 96.0), self.height() - int(50 * dpi / 96.0))
        self.mainlabel.move(self.width() // 2 - self.mainlabel.width() // 2, self.height() // 2 - self.mainlabel.height() // 2)
        self.iconlabel = QLabel(self)
        icon = parent.windowIcon()
        iconsize = [150 * dpi / 96.0] * 2
        try:
            pixmap = QPixmap.fromImage(icon.pixmap(icon.availableSizes()[0]).toImage()).scaled(*iconsize, transformMode=Qt.SmoothTransformation)
            self.iconlabel.setPixmap(pixmap)
        except: pass
        self.iconlabel.resize(*iconsize)
        self.iconlabel.move(self.width() // 2 - self.iconlabel.width() // 2, self.height() // 2 - self.iconlabel.height() // 2)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(int(50 * dpi / 96.0))
        shadow.setColor(shadowcolour)
        shadow.setOffset(0, 0)
        self.mainlabel.setGraphicsEffect(shadow)


class CustomizedWindow(QWidget):
    '''A customized window based on PySideX.'''
    def __init__(self):
        super(CustomizedWindow, self).__init__()
        user32 = ctypes.windll.user32
        self.hwnd = gethwnd(self)
        self.animation1 = QPropertyAnimation(self, b'windowOpacity')
        self.animation1.setDuration(250)
        self.animation1.setStartValue(0.0)
        self.animation1.setEndValue(1.0)
        self.animation2 = QPropertyAnimation(self, b'windowOpacity')
        self.animation2.setDuration(250)
        self.animation2.setStartValue(1.0)
        self.animation2.setEndValue(0.0)
        self.isblurwindow = isinstance(self, BlurWindow)
        self.isaeroenabled = isAeroEnabled()
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.SetWindowLong = user32.SetWindowLongPtrW if hasattr(user32, 'SetWindowLongPtrW') else user32.SetWindowLongW 
        WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_int)
        self.BasicMessageHandlerAddress = ctypes.cast(WNDPROC(self.BasicMessageHandler), ctypes.c_void_p).value
        if hasattr(user32, 'GetWindowLongPtrW'): self.originalBasicMessageHandler = user32.GetWindowLongPtrW(self.hwnd, -4)
        else: self.originalBasicMessageHandler = user32.GetWindowLongW(self.hwnd, -4)
        self.splashscreen = None
        self.windowinited = False
        self.handle_setWindowFlags()
        if self.isaeroenabled: self.setBlurEffect() if self.isblurwindow else self.setDWMShadowEffect()
        self.realdpi = getdpiforwindow_winapi(self.hwnd)
        self.highdpiscalingenabled = False
        self.highdpiscalefactorroundingpolicy = 3
        if hasattr(Qt, 'AA_EnableHighDpiScaling'):
            if QApplication.testAttribute(Qt.AA_EnableHighDpiScaling): self.highdpiscalingenabled = True
        if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy'):
            policy_dict = {Qt.HighDpiScaleFactorRoundingPolicy.Ceil: 1, Qt.HighDpiScaleFactorRoundingPolicy.Floor: 2, Qt.HighDpiScaleFactorRoundingPolicy.PassThrough: 3, Qt.HighDpiScaleFactorRoundingPolicy.Round: 4, Qt.HighDpiScaleFactorRoundingPolicy.RoundPreferFloor: 5}
            if hasattr(Qt.HighDpiScaleFactorRoundingPolicy, 'Unset'): self.highdpiscalefactorroundingpolicy = 3 if QApplication.highDpiScaleFactorRoundingPolicy() == Qt.HighDpiScaleFactorRoundingPolicy.Unset else policy_dict[QApplication.highDpiScaleFactorRoundingPolicy()]
            else: self.highdpiscalefactorroundingpolicy = policy_dict[QApplication.highDpiScaleFactorRoundingPolicy()]
        self.dpi = self.getdpibyrealdpi(self.realdpi)
        dpi = self.dpi
        self.maximizedwindowborderwidth_list = self.getMaximizedWindowBorderWidth()
        self.themecolour = 0
        self.isdarktheme = isdarktheme()
        self.setMinimumSize(int(220.0 * dpi / 96.0), int(48.0 * dpi / 96.0))
        self.updateconstantsfordpi()
        self.updateautohidetaskbarwidth()
        self.inminsizebutton = False
        self.inmaxsizebutton = False
        self.inclosebutton = False
        self.intitlebar = False
        self.intopborder = False
        self.inleftborder = False
        self.inbottomborder = False
        self.inrightborder = False
        self.windowtitle = ''
        self.captionfont = getcaptionfont()
        self.windowmargin_left = 0
        self.windowmargin_right = 0
        self.windowmargin_top = 0
        self.windowmargin_bottom = 0
        self.titleBar = TitleBar(self)
        self.clientAreaLabel = ClientAreaLabel(self)
        self.clientArea = QWidget(self)
        self.titleIconLabel = TitleIconLabel(self)
        self.titleTextLabel = TitleTextLabel(self)
        self.minSizeButton = MinSizeButton(self)
        self.maxSizeButton = MaxSizeButton(self)
        self.closeButton = CloseButton(self)
        self.placeTitleBarAndClientArea()
        self.setDarkTheme(0)
        self.originalSetWindowTitle = self.setWindowTitle
        self.setWindowTitle = self.setWindowTitle2
        self.originalSetWindowIcon = self.setWindowIcon
        self.setWindowIcon = self.setWindowIcon2
        if not ISPYSIDE1: self.windowHandle().screenChanged.connect(self.screenChangedHandler)
    def setDarkTheme(self, themecolour=0):
        '''themecolour=0: Auto; themecolour=1: Light; themecolour=2: Dark'''
        self.themecolour = themecolour
        if themecolour == 0: self.isdarktheme = isdarktheme()
        elif themecolour == 1: self.isdarktheme = False
        elif themecolour == 2: self.isdarktheme = True
        else: raise Exception
        self.minSizeButton.update()
        self.maxSizeButton.update()
        self.closeButton.update()
        self.titleBar.update()
        self.clientAreaLabel.update()
        SWP_NOSIZE, SWP_NOMOVE, SWP_NOZORDER = 0x1, 0x2, 0x4
        try:
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, ctypes.byref(ctypes.c_int(0)), ctypes.sizeof(ctypes.c_int(0)))
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(ctypes.c_int(0)), ctypes.sizeof(ctypes.c_int(0)))
        except: pass
        hwnd = self.hwnd
        ctypes.windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER)
    def setWindowTitle2(self, arg__1):
        self.originalSetWindowTitle(arg__1)
        self.windowtitle = arg__1
        self.titleTextLabel.update()
    def setWindowIcon2(self, icon):
        self.originalSetWindowIcon(icon)
        self.titleIconLabel.update()
    def setWindowFlag(self, arg__1, on=True):
        raise AttributeError('Function setWindowFlag has been deleted.')
    def setWindowFlags(self, type):
        raise AttributeError('Function setWindowFlags has been deleted.')
    def handle_setWindowFlags(self):
        user32 = ctypes.windll.user32
        if ISPYSIDE1:
            if hasattr(self, 'originalBasicMessageHandler'):
                if hasattr(user32, 'SetWindowLongPtrW'): self.SetWindowLong(self.hwnd, -4, ctypes.c_int64(self.originalBasicMessageHandler))
                else: self.SetWindowLong(self.hwnd, -4, self.originalBasicMessageHandler)
        self.hwnd = gethwnd(self)
        BasicMessageHandlerAddress = self.BasicMessageHandlerAddress
        if hasattr(user32, 'GetWindowLongPtrW'): self.originalBasicMessageHandler = user32.GetWindowLongPtrW(self.hwnd, -4)
        else: self.originalBasicMessageHandler = user32.GetWindowLongW(self.hwnd, -4)
        self.nonclientareasizeinited = False
        if ISPYSIDE1:
            if hasattr(self, 'originalBasicMessageHandler'):
                if hasattr(user32, 'SetWindowLongPtrW'): self.SetWindowLong(self.hwnd, -4, ctypes.c_int64(BasicMessageHandlerAddress))
                else: self.SetWindowLong(self.hwnd, -4, BasicMessageHandlerAddress)
            self.windowlong = self.SetWindowLong(self.hwnd, -16, 0x40000 | 0x20000 | 0x10000)
        else:
            self.windowlong = self.SetWindowLong(self.hwnd, -16, 0xc00000 | 0x40000 | 0x20000 | 0x10000)
        if self.isaeroenabled: self.setBlurEffect() if self.isblurwindow else self.setDWMShadowEffect()
    def placeTitleBarAndClientArea(self):
        dpi, realdpi = self.dpi, self.realdpi
        title_height = self.title_height
        titleiconlabel_margin = self.titleiconlabel_margin
        menubutton_width = self.menubutton_width
        windowmargin_left, windowmargin_right, windowmargin_top, windowmargin_bottom = self.windowmargin_left, self.windowmargin_right, self.windowmargin_top, self.windowmargin_bottom
        windowmargin_left_for_pyside, windowmargin_right_for_pyside, windowmargin_top_for_pyside, windowmargin_bottom_for_pyside = int(windowmargin_left / 1.0 / realdpi * dpi), int(windowmargin_right / 1.0 / realdpi * dpi), int(windowmargin_top / 1.0 / realdpi * dpi), int(windowmargin_bottom / 1.0 / realdpi * dpi)
        windowrect = self.GetWindowRect()
        windowx, windowy = windowrect.left, windowrect.top
        width, height = windowrect.right - windowx, windowrect.bottom - windowy
        widthforpyside, heightforpyside = int(width / 1.0 / realdpi * dpi), int(height / 1.0 / realdpi * dpi)
        self.titleBar.setGeometry(0, 0, widthforpyside, title_height)
        self.clientAreaLabel.setGeometry(0, title_height, widthforpyside, heightforpyside - title_height - windowmargin_top_for_pyside - windowmargin_bottom_for_pyside)
        self.clientArea.setGeometry(0, title_height, widthforpyside, heightforpyside - title_height - windowmargin_top_for_pyside - windowmargin_bottom_for_pyside)
        self.titleIconLabel.setGeometry(titleiconlabel_margin, titleiconlabel_margin, title_height - 2 * titleiconlabel_margin, title_height - 2 * titleiconlabel_margin)
        self.titleTextLabel.setGeometry(title_height, 0, widthforpyside - title_height - windowmargin_left_for_pyside - windowmargin_right_for_pyside - 3 * menubutton_width, title_height)
        self.minSizeButton.setGeometry(widthforpyside - windowmargin_left_for_pyside - windowmargin_right_for_pyside - 3 * menubutton_width, 0, menubutton_width, title_height)
        self.maxSizeButton.setGeometry(widthforpyside - windowmargin_left_for_pyside - windowmargin_right_for_pyside - 2 * menubutton_width, 0, menubutton_width, title_height)
        self.closeButton.setGeometry(widthforpyside - windowmargin_left_for_pyside - windowmargin_right_for_pyside - menubutton_width, 0, menubutton_width, title_height)
    def setMenuButtonStyle(self, button, state=1):
        backgroundcolour1, backgroundcolour2, backgroundcolour3 = [Qt.transparent] * 3
        if button == 1:
            if state == 1: backgroundcolour1 = QColor(255, 255, 255, 25) if self.isdarktheme else QColor(0, 0, 0, 25)
            elif state == 2: backgroundcolour1 = QColor(255, 255, 255, 50) if self.isdarktheme else QColor(0, 0, 0, 50)
        elif button == 2:
            if state == 1: backgroundcolour2 = QColor(255, 255, 255, 25) if self.isdarktheme else QColor(0, 0, 0, 25)
            elif state == 2: backgroundcolour2 = QColor(255, 255, 255, 50) if self.isdarktheme else QColor(0, 0, 0, 50)
        elif button == 3:
            if state == 1: backgroundcolour3 = QColor(255, 0, 0, 255)
            elif state == 2: backgroundcolour3 = QColor(255, 0, 0, 127)
        self.minSizeButton.backgroundcolour = backgroundcolour1
        self.maxSizeButton.backgroundcolour = backgroundcolour2
        self.closeButton.backgroundcolour = backgroundcolour3
        self.minSizeButton.update()
        self.maxSizeButton.update()
        self.closeButton.update()
    def MessageHandler(self, hwnd, message, wParam, lParam):
        '''Example:
class MyOwnWindow(self):
|->|...
|->|def MessageHandler(self, hwnd, message, wParam, lParam):
|->||->|print(hwnd, message, wParam, lParam)
|->||->|...'''
        pass
    def BasicMessageHandler(self, hwnd, message, wParam, lParam):
        '''For PySide1/2/6, you should define MessageHandler instead of BasicMessageHandler.'''
        user32 = ctypes.windll.user32
        WM_SIZE = 0x5
        WM_ACTIVATE = 0x6
        WM_PAINT = 0xf
        WM_SHOWWINDOW = 0x18
        WM_SETTINGCHANGE = 0x1a
        WM_STYLECHANGED = 0x7d
        WM_NCCALCSIZE = 0x83
        WM_NCHITTEST = 0x84
        WM_NCLBUTTONDOWN = 0xa1
        WM_NCLBUTTONUP = 0xa2
        WM_LBUTTONUP = 0x2a2
        WM_DPICHANGED = 0x2e0
        WM_SYSCOMMAND = 0x112
        WM_DWMCOMPOSITIONCHANGED = 0x31e
        WM_DWMNCRENDERINGCHANGED = 0x31f
        SW_PARENTOPENING = 0x3
        SC_SIZE, SC_MOVE, SC_MINIMIZE, SC_MAXIMIZE, SC_CLOSE, SC_RESTORE = 0xf000, 0xf010, 0xf020, 0xf030, 0xf060, 0xf120
        HTCLIENT, HTCAPTION, HTMINBUTTON, HTMAXBUTTON, HTCLOSE = 0x1, 0x2, 0x8, 0x9, 0x14
        HTLEFT, HTRIGHT, HTTOP, HTTOPLEFT, HTTOPRIGHT, HTBOTTOM, HTBOTTOMLEFT, HTBOTTOMRIGHT = 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0x10, 0x11
        SWP_NOSIZE, SWP_NOMOVE, SWP_NOZORDER, SWP_FRAMECHANGED = 0x1, 0x2, 0x4, 0x20
        SPI_SETNONCLIENTMETRICS, SPI_SETWORKAREA = 0x2a, 0x2f
        try:
            dpi = self.dpi
            realdpi = self.realdpi
            real_border_width = self.real_border_width
            real_title_height = self.real_title_height
            real_menubutton_width = self.real_menubutton_width
            windowmargin_left = self.windowmargin_left
            windowmargin_right = self.windowmargin_right
            windowmargin_top = self.windowmargin_top
            windowmargin_bottom = self.windowmargin_bottom
        except:
            dpi, realdpi = 96, 96
            real_border_width, real_title_height, real_menubutton_width, windowmargin_left, windowmargin_right, windowmargin_top, windowmargin_bottom = [0] * 7
        try: windowrect = self.GetWindowRect()
        except: windowrect = RECT(0, 0, 0, 0)
        windowx, windowy = windowrect.left, windowrect.top
        try:
            globalpos = POINT()
            user32.GetPhysicalCursorPos(ctypes.byref(globalpos))
            user32.PhysicalToLogicalPoint(self.hwnd, ctypes.byref(globalpos))
            x = globalpos.x - windowx
            y = globalpos.y - windowy
        except:
            globalpos = POINT()
            user32.GetCursorPos(ctypes.byref(globalpos))
            x = globalpos.x - windowx
            y = globalpos.y - windowy
        width, height = windowrect.right - windowx, windowrect.bottom - windowy
        intitlebar = windowmargin_top <= y < real_title_height + windowmargin_top
        inminsizebutton = width - windowmargin_left - 3 * real_menubutton_width <= x < width - windowmargin_left - 2 * real_menubutton_width and intitlebar
        inmaxsizebutton = width - windowmargin_left - 2 * real_menubutton_width <= x < width - windowmargin_left - real_menubutton_width and intitlebar
        inclosebutton = width - windowmargin_left - real_menubutton_width <= x < width - windowmargin_left and intitlebar
        intopborder = y <= real_border_width
        inleftborder = x <= real_border_width
        inbottomborder = height - y <= real_border_width
        inrightborder = width - x <= real_border_width
        self.inminsizebutton = inminsizebutton
        self.inmaxsizebutton = inmaxsizebutton
        self.inclosebutton = inclosebutton
        self.intitlebar = intitlebar
        self.intopborder = intopborder
        self.inleftborder = inleftborder
        self.inbottomborder = inbottomborder
        self.inrightborder = inrightborder
        if message == WM_NCCALCSIZE: return self.Handle_WM_NCCALCSIZE_Message(hwnd, message, wParam, lParam)
        if message == WM_NCHITTEST:
            VK_LBUTTON = 0x1
            isleftbuttonpressed = user32.GetKeyState(VK_LBUTTON) not in [0, 1]
            if not self.isMaximized():
                if intopborder and inleftborder: WM_NCHITTEST_result = HTTOPLEFT
                elif intopborder and inrightborder: WM_NCHITTEST_result = HTTOPRIGHT
                elif inbottomborder and inleftborder: WM_NCHITTEST_result = HTBOTTOMLEFT
                elif inbottomborder and inrightborder: WM_NCHITTEST_result = HTBOTTOMRIGHT
                elif inleftborder: WM_NCHITTEST_result = HTLEFT
                elif intopborder: WM_NCHITTEST_result = HTTOP
                elif inrightborder: WM_NCHITTEST_result = HTRIGHT
                elif inbottomborder: WM_NCHITTEST_result = HTBOTTOM
            if not 'WM_NCHITTEST_result' in dir():
                if inminsizebutton:
                    if not isleftbuttonpressed: self.setMenuButtonStyle(1, 1)
                    WM_NCHITTEST_result = HTMINBUTTON
                elif inmaxsizebutton:
                    if not isleftbuttonpressed: self.setMenuButtonStyle(2, 1)
                    WM_NCHITTEST_result = HTMAXBUTTON
                elif inclosebutton:
                    if not isleftbuttonpressed: self.setMenuButtonStyle(3, 1)
                    WM_NCHITTEST_result = HTCLOSE
                elif intitlebar:
                    WM_NCHITTEST_result = HTCAPTION
                else: WM_NCHITTEST_result = HTCLIENT
            if WM_NCHITTEST_result not in [HTMINBUTTON, HTMAXBUTTON, HTCLOSE]:
                if not isleftbuttonpressed: self.setMenuButtonStyle(0)
            return WM_NCHITTEST_result
        if message == WM_NCLBUTTONDOWN:
            if wParam in [HTMINBUTTON, HTMAXBUTTON, HTCLOSE]:
                if wParam == HTMINBUTTON: self.setMenuButtonStyle(1, 2)
                if wParam == HTMAXBUTTON: self.setMenuButtonStyle(2, 2)
                if wParam == HTCLOSE: self.setMenuButtonStyle(3, 2)
                return 0
            return user32.DefWindowProcW(hwnd, message, wParam, lParam)
        if message == WM_NCLBUTTONUP:
            self.setMenuButtonStyle(0)
            if wParam == HTMINBUTTON: self.minSizeButtonClicked()
            elif wParam == HTMAXBUTTON: self.maxSizeButtonClicked()
            elif wParam == HTCLOSE: self.closeButtonClicked()
            return user32.DefWindowProcW(hwnd, message, wParam, lParam)
        if message == WM_LBUTTONUP:
            self.setMenuButtonStyle(0)
        if message == WM_DPICHANGED:
            window_rect = RECT.from_address(lParam)
            realdpi = wParam >> 16
            self.realdpi = realdpi
            self.maximizedwindowborderwidth_list = self.getMaximizedWindowBorderWidth()
            x = window_rect.left
            y = window_rect.top
            width = int(window_rect.right - window_rect.left)
            height = int(window_rect.bottom - window_rect.top)
            if not self.highdpiscalingenabled: self.setGeometry(x, y, width, height)
            dpi = self.getdpibyrealdpi(realdpi)
            self.dpi = dpi
            self.setMinimumSize(int(220.0 * dpi / 96.0), int(48.0 * dpi / 96.0))
            self.updateconstantsfordpi()
            self.placeTitleBarAndClientArea()
            self.minSizeButton.update()
            self.maxSizeButton.update()
            self.closeButton.update()
            self.titleTextLabel.update()
            self.titleIconLabel.update()
        if message == WM_SETTINGCHANGE:
            try: lParam_string = str(ctypes.cast(lParam, ctypes.c_wchar_p).value)
            except: lParam_string = ''
            if wParam == SPI_SETWORKAREA:
                self.updateautohidetaskbarwidth()
                user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER | SWP_FRAMECHANGED)
            if wParam == SPI_SETNONCLIENTMETRICS:
                self.maximizedwindowborderwidth_list = self.getMaximizedWindowBorderWidth()
                self.captionfont = getcaptionfont()
                self.titleTextLabel.update()
            if self.themecolour == 0 and lParam_string == 'ImmersiveColorSet':
                self.setDarkTheme(0)
        if message == WM_DWMCOMPOSITIONCHANGED:
            self.isaeroenabled = isAeroEnabled()
            if self.isaeroenabled: self.setBlurEffect() if self.isblurwindow else self.setDWMShadowEffect()
            self.titleBar.update()
            self.clientAreaLabel.update()
        if message == WM_DWMNCRENDERINGCHANGED:
            if self.isaeroenabled: self.setBlurEffect() if self.isblurwindow else self.setDWMShadowEffect()
        if message == WM_ACTIVATE:
            isactivewindow = 0 if wParam == 0 else 1
            if not isactivewindow: self.setMenuButtonStyle(0)
        if message == WM_STYLECHANGED:
            if hasattr(self, 'nonclientareasizeinited'):
                if self.nonclientareasizeinited: self.SetWindowLong(self.hwnd, -16, 0xc00000 | 0x40000 | 0x20000 | 0x10000)
        if message == WM_SIZE:
            try: self.placeTitleBarAndClientArea()
            except: pass
        if message == WM_PAINT:
            if not self.windowinited: self.windowinited = True
        messagehandlerresult = self.MessageHandler(hwnd, message, wParam, lParam)
        if messagehandlerresult != None: return messagehandlerresult
        if ISPYSIDE1: return user32.CallWindowProcW(self.originalBasicMessageHandler, hwnd, message, wParam, lParam)
    def Handle_WM_NCCALCSIZE_Message(self, hwnd, message, wParam, lParam):
        user32 = ctypes.windll.user32
        try:
            leftautohidetaskbarwidth = self.leftautohidetaskbarwidth
            topautohidetaskbarwidth = self.topautohidetaskbarwidth
            rightautohidetaskbarwidth = self.rightautohidetaskbarwidth
            bottomautohidetaskbarwidth = self.bottomautohidetaskbarwidth
        except:
            leftautohidetaskbarwidth, topautohidetaskbarwidth, rightautohidetaskbarwidth, bottomautohidetaskbarwidth = 0, 0, 0, 0
        if wParam:
            rect = ctypes.cast(lParam, ctypes.POINTER(NCCALCSIZE_PARAMS)).contents.rgrc[0]
        else:
            rect = ctypes.cast(lParam, ctypes.POINTER(RECT)).contents
        ISMAXIMIZED = user32.IsZoomed(hwnd)
        try:
            maximizedwindowborderwidth_list = self.maximizedwindowborderwidth_list
        except:
            maximizedwindowborderwidth_list = [0, 0]
        if ISMAXIMIZED:
            self.windowmargin_left = maximizedwindowborderwidth_list[0] + leftautohidetaskbarwidth
            self.windowmargin_right = maximizedwindowborderwidth_list[0] + rightautohidetaskbarwidth
            self.windowmargin_top = maximizedwindowborderwidth_list[1] + topautohidetaskbarwidth
            self.windowmargin_bottom = maximizedwindowborderwidth_list[1] + bottomautohidetaskbarwidth
        else: self.windowmargin_left, self.windowmargin_right, self.windowmargin_top, self.windowmargin_bottom = 0, 0, 0, 0
        windowmargin_left = self.windowmargin_left
        windowmargin_right = self.windowmargin_right
        windowmargin_top = self.windowmargin_top
        windowmargin_bottom = self.windowmargin_bottom
        rect.left += windowmargin_left
        rect.right -= windowmargin_right
        rect.top += windowmargin_top
        rect.bottom -= windowmargin_bottom
        if hasattr(self, 'nonclientareasizeinited'):
            nonclientareasizeinited = self.nonclientareasizeinited
            if not nonclientareasizeinited:
                if ISPYSIDE1: self.SetWindowLong(self.hwnd, -16, 0xc00000 | 0x40000 | 0x20000 | 0x10000)
                self.nonclientareasizeinited = True
        return 0
    def minSizeButtonClicked(self):
        WM_SYSCOMMAND = 0x112
        SC_MINIMIZE = 0xf020
        ctypes.windll.user32.PostMessageW(self.hwnd, WM_SYSCOMMAND, SC_MINIMIZE, 0)
    def maxSizeButtonClicked(self):
        WM_SYSCOMMAND = 0x112
        SC_MAXIMIZE = 0xf030
        SC_RESTORE = 0xf120
        if self.isMaximized(): ctypes.windll.user32.PostMessageW(self.hwnd, WM_SYSCOMMAND, SC_RESTORE, 0)
        elif self.isFullScreen(): pass
        else: ctypes.windll.user32.PostMessageW(self.hwnd, WM_SYSCOMMAND, SC_MAXIMIZE, 0)
    def closeButtonClicked(self):
        WM_SYSCOMMAND = 0x112
        SC_CLOSE = 0xf060
        ctypes.windll.user32.PostMessageW(self.hwnd, WM_SYSCOMMAND, SC_CLOSE, 0)
    def getMaximizedWindowBorderWidth(self):
        SM_CXSIZEFRAME = 32
        SM_CYSIZEFRAME = 33
        SM_CXPADDEDBORDER = 92
        realdpi = self.realdpi
        if hasattr(ctypes.windll.user32, 'GetSystemMetricsForDpi'):
            borderwidth_x = ctypes.windll.user32.GetSystemMetricsForDpi(SM_CXSIZEFRAME, realdpi) + ctypes.windll.user32.GetSystemMetricsForDpi(SM_CXPADDEDBORDER, realdpi)
            borderwidth_y = ctypes.windll.user32.GetSystemMetricsForDpi(SM_CYSIZEFRAME, realdpi) + ctypes.windll.user32.GetSystemMetricsForDpi(SM_CXPADDEDBORDER, realdpi)
        else:
            borderwidth_x = ctypes.windll.user32.GetSystemMetrics(SM_CXSIZEFRAME) + ctypes.windll.user32.GetSystemMetrics(SM_CXPADDEDBORDER)
            borderwidth_y = ctypes.windll.user32.GetSystemMetrics(SM_CYSIZEFRAME) + ctypes.windll.user32.GetSystemMetrics(SM_CXPADDEDBORDER)
        return [borderwidth_x, borderwidth_y]
    def nativeEvent(self, eventType, msg):
        '''For PySide2/6, you should define MessageHandler instead of nativeEvent.'''
        WM_PAINT = 0xf
        WM_NCCALCSIZE = 0x83
        msg = MSG.from_address(msg.__int__())
        hwnd = msg.hWnd
        message = msg.message
        wParam = msg.wParam
        lParam = msg.lParam
        basicmessagehandlerresult = self.BasicMessageHandler(hwnd, message, wParam, lParam)
        if basicmessagehandlerresult != None: return True, basicmessagehandlerresult
        return super(CustomizedWindow, self).nativeEvent(eventType, msg)
    def setBlurEffect(self, hwnd=None, isEnableShadow=False):
        if hwnd == None: hwnd = self.hwnd
        try:
            dwmapi = ctypes.windll.dwmapi
            dwmapi.DwmSetWindowAttribute(hwnd, 2, ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int(2)))
            bb = DWM_BLURBEHIND()
            bb.dwFlags = 1
            bb.fEnable = 1
            win11_21h2_blur_code, win11_22h2_blur_code = self.setwin11blur(hwnd)
            if win11_22h2_blur_code:
                dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(MARGINS(1, 1, 0, 0)))
                dwmapi.DwmEnableBlurBehindWindow(ctypes.c_int(hwnd), ctypes.byref(bb))
            else:
                dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(MARGINS(-1, -1, -1, -1)))
                return 3
            try:
                AeroEffect = Win10BlurEffect()
                win10_blur_code = AeroEffect.setAeroEffect(hwnd, isEnableShadow=isEnableShadow)
                if win10_blur_code != 0: return 2
            except: pass
            return 1
        except: return 0
    def setDWMShadowEffect(self, hwnd=None):
        if hwnd == None: hwnd = self.hwnd
        try:
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 2, ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int(2)))
            ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(MARGINS(1, 1, 0, 0)))
            return 1
        except: return 0
    def getdpibyrealdpi(self, realdpi):
        realscalefactor = realdpi / 96.0
        if self.highdpiscalingenabled:
            if self.highdpiscalefactorroundingpolicy == 1: scalefactor = int(realscalefactor + 1) if realscalefactor - int(realscalefactor) > 0 else int(realscalefactor)
            elif self.highdpiscalefactorroundingpolicy == 2: scalefactor = int(realscalefactor)
            elif self.highdpiscalefactorroundingpolicy == 3: scalefactor = realscalefactor
            elif self.highdpiscalefactorroundingpolicy == 4: scalefactor = int(realscalefactor + 1) if realscalefactor - int(realscalefactor) >= 0.5 else int(realscalefactor)
            elif self.highdpiscalefactorroundingpolicy == 5: scalefactor = int(realscalefactor + 1) if realscalefactor - int(realscalefactor) > 0.5 else int(realscalefactor)
            dpi = int(float(realdpi) / scalefactor)
        else: dpi = realdpi
        return dpi
    def updateconstantsfordpi(self):
        dpi, realdpi = self.dpi, self.realdpi
        self.border_width = int(5.0 * dpi / 96.0)
        self.title_height = int(30.0 * dpi / 96.0)
        self.menubutton_width = int(46.0 * dpi / 96.0)
        self.title_font_size = int(13.0 * dpi / 96.0)
        self.real_border_width = int(5.0 * realdpi / 96.0)
        self.real_title_height = int(30.0 * realdpi / 96.0)
        self.real_menubutton_width = int(46.0 * realdpi / 96.0)
        self.titleiconlabel_margin = int(7.0 * dpi / 96.0)
    def updateautohidetaskbarwidth(self):
        autohidetaskbarposition = getautohidetaskbarposition()
        self.leftautohidetaskbarwidth = 2 if autohidetaskbarposition == 0 else 0
        self.topautohidetaskbarwidth = 2 if autohidetaskbarposition == 1 else 0
        self.rightautohidetaskbarwidth = 2 if autohidetaskbarposition == 2 else 0
        self.bottomautohidetaskbarwidth = 2 if autohidetaskbarposition == 3 else 0
    def setwin11blur(self, hWnd):
        Win11_21H2_ENTRY, Win11_22H2_ENTRY = 1029, 38
        Win11_21H2_VALUE, Win11_22H2_VALUE = 1, 3
        Win11_21H2_COMMAND, Win11_22H2_COMMAND = list(map(ctypes.windll.dwmapi.DwmSetWindowAttribute, [hWnd] * 2, [Win11_21H2_ENTRY, Win11_22H2_ENTRY], [ctypes.byref(ctypes.c_int(Win11_21H2_VALUE)), ctypes.byref(ctypes.c_int(Win11_22H2_VALUE))], [ctypes.sizeof(ctypes.c_int)] * 2))
        return (Win11_21H2_COMMAND, Win11_22H2_COMMAND)
    def GetWindowRect(self):
        lpRect = RECT()
        ctypes.windll.user32.GetWindowRect(self.hwnd, ctypes.byref(lpRect))
        return lpRect
    def GetClientRect(self):
        lpRect = RECT()
        ctypes.windll.user32.GetClientRect(self.hwnd, ctypes.byref(lpRect))
        return lpRect
    def splashScreen(self):
        '''You should call splashscreen.show after window.setWindowIcon, window.setDarkTheme,
and before window.setGeometry, window.move, window.resize,
call splashscreen.finish before window.show.
Example:
window.setWindowIcon(QIcon('Icon.ico'))
splashscreen = window.splashScreen()
splashscreen.show()
window.resize(int(400.0 * window.dpi / 96.0), int(175.0 * window.dpi / 96.0))
...
window.show()
splashscreen.finish(window)'''
        self.splashscreen = SplashScreen(self)
        return self.splashscreen
    def screenChangedHandler(self):
        hwnd = gethwnd(self.windowHandle())
        SWP_NOSIZE = 0x1
        SWP_NOMOVE = 0x2
        SWP_NOZORDER = 0x4
        SWP_FRAMECHANGED = 0x20
        ctypes.windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER | SWP_FRAMECHANGED)


class BlurWindow(CustomizedWindow):
    '''A blur window based on PySideX.
Blur effect is avaliable on Windows Vista and newer.'''
    def __init__(self):
        super(BlurWindow, self).__init__()


if __name__ == '__main__':
    try:
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    except: pass
    app = QApplication(sys.argv)
    window = BlurWindow()
    window.setDarkTheme(2)
    window.setWindowIcon(QIcon('Icon.ico'))
    splashscreen = window.splashScreen()
    splashscreen.show()
    window.resize(int(400.0 * window.dpi / 96.0), int(175.0 * window.dpi / 96.0))
    window.setWindowTitle('Window')
    button = QPushButton('Button', window.clientArea)
    window.show()
    splashscreen.finish(window)
    app.exec_()
