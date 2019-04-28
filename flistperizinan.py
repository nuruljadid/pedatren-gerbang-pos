
import sys, os, json, pedatren, notification, fdetailperizinan
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from datetime import datetime


Pedatren = pedatren.Pedatren()

class Ui_TablePerizinan(QtWidgets.QMainWindow):
    __childDialog = None
    __userProfile = None
    switch_window = QtCore.pyqtSignal()
    switchClose = False

    def __init__(self):
        super(Ui_TablePerizinan, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui_listperizinan.ui'), self)
        self.setWindowIcon( QtGui.QIcon( os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img/logo.png') ) )
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.label_fotodiri.setText('')

        self.buttonRefresh.clicked.connect(self.refreshOnClicked)
        self.tablePerizinan.doubleClicked.connect(self.doubleClickRow)

        self.buildTable()



    def buildTable(self):

        response = Pedatren.getListPerizinan()
        if response.status_code < 200 or response.status_code >= 300:
            self.switchClose = True
            self.close()
            self.switch_window.emit()
            return False


        listPerizinan = json.loads(response.text)
        self.buildHeaderTable()
        self.buildRowTable(listPerizinan)

        self.tablePerizinan.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tablePerizinan.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.tablePerizinan.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.tablePerizinan.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        self.tablePerizinan.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        self.tablePerizinan.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        self.tablePerizinan.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
        self.tablePerizinan.horizontalHeader().setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
        self.tablePerizinan.horizontalHeader().setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
        self.tablePerizinan.horizontalHeader().setSectionResizeMode(9, QtWidgets.QHeaderView.Stretch)
        self.tablePerizinan.horizontalHeader().setSectionResizeMode(10, QtWidgets.QHeaderView.ResizeToContents)

        self.statusBar().showMessage(' Data terakhir diperbaharui: ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) )

        responseUserProfile = Pedatren.getUserProfile()
        if responseUserProfile.status_code >= 200 or responseUserProfile.status_code < 300:
            self.__userProfile = json.loads(responseUserProfile.text)

        if self.__userProfile:
            self.label_credential_nama_lengkap.setText(Pedatren.credentials['nama_lengkap'] if Pedatren.credentials else '-')
            self.label_credential_nama_lengkap.adjustSize()


            userProfileFoto = Pedatren.getImage(self.__userProfile['fotodiri']['small'])
            qimg = QtGui.QImage.fromData(userProfileFoto.content)
            pixmap = QtGui.QPixmap.fromImage(qimg)
            self.label_fotodiri.setPixmap(pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio))

            self.label_credential_nik.setText(self.__userProfile['nik'])
            self.label_credential_nik.adjustSize()



        return True

    def buildHeaderTable(self):
        headers = ['id_perizinan', 'NIS Santri', 'Nama Lengkap', 'Gender', 'Domisili', 'Lembaga', 'Alasan Izin', 'Bermalam', 'Rombongan', 'Tujuan', 'status']
        self.tablePerizinan.setColumnCount(len(headers))
        self.tablePerizinan.setHorizontalHeaderLabels(headers)
        font = QtGui.QFont()
        font.setBold(True)
        self.tablePerizinan.horizontalHeader().setFont(font)

    def buildRowTable(self, data):
        no = 0
        self.tablePerizinan.setRowCount(len(data))
        for row in data:
            pemohonIzin = row['pemohon_izin']

            self.tablePerizinan.setItem(no, 0, QtWidgets.QTableWidgetItem(row['id']))
            self.tablePerizinan.setItem(no, 1, QtWidgets.QTableWidgetItem(pemohonIzin['nis_santri']))
            self.tablePerizinan.setItem(no, 2, QtWidgets.QTableWidgetItem(pemohonIzin['nama_lengkap']))

            jenis_kelamin = QtWidgets.QTableWidgetItem(pemohonIzin['jenis_kelamin'])
            jenis_kelamin.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.tablePerizinan.setItem(no, 3, jenis_kelamin)

            self.tablePerizinan.setItem(no, 4, QtWidgets.QTableWidgetItem(pemohonIzin['domisili_santri']))
            self.tablePerizinan.setItem(no, 5, QtWidgets.QTableWidgetItem(pemohonIzin['lembaga']))

            self.tablePerizinan.setItem(no, 6, QtWidgets.QTableWidgetItem(row['alasan_izin']))

            self.tablePerizinan.setItem(no, 7, QtWidgets.QTableWidgetItem( row['bermalam'] + ( ' - (' + row['selama'] + ')' if row['bermalam'] == 'Y' else '') ) )
            rombongan = QtWidgets.QTableWidgetItem(row['rombongan'])
            rombongan.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            self.tablePerizinan.setItem(no, 8, rombongan)

            self.tablePerizinan.setItem(no, 9, QtWidgets.QTableWidgetItem(row['kecamatan_tujuan']))

            statusIzin = QtWidgets.QTableWidgetItem(row['status_perizinan'])
            statusIzin.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            font = QtGui.QFont()
            font.setBold(True)
            statusIzin.setFont(font)
            if row['id_status_perizinan'] == 5:
                statusIzin.setForeground(QtGui.QColor.fromRgb(255, 0, 0))
            elif row['id_status_perizinan'] == 4:
                statusIzin.setForeground(QtGui.QColor.fromRgb(0, 85, 255))
            elif row['id_status_perizinan'] == 3:
                statusIzin.setForeground(QtGui.QColor.fromRgb(0, 170, 0))
            self.tablePerizinan.setItem(no, 10, statusIzin)

            no += 1

        self.tablePerizinan.hideColumn(0)


    def refreshOnClicked(self):
        # Preventif dari badai klik tombol refresh yg seakan-akan spt ngeflood request api
        self.buttonRefresh.setEnabled(False)
        QtCore.QTimer.singleShot(10000, lambda: self.buttonRefresh.setDisabled(False))

        self.tablePerizinan.clear()
        self.tablePerizinan.setRowCount(0)
        self.tablePerizinan.setColumnCount(0)
        self.buildTable()

    def doubleClickRow(self):

        self.tablePerizinan.showColumn(0)
        # for currentQTableWidgetItem in self.tablePerizinan.selectedItems():
        #     print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
        # print('*****************************')
        # print(self.tablePerizinan.selectedItems()[0].text())
        # print('*****************************')
        selectedIdPerizinan = self.tablePerizinan.selectedItems()[0].text()
        self.tablePerizinan.hideColumn(0)

        response = Pedatren.getItemPerizinan(selectedIdPerizinan)
        if response.status_code < 200 or response.status_code >= 300:
            textBody = json.loads(response.text)
            notification.showNotif(textBody['message'])
        else:

            dataPerizinan = json.loads(response.text)

            pemohonIzin = dataPerizinan['pemohon_izin']

            pengantar = dataPerizinan['pengantar']
            pembuatIzin = dataPerizinan['pembuat_izin']
            persetujuanPengasuh = dataPerizinan['persetujuan_pengasuh']
            persetujuanBiktren = dataPerizinan['persetujuan_biktren']
            pemberitahuanKamtib = dataPerizinan['pemberitahuan_kamtib']

            self.__childDialog = fdetailperizinan.Ui_DetailPerizinan()

            fotodiri = pemohonIzin['fotodiri']
            fotoPemohonIzin = Pedatren.getImage(fotodiri['medium'])
            # print(fotoPemohonIzin.content)
            qimg = QtGui.QImage.fromData(fotoPemohonIzin.content)
            pixmap = QtGui.QPixmap.fromImage(qimg)
            self.__childDialog.label_fotodiri.setPixmap(pixmap.scaled(170, 170, QtCore.Qt.KeepAspectRatio))

            self.__childDialog.label_nama_lengkap.setText(pemohonIzin['nama_lengkap'])
            self.__childDialog.label_nama_lengkap.adjustSize()
            self.__childDialog.label_domisili.setText(pemohonIzin['domisili_santri'])
            self.__childDialog.label_domisili.adjustSize()
            lembaga = pemohonIzin['lembaga'] if pemohonIzin['lembaga'] else '-'
            jurusan = ' - ' + pemohonIzin['jurusan'] if pemohonIzin['jurusan'] else ''
            kelas = ' [' + pemohonIzin['kelas'] + ']' if pemohonIzin['kelas'] else ''
            self.__childDialog.label_lembaga.setText(lembaga+jurusan+kelas)
            self.__childDialog.label_lembaga.adjustSize()
            self.__childDialog.label_alamat.setText(pemohonIzin['alamat'])
            self.__childDialog.label_alamat.adjustSize()

            self.__childDialog.label_alasan_izin.setText(dataPerizinan['alasan_izin'])
            self.__childDialog.label_alasan_izin.adjustSize()
            self.__childDialog.label_tujuan.setText(dataPerizinan['kecamatan_tujuan'])
            self.__childDialog.label_tujuan.adjustSize()
            self.__childDialog.label_lama_izin.setText(dataPerizinan['selama'] + '\nSejak      ' + dataPerizinan['sejak_tanggal'] + '\nSampai   ' + dataPerizinan['sampai_tanggal'])
            self.__childDialog.label_lama_izin.adjustSize()
            self.__childDialog.label_bermalam.setText(dataPerizinan['bermalam'])
            self.__childDialog.label_bermalam.adjustSize()
            self.__childDialog.label_rombongan.setText(dataPerizinan['rombongan'])
            self.__childDialog.label_rombongan.adjustSize()

            self.__childDialog.label_pengantar.setText(pengantar['nama_lengkap'] if pengantar['nama_lengkap'] else '-')
            self.__childDialog.label_pengantar.adjustSize()
            self.__childDialog.label_pembuat_izin.setText(pembuatIzin['nama_lengkap'] if pembuatIzin['nama_lengkap'] else '-')
            self.__childDialog.label_pembuat_izin.adjustSize()
            self.__childDialog.label_biktren.setText(persetujuanBiktren['nama_lengkap'] if persetujuanBiktren['nama_lengkap'] else '-')
            self.__childDialog.label_biktren.adjustSize()
            self.__childDialog.label_pengasuh.setText(persetujuanPengasuh['nama_lengkap'] if persetujuanPengasuh['nama_lengkap'] else '-')
            self.__childDialog.label_pengasuh.adjustSize()
            self.__childDialog.label_kamtib.setText(pemberitahuanKamtib['nama_lengkap'] if pemberitahuanKamtib['nama_lengkap'] else '-')
            self.__childDialog.label_kamtib.adjustSize()

            self.__childDialog.exec_()


    def closeEvent(self, event):
        if self.switchClose:
            self.switchClose = False
        else:
            close = QtWidgets.QMessageBox.question(self, 'Konfirmasi', 'Yakin akan keluar? ', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if close == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
