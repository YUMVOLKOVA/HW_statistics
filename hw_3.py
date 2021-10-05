import pandas as pd
from argparse import ArgumentParser

def read_file(input):
    x = []
    y = []

    with open(input) as f:
        for line in f:
            x.append(float(line.split()[0]))
            y.append(float(line.split()[1]))
    dataset = pd.DataFrame({'x': x, 'y': y})

    return dataset

def write_output(output, diff, std_err, conjugacy):
    with open(output,'w') as f:
        f.write(f'{diff} {std_err} {conjugacy}\n')


def monotonic_conjugacy(input, output):
    '''
    Метод проверки монотонной сопряжённости
    Принимает на вход название файла .txt, из которого берутся данные (строки из двух целых чисел, разделённых пробелом),
    а также название файла .txt, куда записывается ответ.
    Выходные данные имеют вид строки из трёх чисел, разделенных пробелом.
    Строка содержит:
        -значение разности (R1-R2), округлённое до целого числа,
        -стандартную ошибку, округлённую для целого числа,
        -меру сопряжённости, округлённую до двух знаков после точки.
    '''

    data = read_file(input)
    data = data.sort_values(by='x')

    N = len(data)
    p = round(N / 3)

    if N < 9:
        print('N должно быть равно по меньшей мере 9')
        return

    data['rank'] = data['y'].rank(method='average', ascending=False)

    R_1 = sum(data['rank'][:p])
    R_2 = sum(data['rank'][-p:])
    diff = round(R_1 - R_2)
    std_err = round((N + 0.5) * ((p / 6) ** 0.5))
    conjugacy = round(diff / (p * (N - p)), 2)

    write_output(output, diff, std_err, conjugacy)


if __name__ == "__main__":
    __arg_parser = ArgumentParser(description=monotonic_conjugacy.__doc__)
    __arg_parser.add_argument("--input", type=str, default="in.txt", help="Путь к входным данным")
    __arg_parser.add_argument("--output", type=str, default="out.txt", help="Путь для файла с ответом")
    __args = __arg_parser.parse_args()
    monotonic_conjugacy(__args.input, __args.output)