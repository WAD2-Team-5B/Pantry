# API Documentation

- 'Parameters' is the user's parameters which the server will receive.
- 'Context_Dict' is the server's response.

## 'Index' Page

### Page Load

- Description:

  - User loads or refreshes page.
  - We need not worry about the search bar at this point.
  - We just need to load in the 'Highest Rated Recipes' and the 'Newest Recipes'.

- Parameters:

- Context_Dict:

  - num_highest_rated : Integer
  - num_newest : Integer
  - highest_rated_recipes : List of Dictionaries
    - {
      name: String,
      link: String?,
      image: String?
      }
  - newest_recipes : List of Dictionaries
    - {
      name: String,
      link: String?,
      image: String?
      }

### Search

- Description:

  - User has clicked the search button.
  - We need to redirect user to 'Recipes' page and display results from his search_query.

- Parameters:

  - search_query : String

- Context_Dict:

## 'Recipes' Page

### Page Load

- Description:

  - User loads or refreshes page. OR USER WAS REDIRECTED FROM 'Index' PAGE!
  - If the user has just refreshed/loaded the page then we dont need to display any search results.
  - If user was redirected then we need to display search results of his query.

#### No Redirect

- Parameters:

- Context_Dict:

  - cuisines : List of String
  - categories : List of String
  - recipes : List of Dictionaries
    - {
      name: String,
      link: String?,
      image: String?,
      rating: Float,
      saves: Integer,
      difficulty: String,
      cuisine: Italian,
      prep: String,
      cook: String
      }

#### Redirect

- Parameters:

  - search_query : String

- Context_Dict:

  - search_query : String
  - cuisines : List of String
  - categories : List of String
  - recipes : List of Dictionaries
    - {
      name: String,
      link: String?,
      image: String?,
      rating: Float,
      saves: Integer,
      difficulty: String,
      cuisine: Italian,
      prep: String,
      cook: String
      }

### Search / Filter / Sort

- Description:

  - User types in search bar or selects a filter or selects a sort.
  - We need to display search results of his query but need to give frontend back the search query itself along with any of his selected filters or sorts so can display nice css.
  - If passed parameters for any of the filters or sorts are NOT empty then user has selected them so must carry out the filter or sort on the data before sending back.

- Parameters:

  - search_query : String
  - selected_difficulty : String
  - selected_cuisines : List of String
  - selected_categories : List of String
  - selected_sort : String

- Context_Dict:

  - search_query : String
  - selected_difficulty : String
  - selected_cuisines : List of String
  - selected_categories : List of String
  - selected_sort : String
  - cuisines : List of String
  - categories : List of String
  - recipes : List of Dictionaries
    - {
      name: String,
      link: String?,
      image: String?,
      rating: Float,
      saves: Integer,
      difficulty: String,
      cuisine: Italian,
      prep: String,
      cook: String
      }

## 'Login' Page

### Page Load

- No Parameters

- Context_Dict:

  - success : True (has to be True to not display error message on page load!)

### Form Submission

- Description:

  - User has submitted valid form data to log into their account.
  - If account exists then a redirect should occur along with cookies. (I think we should redirect them to their profile?)
  - If no account exists then send frontend error response.

- Parameters:

  - username : String
  - password : String

- Context_Dict:

  - success : Boolean (if success maybe dont even need to send. just deal with the redirect and cookies?)

## 'Sign Up' Page

### Page Load

- No Parameters
- No Context_Dict

### Form Submission

- Description:

  - User has submitted valid form data to create an account.
  - No need for a server response since the data is valid.
  - Just need to create their account and log them in and redirect them to their profile page.

- Parameters:

  - username : String
  - password : String

- Context_Dict:
