- [算法](#算法)
    - [题目](#题目)
        - [1.红黑树](#1红黑树)
        - [2.基本排序算法汇总(桶排序,归并,快排,希尔,插入,选择,冒泡)](#2基本排序算法汇总桶排序归并快排希尔插入选择冒泡)
        - [3.数组中出现次数超过一半的数字-Python版](#3数组中出现次数超过一半的数字-python版)
        - [4.求100以内的质数](#4求100以内的质数)
        - [5.无重复字符的最长子串-Python实现](#5无重复字符的最长子串-python实现)
        - [6.通过2个5/6升得水壶从池塘得到3升水](#6通过2个5/6升得水壶从池塘得到3升水)
        - [7.什么是MD5加密，有什么特点？](#7什么是md5加密有什么特点)
        - [8.什么是对称加密和非对称加密](#8什么是对称加密和非对称加密)
        - [9.如何判断单向链表中是否有环？](#9如何判断单向链表中是否有环)
        - [10.斐波那契数列](#10斐波那契数列)
        - [11.如何翻转一个单链表？](#11如何翻转一个单链表)
        - [12.两数之和 Two Sum](#12两数之和-two-sum)
        - [13.搜索旋转排序数组 Search in Rotated Sorted Array](#13搜索旋转排序数组-search-in-rotated-sorted-array)
        - [14.Python实现一个Stack的数据结构](#14python实现一个stack的数据结构)
        - [15.写一个二分查找](#15写一个二分查找)
        - [16.set 用 in 时间复杂度是多少，为什么？](#16set-用-in-时间复杂度是多少为什么)
        - [17.列表中有n个正整数范围在[0，1000]，进行排序；](#17列表中有n个正整数范围在[01000]进行排序；)
# 算法
## 题目
算法题直接刷leetcode即可
### 1.红黑树
红黑树与AVL的比较：

AVL是严格平衡树，因此在增加或者删除节点的时候，根据不同情况，旋转的次数比红黑树要多；

红黑是用非严格的平衡来换取增删节点时候旋转次数的降低；

所以简单说，如果你的应用中，搜索的次数远远大于插入和删除，那么选择AVL，如果搜索，插入删除次数几乎差不多，应该选择RB。

红黑树详解: https://xieguanglei.github.io/blog/post/red-black-tree.html

教你透彻了解红黑树: https://github.com/julycoding/The-Art-Of-Programming-By-July/blob/master/ebook/zh/03.01.md

### 2.基本排序算法汇总(桶排序,归并,快排,希尔,插入,选择,冒泡)

![](../pics/python/all_sort.png)

https://blog.csdn.net/mrlevo520/article/details/77829204
https://blog.csdn.net/stdio1916/article/details/90485867

归并排序
```python
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
    result.extend(left)
    result.extend(right)
    return result
```

快速

```python
def quick_sort(arr1):
    if len(arr1) < 2:
        return arr1
    else:
        pivot = arr1[0]
        less = [i for i in arr1[1:] if i < pivot]
        greater = [j for j in arr1[1:] if j >= pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)
```

插入
```python
def insert_sort(relist):
    len_ = len(relist)
    for i in range(1,len_):
        for j in range(i):
            if relist[i] < relist[j]:
                relist.insert(j,relist[i])
                relist.pop(i+1)
                break
    return relist
```


冒泡
```
def bubble_sort(arr1):
    for i in range(len(arr1)):
        for j  in range(len(arr1[1:])):
            if arr1[i] < arr1[j]:
                arr1[i], arr1[j] = arr1[j], arr1[i]
    return arr1
```

### 3.数组中出现次数超过一半的数字-Python版
```
# -*- coding:utf-8 -*-
class Solution:
    def more_than_half(self, numbers):
# write code here
        dict = {}
        for num in numbers:
            if num not in dict:
                dict[num] = 1
            else:
                dict[num]+=1
            if dict[num] > len(numbers)/2:
                return num
        return 0
```
### 4.求100以内的质数
### 5.无重复字符的最长子串-Python实现
```
class Solution(object):
    def lengthOfLongestSubstring(self, s):
        res = 0;i = 0; val = ""
        for j in range(len(s)):
            if s[j] not in s[i:j]:
                res = max(res,j+1-i)
            else:
                i += s[i:j].index(s[j]) + 1
        return res

```
### 6.通过2个5/6升得水壶从池塘得到3升水
### 7.什么是MD5加密，有什么特点？
### 8.什么是对称加密和非对称加密
### 9.如何判断单向链表中是否有环？
```
# 快慢指针
class Solution(object):
    def hasCycle(self, head):
        if(head == None or head.next == None):
            return False
        node1 = head
        node2 = head.next
        while(node1 != node2):
            if(node2 == None or node2.next == None):
                return False
            node1 = node1.next
            node2 = node2.next.next

        return True
```
### 10.斐波那契数列
```
def fib();
a, b = 0, 1
while true:
    yield a
    a, b = b, a+b

from itertools import islice
print list(islice(fib(), 5))
```
### 11.如何翻转一个单链表？
```
class Solution(object):
	def reverseList(self, head):
		"""
		:type head: ListNode
		:rtype: ListNode
		"""
# 申请两个节点，pre和 cur，pre指向None
		pre = None
		cur = head
# 遍历链表，while循环里面的内容其实可以写成一行
# 这里只做演示，就不搞那么骚气的写法了
		while cur:
# 记录当前节点的下一个节点
			tmp = cur.next
# 然后将当前节点指向pre
			cur.next = pre
# pre和cur节点都前进一位
			pre = cur
			cur = tmp
		return pre
```
### 12.两数之和 Two Sum
```
class Solution(object):
    def twoSum(self, nums, target):
        _dict = {}
        for i, m in enumerate(nums):
            if _dict.get(target - m) is not None:
                return [_dict.get(target - m), i]
            _dict[m] = i
```
### 13.搜索旋转排序数组 Search in Rotated Sorted Array
### 14.Python实现一个Stack的数据结构
### 15.写一个二分查找
```
def binary_chop(alist, data):
    """
    非递归解决二分查找
    """
    n = len(alist)
    first = 0
    last = n - 1
    while first <= last:
        mid = (last+first)//2
        if alist[mid] > data:
            last = mid - 1
        elif alist[mid] < data:
            first = mid + 1
        else:
            return True
    return False

def binary_chop2(alist, data):
    """
    递归解决二分查找
    """
    n = len(alist)
    if n < 1:
        return False
    mid = n // 2
    if alist[mid] > data:
        return binary_chop2(alist[0:mid], data)
    elif alist[mid] < data:
        return binary_chop2(alist[mid+1:], data)
    else:
        return True

if __name__ == "__main__":
    lis = [2,4, 5, 12, 14, 23]
    if binary_chop(lis, 12):
        print('ok')
    else:
        print('false')
```
### 16.set 用 in 时间复杂度是多少，为什么？
### 17.列表中有n个正整数范围在[0，1000]，进行排序；
