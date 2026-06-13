class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        lowestBuy = prices[0]
        bestProfit = 0

        for price in prices:
            profit = price - lowestBuy

            if profit > bestProfit:
                bestProfit = profit

            if price < lowestBuy:
                lowestBuy = price

        return bestProfit
