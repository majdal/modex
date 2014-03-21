
/* experimenting with js's constructors
 
 * a 'constructor' in js is several things:
   i.   
   ii.
   iii.
 
 difference between 'new' and not-'new':
  ...
 */

// see also http://www.bennadel.com/blog/2522-Providing-A-Return-Value-In-A-JavaScript-Constructor.htm
//   and    http://stackoverflow.com/questions/1978049/what-values-can-a-constructor-return-to-avoid-returning-this
//    which say that you can override the result by returning an Object (as opposed to a 'basic' type like a string or a number)

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


function butts2() {
    console.log("butts constructor begin")
 
    // you can override the 'new' object by returning a complex object
    
    // so to make 'new' and not-'new' uniform
    // instead of using 'this' create a 'self' object:
    self = {}
    // and treat it like it was 'this', and return it at the end of the constructor
    // the only drawback is that then you don't get 'instanceof'
    // but you didn't want that in the first place, did you?
    
    // you can do private members and methods by defining them as local variables
    // and relying on closures
    
    self.empty = 43
    self.args = Array.prototype.slice.call(arguments) //record what we were called iwith
    
    console.log("butts constructor end")
    return self;
}

//butts = butts2;

var v1 = butts(1,2,3)
var v2 = new butts(4,5,6)
console.log(v1, v2)
console.log("v1:", v1.args.toString(), "v2:", v2.args.toString()) //--> "v1:" "1,2,3" "v2:" "4,5,6"
console.log(typeof(v1), typeof(v2)) //--> 'object'
console.log(v1 instanceof butts, v2 instanceof butts) //--> true
