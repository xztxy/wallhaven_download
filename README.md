# Wallhaven_download
简单弄了一个GUI界面，来实现批量下载[wallhaven](https://wallhaven.cc/)图片的功能。

使用 PyQt5 库来创建一个图形用户界面 (GUI)。下面是程序的主要功能：
1、允许用户选择下载路径。
2、允许用户在 Wallhaven 上搜索图片。
3、允许用户选择搜索条件，如分辨率、纯度、类别等。
4、下载用户选择的图片并保存到所选文件夹中。
以下是实现这些功能的主要步骤：

导入必要的 Python 库。代码导入了以下库：

sys：提供系统相关的功能。
requests：用于 HTTP 请求和响应处理。
os：用于访问操作系统的功能，例如在文件系统中创建和操作文件夹。
BeautifulSoup：用于解析 HTML 和 XML 文档。
PyQt5：用于创建图形用户界面。
创建 WallhavenDownloader 类，该类继承了 QWidget。这个类包含以下方法：

init：类的构造函数。初始化各种变量和 GUI 组件，以及连接信号和槽。
initUI：创建 GUI 界面的布局和组件。
selectFolder：允许用户选择下载路径的函数。
setCategory：设置搜索条件中的类别。
setPurity：设置搜索条件中的纯度。
setAtleast：设置搜索条件中的至少分辨率。
setRatio：设置搜索条件中的宽高比。
setfenbianlv：设置搜索条件中的分辨率。
setPage：设置搜索条件中的页数。
searchImages：搜索符合条件的图片。
downloadImages：下载用户选择的图片。
创建 GUI 界面。
initUI 方法创建了各种组件，包括标签、文本框、下拉框、按钮等，然后将这些组件添加到垂直或水平布局中，并将这些布局添加到主布局中。

实现搜索功能。当用户点击搜索按钮时，searchImages 方法会执行以下操作：

构造 URL，将搜索条件添加到 URL 中。
发送 HTTP 请求，获取响应。
使用 BeautifulSoup 解析响应，提取图像 URL 并将其存储在 image_urls 变量中。
将这些 URL 显示在 QTextEdit 组件中。
实现下载功能。当用户点击下载按钮时，downloadImages 方法会执行以下操作：

创建所选文件夹（如果不存在）。
显示一个进度对话框，显示下载进度。
依次下载每个图像，将其保存到所选文件夹中。
