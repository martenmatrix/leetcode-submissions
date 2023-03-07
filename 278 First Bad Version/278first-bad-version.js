/**
 * Definition for isBadVersion()
 * 
 * @param {integer} version number
 * @return {boolean} whether the version is bad
 * isBadVersion = function(version) {
 *     ...
 * };
 */

/**
 * @param {function} isBadVersion()
 * @return {function}
 */
var solution = function(isBadVersion) {
    /**
     * @param {integer} n Total versions
     * @return {integer} The first bad version
     */
    return function(n) {
        let left = 1;
        let right = n;

        while(left<right) {
            const middle = Math.floor(left + (right-left) / 2);
            const isBad = isBadVersion(middle);
            
            if(!isBad) {
                // middle is good
                // remove everything left included self
                left = middle + 1;
            } else if (isBad) {
                // middle is bad
                // remove everything right not included self
                right = middle;
            }
        }
        // left and right are equal, one number is left, must be bad because it does not exclude itself
        return left;
    };
};