# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.py'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!




import sys,re,json,zipfile,random,string
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import  QtGui
import signin
import dkdrive_2
import request,time
import  webbrowser,OC_api,os

login_url = 'http://10.20.30.25'
user_name = 'admin'
user_pass = 'admin'
user_oc = OC_api.rewrite_oc(login_url, user_name, user_pass)
#
cwd = os.getcwd()
conf_dir = os.path.join(cwd , 'conf')
conf_file = os.path.join(cwd,'conf/config')
with open(conf_file,mode='r',encoding='utf-8') as f:
    oc_config = json.load(f)
data_dir = oc_config['data_dir']


#
class Mylabel(QLabel):
    clicked = QtCore.pyqtSignal()
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()


# 
class sign_in_page(QDialog, signin.Ui_Dialog):
    def __init__(self, parent=None):
        super(sign_in_page, self).__init__(parent)
        self.setupUi(self)
        #
        self.user_passwd.setEchoMode(QLineEdit.Password)
    # 
    def sign_in(self):
        user_name = self.user_name.text()
        user_passwd = self.user_passwd.text()
        try:
            oc.login(user_name.strip(),user_passwd.strip())
        except Exception as  e:
            print(e)
            self.user_name.setText("")
            self.user_passwd.setText("")
            self.check_ret.setText("wrong")
        else:
            dkd.show()
            myWin.close()
    # 
    def sign_up(self):
        pass

