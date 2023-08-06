# CustomTkinterX
`customtkinter`的扩展组件功能库

## Fluent主题
尚未完善设置，修改了`CTk` `CTkToplevel` `CTkFrame` `CTkButton` `CTKEntry` `CTkComboBox`等类。
```python
from customtkinter import *
from customtkinterx import *

CTkFluentTheme()
```

## CTkCustom 自定义窗口
原窗口因标题栏与边框的限制，导致界面效果极差，但是仍可以通过一些方法自定义窗口`wm_overrideredirect`。
平台支持`Windows` `MacOS` `Linux`，其中界面效果支持最好的是`Windows`，`MacOS` `Linux`无法使用透明色，完全消除边框使用圆角，
及将图标保留至任务栏，采用置顶的方法保持窗口的显示。

### 组件结构
```markdown
| CTkCustom -> CTk
|-->> __frame_border(mainframe): CTkFrame
|-->> __frame_title(titlebar): CTkFrame
|-->> __label_title(titlebar_title): CTkLabel
|-->> __button_close(titlebar_closebutton): CTkButton
|-->> __button_minimize(titlebar_minimizebutton): CTkButton
```

### 基础示例
```python
from customtkinter import *
from customtkinterx import *

root = CTkCustom()

root.mainloop()
```

### 添加缩放窗口大小的手柄
```python
CTKCustom.create_sizegrip()
```
```python
from customtkinter import *
from customtkinterx import *

root = CTkCustom()
root.create_sizegrip()

root.mainloop()
```

## CTkInfoBar 消息栏
### 组件结构
```markdown
| CTkInforBar -> CTkFrame
|-->> __label_info(info): CTkLabel
```