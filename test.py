for number in range(1000):
    if number >= 100:
        if int(number / 100) ** 3 + int((number % 100) / 10) ** 3 + int(number % 10) ** 3 == number:
            print(number)