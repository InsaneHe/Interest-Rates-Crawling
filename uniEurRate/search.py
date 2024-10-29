from PyQt5.QtWidgets import QDialog, QLabel, QTableWidgetItem, QVBoxLayout, QTableWidget, QPushButton, QLineEdit,  QSizePolicy
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QIcon

ALL_SEARCH_RATE_TYPES = ("EURibor", "SONIA", "EURibor1", "EURibor2", "EURibor3", "EURiborZ")
from typing import Tuple
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
import re
_context = 't'
from datetime import date, timedelta
from datetime import datetime
from sonia import sonia
from typing import List
class SearchDialog(QDialog):

    def DisplayAfterCall(self):

        #self.Display()
        pass

    def before_close(self):


        #
        #pass TODO: check input date
        #

        d = date.today()
        try:
            #pass TODO: 时差
            while d.weekday() == 5 or d.weekday() == 6 or d.weekday() == 7: d = d - timedelta(days = 1)
        except BaseException as o:
            pass

        today_yyymmdd_str = d.strftime('%Y%m%d')
        view_dialog_shown_sonia = SoniaValueDialog.show_changed_sonia_rates(1, "", today_yyymmdd_str.rstrip().lstrip())
        today_yyymmdd_str = d.strftime('%Y%m%d')
        view_dialog_shown_euribor = InterActAppearOnceValueDialog.show_changed_euribor_rates(0, "",
             today_yyymmdd_str.rstrip().lstrip())


        TEXT_Type = ""
        try:
            TEXT_Type = self.line_euribor_date_edit.displayText().lstrip().rstrip()
            if (TEXT_Type.lower() == "sonia"):
                view_dialog_shown_sonia.setFocus()
                view_dialog_shown_sonia.exec_()

            elif (TEXT_Type.lower() == "euribor"):
                view_dialog_shown_euribor.setFocus()
                view_dialog_shown_euribor.exec_()
            else:
                self.quit()
        except BaseException as tb:
            print(tb)

        self.minimumWidth()
        #self.setMouseTracking()
        self.maximumHeight()
        #self.Display()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Starting Search")
        self.setWindowIcon(QIcon('iconSearch.png'))
        self.line_euribor_date_edit = None
        self.setGeometry(200, 200, 400, 200)  # Set dialog position and size
        self.setStyleSheet("background-color: #CBCBCB; font-weight: bold;")  # Set background color of dialog

        # Dialog layout
        dialog_layout = QVBoxLayout(self)

        # Title label
        title_label = QLabel(r'Input ("Euribor") or ("Sonia")) to start !!', self)
        title_label.setStyleSheet("color: green; font-size: 20px; padding: 10px;border: 1px solid; border-color:black; font-weight: bold;")
        dialog_layout.addWidget(title_label)

        # Input
        self.line_euribor_date_edit = QLineEdit("", self)
        self.line_euribor_date_edit.setFocus()
        dialog_layout.addWidget(self.line_euribor_date_edit)

        # Version label
        version_label = QLabel("Rates Search Application Version 1.0", self)
        version_label.setStyleSheet("color: yellow; font-size: 18px; padding: 10px;border: 1px solid; border-color:black; font-weight: bold;")
        dialog_layout.addWidget(version_label)

        # Created by label
        created_by_label = QLabel("Demo App Created by: Undergrad Stu Insane.He", self)
        created_by_label.setStyleSheet("color: black; font-size: 18px; padding: 10px;border: 1px solid; border-color:black; font-weight: bold;")
        dialog_layout.addWidget(created_by_label)

        # Search button

        self.search_button = QPushButton("Start Searching >> ", self)
        self.search_button.setStyleSheet("QPushButton {" "background-color: #7289da; ""color: #fff; ""font-weight: bold; ""font-size: 18px; ""}""QPushButton:hover {" "background-color: #4e6eff; ""}")

        self.search_button.clicked.connect(self.before_close)
        dialog_layout.addWidget(self.search_button)


