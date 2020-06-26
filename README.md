#Wewalk Interview Task

The backend application that lists the locations on the specified route.
Google and Foursquare APIs were used in the application.

## Installation

Clone the repo to run the application, then go to the project directory and run the command below on the terminal.

```
docker-compose up
```

###Api Endpoints

- account/sign-up   --> registration
- account/login     --> login
- account/logout    --> logout
- api/v1/places     --> lists venues on route (must enter origin and destination latitude, longitude values as a GET request parameter)
- api/v1/favourites --> lists favourite venues of auth user (GET)
- api/v1/favourites --> add places to favorites. (POST)