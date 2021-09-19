from PR1_var_11 import Pr1Task
from PR2_var_12 import Pr2Task

TASKS = {
    'PR1': Pr1Task,
    'PR2': Pr2Task,
}


def task_runner():
    task_num = input('Enter task name: ')
    if task_num in TASKS:
        task = TASKS[task_num]()
        task.run()
    else:
        print('There is no such task in a list')


commands = {
    'run': task_runner,
    'list': lambda: print('Available task names: ' + ' '.join(TASKS.keys())),
    'exit': exit,
}

if __name__ == '__main__':
    print('Hi, this is task handler')
    while True:
        command = input('To exit a program enter exit, to get a list of all available tasks enter list, to get tasks'
                        ' menu enter run: ')
        if command in commands.keys():
            commands[command]()
        else:
            print('Sorry, but there is no such command, try again')
