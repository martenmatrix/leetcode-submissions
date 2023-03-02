/** 
 * Forward declaration of guess API.
 * @param {number} num   your guess
 * @return 	     -1 if num is higher than the picked number
 *			      1 if num is lower than the picked number
 *               otherwise return 0
 * var guess = function(num) {}
 */

/**
 * @param {number} n
 * @return {number}
 */
var guessNumber = function(n) {
    let left = 1;
    let right = n;
    
    while (left <= right) {
        const pivot = Math.floor((left + right) / 2);
        const apiResponse = guess(pivot);
        
        if (apiResponse === 0) {
            // correct guess
            return pivot;
        } else if (apiResponse === -1) {
            right = pivot - 1;
        } else {
            left = pivot + 1;
        }
    }
};