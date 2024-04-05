import random

def generate_decimal_list():
    # 生成长度为10的随机小数列表
    decimal_list = [round(random.uniform(-120, 120), 2) for _ in range(10)]
    
    # 将列表中的数字之和设为0
    sum_decimal = sum(decimal_list)
    for i in range(10):
        if sum_decimal > 0:
            if decimal_list[i] > 0:
                diff = min(decimal_list[i], sum_decimal)
                decimal_list[i] -= diff
                sum_decimal -= diff
        elif sum_decimal < 0:
            if decimal_list[i] < 0:
                diff = min(abs(decimal_list[i]), abs(sum_decimal))
                decimal_list[i] += diff
                sum_decimal += diff
    
    return decimal_list

if __name__ == "__main__":
    decimal_list = generate_decimal_list()
    print("生成的随机小数列表：", decimal_list)
    print("列表中数字之和：", sum(decimal_list))
