/* 
When testing javascript the DOM element after each
test needs to be back in initialised state for the
tests to pass.
When the file loads, the event listener is attached
to the input element that listens for keypress. When
the firest test is run the keypress even happens
and the element with .has-error element is hidden.

In the second test we then test that under nomal 
circumstances the .has-error element should not
be hidden, but because of the first test the
second fails.

In JS the order that the tests are run is not fixed
tests will be run in no particular order. Therefore
we created initialize function that we call after 
each test to put the DOM in the initial state
*/
/*  
What if we include some third party javaScript tool later
that also defines a function initialize. We therefore 
explicitly declare an object as a property of the window
global, giving it a name that we think no one else is likely
to use. Then we make our initialize function an attribute of
that namespace objects.
*/
window.Superlists = {};
window.Superlists.initialize = function(e){
    console.log('initialize called');
    $("input[name='text']").keypress(function (e){
        $(".help-block").hide();
    });
};
console.log('list.js loadded');

$("input[name='text']").keypress(function(){
    console.log("the second function has been called")
    $("button").removeAttr("disabled").addClass("active").attr("aria-pressed");
})

