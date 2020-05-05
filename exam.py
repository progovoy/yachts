import random
import pickle
import os
import tempfile

import tkinter as tk


def init_game(exam_name):
    encoding = 'utf-8'

    with open(f'a_{exam_name}.txt', 'r', encoding=encoding) as f:
        ans = f.read()

    answers = {}
    n = 0
    if exam_name == 'mec':
        sums = ((1, 46, 91, 136),)
    elif exam_name == 'equ':
        sums = ((1, 31, 61, 91, 121, 151, 181),)
    elif exam_name == 'yam':
        sums = ((1, 48, 95, 142, 189, 236, 283),
                (330, 338, 346, 354, 362)
                )
    else:
        raise RuntimeError(f'Unsupported exam name: {exam_name}')

    for tsum in sums:
        num = [0] * len(tsum)
        index = 0
        for a in ans.split('\n'):
            if a == '':
                break

            for b in a.split()[1::2]:
                if b == 'א':
                    b = 'a'
                elif b == 'ב':
                    b = 'b'
                elif b == 'ג':
                    b = 'c'
                elif b == 'ד':
                    b = 'd'

                answers.update({num[index] + tsum[index]: b})
                num[index] += 1
                index = (index + 1) % len(tsum)

    with open(f'q_{exam_name}.txt', 'r', encoding=encoding) as f:
        q = f.read()

    exam = {}
    cur_q = None
    for a in q.split('\n'):
        split = a.split()
        if split[0][0].isdigit() > 0:
            l = [int(s) for s in split if s.isdigit()]
            split[1] = split[1].replace('.', '')

            exam[l[0]] = {
                'q': ' '.join(split[1:]),
                'opts': {},
                'ans': answers[l[0]]
            }

            cur_q = l[0]
        else:
            op = split[0][0]
            if op == 'א':
                op = 'a'
            elif op == 'ב':
                op = 'b'
            elif op == 'ג':
                op = 'c'
            elif op == 'ד':
                op = 'd'
            else:
                raise RuntimeError('Wrong questions file format')

            exam[cur_q]['opts'][op] = ' '.join(split[1:])

    game = {}
    for key in exam.keys():
        game[key] = {'sucess_count': 0}

    return dict(exam_name=exam_name, exam=exam, game=game, answers=answers)


root = tk.Tk()
root.geometry('750x500')
root.pack_propagate(0)


class Game:
    DIFFICULTY = 1

    def __init__(self, exam_name, exam, game, answers):
        self.exam_name = exam_name
        self.game = game
        self.exam = exam
        self.answers = answers
        self.correct = 0
        self.correct_live = 0
        for k, v in game.items():
            self.correct_live += v['sucess_count']

        frame = tk.Frame(root, background="bisque")
        frame.pack(anchor=tk.N)

        self.question = tk.StringVar()
        self.label = tk.Label(frame,
                              font=('Tahoma', 20),
                              wraplength=root.winfo_width(),
                              textvariable=self.question)
        self.label.pack(anchor=tk.N)

        self.opts_text = {}
        self.opts = {}
        self.ans_v = tk.StringVar()
        for i in ['a', 'b', 'c', 'd']:
            self.opts_text[i] = tk.StringVar()
            self.opts[i] = tk.Radiobutton(frame,
                                     textvariable=self.opts_text[i],
                                     variable=self.ans_v,
                                     value=i,
                                     indicator=0,
                                     font=('Tahoma', 16),
                                     justify='right',
                                     wraplength=root.winfo_width(),
                                     command=self.check_answer)
            self.opts[i].pack(anchor=tk.E)
        tk.Button(frame,
                  text='Next',
                  command=self.update,
                  background='MOCCASIN').pack(anchor=tk.S)

        tk.Button(frame,
                  text='Save',
                  command=self.save,
                  background='MOCCASIN').pack(anchor=tk.S)

        self.stats_v = tk.StringVar()
        tk.Label(frame,
                 textvariable=self.stats_v).pack(anchor=tk.NW)

        self.curr_question = None
        self.update()

    @classmethod
    def load(cls, exam_name, clear):
        if clear or not os.path.exists(f'{tempfile.gettempdir()}/save_answers_{exam_name}.pickle'):
            return cls(**init_game(exam_name=exam_name))
        else:
            with open(f'{tempfile.gettempdir()}/save_exam_{exam_name}.pickle', 'rb') as f:
                exam = pickle.load(f)
            with open(f'{tempfile.gettempdir()}/save_game_{exam_name}.pickle', 'rb') as f:
                game = pickle.load(f)
            with open(f'{tempfile.gettempdir()}/save_answers_{exam_name}.pickle', 'rb') as f:
                answers = pickle.load(f)
            return cls(exam_name=exam_name, exam=exam, game=game, answers=answers)

    def save(self):
        with open(f'{tempfile.gettempdir()}/save_exam_{self.exam_name}.pickle', 'wb') as f:
            pickle.dump(self.exam, f)
        with open(f'{tempfile.gettempdir()}/save_game_{self.exam_name}.pickle', 'wb') as f:
            pickle.dump(self.game, f)
        with open(f'{tempfile.gettempdir()}/save_answers_{self.exam_name}.pickle', 'wb') as f:
            pickle.dump(self.answers, f)

    def update(self):
        self.curr_question = random.choice(list(self.exam.keys()))
        val = self.exam[self.curr_question]
        self.question.set(val['q'])
        for i, opt in val['opts'].items():
            self.opts_text[i].set(opt)
            self.opts[i].configure(background='light blue', state='normal')
        self.stats_v.set(f'Correct {self.correct}/{len(self.exam)}\n'
                         f'Q success count {self.game[self.curr_question]["sucess_count"]}\n'
                         f'correct_live {self.correct_live}')

    def check_answer(self):
        ans = self.ans_v.get()
        correct = self.answers[self.curr_question]
        if ans == correct:
            self.correct_live += 1
            self.game[self.curr_question]['sucess_count'] += 1
            if self.game[self.curr_question]['sucess_count'] == self.DIFFICULTY:
                self.game.pop(self.curr_question)
                self.exam.pop(self.curr_question)
                self.answers.pop(self.curr_question)
                self.correct += 1
        else:
            self.correct_live -= self.game[self.curr_question]['sucess_count']
            self.game[self.curr_question]['sucess_count'] = 0

        for opt in self.opts.values():
            opt.configure(state='disabled')

        self.opts[ans].deselect()
        self.opts[ans].configure(background='LIGHTCORAL')
        self.opts[correct].configure(background='LIGHTGREEN')

bottomframe = tk.Frame(root)
bottomframe.pack(side=tk.BOTTOM)

exam_name='equ'
tk.Button(bottomframe,
          text='Load',
          command=lambda: Game.load(exam_name=exam_name, clear=False),
          background='MOCCASIN').pack(anchor=tk.S)


tk.Button(bottomframe,
          text='New Game',
          command=lambda: Game.load(exam_name=exam_name, clear=True),
          background='MOCCASIN').pack(anchor=tk.S)

root.mainloop()