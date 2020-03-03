# coding:utf-8
# 快排
def quick_sort(arr1):
    if len(arr1) < 2:
        return arr1
    else:
        pivot = arr1[0]
        less = [i for i in arr1[1:] if i < pivot]
        greater = [j for j in arr1[1:] if j >= pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)

# 归并
def merge_sort(arr1):
    if len(arr1) < 2:
        return arr1
    half = int(len(arr1) / 2)
    left_arr1 = merge_sort(arr1[:half])
    right_arr1 = merge_sort(arr1[half:])
    return merge(left_arr1, right_arr1)

def merge(left, right):
    result = []
    while left and right:
        result.append(left.pop(0) if left[0] <= right[0] else right.pop(0))
    # while left:
        # result.append(left.pop(0))
    result.extend(left)
    result.extend(right)
    # while right:
        # result.append(right.pop(0))
    return result


# 希尔
def shell_sort(relist):
    n = len(relist)
    gap = int(n / 2)  # 初始步长
    while gap > 0:
        for i in range(gap, n):
            relist[:i] = insertSort(relist[:i])
            print(relist)
        gap = int(gap / 2)  # 得到新的步长

    return relist


# 插入
def insert_sort(arr1):
    temp = [arr1[0]]
    arr1 = arr1[1:]
    while arr1:
        for j in range(len(temp)):
            if temp[j] > arr1[0]:
                temp.insert(j, arr1[0])
                break
        else:
            temp.insert(len(temp), arr1[0])
        arr1.pop(0)
    return temp

def insertSort(relist):
    len_ = len(relist)
    for i in range(1,len_):
        for j in range(i):
            if relist[i] < relist[j]:
                relist.insert(j,relist[i])  # 首先碰到第一个比自己大的数字，赶紧刹车，停在那，所以选择insert
                relist.pop(i+1)  # 因为前面的insert操作，所以后面位数+1，这个位置的数已经insert到前面去了，所以pop弹出
                break
    return relist

# 冒泡
def bubble_sort(arr1):
    for i in range(len(arr1)):
        for j  in range(len(arr1[1:])):
            if arr1[i] < arr1[j]:
                arr1[i], arr1[j] = arr1[j], arr1[i]
    return arr1

print(merge_sort([1,7,6, 8,22,6,77,11, 66, 14]))


