### Conceptual Exercise

Answer the following questions below:

- What are important differences between Python and JavaScript?
    1. python has A big, vast library with it unlike javascripts limited library.
    2. python is a server side language and javascript is a web developing language.
    3. python is used for math and autonomous applications while javascript is more for front-end web design.

- Given a dictionary like ``{"a": 1, "b": 2}``: , list two ways you
  can try to get a missing key (like "c") *without* your programming
  crashing.
  1. use get() to print out the value if its missing.
  2. defaultdict is a container and will return a value if the key is missing.

- What is a unit test?
    1. when specifics units of code are tested to make sure they run correctly for the thier part in the application.

- What is an integration test?
    1. integration testing is when multiple parts of the application are checked to make sure that everything runs together correctly.

- What is the role of web application framework, like Flask?
    1. it helps to make a web application with python because python isn't ran in a web browser.

- You can pass information to Flask either as a parameter in a route URL
  (like '/foods/pretzel') or using a URL query param (like
  'foods?type=pretzel'). How might you choose which one is a better fit
  for an application?
    1. if you need to sort or filter use a URL query param but if its just to call for a page then it would be easier to just use the route URL.

- How do you collect data from a URL placeholder parameter using Flask?
    1. use request.data()
- How do you collect data from the query string using Flask?
    1. use request.get.args()
- How do you collect data from the body of the request using Flask?
    1. use request.data()
- What is a cookie and what kinds of things are they commonly used for?
    1. a cookie is a way for web servers to get needed info from the web browser, they can help to store info on your system from the site for you in their own .txt file.

- What is the session object in Flask?
    1. is a dictionary with key value pairs for session variables and associated values.

- What does Flask's `jsonify()` do?
    1. is a helper method that returns a response object of JSON instead of a JSON string.
