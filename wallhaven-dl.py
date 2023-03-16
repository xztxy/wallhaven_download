import sys
import requests
import os
from bs4 import BeautifulSoup
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QLineEdit, QProgressDialog, QMessageBox


class WallhavenDownloader(QWidget):
    def __init__(self):
        super().__init__()

        # load the folder path if it exists
        self.settings = QSettings('MyApp', 'ImageDownloader')
        self.folder = self.settings.value('folder', None)
        self.folder_button = QPushButton("选择下载路径", self)
        self.folder_button.clicked.connect(self.selectFolder)
        self.search_edit = QLineEdit()
        self.search_edit.returnPressed.connect(self.searchImages)
        self.page_options = [str(i+1) for i in range(10)]

        self.category = "111"
        self.purity = "111"
        self.atleast = ""
        self.fenbianlv ="resolutions"
        self.ratio = ""
        self.page = "1"
        self.image_urls = []

        self.initUI()

    def initUI(self):

        category_label = QLabel("类别:")
        self.category_combo = QComboBox()
        self.category_combo.addItem("ALL", "111")
        self.category_combo.addItem("Anime", "010")
        self.category_combo.addItem("General", "100")
        self.category_combo.addItem("People", "001")       
        self.category_combo.currentIndexChanged.connect(self.setCategory)


        purity_label = QLabel("纯度:")
        self.purity_combo = QComboBox()
        purity_label = QLabel("纯度:")
        self.purity_combo = QComboBox()
        self.purity_combo.addItem("All", "111")
        self.purity_combo.addItem("SFW", "100")
        self.purity_combo.addItem("Sketchy", "010")
        self.purity_combo.addItem("NSFW", "001")
        self.purity_combo.addItem("SFW & Sketchy", "110")
        self.purity_combo.addItem("NSFW & Sketchy", "011")
        self.purity_combo.addItem("SFW & NSFW", "101")
        self.purity_combo.currentIndexChanged.connect(self.setPurity)

        atleast_label = QLabel("分辨率:")
        self.atleast_edit = QLineEdit()
        self.atleast_edit.setMaximumHeight(40)
        self.atleast_edit.setMinimumHeight(20)
        self.atleast_edit.setPlaceholderText("e.g. 1920x1080")
        self.atleast_edit.textChanged.connect(self.setAtleast)
        atleast_combo = QComboBox()
        atleast_combo.addItems(["", "640x480", "800x600", "1024x768", "1280x720", "1280x800", "1366x768",
                                "1440x900", "1600x900", "1680x1050", "1920x1080", "2560x1440", "3840x2160", "7680×4320", "4320x7680"])
        atleast_combo.activated[str].connect(self.setAtleast)
        self.atleast_edit.textChanged.connect(self.setAtleast)

        ratio_label = QLabel("宽高比:")
        self.ratio_combo = QComboBox()
        self.ratio_combo.addItem("")
        self.ratio_combo.addItem("16x9")
        self.ratio_combo.addItem("16x10")
        self.ratio_combo.addItem("9x16")
        self.ratio_combo.addItem("10x16")
        self.ratio_combo.addItem("21x9")
        self.ratio_combo.addItem("32x9")
        self.ratio_combo.addItem("48x9")
        self.ratio_combo.addItem("9x18")
        self.ratio_combo.addItem("5x4")
        self.ratio_combo.addItem("4x3")
        self.ratio_combo.currentIndexChanged.connect(self.setRatio)

        fenbianlv_label = QLabel()
        self.fenbianlv_combo = QComboBox()
        self.fenbianlv_combo.addItem("精准分辨率", "resolutions")
        self.fenbianlv_combo.addItem("至少分辨率", "atleast")
        self.fenbianlv_combo.currentIndexChanged.connect(self.setfenbianlv)

        page_label = QLabel("页数:")
        self.page_combo = QComboBox()
        for option in self.page_options:
            self.page_combo.addItem(option)
        self.page_combo.currentIndexChanged.connect(self.setPage)

        search_button = QPushButton("搜索")
        search_button.clicked.connect(self.searchImages)

        download_button = QPushButton("开始下载")
        download_button.clicked.connect(self.downloadImages)

        self.image_url_edit = QTextEdit()
        self.image_url_edit.setReadOnly(True)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.fenbianlv_combo)
 
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.folder_button)
        hbox4.addWidget(search_button)
        hbox4.addWidget(download_button)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(atleast_label)
        hbox5.addWidget(self.atleast_edit)
        hbox5.addWidget(atleast_combo)

        hbox6 = QHBoxLayout()
        hbox6.addWidget(category_label)
        hbox6.addWidget(self.category_combo)
        hbox6.addWidget(purity_label)
        hbox6.addWidget(self.purity_combo)

        hbox7 = QHBoxLayout()
        hbox7.addWidget(ratio_label)
        hbox7.addWidget(self.ratio_combo)
        hbox7.addWidget(page_label)
        hbox7.addWidget(self.page_combo)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addWidget(self.search_edit)
        vbox.addLayout(hbox7)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox4)
        vbox.addWidget(self.image_url_edit)
        self.setLayout(vbox)
        self.setWindowTitle("Wallhaven壁纸下载")
        
    def setCategory(self, index):
        self.category = self.category_combo.currentData()

    def setPurity(self, index):
        self.purity = self.purity_combo.currentData()

    def setAtleast(self, text):
        self.atleast = text

    def setRatio(self, index):
        self.ratio = self.ratio_combo.currentText()

    def setfenbianlv(self, index):
        self.fenbianlv = self.fenbianlv_combo.currentData()

    def setPage(self, index):
        self.page = self.page_combo.currentText()

    def selectFolder(self):
        self.folder = QFileDialog.getExistingDirectory(self, "选择下载路径", "./")
        if self.folder:
            self.settings.setValue('folder', self.folder)

    def searchImages(self):
        self.image_urls.clear()  # 清空之前的搜索记录
        query = self.search_edit.text()
        page_count = int(self.page_combo.currentText())
        for page in range(1, page_count+1):
            url = f"https://wallhaven.cc/search?q={query}&categories={self.category}&purity={self.purity}&{self.fenbianlv}={self.atleast}&ratios={self.ratio}&page={page}"
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                wallpapers = soup.select('figure > a.preview')
                for wallpaper in wallpapers:
                    preview_url = wallpaper['href']
                    response = requests.get(preview_url)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        img_tag = soup.select_one('img#wallpaper')
                        if img_tag:
                            self.image_urls.append(img_tag['src'])
            if self.image_urls:
                self.image_url_edit.setText("\n".join(self.image_urls))
            else:
                self.image_url_edit.setText("未发现壁纸.")



    def downloadImages(self):
        if not self.image_urls:
            self.image_url_edit.setText("未下载壁纸.")
            return

        # if the folder has not been set, ask the user to select one
        if not self.folder:
            self.selectFolder()
            # if the user cancels the dialog, abort the download
            if not self.folder:
                return

        # create a progress dialog to show download progress
        progress = QProgressDialog("下载中...", "取消", 0, len(self.image_urls), self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        progress.setWindowTitle("进度框")
        progress.setAutoReset(False)
        progress.show()

        downloaded_images = 0
        skipped_images = 0
        messages = []

        for i, url in enumerate(self.image_urls):
            filename = url.split("/")[-1]
            filepath = f"{self.folder}/{filename}"
            if os.path.isfile(filepath):
                skipped_images += 1
                message = f"{filename} 已存在."
                self.image_url_edit.setText(message)
                messages.append(message)
            else:
                response = requests.get(url, stream=True)
                total_length = response.headers.get('content-length')
                if total_length is None: # no content length header
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    with open(filepath, "wb") as f:
                        for data in response.iter_content(chunk_size=4096):
                            dl += len(data)
                            f.write(data)
                            done = int(100 * dl / total_length)
                            app.processEvents()  # allow the GUI to update
                            if progress.wasCanceled():
                                # stop the download and close the progress dialog
                                response.close()
                                progress.close()
                                message = f"{filename} 下载已取消."
                                self.image_url_edit.setText(message)
                                messages.append(message)
                                return
                downloaded_images += 1
                message = f"{filename} 下载成功."
                self.image_url_edit.setText(message)
                messages.append(message)
            progress.setValue(downloaded_images + skipped_images)
            progress.setLabelText(f"正在下载... ({downloaded_images + skipped_images}/{len(self.image_urls)})")
            if downloaded_images + skipped_images == len(self.image_urls):
                progress.setLabelText(f"所有壁纸下载完成.")
        self.image_url_edit.setText(f"成功下载 {downloaded_images} 张壁纸，{skipped_images} 张已存在.")
        if messages:
            QMessageBox.information(self, "提示", "\n".join(messages))

        # reset the folder attribute after download completes
        progress.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = WallhavenDownloader()
    widget.show()
    sys.exit(app.exec_())
