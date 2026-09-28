# REST in one page

Every AI service in this course is reached the same way: an HTTP request to a URL, with JSON in and JSON out. That style is called REST. Roy Fielding described it in his 2000 PhD dissertation as a way to build distributed applications that scale the way the web does.

## The verbs

| Verb | Means | Changes the server? | Safe to repeat? |
|---|---|---|---|
| `GET` | Read a resource | No | Yes |
| `POST` | Create, or run an action | Yes | No |
| `PUT` | Replace a resource completely | Yes | Yes |
| `PATCH` | Change part of a resource | Yes | Not always |
| `DELETE` | Remove a resource | Yes | Yes |

"Safe to repeat" is called **idempotent**: sending the request twice leaves the server in the same state as sending it once. `GET`, `PUT`, and `DELETE` are idempotent; `POST` is not. `HEAD` (a `GET` without the body) and `OPTIONS` (which verbs are allowed here?) also exist.

## The principles you will notice

- **Resources have URLs; verbs say what to do.** A URL names a thing (`/employees/3`), never an action (`/updateEmployee`). You send `PUT /employees/3` with the new data.
- **A uniform interface.** Every resource is used through the same small set of verbs.
- **Stateless.** Every request carries everything the server needs, including who you are. The server remembers nothing between requests. That is why each request has the `Authorization` header, and why a chat conversation resends every earlier message each turn: there is no memory on the server, so the tokens add up.
- **Representations.** The server sends a representation of the resource, usually JSON, and says which with `Content-Type`.

Websites keep state across stateless requests with cookies: a small ID the browser sends back every time, which the server uses to find your shopping cart. AI chat APIs have no equivalent; your program keeps the history.

## AI APIs in these terms

| You do | Request |
|---|---|
| List the available models | `GET /api/v1/models` |
| Ask a chat model | `POST /api/v1/chat/completions` |
| Embed text | `POST /api/v1/embeddings` |

Almost everything is a `POST`, because each call runs a computation and bills you for it. There is nothing to update or delete.

## Status codes you will see

`200` OK · `400` bad request (often a typo in the model name) · `401` no or wrong key · `402` out of credit · `404` wrong URL · `429` too many requests, slow down · `5xx` the service failed, not you.
