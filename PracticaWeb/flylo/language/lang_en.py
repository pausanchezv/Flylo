# coding=utf-8
class Language(object):
    """ Retorna un diccionari amb les constants d'idioma 'en' """

    @staticmethod
    def get_language():

        language = {
            'LANGUAGE': 'Language',
            'SLOGAN': "Application to search and buy flight tickets",
            'SUBJECT': 'Subject',
            'AUTHORS': 'Authors',
            'SUBJECT_NAME': 'Software Distribuït UB',
            'AUTHORS_NAME': 'Albert Espín and Pau Sanchez',

            'FLIGHT_LIST': "List of flights",
            'SELECT': "Select",
            'FLIGHT_DETAILS': "Flight details",
            'SELECT_DEPARTURE_AIRPORT': "Select a departures airport",
            'VIEW_ALL_AVAILABLE_FLIGHTS': "View all the available flights",
            'NO_FLIGHTS_AVAILABLE': "There are no flights available",
            'AVAILABLE_FLIGHTS_FROM': 'Available flights from',
            'AVAILABLE_ALL_FLIGHTS': 'All the available flights from',
            'AIRPORT_DEPARTURE': 'Departures airport',
            'AIRPORT_ARRIVAL': "Arrivals airport",
            'DEPARTURE_MOMENT': 'Time of departure',
            'ARRIVAL_MOMENT': "Time of arrival",
            'STATUS': 'Status',
            'RETURN_TO_INDEX': "Return to home page",

            'FLIGHT_ID': 'Flight identifier',
            'FLIGHT_DETAILS_FROM_ID': 'Details of the flight with number: ',
            'ESTIMATED_DEPARTURE_DATE': 'Estimated departure date',
            'ESTIMATED_DEPARTURE_TIME': 'Estimated departure time',
            'ESTIMATED_ARRIVAL_DATE': "Estimated arrival date",
            'ESTIMATED_ARRIVAL_TIME': "Estimated arrival time",
            'AIRLINE': 'Airline',
            'AIRPLANE': 'Airplane',
            'MORE_INFO': 'More information',

            'AIRCRAFT_INFO': "Aircraft information",
            'AIRLINE_INFO': "Airline information",
            'RETURN_TO_FLIGHT_LIST': "Return to flight list",
            'AICRAFT_DETAILS': "Airplane details",
            'AIRCRAFT_ID': "Airplane identifier",
            'AIRLINE_OF_AIRCRAFT': "Airline of plane",
            'CONSTRUCTION_DATE': "Assembly date",
            'FIRST_FLIGHT_DATE': "First flight date",
            'MAXIMUM_SPEED': "Maximum speed",
            'NUMBER_OF_PASSENGERS_FROM_CLASS': 'Number of passengers of class',
            'NUMBER_OF_PASSENGERS_TOTAL': 'Total number of passengers',
            'RETURN_TO_FLIGHT_INFO': "Return to flight information",

            'NAME': 'Name',
            'AIRCRAFTS_OF_AIRLINE': "Planes of the airline",
            'CATEGORIES_OF_AIRLINE': "Categories offered by the airline in this flight",
            'COUNTRY': "Country",
            'TELEPHONE': 'Telephone number',
            'FOUNDATION_YEAR': "Foundation year",
            'RETURN_TO_BACK': "Go back",

            'AIRCRAFT_FLIGHT': "Flight airplane",
            'AIRLINES_FLIGHT': "Airlines that offer the flight",
            'AIRLINE_DETAILS': "Airline details",
            'LONG_NAME': 'Complete name',
            'SHORT_NAME': 'Pseudonymous',

            'SELECT_SEATS_AND_AIRLINE': "Select the seat number and the airline",
            'WANT_RETURN_FLIGHT_QUESTION': "Do you want a return flight?",
            'SEE_FLIGHT_INFO': "See flight information",
            'FLIGHT_WITH_RETURN': "Flight with return",
            'FLIGHT_WITHOUT_RETURN': "Flight without return",

            'BOUGHT_SEATS': "Number of seats purchased:",
            'SEATS': "seats",

            'SHOPPING_CART': "Shopping cart",
            'REMOVE_FLIGHT_FROM_CART': "I want to remove the flight from the cart or modify it",
            'PURCHASE': "Purchase",
            'SAVE_AND_GO_TO_SHOPPING_CART': 'Save and go to shopping cart',
            'ADD_TO_CART': 'Add to cart',
            'ACCEPT': 'Acceptar',
            'SELECT_FLIGHT_RETURN': 'Select returning flight',
            'CANCEL': 'Cancel',
            'ADDED': 'Added',

            'LOGOUT': 'Log out',
            'LOGIN': 'Log in',
            'CLOSE': 'Close',
            'USERNAME': "Username",
            'WRITE_USERNAME': "Type the username",
            'PASSWORD': 'Password',
            'WRITE_PASSWORD': 'Type password',
            'HAVE_ACCOUNT_QUESTION': 'Do you not have an account yet?',
            'REGISTER': 'Register',
            'EMAIL': 'Email',
            'WRITE_EMAIL': 'Type your email',
            'HAVE_ACCOUNT_QUESTION_SIGNIN': 'Do you already have an account?',
            'NO_SELECTED_FLIGHTS_YET': 'You have not chosen a flight yet!',
            'NO_SELECTED_FLIGHTS_YET_TEXT': 'You can select one or more flights clicking the bottom-right button or from the main page',
            'SELECT_ONE_OR_MORE_FLIGHTS': 'Select one or more flights',
            'MORE_INFO_ABOUT_RETURNING_FLIGHT': 'More information about the return flight',
            'RETURNING_FLIGHT': 'Return flight',

            'ACQUIRED': 'Acquired!',
            'DO_CHECKIN_OR_VIEW_STATUS': "Check-in or see the state",
            'PASSENGER_NAME': 'Passenger name',
            'WRITE_NAME': 'Type the name',
            'WRITE_SURNAME': 'Type the surname',
            'CHOOSE_SEAT': 'Choose the seat',
            'WRITE_SEAT': 'Type the seat number',
            'DO_CHECKIN': 'Check-in',
            'ALL_FILEDS_ARE_REQUIRED': 'All the fields must me filled',
            'MULTIPLE_PASSENGERS_HAS_A_SAME_SEAT': 'There are multiple passengers with the same seat',
            'USERHOME_OF': 'Userhome of',
            'USERHOME_INTRO': "This is your private userhome. Here you will find the flights you have acquired and you will be able to know in which state they are. In the bottom you can see your personal data as a flylo user",
            'FLIGHT': 'Flight',
            'MORE_INFO_ABOUT_FLIGHT': 'More information about the flight',
            'USER_NOT_EXISTS': "The user does not exist",
            'USER_EXISTS': "The username already exists. Choose a different one",
            'PRICE': 'Price',
            'PASSENGER': 'Passenger',
            'CATEGORY': 'Category',
            'DISTANCE_FLIGHT': 'Flight distance',

            'BUY_SUCCESS': 'Purchase completed successfully!',
            'BUY_SUCCESS_TEXT': 'Your purchase has been completed successfully. In your userhome you will find your acquired flights and you will be able to do the CheckIn',
            'RETURN_TO_HOME_AND_MANAGE_FLIGHTS': "Return to my userhome and manage my flights",
            'OCCUPIED_SEATS': 'Occupied seats',
            'PASSENGER_DATA': 'Passenger data',
            'ALL_SEATS_ARE_FREE': 'All seats are available',
            'ANY_NUMBER_OF_SEAT_HAS_ERROR': 'One or more seat numbers are out of range!',
            'FLIGHT_CHECKIN_SUCCESS': "Successfully checked-in for flight:",
            'FLIGHT_CHECKIN_SUCCESS_TEXT': "Check-in has been completed successfully. Choose one of the following options to continue enjoying your time with flylo.",
            'RETURN_TO_USERHOME': "Return to userhome",
            'LOGIN_TO_FLYLO_TEXT': "Join FlyLo and discover the best offers to worldwide destinations",
            'GO': 'Go!',
            'UNEXPECTED_EMAIL_FORMAT': "The email you have just introduced does not have the expected format!",
            'USER_MONEY_ALERT': 'Beware! Your balance is:',
            'USER_MONEY_ALERT_TEXT': "You do not have enough money to buy, the administrator might update your balance",
            'TRANSACTION_ERROR': "A transaction error has occurred!",
            'TRANSACTION_ERROR_TEXT': "A transaction error has occurred due to atomicity reasons when accessing the database. Please try again.",
            'SESSION_USER_ALERT': "Beware! Your are logged in as an administrator. Please log in as a client!",
            'PERSONNEL_DATA': 'Personal Data',
            'ACQUIRED_FLIGHTS': 'Acquired flights',
            'FILTER_FLIGHTS_BY_DEPARTURE': 'Filter flights by departure city',
            'WELCOME_WHEN_USER_HAS_NOT_FLIGHTS': "We have detected that you have not acquired any flights yet. We want to welcome you to FlyLo and tell you that following this link you will gain access to our most competitive prices",

            'TRANSACTION_ERROR_META': "Transaction error",
            'USERHOME': "Userhome",
            'CHECK_IN_SUCCESS_META': "Successfully checked-in",
            'CHECKIN_META': "Executing check-in",
            'BUY_SUCCESS_META': "Purchase completed successfully",
            'ERROR_USER_IS_NOT_A_CLIENT': "This user is not a client. Sign in with a client account.",

            'FLIGHTS': "Flights",
            'COMPARATOR': "Comparator",
            'FLIGHT_COMPARATOR': "Flight comparator",
            'FLIGHT_COMPARATOR_TEXT': "Fill in those fields you want to use to search and leave the rest empty. Do not leave all fields empty.",
            'PUSH_DATA_FLIGHTS': "Introduce the flight data",
            'SORTING_BY_PRICE': "Ordering the search by price...",
            'NO_FLIGHT_ARE_AVAILABLE_FOR_THIS_ARGUMENT': "There are no flights available for these search parameters.",
            'INIT_SEARCH': "Start the search",
            'DAY': "Day",
            'MONTH': "Month",
            'YEAR': "Year",
            'ONE_FIELD_REQUIRED': "You must fill in at least one field.",

            'WORK_IN_PROGRESS': "Work in progress",
            'AIRPORTS_DEPARTURE_AND_ARRIVAL': "Departure and arrival airports",
            'SEARCH_BY': "Search by",
            'EQUIPARATE_FLIGHT': "Flight comparator",
            'USE_COMPARATOR_GOR_THIS_FLIGHT': "Use comparator for this flight",

            'ALL_POSSIBLE_COMBINATIONS': "It supports all possible combinations of "
                                         "search",
            'MINUTE': "Minute",
            'HOUR': "Hour",
            'SELECTED': "Selected",
            'ALERT_USER_AGENT': 'Mozilla/Firefox does not support date masks! Note: We recommend using Chorme, or other browser as Microsoft Edge comfortably to manipulate dates using masks.'
        }

        return language