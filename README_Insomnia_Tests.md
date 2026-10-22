# Insomnia API Tests — User (REST) & Booking (GraphQL)

## A. User Service — REST (`localhost:3004`)

### U1 — List all users

**Method:** `GET`  
**URL:** `http://localhost:3004/users`

### U2 — Get an existing user

**Method:** `GET`  
**URL:** `http://localhost:3004/users/chris_rivers`

### U4 — Create a test user

**Method:** `POST`  
**URL:** `http://localhost:3004/users`  

```json
{
  "id": "insomnia_demo_user",
  "name": "Insomnia Demo User",
  "last_active": 1360031010
}
```

### U8 — Delete the test user (do this after Booking tests)

**Method:** `DELETE`  
**URL:** `http://localhost:3004/users/insomnia_demo_user`

**Expected:** HTTP `200 OK`:

```json
{"message": "user deleted"}
```

## B. Booking Service — GraphQL (`localhost:3003/graphql`)

For **every** Booking test, use:

- **Method:** `POST`
- **URL:** `http://localhost:3003/graphql`


### B1 — Get all bookings

```graphql
query {
  get_bookings {
    userid
    dates {
      date
      movies {
        id
        title
        director
        rating
      }
    }
  }
}
```

### B2 — Get a booking by user ID

```graphql
query {
  get_booking_by_id(userid: "chris_rivers") {
    userid
    dates {
      date
      movies {
        id
        title
        director
        rating
      }
    }
  }
}
```

### B4 — Add a booking for the demo user

```graphql
mutation {
  add_booking(
    userid: "insomnia_demo_user"
    dates: [
      {
        date: "20151201"
        movies: ["267eedb8-0f5d-42d5-8f43-72426b9fb3e6"]
      }
    ]
  ) {
    userid
    dates {
      date
      movies {
        id
        title
        director
        rating
      }
    }
  }
}
```

### (optional) B5 — Verify booking creation

```graphql
query {
  get_booking_by_id(userid: "insomnia_demo_user") {
    userid
    dates {
      date
      movies { id title director rating }
    }
  }
}
```


### B7 — Add a booking with an invalid date/movie

Use a **different** test ID, since existing bookings are checked first:

```graphql
mutation {
  add_booking(
    userid: "insomnia_invalid_booking"
    dates: [
      {
        date: "19000101"
        movies: ["267eedb8-0f5d-42d5-8f43-72426b9fb3e6"]
      }
    ]
  ) {
    userid
  }
}
```



### B10 — Delete the demo user's booking

```graphql
mutation {
  delete_booking(userid: "insomnia_demo_user") {
    userid
    dates { date }
  }
}
```

## C. Schedule Service — REST (`localhost:3002`)

### S1 — List all schedules

**Method:** `GET`  
**URL:** `http://localhost:3002/schedule`

### S2 — Get a schedule by date

**Method:** `GET`  
**URL:** `http://localhost:3002/schedule/20151201`

### S3 — Get a schedule with movie details

**Method:** `GET`  
**URL:** `http://localhost:3002/schedule/20151201/details`

### S4 — Get a schedule for a non-existing date

**Method:** `GET`  
**URL:** `http://localhost:3002/schedule/19000101`

**Expected:** HTTP `404 Not Found`:

```json
{
  "error": "no schedule found for this date"
}
```

### S5 — Create a test schedule

**Method:** `POST`  
**URL:** `http://localhost:3002/schedule/20260101`

```json
{
  "date": "20260101",
  "movies": ["267eedb8-0f5d-42d5-8f43-72426b9fb3e6"]
}
```

### S10 — Delete the test schedule

**Method:** `DELETE`  
**URL:** `http://localhost:3002/schedule/20260101`

## D. Movie Service — GraphQL (`localhost:3001/graphql`)

For **every** Movie test, use:

- **Method:** `POST`
- **URL:** `http://localhost:3001/graphql`

### M1 — Get all movies

```graphql
query {
  get_movies {
    id
    title
    director
    rating
  }
}
```

### M2 — Get a movie by ID

```graphql
query {
  movie_with_id(_id: "267eedb8-0f5d-42d5-8f43-72426b9fb3e6") {
    id
    title
    director
    rating
  }
}
```

### M3 — Get a movie with its actors

```graphql
query {
  movie_with_id(_id: "a8034f44-aee4-44cf-b32c-74cf452aaaae") {
    id
    title
    actors {
      id
      firstname
      lastname
      birthyear
      films
    }
  }
}
```

**Expected:** Movie details with the list of associated actors.


### M5 — Add a test movie

```graphql
mutation {
  add_movie(
    movie: {
      id: "insomnia_demo_movie"
      title: "Insomnia Test Movie"
      director: "Test Director"
      rating: 8.0
    }
  ) {
    id
    title
    director
    rating
  }
}
```

### M7 — Update the test movie rating

```graphql
mutation {
  update_movie_rate(
    _id: "insomnia_demo_movie"
    _rate: 9.5
  ) {
    id
    title
    director
    rating
  }
}
```

### M9 — Delete the test movie

```graphql
mutation {
  delete_movie(_id: "insomnia_demo_movie") {
    id
    title
    director
    rating
  }
}
```
