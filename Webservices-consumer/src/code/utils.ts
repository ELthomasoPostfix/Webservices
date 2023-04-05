/** Check if the value is of type Number */
export function isNumber(value: any): Boolean {
    return typeof value === typeof Number();
}

/** Check if the input value is a numeric string.
 * 
 * Any value of a type different from String
 * fails automatically.
 * source: https://stackoverflow.com/a/175787
 */
export function isNumeric(str: any): Boolean {
    if (typeof str !== typeof String()) return false // we only process strings!  
    return !isNaN(Number(str)) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
           !isNaN(parseFloat(str)) // ...and ensure strings of whitespace fail
}
