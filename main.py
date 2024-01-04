import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from pytube import YouTube

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        def get_immediate_subdirectories(a_dir):
            return [name for name in os.listdir(a_dir)
                if os.path.isdir(os.path.join(a_dir, name))]

        self.setWindowTitle("LCSongs by LimeGradient")
        self.setWindowIcon(QIcon('lc.ico'))
        self.setGeometry(0, 0, 500, 130)

        profiles = get_immediate_subdirectories(f"{os.getenv('APPDATA')}\\Thunderstore Mod Manager\\DataFolder\\LethalCompany\\profiles")
        songs_dir = ""
        def setSongDir(dir):
            nonlocal songs_dir
            songs_dir = dir

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(2)
        yt_link_layout = QHBoxLayout()
        output_path_layout = QHBoxLayout()

        title_label = QLabel("LCSongs by LimeGradient")
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        mainLayout.addWidget(title_label)

        yt_link_label = QLabel("Youtube Link: ")
        yt_link_enter = QLineEdit()
        yt_link_enter.setMaxLength(75)

        # C:\Users\Kevin Burns\AppData\Roaming\Thunderstore Mod Manager\DataFolder\LethalCompany\profiles\Main\BepInEx\plugins\Custom Songs

        output_path_label = QLabel("Output Path: ")
        output_path_enter = QLineEdit()
        for profile in profiles:
            profile_button = QPushButton(f"Select Profile: {profile}")
            profile_button.clicked.connect(lambda: output_path_enter.insert(f"{os.getenv('APPDATA')}\\Thunderstore Mod Manager\\DataFolder\\LethalCompany\\profiles\\{profile}\\BepInEx\\plugins\\Custom Songs"))
            mainLayout.addWidget(profile_button)


        yt_link_layout.addWidget(yt_link_label)
        yt_link_layout.addWidget(yt_link_enter)
        output_path_layout.addWidget(output_path_label)
        output_path_layout.addWidget(output_path_enter)

        mainLayout.addLayout(yt_link_layout)
        mainLayout.addLayout(output_path_layout)

        download_button = QPushButton("Download", self)
        download_button.clicked.connect(lambda: self.DownloadYTToMP3(yt_link_enter.text(), output_path_enter.text()))
        mainLayout.addWidget(download_button)

        open_profile_folder_button = QPushButton("Open Profile Folder", self)
        open_profile_folder_button.clicked.connect(lambda: os.system(f"explorer {output_path_enter.text()}"))
        mainLayout.addWidget(open_profile_folder_button)

        wid = QWidget(self)
        wid.setLayout(mainLayout)
        self.setCentralWidget(wid)
        self.show()
    
    def DownloadYTToMP3(self, link, path):
        if path == "":
            path = "."
        yt = YouTube(link)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=path)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        print(yt.title + " successfully downloaded")
        msg = QMessageBox()
        msg.setWindowTitle("Downloaded " + yt.title)
        msg.setText("Downloaded " + yt.title)
        x = msg.exec_()

app = QApplication(sys.argv)
mw = MainWindow()
sys.exit(app.exec_())