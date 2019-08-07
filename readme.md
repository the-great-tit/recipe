Recipe - Sharing the African heritage through the African meals.
=======

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/928287e0ec2e4803ba0919f24d8d689e)](https://app.codacy.com/app/willeswa/recipe?utm_source=github.com&utm_medium=referral&utm_content=the-great-tit/recipe&utm_campaign=Badge_Grade_Dashboard)

## Vision
Create a community where anyone can cook. 

---

## API Spec
The preferred JSON object to be returned by the API should be structured as follows:

### Users (for authentication)

```source-json
{
  "user": {
    "email": "jake@jake.jake",
    "token": "jwt.token.here",
    "username": "jake",
    "bio": "I work at statefarm",
    "image": null
  }
}
```
### Profile
```source-json
{
  "profile": {
    "username": "jake",
    "bio": "I work at statefarm",
    "image": "image-link",
    "following": false,
    "country": "kenya",
    "level": "novice"
  }
}
```
### Single Recipe
```source-json
{
  "recipe": {
    "slug": "managu-with-milk",
    "title": "Managu with Milk",
    "description": "Delicious Managu with Milk",
    "ingredients": ["Managu", "Milk"],
    "tagList": ["vegetables"],
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "rating": 3.5
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "image-link",
      "following": false,
      "country": "kenya",
      "level": "novice"
    }
  }
}
```
### Multiple recipes
```source-json
{
  "recipes":[{
    "slug": "managu-with-milk",
    "title": "Managu with Milk",
    "description": "Delicious Managu with Milk",
    "ingredients": ["Managu", "Milk"],
    "tagList": ["vegetables"],
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "rating": 3.5
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "image-link",
      "following": false,
      "country": "kenya",
      "level": "novice"
    }
  }
  }, {
    "slug": "managu-with-milk",
    "title": "Managu with Milk",
    "description": "Delicious Managu with Milk",
    "ingredients": ["Managu", "Milk"],
    "tagList": ["vegetables"],
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:48:35.824Z",
    "rating": 3.5
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "image-link",
      "following": false,
      "country": "kenya",
      "level": "novice"
    }
  }],
  "recipesCount": 2
}
```
### Single Comment
```source-json
{
  "comment": {
    "id": 1,
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:22:56.637Z",
    "body": "It takes a Jacobian",
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "image-link",
      "following": false,
      "country": "kenya",
      "level": "novice"
    }
  }
}
```
### Multiple Comments
```source-json
{
  "comments": [{
    "id": 1,
    "createdAt": "2016-02-18T03:22:56.637Z",
    "updatedAt": "2016-02-18T03:22:56.637Z",
    "body": "It takes a Jacobian",
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "image-link",
      "following": false,
      "country": "kenya",
      "level": "novice"
    }
  }],
  "commentsCount": 1
}
```
### List of Tags
```source-json
{
  "tags": [
    "kenyan",
    "dessert"
  ]
}
```
### Errors and Status Codes
If a request fails any validations, expect errors in the following format:

```source-json
{
  "errors":{
    "body": [
      "can't be empty"
    ]
  }
}
```
### Other status codes:
401 for Unauthorized requests, when a request requires authentication but it isn't provided

403 for Forbidden requests, when a request may be valid but the user doesn't have permissions to perform the action

404 for Not found requests, when a resource can't be found to fulfill the request


Endpoints:
----------

### Authentication:

`POST /api/users/login`

Example request body:

```source-json
{
  "user":{
    "email": "jake@jake.jake",
    "password": "jakejake"
  }
}
```

No authentication required, returns a User

Required fields: `email`, `password`

### Registration:

`POST /api/users`

Example request body:

```source-json
{
  "user":{
    "username": "Jacob",
    "email": "jake@jake.jake",
    "password": "jakejake"
  }
}
```

No authentication required, returns a User

Required fields: `email`, `username`, `password`

### Get Current User

`GET /api/user`

Authentication required, returns a User that's the current user

### Update User

`PUT /api/user`

Example request body:

```source-json
{
  "user":{
    "email": "jake@jake.jake",
    "bio": "I like to skateboard",
    "image": "https://i.stack.imgur.com/xHWG8.jpg"
  }
}
```

Authentication required, returns the User

Accepted fields: `email`, `username`, `password`, `image`, `bio`

### Get Profile

`GET /api/profiles/:username`

Authentication optional, returns a Profile

### Follow user

`POST /api/profiles/:username/follow`

Authentication required, returns a Profile

No additional parameters required

### Unfollow user

`DELETE /api/profiles/:username/follow`

Authentication required, returns a Profile

No additional parameters required

### List Recipes

`GET /api/recipes`

Returns most recent recipes globally by default, provide `tag`, `author` or `culture`, `meal-time` query parameter to filter results

Query Parameters:

Filter by tag:

`?tag=AngularJS`

Filter by author:

`?author=jake`

Favorited by user:

`?favorited=jake`

Limit number of recipes (default is 20):

`?limit=20`

Offset/skip number of recipes (default is 0):

`?offset=0`

Authentication optional, will return multiple recipes, ordered by most recent first

### Feed Recipes

`GET /api/recipes/feed`

Can also take `limit` and `offset` query parameters like List recipes

Authentication required, will return multiple recipes created by followed users, ordered by most recent first.

### Get Recipe

`GET /api/recipes/:slug`

No authentication required, will return single recipe

### Create recipe

`POST /api/recipes`

Example request body:

```source-json
{
  "recipe": {
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "You have to believe",
    "tagList": ["reactjs", "angularjs", "dragons"]
  }
}
```

Authentication required, will return an recipe

Required fields: `title`, `description`, `body`

Optional fields: `tagList` as an array of Strings

### Update recipe

`PUT /api/recipes/:slug`

Example request body:

```source-json
{
  "recipe": {
    "title": "Did you train your dragon?"
  }
}
```

Authentication required, returns the updated recipe

Optional fields: `title`, `description`, `body`

The `slug` also gets updated when the `title` is changed

### Delete recipe

`DELETE /api/recipes/:slug`

Authentication required

### Add Comments to an recipe

`POST /api/recipes/:slug/comments`

Example request body:

```source-json
{
  "comment": {
    "body": "His name was my name too."
  }
}
```

Authentication required, returns the created Comment
Required field: `body`

### Get Comments from an recipe

`GET /api/recipes/:slug/comments`

Authentication optional, returns multiple comments

### Delete Comment

`DELETE /api/recipes/:slug/comments/:id`

Authentication required

### Favorite recipe

`POST /api/recipes/:slug/favorite`

Authentication required, returns the recipe
No additional parameters required

### Unfavorite recipe

`DELETE /api/recipes/:slug/favorite`

Authentication required, returns the recipe

No additional parameters required

### Get Tags

`GET /api/tags`

