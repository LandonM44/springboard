const express = require('express');
const axios = require('axios');
const ExpressError = require("./error");
const app = express();

const USER_API = 'https://api.github.com/users';

app.post('/', async function(req, res, next) {
  try {
    let promises = req.body.developers.map(developer =>
      axios.get(`${USER_API}/${developer}`)
    );

    let results = await Promise.all(promises);

    let out = results.map(r => ({ name: r.data.name, bio: r.data.bio }));//({developers: [name: r.data.name, bio: r.data.bio]})

    return res.json(out);
  } catch (err) {
    return next(err);
  }
});

app.use(function(req, res, next) {
  const err = new ExpressError('not found', 404);
  return next(err);
});

app.use(function(err, req, res, next) {
  let status = err.status || 500;

  return res.status(status).json({
    status,
    message: err.message
  });
});

app.listen(3000, function() {
  console.log('server is listening on 3000');
});

module.exports= app;
