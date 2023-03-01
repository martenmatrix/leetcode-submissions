/**
 * @param {number} x
 * @return {number}
 */
var mySqrt = function(x) {
    
    if (x < 2) return x; // can only be between 0 and 1 sqrt(1) is 1 and sqrt(0) is 0 => no float numbers, negative values would give use imaginary numbers

    // binary search
    let left = 2;
    let right = Math.floor(x / 2); // sqrt is smaller than number / 2
    
    while (right >= left) {
        const midNumber = Math.floor((left + right) / 2);
        const squared = midNumber * midNumber;
        
        if (squared == x) {
            return midNumber;
        } else if (squared > x) {
            right = midNumber - 1;
        } else {
            left = midNumber + 1;
        }
    }
    return right;
};