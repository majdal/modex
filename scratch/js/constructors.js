
/* experimenting with js's constructors
 
 * a 'constructor' in js is several things:
   i.   
   ii.
   iii.
 
 difference between 'new' and not-'new':
  ...
 */

console.log("-------------------------------")
function butts() {
    console.log("butts constructor begin")
    //console.log("constructor?", this.constructor == butts);
    // this gunk makes 'butts()' behave the same as 'new butts()'
    if(! (this instanceof butts)) { //careful with the parens here
        console.log("WRAPPING")
        o = new butts; //durp. this calls the constructor a bunch of times..
        console.log("o =", o, o instanceof butts)
        butts.apply(o, arguments)
        console.log("DONE WRAPPING")
        return o;
    } 
    
    //var this.s = {}
    this.empty = 43
    this.args = Array.prototype.slice.call(arguments) //record what we were called iwith
    
    console.log("butts constructor end")
}
var v1 = butts(1,2,3)
var v2 = new butts(4,5,6)
console.log(v1, v2)
console.log("v1:", v1.args.toString(), "v2:", v2.args.toString()) //--> "v1:" "1,2,3" "v2:" "4,5,6"
console.log(typeof(v1), typeof(v2)) //--> 'object'
console.log(v1 instanceof butts, v2 instanceof butts) //--> true
