import random
import pickle
import os
import json
import csv
import re


def init_game():
    answers = {}
    with open(f'a_{exam_name}.csv', 'r', encoding='utf-8') as f:
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

    with open(f'q_{exam_name}.txt', 'r', encoding='utf-8') as f:
        q = f.read()

    exam = {}
    rtl = "\u200F"
    cur_q = None
    patt = re.compile('^[ .]*([^. ].*)')
    q_patt = re.compile('^([0-9,א-ד]+)[ .]*(.*)')
    for a in q.split('\n'):
        try:
            m = q_patt.match(a)
            op = m.group(1)
            text = m.group(2)
            if op.isnumeric():
                cur_q = int(op)
                exam[cur_q] = {
                    'q': rtl + op + '-' + text,
                    'opts': {},
                    'ans': answers[cur_q]
                }
            else:
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
                exam[cur_q]['opts'][op] = rtl + text
        except Exception as e:
            print(f'{a} {e}')
            raise


    game = {}
    for key in exam.keys():
        game[key] = {'success_count': 0}

    save(exam, game, answers)


def save(exam, game, answers):
    with open(f'/tmp/save_exam_{exam_name}.pickle', 'wb') as f:
        pickle.dump(exam, f)
    with open(f'/tmp/save_game_{exam_name}.pickle', 'wb') as f:
        pickle.dump(game, f)
    with open(f'/tmp/save_answers_{exam_name}.pickle', 'wb') as f:
        pickle.dump(answers, f)

    # Writing a JSON file
    with open(f'/tmp/save_answers_{exam_name}.json', 'w') as f:
        json.dump(answers, f)
    with open(f'/tmp/save_game_{exam_name}.json', 'w') as f:
        json.dump(game, f)
    with open(f'/tmp/save_exam_{exam_name}.json', 'w') as f:
        json.dump(exam, f)

    print('Saved successfully')


def load():
    with open(f'/tmp/save_exam_{exam_name}.pickle', 'rb') as f:
        exam = pickle.load(f)
    with open(f'/tmp/save_game_{exam_name}.pickle', 'rb') as f:
        game = pickle.load(f)
    with open(f'/tmp/save_answers_{exam_name}.pickle', 'rb') as f:
        answers = pickle.load(f)

    return exam, game, answers


def print_status():
    print(
        'You have finished {0} questions '
        'correctly. Left {1}'.format(correct,
                                     num_of_q - correct
                                     )
    )
    print('{0} answered correctly'.format(correct_live))


def print_help():
    print('Commands are:\n'
          '?/help - help\n'
          's - status\n'
          'save - save exam to continue later\n'
          'skip - skip question\n'
          'exit - exit exam\n'
          )


def print_question():
    print('{0} of {1}'.format(game[q]['success_count'], DIFFICULTY))
    print('{0} - {1}'.format(q, val['q']))
    for k, opt in val['opts'].items():
        print('{0} - {1}'.format(k, opt))


uinput = input(
    "Choose exam\n"
    "1 - yamaut\n"
    "2 - mehona\n"
    "3 - mahshirim\n")
while uinput not in ['1', '2', '3']:
    uinput = input(
        "Choose exam\n"
        "1 - yamaut\n"
        "2 - mehona\n"
        "3 - mahshirim\n")

exam_name = None
if uinput == '1':
    exam_name = 'yam'
elif uinput == '2':
    exam_name = 'mec'
elif uinput == '3':
    exam_name = 'equ'

if os.path.isfile(f'/tmp/save_exam_{exam_name}.pickle'):
    uinput = input("Start from scratch? y / n")
    if uinput == 'y':
        uinput = input("Are you sure? Type: 'yes i do' or 'no'")
        if uinput == 'yes i do':
            init_game()
else:
    init_game()

exam, game, answers = load()

num_of_q = len(game.keys())
correct = 0

correct_live = 0
for k,v in game.items():
    correct_live += v['success_count']

for item in exam.items():
    if len(item[1]['opts']) != 4:
        raise RuntimeError('Wrong questions file format')

DIFFICULTY = 2
while game:
    q, val = random.choice(list(exam.items()))

    print_question()

    user_choice = input("")
    while user_choice in ['s', 'save', '?', 'help']:
        if user_choice == 's':
            print_status()
        elif user_choice == 'save':
            save(exam, game, answers)
        elif user_choice in ['?', 'help']:
            print_help()

        print_question()
        user_choice = input("")

    if user_choice == 'exit':
        break

    if user_choice == 'skip':
        continue

    if user_choice == val['ans']:
        print('Correct!')
        for i in range(3):
            print()

        correct_live += 1
        game[q]['success_count'] += 1
        if game[q]['success_count'] == DIFFICULTY:
            game.pop(q)
            exam.pop(q)
            answers.pop(q)
            correct += 1
    else:
        print('Wrong!')
        print(
            'The answer is: {0} - {1}'.format(
                answers[q], val['opts'][answers[q]]
            )
        )

        for i in range(3):
            print()

        correct_live -= game[q]['success_count']
        game[q]['success_count'] = 0


def main():
    pass


if __name__ == "__main__":
    main()
