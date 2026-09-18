from math import inf, isinf

class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
      coinsReq = [inf] * (amount + 1)
      coinsReq[0] = 0
      
      for amount in range(0, amount + 1):
        for coin in coins:
          result = amount - coin
          if result >= 0:
            coinsRequiredForLevtover = coinsReq[result]
            coinsReq[amount] = min(coinsReq[amount], coinsRequiredForLevtover + 1)

      result = coinsReq[amount]
      if isinf(result):
        return -1
      return result
        