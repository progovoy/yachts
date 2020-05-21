import csv
import random
import pickle
import os
import re
import sys
import tempfile
from PySide2 import QtCore, QtWidgets, QtGui

save_dir = tempfile.gettempdir()
save_dir = './saved/'

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
        game[key] = {'sucess_count': 0, 'fail_count': 0}

    return dict(exam_name=exam_name, exam=exam, game=game, answers=answers)


class Game(QtWidgets.QWidget):
    def __init__(self, exam_name, exam, game, answers, difficulty, continue_failed, parent=None):
        super().__init__(parent=parent)

        # self.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.exam_name = exam_name
        self.game = game
        self.exam = exam
        self.answers = answers
        self._difficulty = difficulty
        self._continue_failed = continue_failed
        self.correct = 0
        self.correct_live = 0
        for k, v in game.items():
            self.correct_live += v['sucess_count']
            if v['sucess_count'] >= self._difficulty:
                self.correct += 1
            v['this_round_success_count'] = 0

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

        self._image_label = QtWidgets.QLabel()
        self._next = QtWidgets.QPushButton("Next")
        self._next.clicked.connect(self.update)
        self._next.setShortcut("n")
        self._reset_fail_count = QtWidgets.QPushButton("Reset Fail Count")
        self._reset_fail_count.clicked.connect(self.reset_fail_count)
        self._reset_fail_count.setShortcut("r")

        self._stats = QtWidgets.QLabel()
        self._stats.setFont(QtGui.QFont('Arial', 12))

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.question)
        self.layout.addLayout(l)
        self.layout.addWidget(self._next)
        self.layout.addWidget(self._reset_fail_count)
        l = QtWidgets.QHBoxLayout()
        l.addWidget(self._image_label)
        w = QtWidgets.QLabel()
        w.setPixmap(QtGui.QPixmap(f'./images/{self.exam_name}/always.jpg').scaledToHeight(400))
        l.addWidget(w)
        l.addWidget(self._stats)
        self.layout.addLayout(l)
        # self.layout.addWidget(self._stats)
        self.setLayout(self.layout)
        self.curr_question = None
        self.update()

    @classmethod
    def load(cls, exam_name, clear, difficulty, continue_failed):
        if clear or not os.path.exists(f'{save_dir}/save_answers_{exam_name}.pickle'):
            return cls(**init_game(exam_name=exam_name),
                       difficulty=difficulty,
                       continue_failed=continue_failed)
        else:
            with open(f'{save_dir}/save_exam_{exam_name}.pickle', 'rb') as f:
                exam = pickle.load(f)
            with open(f'{save_dir}/save_game_{exam_name}.pickle', 'rb') as f:
                game = pickle.load(f)
            with open(f'{save_dir}/save_answers_{exam_name}.pickle', 'rb') as f:
                answers = pickle.load(f)
            return cls(exam_name=exam_name, exam=exam, game=game, answers=answers,
                       difficulty=difficulty,
                       continue_failed=continue_failed)

    def save(self):
        with open(f'{save_dir}/save_exam_{self.exam_name}.pickle', 'wb') as f:
            pickle.dump(self.exam, f)
        with open(f'{save_dir}/save_game_{self.exam_name}.pickle', 'wb') as f:
            pickle.dump(self.game, f)
        with open(f'{save_dir}/save_answers_{self.exam_name}.pickle', 'wb') as f:
            pickle.dump(self.answers, f)

    def set_stats(self):
        self._stats.setText(f'Correct {self.correct}/{len(self.exam)}\n'
                            f'Q success count {self.game[self.curr_question]["sucess_count"]}\n'
                            f'Q fail count {self.game[self.curr_question]["fail_count"]}\n'
                            f'Q remaining {len(self.questions_pool)}\n'
                            f'correct_live {self.correct_live}')

    def reset_fail_count(self):
        self.game[self.curr_question]['fail_count'] = 0
        self.set_stats()

    def update(self):
        def done(q_stats):
            if q_stats['sucess_count'] < self._difficulty:
                return False
            elif q_stats['fail_count'] > 0 and self._continue_failed and q_stats['this_round_success_count'] < self._difficulty:
                return False
            return True

        self.questions_pool = [k for k in self.exam.keys() if not done(self.game[k])]
        if len(self.questions_pool) == 0:
            image_file = f'./images/done.jpg'
            self._image_label.setPixmap(QtGui.QPixmap(image_file).scaledToHeight(800))
            self.question.hide()
            for i in range(1,5):
                self.opts_text[i].hide()
                self.opts.button(i).hide()
            self._next.hide()
            self._reset_fail_count.hide()
            return

        self.curr_question = random.choice(self.questions_pool)
        assert self.curr_question in self.questions_pool
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
        image_file = f'./images/{self.exam_name}/{self.curr_question}.jpg'
        if os.path.exists(image_file):
            self._image_label.setPixmap(QtGui.QPixmap(image_file).scaledToHeight(400))
        else:
            self._image_label.clear()
        self.set_stats()

    def check_answer(self, ans):
        correct = self.answers[self.curr_question]
        if ans == correct:
            self.correct_live += 1
            self.game[self.curr_question]['this_round_success_count'] += 1
            if self.game[self.curr_question]['sucess_count'] < self._difficulty:
                self.game[self.curr_question]['sucess_count'] += 1
                self.correct += int(self._difficulty == self.game[self.curr_question]['sucess_count'])
        else:
            self.correct -= int(self._difficulty == self.game[self.curr_question]['sucess_count'])
            self.correct_live -= self.game[self.curr_question]['sucess_count']
            self.game[self.curr_question]['sucess_count'] = 0
            self.game[self.curr_question]['fail_count'] += 1
            self.game[self.curr_question]['this_round_success_count'] = 0

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
        self.set_stats()
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

        self.difficulty = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.difficulty.setMaximumWidth(100)
        self.difficulty.setMinimum(1)
        self.difficulty.setMaximum(5)
        self.difficulty_label = QtWidgets.QLabel()
        self.difficulty.valueChanged[int].connect(lambda x: self.difficulty_label.setText(f'Difficulty is {x}'))
        self.difficulty.setValue(2)

        self.failed_checkbox = QtWidgets.QCheckBox()
        self.failed_checkbox.setText("continue iterating through any failed questions")

        self.load_game = QtWidgets.QPushButton("Load Game")
        self.load_game.clicked.connect(lambda: self._load(clear=False,
                                                          difficulty=self.difficulty.value(),
                                                          continue_failed=self.failed_checkbox.isChecked()))
        self.new_game = QtWidgets.QPushButton("New Game")
        self.new_game.clicked.connect(lambda: self._load(clear=True,
                                                          difficulty=self.difficulty.value(),
                                                          continue_failed=self.failed_checkbox.isChecked()))

        self.layout = QtWidgets.QVBoxLayout()
        self.top_layout = QtWidgets.QVBoxLayout()
        self.bottom_layout = QtWidgets.QVBoxLayout()
        self.bottom_layout.setAlignment(QtCore.Qt.AlignBottom)
        self.layout.addLayout(self.top_layout)
        self.layout.addLayout(self.bottom_layout)
        [self.bottom_layout.addWidget(b) for b in self.exams.buttons()]
        diff_layout = QtWidgets.QHBoxLayout()
        self.difficulty_label.setAlignment(QtCore.Qt.AlignRight)
        diff_layout.addWidget(self.difficulty)
        diff_layout.addWidget(self.difficulty_label)
        self.bottom_layout.addWidget(self.failed_checkbox)
        self.bottom_layout.addLayout(diff_layout)
        self.bottom_layout.addWidget(self.load_game)
        self.bottom_layout.addWidget(self.new_game)
        self.setLayout(self.layout)

    def _load(self, clear, difficulty, continue_failed):
        if self.exams.checkedButton() is None:
            return
        self.top_layout.addWidget(
            Game.load(self.exams.checkedButton().text(),
                      clear=clear,
                      difficulty=difficulty,
                      continue_failed=continue_failed))
        self.new_game.hide()
        self.load_game.hide()
        self.difficulty.hide()
        self.difficulty_label.hide()
        self.failed_checkbox.hide()
        [b.hide() for b in self.exams.buttons()]


if __name__ == '__main__':
    os.makedirs(save_dir, exist_ok=True)

    QtCore.Qt.LayoutDirection(QtCore.Qt.RightToLeft)
    app = QtWidgets.QApplication([])
    app.setLayoutDirection(QtCore.Qt.RightToLeft)
    widget = MainWidget()
    # widget.resize(1024, 800)
    widget.showFullScreen()
    widget.show()

    sys.exit(app.exec_())