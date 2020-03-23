class Solution:
    def removeDuplicates(self, nums: [int]):
        if not nums: return []
        k = 1
        for i in range(1, len(nums)):
            if nums[i] != nums[i - 1]:
                k += 1
        return k


print(Solution().removeDuplicates([1,1,2,3,3,3,4,4,5,5]))