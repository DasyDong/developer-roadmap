# coding: utf-8

def two_sum(nums, target):
    """
    :type nums: List[int]
    :type target: int
    :rtype: List[int]
    """
    for i in nums:
        if target - i in nums and i is not target-i:
            return [nums.index(i), nums.index(target - i)]


def run_twosum():
    nums_all = [3, 2, 7, 6, 11, 15]
    target = 9
    nums = two_sum(nums_all, target)
    print(nums)
# run_twosum()
##################################################


def func1(l):
    if isinstance(l,str):
        l = list(l)
        l = [int(i) for i in l]
    l.sort(reverse=True)
    print l
    for i in range(len(l)):
        if l[i] % 2>0:
            l.insert(0,l.pop(i))
    print(''.join(str(e) for e in l))
# func1('1982376455')
##################################################


def count_str(str_data):
    """定义一个字符出现次数的函数"""
    dict_str = {}
    for i in str_data:
        dict_str[i] = dict_str.get(i, 0)+1
    return dict_str


def test_count_str():
    dict_str = count_str("AAABBCCAC")
    str_count_data = ""
    for k, v in dict_str.items():
        str_count_data += k + str(v)
    print(str_count_data)

# test_count_str()
##################################################


if __name__ == "__main__":
    test_count_str()