class SoniaValueDialog(QDialog):

    @classmethod
    def show_changed_sonia_rates(self, type_index: int = 1, search_regex="", search_date: str = "18900101"):
        returnDlgSonia = SoniaValueDialog(type_index, search_date)
        return returnDlgSonia
        pass

    def __init__(self, search_type_idx, search_date):

        self.search_type_idx = search_type_idx
        super().__init__()
        self.search_type_colums = ALL_SEARCH_RATE_TYPES

        self.setWindowTitle("View RATE(Sonia)")
        self.setWindowIcon(QIcon('icon_s_sonia.png'))
        self.search_date = search_date
        self.line_euribor_date_edit = None
        self.setGeometry(780, 300, 900, 500)  # Set dialog position and size

        # Table Layout
        item_tbl = QTableWidgetWithModel(self)
        item_tbl.setColumnCount(6)
        item_tbl.setRowCount(2)

        SONIA_WEBSITE_data = [
            ['item/dat', '', '', '', '', ''],
            ['...', '', '', '', '', ''],
        ]
        # Item label
        try:
            yyyy = int(self.search_date[0:4])
            mm = int(self.search_date[4:6])
            dd = int(self.search_date[6:8])
            input_date = datetime(yyyy, mm, dd)
            item_label = QLabel("Item To show Rate(%s) from date-[ %s ] to date-[ %s ] " % (
                self.search_type_colums[self.search_type_idx], '.............', self.search_date))
        except BaseException as b:
            item_label = QLabel("Item To show Rate(%s) from date-[ %s ] to date-[ %s ] " % (
                self.search_type_colums[self.search_type_idx], '-00000000', '-' + str(int('99999994') + 5)))
        item_label.setStyleSheet(
            "color: black; font-size: 18px; padding: 10px;border: 1px solid; border-color:black; font-weight: bold;")

        dialog_layout = QVBoxLayout(self)
        dialog_layout.addWidget(item_tbl)
        dialog_layout.addWidget(item_label)

        #

        try:
            model = TableModel(SONIA_WEBSITE_data)
            item_tbl.SetModelWithModel(model, 6, 2)
        except BaseException as tblExcep:
            print(tblExcep)

        # 爬数据网页

        try:
            retDates = sonia()[1]
            retValues = sonia()[2]
            SONIA_WEBSITE_data = [
                ['item/dat', retDates[0], retDates[1], retDates[2], retDates[3], retDates[4]],
                ['....', retValues[0 + 0 * 5], retValues[1 + 0 * 5], retValues[2 + 0 * 5],
                 retValues[3 + 0 * 5], retValues[4 + 0 * 5]],
            ]
            model = TableModel(SONIA_WEBSITE_data)

            item_tbl.SetModelWithModel(model, 2, 6)
        except BaseException as tblExcep:
            print(tblExcep)

        # Content label
        content_label = QLabel(
            "Rates Search Might Be Inconsistent",
            self)
        content_label.setStyleSheet(
            "color: pink; font-size: 14px; padding: 10px;border: 1px solid; border-color:black; font-weight: bold;")
        dialog_layout.addWidget(content_label)

        # Close button
        close_button = QPushButton("Close", self)
        close_button.setStyleSheet(
            "QPushButton {" "background-color: #5289da; ""color: #ccf; ""font-weight: bold; ""font-size: 18px; ""}""QPushButton:hover {" "background-color: #4e6eff; ""}")
        close_button.clicked.connect(self.close)
        dialog_layout.addWidget(close_button)




