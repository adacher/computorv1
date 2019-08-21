import sys
import re


def custom_sqrt(delta):
    half = delta / 2
    limit = half + 1
    while (half != limit):
        x = delta / half
        limit = half
        half = (half + x) / 2
    return half


def delta_is_below_zero(delta, coefficient):
    print("Discriminant is strictly negative, the two complexe solutions are:\n")
    a = 0
    b = 0
    ndelta = (-1) * delta
    for elem in coefficient:
        if elem[0] == 1:
            b = elem[1]
        if elem[0] == 2:
            a = 2 * elem[1]
    if coefficient[1] != 0:
        print("(-" + str(b) + " - iV(" + str(ndelta) + ")) / " + str(a) + "\n")
        print("(-" + str(b) + " + iV(" + str(ndelta) + ")) / " + str(a))
    else:
        print("(-iV(" + str(ndelta) + ")) / (" + str(a) + ")\n")
        print("(iV(" + str(ndelta) + ")) / (" + str(a) + ")")


def delta_is_above_zero(delta, coefficient):
    a = 0
    b = 0
    x_one = 0
    x_two = 0
    square = 0 if delta == 0 else custom_sqrt(delta)
    print("Discriminant is strictly positive, the two solutions are:")
    for elem in coefficient:
        if elem[0] == 1:
            b = (-1) * elem[1]
        if elem[0] == 2:
            a = 2 * elem[1]
    if a == 0:
        print("0")
        print("0")
    else:
        x_one = (b + square) / a
        x_two = (b - square) / a
        if len(str(x_one)) > 8:
            print("%2f" % x_one)
        else:
            print(str(x_one))
        if len(str(x_two)) > 8:
            print("%2f" % x_two)
        else:
            print(str(x_two))


def delta_is_zero(delta, coefficient):
    x = 0
    a = 0
    b = 0
    for elem in coefficient:
        if elem[0] == 1:
            b = (-1) * elem[1]
        if elem[0] == 2:
            a = 2 * elem[1]
    if a == 0:
        print("The solution is")
        print("0")
    else:
        x = b / a
        print("The solution is")
        if str(x) == "-0.0" and len(str(x)) == 4:
            print("0")
        elif str(x) == "0.0" and len(str(x)) == 3:
            print("0")
        elif len(str(x)) > 8:
            print("%2f" % x)
        else:
            print(str(x))


def degree_is_two(degree, coefficient):
    a = 0
    b = 0
    c = 0
    delta = 0
    for elem in coefficient:
        if elem[0] == 0:
            c = elem[1]
        if elem[0] == 1:
            b = elem[1]
        if elem[0] == 2:
            a = elem[1]
    delta = b * b - 4 * a * c
    if delta == 0:
        delta_is_zero(delta, coefficient)
    elif delta > 0:
        delta_is_above_zero(delta, coefficient)
    else:
        delta_is_below_zero(delta, coefficient)


def degree_is_below_two(degree, coefficient):
    x = 0
    b = 0
    c = 0
    for elem in coefficient:
        if elem[0] == 0:
            c = elem[1]
        if elem[0] == 1:
            b = elem[1]
    deno = (-1) * b
    if degree == 0:
        if coefficient[0][1] != 0:
            print("The solution is : " + str(c))
        else:
            print("All real numbers are solution.")
    elif degree == 1:
        if len(coefficient) < 2:
            print("The solution is : " +
                  str(b) + " * " + "X^" + str(int(coefficient[0][0])) + " which is 0.")
        else:
            if deno == 0:
                print("The solution is : ")
                print("0")
            else:
                x = c / deno
                print("The solution is : ")
                if len(str(x)) > 8:
                    print("%2f" % x)
                else:
                    print(str(x))


def solve_equation(coefficient, degree):
    if degree == 0 or degree == 1:
        degree_is_below_two(degree, coefficient)
    elif degree == 2:
        degree_is_two(degree, coefficient)
    else:
        print("The polynomial degree " + str(int(degree)) +
              " is stricly greater than 2, I can't solve.")


def get_highest_degree(coefficient):
    degree = 0
    for elem in coefficient:
        if elem[0] < 2 and elem[0] >= 0:
            degree = elem[0]
        elif elem[0] == 2:
            degree = elem[0]
        else:
            degree = elem[0]
    return degree


def display(simplified):
    i = 0
    output = "Reduced form : "
    for elem in simplified:
        if elem[1] != 0:
            if elem[1] < 0:
                if i != 0:
                    output += " - "
                else:
                    output += "-"
                elem[1] = elem[1] * (-1)
                output += str(elem[1])
                elem[1] = elem[1] * (-1)
            else:
                if i != 0:
                    output += " + "
                output += str(elem[1])
            output += " * X^"
            output += str(int(elem[0]))
        i += 1
    output += " = 0\n"
    print(output)


def add_same_degree(matrix):
    matrix.sort()
    values = []
    for elem in matrix:
        found = False
        for elem2 in values:
            if elem2:
                if elem2[0] == elem[0]:
                    elem2[1] = elem2[1] + elem[1]
                    found = True
                    break
        if found == False:
            values.append(elem)
    return values


def simplify(left, right):
    result = []
    for elem in right:
        elem[1] = elem[1] * (-1)
    result = left + right
    result = add_same_degree(result)
    return(result)


def simplify_sides(equation):
    terms = []
    puissance = []
    for match in re.finditer(r'[+-]?([0-9]+)?\.?[0-9]+\*X\^[0-9]([0-9]+)?', equation):
        tmp = re.split(r'\*X\^[0-9]([0-9]+)?$', match.group(0))
        tmp2 = re.split(r'[+-]?[0-9]\*X\^', match.group(0))
        terms.append(float(tmp[0]))
        puissance.append(float((tmp2[1])))
    matrix = [[] for i in range(len(puissance))]
    for i in range(len(puissance)):
        for j in range(1):
            matrix[i].append(puissance[i])
            matrix[i].append(terms[i])
    result = add_same_degree(matrix)
    return result


def split_equation():
    equation = sys.argv[1].replace(" ", "")
    equation = equation.split("=")
    return equation


def solve():
    equation = split_equation()
    left = simplify_sides(equation[0])
    right = simplify_sides(equation[1])
    simplified = simplify(left, right)
    display(simplified)
    degree = get_highest_degree(simplified)
    solve_equation(simplified, degree)


def check_arguments():
    if len(sys.argv) != 2:
        print("Wrong argument number")
        return -1
    return 0


def main():
    if check_arguments() == 0:
        solve()
        return 0
    else:
        return -1


if __name__ == "__main__":
    main()
