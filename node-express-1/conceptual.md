### Conceptual Exercise

Answer the following questions below:

- What are some ways of managing asynchronous code in JavaScript?

    callbacks, allow you to give a function to call once the async has finished. Promises, allow for chaining methods together. async/await.

- What is a Promise?

    an object that may hold a value later on.

- What are the differences between an async function and a regular function?
    async functions will return with a promise

- What is the difference between Node.js and Express.js?
    express is a framework for node to be used to build applications.

- What is the error-first callback pattern?
    takes the error first if one occured and then results in the request if successful.

- What is middleware?
    functions that are ran during the cycle of a request on the express server.

- What does the `next` function do?
    when called will run the middleware.

- What does `RETURNING` do in SQL? When would you use it?
    helps you retrieve values of columns. you would use it after using SELECT statement.

- What are some issues with the following code? (consider all aspects: performance, structure, naming, etc)


```js
async function getUsers() {
  const elie = await $.getJSON('https://api.github.com/users/elie');
  const joel = await $.getJSON('https://api.github.com/users/joelburton');
  const matt = await $.getJSON('https://api.github.com/users/mmmaaatttttt');

  return [elie, matt, joel];
}
```
performance wise you shouldn't have to wait to get the promise from the other awaits. The naming could be changed to what is coming back from the calls.