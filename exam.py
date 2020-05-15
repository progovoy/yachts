import csv
import random
import pickle
import os
import re
import sys
import tempfile

save_dir = tempfile.gettempdir()
save_dir = './saved/'

import tkinter as tk
from PySide2 import QtCore, QtWidgets, QtGui



def init_game(exam_name):
    encoding = 'utf-8'

    answers = {}
    with open(f'a_{exam_name}.csv', 'r', encoding=encoding) as f:
        for i, b in csv.reader(f):
            if b == 'א':
                b = 1
            elif b == 'ב':
                b = 2
            elif b == 'ג':
                b = 3
            elif b == 'ד':
                b = 4
            answers[int(i)] = b

    with open(f'q_{exam_name}.txt', 'r', encoding=encoding) as f:
        q = f.read()

    exam = {}
    rtl = "\u200F"
    cur_q = None
    patt = re.compile('^[ .]*([^. ].*)')
    for a in q.split('\n'):
        split = a.split()
        if split[0][0].isdigit() > 0:
            l = [int(s) for s in split if s.isdigit()]
            split[1] = split[1].replace('.', '')

            exam[l[0]] = {
                'q': rtl + ' '.join(split),
                'opts': {},
                'ans': answers[l[0]]
            }

            cur_q = l[0]
        else:
            op = split[0][0]
            if op == 'א':
                op = 1
            elif op == 'ב':
                op = 2
            elif op == 'ג':
                op = 3
            elif op == 'ד':
                op = 4
            else:
                raise RuntimeError('Wrong questions file format')
            split[0] = split[0][2:]
            op_text = ' '.join(split)
            op_text = patt.match(op_text).group(1)
            exam[cur_q]['opts'][op] = rtl + op_text

    game = {}
    for key in exam.keys():
        game[key] = {'sucess_count': 0}

    return dict(exam_name=exam_name, exam=exam, game=game, answers=answers)


