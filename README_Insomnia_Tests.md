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
