"""
    Created January 2021
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from __future__ import absolute_import, division, print_function
import inspect
import sys,os,platform,time,traceback
import pickle, gzip
from collections import OrderedDict
from tablexplore.qt import *
import pandas as pd
from tablexplore import util, data, core, dialogs
from tablexplore.plugin import Plugin
import difflib, re

def find_word(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def find_match(x,r):
    name = x['name'].lower()
    if r.surname.lower() in name and find_word(r.firstname)(name): #r.firstname.lower() in name:
        return True
    return False

def run_search(db, targets, keep=1):
    """Search rip.ie table for known persons"""

    print ('searching %s rows' %len(db))
    results = []
    for i,r in targets.iterrows():
        print (r.case_id,r.surname)
        A = r.address
        f = db.apply(lambda x: find_match(x,r),1)
        res = db[f].copy()
        if len(res) == 0:
            print ('no names match')
            res=pd.DataFrame([(r.case_id,0,'NA')],columns=['case_id','year','id'])

        elif len(res) == 1:
            print ('one unique hit')
            #res = res.iloc[0]
        else:
            #get best match address
            print ('found %s hits' %len(res))
            addresses=list(res.address)
            #res['score']=res.apply(lambda x: fuzz.ratio(A, x.address),1)
            res['score']=res.apply(lambda x: difflib.SequenceMatcher(None, A, x.address).ratio(),1)
            res = res.sort_values('score',ascending=False)
            res = res[:keep]
            #res = res.iloc[0]
        res['case_id'] = r.case_id
        results.append(res)

    results = pd.concat(results).reset_index(drop=True)
    results = targets.merge(results,on='case_id')
    return results

class RIPSearchPlugin(Plugin):
    """search rip data plugin"""

    #uncomment capabilities list to appear in menu
    capabilities = ['gui','docked']
    requires = ['']
    menuentry = 'RIP.ie search'
    name = 'ripsearch'

    def __init__(self, parent=None, table=None):
        """Customise this and/or doFrame for your widgets"""

        if parent==None:
            return
        self.parent = parent
        self.table = table
        self.ID = 'Testing'
        self.createWidgets()
        self.threadpool = QtCore.QThreadPool()
        return

    def createButtons(self, parent):

        bw = QWidget(parent)
        bw.setMaximumWidth(100)
        vbox = QVBoxLayout(bw)
        button = QPushButton("Run")
        button.clicked.connect(self.run)
        vbox.addWidget(button)
        button = QPushButton("Close")
        button.clicked.connect(self.quit)
        vbox.addWidget(button)
        return bw

    def createWidgets(self):
        """Create widgets if GUI plugin"""

        if 'docked' in self.capabilities:
            self.main = QDockWidget()
            self.main.setFeatures(QDockWidget.DockWidgetClosable)
        else:
            self.main = QWidget()
        self.frame = QWidget(self.main)
        self.main.setWidget(self.frame)
        layout =  QHBoxLayout()
        self.frame.setLayout(layout)

        sheets = self.parent.sheets
        left = QWidget()
        l=QVBoxLayout()
        left.setLayout(l)
        self.s1 = s1 = QComboBox()
        s1.addItems(sheets)
        l.addWidget(QLabel('search table:'))
        l.addWidget(s1)
        self.s2 = s2 = QComboBox()
        s2.addItems(sheets)
        l.addWidget(QLabel('RIP.ie data:'))
        l.addWidget(s2)
        l.addWidget(QLabel('Hits to keep:'))
        w=self.keepw=QSpinBox()
        w.setRange(1,20)
        l.addWidget(w)
        layout.addWidget(left)
        bw = self.createButtons(self.frame)
        layout.addWidget(bw)
        return

    def run_threaded_process(self, process, on_complete):
        """Execute a function in the background with a worker"""

        worker = dialogs.Worker(fn=process)
        self.threadpool.start(worker)
        worker.signals.finished.connect(on_complete)
        self.progdlg.progressbar.setRange(0,0)
        return

    def completed(self):
        """Generic process completed"""

        self.progdlg.progressbar.setRange(0,1)
        self.progdlg.close()
        self.parent.addSheet('search result',df=self.result)
        return

    def run(self):
        """Get sheets and run search"""

        sheet1 = self.s1.currentText()
        targets = self.parent.sheets[sheet1].table.model.df
        sheet2 = self.s2.currentText()
        db = self.parent.sheets[sheet2].table.model.df
        keep = self.keepw.value()
        self.progdlg = dlg = dialogs.ProgressWidget(label='Searching...')
        dlg.show()
        def func(progress_callback):
            self.result = run_search(db, targets, keep=keep)
        self.run_threaded_process(func, self.completed)
        return

    def quit(self, evt=None):
        """Override this to handle pane closing"""

        self.main.close()
        del self.table.openplugins[self.name]
        return
