// store



let jwt = document.URL.split('&')[0].split('access_token=')
localStorage.setItem("token", jwt)

//  use jwt
// jwt = localStorage.getItem("token")