# 
class general_dialog(QWidget):
    def __init__(self,sharelink_info):
        super(general_dialog,self).__init__()
        self.setObjectName("general_dialog")
        self.resize(629, 104)
        self.setMinimumSize(QtCore.QSize(629, 104))
        self.setMaximumSize(QtCore.QSize(629, 104))
        self.copy_btn = QPushButton(self)
        self.copy_btn.setGeometry(QtCore.QRect(550, 40, 41, 23))
        self.copy_btn.setObjectName("copy_btn")
        self.copy_btn.setText('复制')
        self.label_context = QLabel(self)
        self.label_context.setGeometry(QtCore.QRect(50, 40, 491, 21))
        self.label_context.setObjectName("label_context")
        self.label_context.setText(sharelink_info)
        #
        self.copy_btn.clicked.connect(lambda :self.copy_text(sharelink_info))
    #
    def copy_text(self,text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        ret = QMessageBox.information(self,'','复制成功')
        self.close()





#
class dkdrive_page2(QMainWindow, dkdrive_2.Ui_MainWindow):
    def __init__(self,parent=None):
        super(dkdrive_page2, self).__init__(parent)
        self.setupUi(self)
        #
        self.left_widget.setFrameShape(QListWidget.NoFrame)
        self.left_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.left_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        for i in [self.finish_table,self.download_table,self.upload_table]:
            i.setEditTriggers(QAbstractItemView.NoEditTriggers)
            i.horizontalHeader().setVisible(False)
            i.verticalHeader().setVisible(False)

        self.table_test = QTableWidget(self.my_drive)
        self.table_test.setGeometry(QtCore.QRect(-1,50,1111,701))
        self.table_test.setObjectName("table_test")
        self.table_test.setColumnCount(4)
        self.table_test.setHorizontalHeaderLabels(['','文件名','修改时间','大小'])
        self.table_test.setStyleSheet('font: 12pt "微软雅黑";')



        self.search_btn.clicked.connect(self.func_search_btn)

        self.search_edit.returnPressed.connect(self.func_search_btn)

        self.return_btn.clicked.connect(self.func_return_btn)

        self.current_dir_edit.returnPressed.connect(self.func_return_btn)

        self.upload_dir.clicked.connect(self.func_upload_dir_btn)
        self.upload_file.clicked.connect(self.func_upload_file_btn)




        self.table_test.setEditTriggers(QAbstractItemView.NoEditTriggers)


        self.table_test.resizeColumnsToContents()

        self.table_test.setColumnWidth(0,20)
        self.table_test.setColumnWidth(1,500)
        self.table_test.setColumnWidth(2,250)
        self.table_test.setColumnWidth(3,100)

        self.table_test.horizontalHeader().setSectionResizeMode(0,QHeaderView.Fixed)
        self.table_test.horizontalHeader().setSectionResizeMode(1,QHeaderView.Fixed)
        self.table_test.horizontalHeader().setSectionResizeMode(2,QHeaderView.Fixed)
        self.table_test.horizontalHeader().setSectionResizeMode(3,QHeaderView.Fixed)
        self.table_test.horizontalHeader().setHighlightSections(False)
        self.table_test.verticalHeader().setVisible(False)
        self.table_test.setVerticalHeaderLabels(['a','b'])
        self.table_test.setShowGrid(False)
        self.table_test.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.table_test.customContextMenuRequested.connect(self.generateMenu)
        self.user_oc = OC_api.rewrite_oc(login_url,user_name,user_pass)
        self.files_refresh()
        self.my_count,self.dir_list=self.user_oc._file_list()
        self.whole_files = self.user_oc._whole_file()
        self.table_test.setRowCount(self.my_count)
        for d in self.dir_list:
            ft = self.user_oc.is_dir(d)
            if ft:
                ft = 'dir'
            else:
                ft = 'file'
            self.table_test.setCellWidget(self.dir_list.index(d),1,self.show_files(my_file_path=d,file_type=ft))
            whole_file_info = self.user_oc.file_info(d)
            if str(whole_file_info['file_size'])  == 'None':
                Size = QTableWidgetItem('-')
                self.table_test.setItem(self.dir_list.index(d),3,Size)
            else:
                s = whole_file_info['file_size']
                if s < 1024:
                    s = str(s) + ' ' + 'B'
                elif 1048576> s >=1024:
                    s = str(format(float(s)/1024,'.2f')) + ' ' + 'KB'
                elif 1073741824> s >=1048576:
                    s = str(format(float(s)/1048576,'.2f')) + ' ' + 'MB'
                elif 1099511627776 > s >=1073741824:
                    s = str(format(float(s)/1073741824,'.2f')) + ' ' + 'GB'
                else :
                    s = str(format(float(s)/1099511627776,'.2f')) + ' ' + 'TB'
                Size = QTableWidgetItem(s)
                self.table_test.setItem(self.dir_list.index(d),3,Size)
            t = str(whole_file_info['file_modify'])
            Date = QTableWidgetItem(t)
            Date.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.table_test.setItem(self.dir_list.index(d),2,Date)

    def files_refresh(self):
        file_stf = self.user_oc._whole_rets()
        ret = []
        for i in range(len(file_stf)):
            ret.append(list(file_stf[i]))
        if os.path.exists('f_lst'):
            with open('f_lst', mode='r', encoding='utf-8') as f:
                self.gg = json.load(f)
                if self.gg != ret:
                    with open('f_lst', mode='w', encoding='utf-8') as f:
                        json.dump(ret, f)
                        return ret
                else:
                    return  ret
        else:
            with open('f_lst',mode='w',encoding='utf-8') as f:
                json.dump(ret,f)
                return ret
    def generateMenu(self,pos):
        cell = self.table_test.selectionModel().selection().indexes()
        if len(cell) == 0:
            return
        self.row_index = cell[0].row()
        column_index = cell[0].column()
        if self.row_index < self.my_count and column_index == 1:
            menu = QMenu()
            item_download = menu.addAction(u'下载')
            item_delete = menu.addAction(u'删除')
            item_share = menu.addAction(u'分享')
            item_rename = menu.addAction(u'重命名')
            item_mv = menu.addAction(u'移动')
            action = menu.exec_(self.table_test.mapToGlobal(pos))

            if action == item_download:
                choice = self.dir_list[self.row_index] 
                ft = self.user_oc.is_dir(choice)
                if ft:
                    ft = 'dir'
                    ret = self.select_local_datapath(ft)
                else:
                    ft = 'file'
                    ret = self.user_oc.file_info(choice)
                    ret = os.path.basename(ret['file_name'])
                    ret = self.select_local_datapath(ft,file_localte=ret) 
                self.downloadThread = download_Thread()
                self.downloadThread.setfun_attr(choice, ft, ret)
                self.downloadThread.start()
                self.downloadThread.trigger.connect(self.link_donothing)
            elif action == item_delete:
                print(2)

            elif action == item_share:
                choice = self.dir_list[self.row_index] 
                check_code = ''.join(random.sample(string.ascii_letters + string.digits,5))
                info = self.user_oc._share_file_link(choice, password=check_code)
                value = info.get_link() + ' 验证码：' + check_code 

                self.sharelink = general_dialog(value)
                self.sharelink.show()



            elif action == item_rename:
                print(4)
            elif action == item_mv:
                print(5)
            else:
                return
        else:
            return


    def label_clicked(self,parent_dir=None,new_item_reload=None):
        if parent_dir == None  : 
            cell = self.table_test.selectionModel().selection().indexes()
            row_index = cell[0].row()
            column_index = cell[0].column()
        else:
            column_index = 1
        if column_index == 1:
            if parent_dir == None :
                select_file = self.dir_list[row_index]
            else:
                select_file = parent_dir
            self.current_dir_edit.setText(str(self.user_oc.file_info(select_file)['file_path']))
            self.next_my_count,self.next_dir_list = self.user_oc._file_list(select_file)
            if self.next_my_count == 0 and self.user_oc.is_dir(select_file) == True:
                self.table_test.setRowCount(0)
            elif self.next_my_count == 0 and self.user_oc.is_dir(select_file) == False:
                pass
            else:
                self.table_test.setRowCount(self.next_my_count)
                self.dir_list = self.next_dir_list
                for d in self.dir_list:
                    ft = self.user_oc.is_dir(d)
                    if ft:
                        ft = 'dir'
                    else:
                        ft = 'file'
                    self.table_test.setCellWidget(self.dir_list.index(d),1,self.show_files(my_file_path=d,file_type=ft))
                    whole_file_info = self.user_oc.file_info(d)
                    if str(whole_file_info['file_size']) == 'None':
                        Size = QTableWidgetItem('-')
                        self.table_test.setItem(self.dir_list.index(d), 3, Size)
                    else:
                        s = whole_file_info['file_size']
                        if s < 1024:
                            s = str(s) + ' ' + 'B'
                        elif 1048576 > s >= 1024:
                            s = str(format(float(s) / 1024, '.2f')) + ' ' + 'KB'
                        elif 1073741824 > s >= 1048576:
                            s = str(format(float(s) / 1048576, '.2f')) + ' ' + 'MB'
                        elif 1099511627776 > s >= 1073741824:
                            s = str(format(float(s) / 1073741824, '.2f')) + ' ' + 'GB'
                        else:
                            s = str(format(float(s) / 1099511627776, '.2f')) + ' ' + 'TB'
                        Size = QTableWidgetItem(s)
                        self.table_test.setItem(self.dir_list.index(d), 3, Size)
                    t = str(whole_file_info['file_modify'])
                    Date = QTableWidgetItem(t)
                    Date.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                    self.table_test.setItem(self.dir_list.index(d), 2, Date)
    def link_donothing(self):
        pass
    def func_search_btn(self):
        search_stf = self.search_edit.text().strip()
        match_list = []
        for stf in self.whole_files:
            if search_stf in stf:
                match_list.append(stf)
        count = len(match_list)
        self.table_test.setRowCount(count)

        self.dir_list = match_list

        for d in self.dir_list:
            ft = self.user_oc.is_dir(d)
            if ft:
                ft = 'dir'
            else:
                ft = 'file'
            self.table_test.setCellWidget(self.dir_list.index(d), 1, self.show_files(my_file_path=d,file_type=ft))
            whole_file_info = self.user_oc.file_info(d)

            if str(whole_file_info['file_size']) == 'None':
                Size = QTableWidgetItem('-')
                self.table_test.setItem(self.dir_list.index(d), 3, Size)
            else:
                s = whole_file_info['file_size']
                if s < 1024:
                    s = str(s) + ' ' + 'B'
                elif 1048576 > s >= 1024:
                    s = str(format(float(s) / 1024, '.2f')) + ' ' + 'KB'
                elif 1073741824 > s >= 1048576:
                    s = str(format(float(s) / 1048576, '.2f')) + ' ' + 'MB'
                elif 1099511627776 > s >= 1073741824:
                    s = str(format(float(s) / 1073741824, '.2f')) + ' ' + 'GB'
                else:
                    s = str(format(float(s) / 1099511627776, '.2f')) + ' ' + 'TB'
                Size = QTableWidgetItem(s)
                self.table_test.setItem(self.dir_list.index(d), 3, Size)

            t = str(whole_file_info['file_modify'])
            Date = QTableWidgetItem(t)

            Date.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.table_test.setItem(self.dir_list.index(d), 2, Date)



    def func_return_btn(self):

        current_dir = self.current_dir_edit.text().strip()

        while current_dir.endswith('/'):
            current_dir = current_dir[:-1]

        if current_dir + '/' not in self.whole_files:
            parent_dir = '/'
        else:
            parent_dir = os.path.dirname(current_dir)

        self.label_clicked(parent_dir=str(parent_dir))

    def func_upload_file_btn(self):

        current_dir = self.current_dir_edit.text().strip()
        self.whole_files.append('/')
        while current_dir + '/' not in self.whole_files:
            if current_dir == '/':
                break
            else:
                current_dir = current_dir[:-1]

        self.current_dir_edit.setText(current_dir)

        if current_dir != '/':
            current_dir += '/'

        fname,_ = QFileDialog.getOpenFileNames()
        for file in fname:

            self.uploadThread = upload_Thread()

            self.uploadThread.setfun_attr(current_dir,'file',file)  
            self.uploadThread.start()
            self.uploadThread.trigger.connect(lambda :self.refresh(current_dir))
        self.message('上传完成')




    def func_upload_dir_btn(self):

        current_dir = self.current_dir_edit.text().strip()
        self.whole_files.append('/')
        while current_dir + '/' not in self.whole_files:
            if current_dir == '/':
                break
            else:
                current_dir = current_dir[:-1]

        self.current_dir_edit.setText(current_dir)

        if current_dir != '/':
            current_dir += '/'
        local_file = oc_config['data_dir']
        fname = QFileDialog.getExistingDirectory(self, '目录', local_file)


        self.uploadThread = upload_Thread()

        self.uploadThread.setfun_attr(current_dir,'dir',fname)  
        self.uploadThread.start()

        self.uploadThread.trigger.connect(lambda :self.refresh(current_dir))





    def show_files(self,my_file_path=None,file_type='dir'):

        my_widget = QWidget()
        my_label1 = Mylabel()
        my_label1.setText('')
        if file_type == 'file':
            my_label1.setStyleSheet('image: url(:/my_pic/file_icon.png);')
        else:

            my_label1.setStyleSheet('image: url(:/my_pic/dir_icon.png);')
        my_label1.clicked.connect(self.link_donothing)

        my_label2 = Mylabel()
        my_label2.setText(str(my_file_path))
        my_label2.setStyleSheet('font: 12pt "微软雅黑";')
        my_label2.clicked.connect(self.label_clicked)

        my_hlayout = QHBoxLayout(self,spacing=10)
        my_hlayout.addWidget(my_label1)
        my_hlayout.addWidget(my_label2)
        my_hlayout.setStretch(0,1)

        my_hlayout.setStretch(1,25)
        my_hlayout.setContentsMargins(0,0,0,0)
        my_widget.setLayout(my_hlayout)
        return my_widget

    def refresh(self,current_dir):
        print(current_dir)
        self.num,self.dir_list = self.user_oc._file_list(file_path=current_dir)
        print(self.num,self.dir_list)
        self.table_test.setRowCount(self.num)
        for d in self.dir_list:
            print(d)
            ft = self.user_oc.is_dir(d)
            if ft:
                ft = 'dir'
            else:
                ft = 'file'
            row_num = self.dir_list.index(d)
            print(row_num)
            self.table_test.setCellWidget(row_num, 1, self.show_files(my_file_path=d, file_type=ft))
            whole_file_info = self.user_oc.file_info(d)

            if str(whole_file_info['file_size']) == 'None':
                Size = QTableWidgetItem('-')
                self.table_test.setItem(row_num, 3, Size)
            else:
                s = whole_file_info['file_size']
                if s < 1024:
                    s = str(s) + ' ' + 'B'
                elif 1048576 > s >= 1024:
                    s = str(format(float(s) / 1024, '.2f')) + ' ' + 'KB'
                elif 1073741824 > s >= 1048576:
                    s = str(format(float(s) / 1048576, '.2f')) + ' ' + 'MB'
                elif 1099511627776 > s >= 1073741824:
                    s = str(format(float(s) / 1073741824, '.2f')) + ' ' + 'GB'
                else:
                    s = str(format(float(s) / 1099511627776, '.2f')) + ' ' + 'TB'
                Size = QTableWidgetItem(s)
                self.table_test.setItem(row_num, 3, Size)

            t = str(whole_file_info['file_modify'])
            Date = QTableWidgetItem(t)

            Date.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.table_test.setItem(row_num, 2, Date)
        self.message('上传完成')


    def select_local_datapath(self,ft,file_localte='example'):
        if ft == 'dir':
            local_file = oc_config['data_dir']
            fname = QFileDialog.getExistingDirectory(self,'目录',local_file)
            return fname
        elif ft == 'file':
            local_file = oc_config['data_dir'] + '\\' + file_localte
            fname = QFileDialog.getSaveFileName(self,'存储地址',local_file,"All Files (*);;Text Files (*.txt)")
            if fname[0]:
                return fname[0]
            else:
                return

    def message(self,text):
        reply = QMessageBox.information(self,'提示',text,QMessageBox.Yes)


def trige_con():
    print('finish_write')




class download_Thread(QtCore.QThread):
    trigger = QtCore.pyqtSignal()
    def __init__(self):
        super(download_Thread,self).__init__()
        self.user_oc = OC_api.rewrite_oc(login_url, user_name, user_pass)
    def setfun_attr(self,choice,ft,local_path): 
        self.choice = choice
        self.ft = ft
        self.data_locate = local_path
    def data_download(self):
        if self.ft == 'dir':

            num = ''
            for i in range(20):
                num += str(random.randint(0, 9))
                i += 1
            local_filename = self.data_locate + '\\' + num + '.zip'

            self.user_oc.get_dir_zip(self.choice, local_filename)
            """unzip zip file"""
            zip_file = zipfile.ZipFile(local_filename)
            zip_file.extractall(self.data_locate)
            zip_file.close()
            os.remove(local_filename)
        elif self.ft == 'file':
            self.user_oc.get_file(self.choice,local_file=self.data_locate)
    def run(self):
        self.data_download()
        self.trigger.emit()


class upload_Thread(QtCore.QThread):
    trigger = QtCore.pyqtSignal()
    def __init__(self):
        super(upload_Thread, self).__init__()
        
    def setfun_attr(self, user_choice, file_type, data_locate):  
        self.choice = user_choice
        self.ft = file_type
        self.data_locate = data_locate

    def data_upload(self):
        if self.ft == 'dir':

            self.user_oc._put_directory(self.choice,self.data_locate)

        elif self.ft == 'file':

            self.user_oc._put_file(self.choice,self.data_locate)

    def run(self):
        self.data_upload()
        self.trigger.emit()






if __name__ == '__main__':
    app = QApplication(sys.argv)

    splash = QSplashScreen(QtGui.QPixmap(":/my_pic/install.jpg"))

    #splash.show()

    splash.showMessage(u'程序正在加载。。。', QtCore.Qt.AlignCenter, QtCore.Qt.red)
    #time.sleep(3)
    app.processEvents()
    #dkd = dkdrive_page2()
    myWin = dkdrive_page2()
    myWin.show()
    splash.finish(myWin)
    sys.exit(app.exec_())