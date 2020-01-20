import random
import pickle


def init_game():
    with open('answers.txt', 'r') as f:
        ans = f.read()

    answers = {}
    sum = [1, 46, 91, 136]
    num = [0, 0, 0, 0]
    index = 0
    for a in ans.split('\n'):
        for b in a.split()[1::2]:
            if b == 'א':
                b = 'a'
            elif b == 'ב':
                b = 'b'
            elif b == 'ג':
                b = 'c'
            elif b == 'ד':
                b = 'd'

            answers.update({num[index] + sum[index]: b})
            num[index] += 1
            index = (index + 1) % 4

    with open('questions.txt', 'r') as f:
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

            exam[cur_q]['opts'][op] = ' '.join(split[1:])

    game = {}
    for key in exam.keys():
        game[key] = {'sucess_count': 0}

        save(exam, game, answers)


def save(exam, game, answers):
    with open('/tmp/save_exam.pickle', 'wb') as f:
        pickle.dump(exam, f)
    with open('/tmp/save_game.pickle', 'wb') as f:
        pickle.dump(game, f)
    with open('/tmp/save_answers.pickle', 'wb') as f:
        pickle.dump(answers, f)


init = input("Start from scratch? y / n")
if init == 'y':
    init = input("REALLY?! yes i do / n")
    if init == 'yes i do':
        init_game()

with open('/tmp/save_exam.pickle', 'rb') as f:
    exam = pickle.load(f)
with open('/tmp/save_game.pickle', 'rb') as f:
    game = pickle.load(f)
with open('/tmp/save_answers.pickle', 'rb') as f:
    answers = pickle.load(f)

num_of_q = len(game.keys())
correct = 0

correct_live = 0
for k,v in game.items():
    correct_live += v['sucess_count']

while game:
    q, val = random.choice(list(exam.items()))

    print('{0} of 2'.format(game[q]['sucess_count']))
    print('{0} - {1}'.format(q, val['q']))
    for k, opt in val['opts'].items():
        print('{0} - {1}'.format(k, opt))

    user_choice = input("")
    while user_choice == 's' or user_choice == 'save':
        if user_choice == 's':
            print(
                'You have finished {0} questions '
                'correctly. Left {1}'.format(correct,
                    num_of_q - correct
                )
            )
            print('{0} answered correctly'.format(correct_live))
        elif user_choice == 'save':
            save(exam, game, answers)

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
        game[q]['sucess_count'] += 1
        if game[q]['sucess_count'] == 2:
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

        correct_live -= game[q]['sucess_count']
        game[q]['sucess_count'] = 0