class InterActAppearOnceValueDialog(QDialog):

    @classmethod
    def show_changed_euribor_rates(self, type_index:int = 0, search_regex = "", search_date: str = "18900101"):

        returnDlgEuribor = InterActAppearOnceValueDialog(type_index, search_date)
        return returnDlgEuribor
        pass

    def __init__(self, search_type_idx, search_date):

        self.search_type_idx = search_type_idx
        super().__init__()
        self.search_type_colums = ALL_SEARCH_RATE_TYPES

        self.setWindowTitle("View RATE(Euribor)")
        self.setWindowIcon(QIcon('icon_search_idx.png'))
        self.search_date = search_date
        self.line_euribor_date_edit = None
        self.setGeometry(780, 600, 900, 500)  # Set dialog position and size


        #Table Layout
        item_tbl = QTableWidgetWithModel(self)
        item_tbl.setColumnCount(6)
        item_tbl.setRowCount(6)

        WEBSITE_data = [
            ['item/dat','','','','',''],
            ['1W', '', '', '', '', ''],
            ['1M', '', '', '', '', ''],
            ['3M', '', '', '', '', ''],
            ['6M', '', '', '', '', ''],
            ['1Y', '', '', '', '', ''],
        ]

        try:
            model = TableModel(WEBSITE_data)
            item_tbl.SetModelWithModel(model, 6, 6)
        except BaseException as tblExcep:
            print(tblExcep)

        self.setStyleSheet("background-color: #CBCBCB; font-weight: bold;")  # Set background color of dialog
        # Dialog layout
        dialog_layout = QVBoxLayout(self)
        dialog_layout.addWidget(item_tbl)

        # Item label
        try:
            yyyy = int(self.search_date[0:4])
            mm = int(self.search_date[4:6])
            dd = int(self.search_date[6:8])
            input_date = datetime(yyyy, mm, dd)
            date_delta_ed = date.today() - timedelta(days=6)  #pass TODO: days=5 ??
            #date_delta_ed = date.today() + datetime.timedelta(days=-5)
            prev_date_string = date_delta_ed.strftime("%Y%m%d")
            item_label = QLabel("Item To show Rate(%s) from date-[ %s ] to date-[ %s ] " % (self.search_type_colums[self.search_type_idx], prev_date_string, self.search_date))
        except BaseException as b:
            item_label = QLabel("Item To show Rate(%s) from date-[ %s ] to date-[ %s ] " % (self.search_type_colums[self.search_type_idx], '-00000000', '-' + str(int('99999994')+5)))
        item_label.setStyleSheet(
            "color: black; font-size: 18px; padding: 10px;border: 1px solid; border-color:black; font-weight: bold;")
        dialog_layout.addWidget(item_label)

        #爬数据网页

        try:

            retResult = InterActAppearOnceValueDialog.get_data_euribor_modified(self.search_date)
            retDates = retResult[2]
            retItemCurValues = [t.lstrip('>') for t in retResult[1]]
            #
            WEBSITE_data = [
                ['item/dat', retDates[0], retDates[1], retDates[2], retDates[3], retDates[4]],
                ['1W', retItemCurValues[0 + 0 * 5], retItemCurValues[1 + 0 * 5], retItemCurValues[2 + 0 * 5],
                 retItemCurValues[3 + 0 * 5], retItemCurValues[4 + 0 * 5]],
                ['1M', retItemCurValues[0 + 1 * 5], retItemCurValues[1 + 1 * 5], retItemCurValues[2 + 1 * 5],
                 retItemCurValues[3 + 1 * 5], retItemCurValues[4 + 1 * 5]],
                ['3M', retItemCurValues[0 + 2 * 5], retItemCurValues[1 + 2 * 5], retItemCurValues[2 + 2 * 5],
                 retItemCurValues[3 + 2 * 5], retItemCurValues[4 + 2 * 5]],
                ['6M', retItemCurValues[0 + 3 * 5], retItemCurValues[1 + 3 * 5], retItemCurValues[2 + 3 * 5],
                 retItemCurValues[3 + 3 * 5], retItemCurValues[4 + 3 * 5]],
                ['1Y', retItemCurValues[0 + 4 * 5], retItemCurValues[1 + 4 * 5], retItemCurValues[2 + 4 * 5],
                 retItemCurValues[3 + 4 * 5], retItemCurValues[4 + 4 * 5]],
            ]

            model = TableModel(WEBSITE_data)
            ###item_tbl.SetWithModel(model)
            ##item_tbl.SetModelWithModel(model, None, 6, 6)
            item_tbl.SetModelWithModel(model, 6, 6)
        except BaseException as tblExcep:
            print(tblExcep)

        # Content label
        content_label = QLabel("Rates Search Might Be Inconsistent Or Inaccurate due to failures of source data website of Erste Group", self)
        content_label.setStyleSheet(
            "color: yellow; font-size: 14px; padding: 10px;border: 1px solid; border-color:black; font-weight: bold;")
        dialog_layout.addWidget(content_label)

        # Close button
        close_button = QPushButton("Close", self)
        close_button.setStyleSheet(
            "QPushButton {" "background-color: #7289da; ""color: #ccf; ""font-weight: bold; ""font-size: 18px; ""}""QPushButton:hover {" "background-color: #4e6eff; ""}")
        close_button.clicked.connect(self.close)
        dialog_layout.addWidget(close_button)


    @staticmethod
    def get_data_euribor_modified(date: str) -> Tuple[List[str], List[str], List[str]]:
        emtpy_links = (
        ###r'https://www.sparkasse.at/investments-en/markets/market-overview/currencies/currencies#EU0009652627-F991341',
        r'https://www.euribor-rates.eu/en/current-euribor-rates',
        r'',
        r'',
        r'',
        r'',)
        ###empty_cols = ['JPY', 'GBP', 'CHF', 'USD', 'EUR']

        WEB_TIMEOUT = 15
        try:

            self_titlecounts = [4, 3, 2, 1, 0]  # 对应五天各自发布的数据量
            import datetime
            import requests
            from urllib import error
            import urllib.request
            from urllib import parse
            global _context
            _context = r"ssl.SSLContext object NONEADDR"
            import ssl
            _context = ssl._create_unverified_context()

            connection_res_s = ""
            i_cnt = -1
            try:
                surl = emtpy_links[0]  # JPY
                # local_var_cnt = 0
                connection_req_s = urllib.request.Request(surl)
                connection_res_s = urllib.request.urlopen(connection_req_s, context=_context, timeout=WEB_TIMEOUT)
                # break
            except error.HTTPError as ehttp:
                print(ehttp)
                if i_cnt > 11:
                    # break
                    pass
                else:
                    # continue
                    pass
            except error.URLError as eurlopen:
                print(eurlopen)
                if i_cnt > 11:
                    # break
                    pass
                else:
                    # continue
                    pass
            try:
                info = connection_res_s.read().decode("utf-8")
                with open('info.html', mode='w', encoding='utf8') as t:
                    t.write(info)

                url_idx = 0
                the_url_to_search = emtpy_links[url_idx]


                Items = re.findall(r'<a href="/en/current-euribor-rates/[0-9]/(.*?)</a>', info)
                CurrentValues = re.findall(r'<td class="text-right"(.*?)</td>', info)
                NeutralDates = re.findall(r'<th class="text-right">(.*?)</th>', info)


                print("Retrieving information from website:\n\t", the_url_to_search)
                print('-----------------------------------------------------------\n\n')
                return (Items, CurrentValues, NeutralDates)

            except requests.exceptions.ReadTimeOut:
                print("INFORMATION TYPE ERROR! -- CHECK IF WEBSITE OR IP ALL OKAY!")
            except BaseException as info_bse:
                print(info_bse)

            ## 开始为表格赋值数据并返回！

        except BaseException as a:
            print(a)

class TableModel(QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def dataRowColumn(self, indexRow, indexColumn, role = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[indexRow][indexColumn]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class QTableWidgetWithModel(QTableWidget):

    def __init__(self, data):
        super(QTableWidgetWithModel, self).__init__()
        self._data = data

    def SetWithModel(self, tableModel: TableModel):
        self.setModel(tableModel)

    def SetModelWithModel(self, tableModel: TableModel, totalRowAssign:int, totalColumnAssign:int):
        rowsCount = tableModel.rowCount(None)
        colsCount = tableModel.columnCount(None)

        for iRow in range(0, rowsCount, 1):
            for iColumn in range (0, colsCount, 1):
                if (iRow + 1 <= totalRowAssign and iColumn + 1 <= totalColumnAssign):
                    tempCell = tableModel.dataRowColumn(iRow, iColumn)
                    widgetItem = QTableWidgetItem(tempCell)
                    self.setItem(iRow, iColumn, widgetItem)
        pass