class Game(QtWidgets.QWidget):
    DIFFICULTY = 2

    def __init__(self, exam_name, exam, game, answers, parent=None):
        super().__init__(parent=parent)

        # self.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.exam_name = exam_name
        self.game = game
        self.exam = exam
        self.answers = answers
        self.correct = 0
        self.correct_live = 0
        for k, v in game.items():
            self.correct_live += v['sucess_count']
            if v['sucess_count'] == self.DIFFICULTY:
                self.correct += 1

        self.question = QtWidgets.QLabel()
        self.question.setWordWrap(True)
        # self.question.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.question.setFont(QtGui.QFont('Arial', 14))

        self.opts = QtWidgets.QButtonGroup()
        self.opts_text = {}

        l = QtWidgets.QGridLayout()
        l.setSpacing(2)
        for i in range(1, 5):
            label = QtWidgets.QLabel()
            label.setWordWrap(True)
            label.setFont(QtGui.QFont('Arial', 12))
            # label.setLayoutDirection(QtCore.Qt.RightToLeft)
            # label.setStyleSheet()
            button = QtWidgets.QPushButton()
            button.setFixedSize(QtCore.QSize(30, 30))
            button.setStyleSheet("QPushButton"
                                   "{"
                                   "background-color : lightblue"
                                   "}")
            l.addWidget(label, i, 1)
            l.addWidget(button, i, 0)
            self.opts_text[i] = label
            self.opts.addButton(button, i)
            self.opts.button(i).setText(str(i))
            self.opts.button(i).setShortcut(str(i))
        self.opts.buttonClicked[int].connect(self.check_answer)

        self._next = QtWidgets.QPushButton("Next")
        self._next.clicked.connect(self.update)
        self._next.setShortcut("Return")

        self._stats = QtWidgets.QLabel()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.question)
        self.layout.addLayout(l)
        self.layout.addWidget(self._next)
        self.layout.addWidget(self._stats)
        self.setLayout(self.layout)
        self.curr_question = None
        self.update()

    @classmethod
    def load(cls, exam_name, clear):
        if clear or not os.path.exists(f'{save_dir}/save_answers_{exam_name}.pickle'):
            return cls(**init_game(exam_name=exam_name))
        else:
            with open(f'{save_dir}/save_exam_{exam_name}.pickle', 'rb') as f:
                exam = pickle.load(f)
            with open(f'{save_dir}/save_game_{exam_name}.pickle', 'rb') as f:
                game = pickle.load(f)
            with open(f'{save_dir}/save_answers_{exam_name}.pickle', 'rb') as f:
                answers = pickle.load(f)
            return cls(exam_name=exam_name, exam=exam, game=game, answers=answers)

    def save(self):
        with open(f'{save_dir}/save_exam_{self.exam_name}.pickle', 'wb') as f:
            pickle.dump(self.exam, f)
        with open(f'{save_dir}/save_game_{self.exam_name}.pickle', 'wb') as f:
            pickle.dump(self.game, f)
        with open(f'{save_dir}/save_answers_{self.exam_name}.pickle', 'wb') as f:
            pickle.dump(self.answers, f)

    def update(self):
        keys = [k for k in self.exam.keys() if self.game[k]['sucess_count'] != self.DIFFICULTY]
        self.curr_question = random.choice(keys)
        assert self.curr_question in keys
        val = self.exam[self.curr_question]
        q = val['q']
        q = q.replace('(', '`').replace(')', '(').replace('`', ')')
        self.question.setText(q)
        for i, opt in val['opts'].items():
            opt = opt.replace('(', '`').replace(')', '(').replace('`', ')')
            self.opts_text[i].setText(opt)
            self.opts_text[i].setStyleSheet("QLabel"
                           "{"
                           "background-color : white"
                           "}")
            self.opts.button(i).setEnabled(True)
            self.opts.button(i).setFont(QtGui.QFont('SansSerif', 14))
        self._stats.setText(f'Correct {self.correct}/{len(self.exam)}\n'
                            f'Q success count {self.game[self.curr_question]["sucess_count"]}\n'
                            f'correct_live {self.correct_live}')

    def check_answer(self, ans):
        correct = self.answers[self.curr_question]
        if ans == correct:
            self.correct_live += 1
            self.game[self.curr_question]['sucess_count'] += 1
            if self.game[self.curr_question]['sucess_count'] == self.DIFFICULTY:
                self.correct += 1
        else:
            self.correct_live -= self.game[self.curr_question]['sucess_count']
            self.game[self.curr_question]['sucess_count'] = 0

        for opt in self.opts.buttons():
            opt.setDisabled(True)

        self.opts_text[ans].setStyleSheet("QLabel"
                                   "{"
                                   "background-color : red"
                                   "}")
        self.opts_text[correct].setStyleSheet("QLabel"
                                   "{"
                                   "background-color : lightgreen"
                                   "}")
        self.save()
        if ans == correct:
            QtCore.QTimer.singleShot(250, self.update)


class MainWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.exams = QtWidgets.QButtonGroup()
        exam_names = ['equ', 'yam', 'mec']
        for exam_name in exam_names:
            self.exams.addButton(QtWidgets.QRadioButton(exam_name))
        self.load_game = QtWidgets.QPushButton("Load Game")
        self.load_game.clicked.connect(lambda: self._load(clear=False))
        self.new_game = QtWidgets.QPushButton("New Game")
        self.new_game.clicked.connect(lambda: self._load(clear=True))

        self.layout = QtWidgets.QVBoxLayout()
        self.top_layout = QtWidgets.QVBoxLayout()
        self.bottom_layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.top_layout)
        self.layout.addLayout(self.bottom_layout)
        [self.bottom_layout.addWidget(b) for b in self.exams.buttons()]
        self.bottom_layout.addWidget(self.load_game)
        self.bottom_layout.addWidget(self.new_game)
        self.setLayout(self.layout)

    def _load(self, clear):
        self.top_layout.addWidget(
            Game.load(self.exams.checkedButton().text(), clear=clear))
        self.new_game.hide()
        self.load_game.hide()
        [b.hide() for b in self.exams.buttons()]


if __name__ == '__main__':
    QtCore.Qt.LayoutDirection(QtCore.Qt.RightToLeft)
    app = QtWidgets.QApplication([])
    app.setLayoutDirection(QtCore.Qt.RightToLeft)
    widget = MainWidget()
    widget.resize(1024, 800)
    widget.show()

    sys.exit(app.exec_())