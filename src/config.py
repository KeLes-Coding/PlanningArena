# Program entry point:
QUERY_RECEIVE = "src/query_receive.py"

"""
	Model Settings
"""
API_KEY = ""
BASE_URL = ""
GLOBAL_MODEL = ""

"""
	Proxy Address
"""
HTTP_PROXY = ""

# JSON file save path
if GLOBAL_MODEL == "qwen-plus":
    JSON_DATA = "data/qwen_data/data"
    ERROR_DATA = "data/qwen_data/ERROR_data"
elif GLOBAL_MODEL == "deepseek-chat":
    JSON_DATA = "data/deepseek_data/data"
    ERROR_DATA = "data/deepseek_data/ERROR_data"
else:
    JSON_DATA = None  # Or other default value

MESSAGE_PLANNER_APP = [
    """Your tools are as follows:
Shopping Scenarios
Ele.me
Dianping
Marriott Mobile App
Mobike App
Amazon
eBay
Walmart Online Store
Target.com
Etsy
Maoyan
Taobao
JD.com
AliExpress
Sephora
ASOS
Zalando

Education Scenarios
Khan Academy
Coursera
Duolingo
edX
Codecademy
Udacity
Skillshare
Udemy
LinkedIn Learning
Babbel
Photomath
Quizlet
Canva

Health Scenarios
MyFitnessPal
Headspace
Fitbit
Calm
Strava
MyPlate by Livestrong
Nike Training Club
WebMD
Healthline
WaterMinder
Mindbody
Teladoc
PillPack
Sleep Cycle
7 Minute Workout
Symptomate
BetterHelp
Quit Genius

Travel Scenarios
Ctrip
Booking.com
Hertz Mobile App
Trenitalia Website
Uber
Airbnb
Google Maps
Skyscanner
TripAdvisor
Grab
BlaBlaCar
Gojek
KakaoTaxi
Citymapper
Agoda
Expedia

Development Scenarios
GitLab
JIRA
Jenkins
GitHub
Docker
Bitbucket
Travis CI
Trello
Asana
Confluence
Slack
Kubernetes
Readme.md
CircleCI
Zendesk
SourceTree

Entertainment Scenarios
Netflix
Spotify
Goodreads
YouTube Premium
Pandora
Crunchyroll
Twitch
Mixer
Stitcher
Photomath
Discord
Steam
Xbox Live
PlayStation Network
Oculus App
GOG Galaxy

Meeting Scenarios
Zoom
Microsoft Teams
Cisco Webex
BlueJeans
GoToMeeting
AnyMeeting
RingCentral
Livestorm
ClickMeeting
Cisco Spark

Calendar Scenarios
Google Calendar
Outlook
Apple Calendar
Calendly
Timely
TimeTree
MyStudyLife
Timetable

Gaming Scenarios
Nintendo eShop Card
Xbox Live
PlayStation Network
Oculus App
GOG Galaxy
Mixer

Dining Scenarios
UberEats
DoorDash
Postmates
Deliveroo
Caviar
Seamless
EatStreet
OrderUp
GrubDirect
Deliveroo App

Other Scenarios
PayPal
Apple Pay
Google Pay
Microsoft Rewards
SF Express
UPS
Royal Mail
FedEx
Didi Chuxing
12306
GrabFood
BlaBlaCar
KakaoTaxi
Citymapper
Alipay
WeChat Pay
IFTTT
Siri
WhatsApp
Telegram
Line
Skype
Viber
Facebook Messenger
Zalo
Todoist
Google Keep
Google Docs

The task is:
"""
]

MESSAGE_RESULT_APP = [""""""]

AGENT_PLANNER_API = [
    """{
    "GlobalThought": {
        "type": "string"
    },
    "OrderSteps": {
        "TotalSteps": {
            "type": "integer"
        },
        "StepDetail": {
            "StepNumber": {
                "type": "integer"
            },
            "Description": {
                "type": "string"
            },
            "Action": {
                "type": "string"
            }
        }
    }
}"""
]

AGENT_RESULT_API = [
    """{
"OrderSteps": {
    "StepDetail": {
            "StepNumber": {
                "type": "integer"
            },
            "Description": {
                "type": "string"
            },
            "Action": {
                "type": "string"
            },
            "Results": {
                "type": "string"
            }
        }
    }
}"""
]

AGENT_PLANNER_APP = [
    """{
    "GlobalThought": {
        "type": "string"
    },
    "OrderSteps": {
        "TotalSteps": {
            "type": "integer"
        },
        "StepDetail": {
            "StepNumber": {
                "type": "integer"
            },
            "Description": {
                "type": "string"
            },
            "Action": {
                "type": "string"
            }
        }
    }
}"""
]

AGENT_RESULT_APP = [
    """{
"OrderSteps": {
    "StepDetail": {
            "StepNumber": {
                "type": "integer"
            },
            "Description": {
                "type": "string"
            },
            "Action": {
                "type": "string"
            },
            "Results": {
                "Status": {
                    "type": "string",
                    "enum": ["Success", "Failure"]
                },
                "Response": {
                    "type": "object"
                }
            }
        }
    }
}"""
]

# Planner Initialization Template DAG
MESSAGE_PLANNER_DAG = [
    """{
	"queryWeather": {
		"requiredParams": {
			"date": {"type": "str"},
			"city": {"type": "str"}
		}
	},
	"getCitySpecialties": {
		"requiredParams": {
			"city": {"type": "str"}
		},
		"optionalParams": {
			"foodType": {"type": "str"}
		}
	},
	"bookRestaurant": {
		"requiredParams": {
			"reservationDate": {"type": "datetime"},
			"reservationTime": {"type": "datetime"},
			"restaurantLocation": {"type": "str"},
			"city": {"type": "str"},
			"userContactNumber": {"type": "str"},
			"peopleNumber": {"type": "int"}
		},
		"optionalParams": {
			"restaurantName": {"type": "str"},
			"restaurantType": {"type": "str"},
			"providingFood": {"type": "str"},
			"specialRequests": {"type": "str"}
		}
	},
	"bookHotel": {
		"requiredParams": {
			"hotelName": {"type": "str"},
			"checkInDate": {"type": "datetime"},
			"checkInTime": {"type": "datetime"},
			"checkOutDate": {"type": "datetime"},
			"roomType": {"type": "str"},
			"numberOfRooms": {"type": "str"},
			"peopleNumber": {"type": "int"},
			"userContactNumber": {"type": "str"}
		},
		"optionalParams": {
			"specialRequests": {"type": "str"}
		}
	},
	"queryFlights": {
		"requiredParams": {
			"departureDate ": {"type": "datetime"},
			"origin": {"type": "str"},
			"destination": {"type": "str"}
		},
		"optionalParams": {
			"departureTime": {"type": "datetime"},
			"airline": {"type": "str"},
			"cabinClass": {"type": "str"}
		}
	},
	"bookFlight": {
		"requiredParams": {
			"flightNumber": {"type": "str"},
			"contactNumber": {"type": "str"},
			"cabinClass": {"type": "str"}
		}
	},
	"queryTrains": {
		"requiredParams": {
			"date": {"type": "datetime"},
			"origin": {"type": "str"},
			"destination": {"type": "str"}
		},
		"optionalParams": {
			"departureTime": {"type": "datetime"},
			"trainType": {"type": "str"},
			"cabinClass": {"type": "str"}
		}
	},
	"bookTrain": {
		"requiredParams": {
			"trainNumber": {"type": "str"},
			"contactNumber": {"type": "str"},
			"cabinClass": {"type": "str"}
		}
	},
	"bookTaxi": {
		"requiredParams": {
			"pickupAddress": {"type": "str"},
			"dropOffAddress": {"type": "str"},
			"pickupTime": {"type": "datetime"},
			"contactNumber": {"type": "str"}
		},
		"optionalParams": {
			"carType": {"type": "str"}
		}
	},
	"searchGoodsOnline": {
		"optionalParams": {
			"goodName": {"type": "str"},
			"goodCategory": {"type": "str"},
			"minPrice": {"type": "float"},
			"maxPrice": {"type": "float"},
			"platform": {"type": "str"},
			"sameDayDelivery": {"type": "bool"},
			"brand": {"type": "str"},
			"rating": {"type": "float"},
			"freeShipping": {"type": "bool"}
		}
	},
	"compareCostEffectiveness": {
		"requiredParams": {
			"product1Name": {"type": "str"},
			"product2Name": {"type": "str"},
			"product1Price": {"type": "float"},
			"product2Price": {"type": "float"},
			"product1Rating": {"type": "float"},
			"product2Rating": {"type": "float"}
		},
		"optionalParams": {
			"product3Name": {"type": "str"},
			"product3Price": {"type": "float"},
			"product3Rating": {"type": "float"}
		}
	},
	"addToCart": {
		"requiredParams": {
			"goodId": {"type": "str"},
			"quantity": {"type": "integer"},
			"goodName": {"type": "str"},
			"goodSinglePrice": {"type": "float"},
			"userContactNumber": {"type": "float"}
		}
	},
	"buyGood": {
		"requiredParams": {
			"goodId": {"type": "str"},
			"quantity": {"type": "int"},
			"pricePerUnit": {"type": "float"},
			"shippingCost": {"type": "float"},
			"totalPrice": {"type": "float"},
			"contactNumber": {"type": "str"},
			"address": {"type": "str"}
		},
		"optionalParams": {
			"promoCode": {"type": "str"},
			"paymentMethod": {"type": "str"}
		}
	},
	"queryOnlineCourses": {
		"optionalParams": {
			"category": {"type": "str"},
			"courseName": {"type": "str"},
			"pay": {"type": "bool"},
			"coursePrice": {"type": "float"},
			"platform": {"type": "str"},
			"level": {"type": "str"},
			"instructorName": {"type": "str"},
			"rating": {"type": "float"},
			"startDate": {"type": "datetime"}
		}
	},
	"enrollCourse": {
		"requiredParams": {
			"courseId": {"type": "str"},
			"courseName": {"type": "str"},
			"userContactNumber": {"type": "str"}
		}
	},
	"getEnrollCourses": {
		"optionalParams": {
			"contactNumber": {"type": "str"}
		}
	},
	"searchEvents": {
		"requiredParams": {
			"eventType": {"type": "str"},
			"location": {"type": "str"},
			"date": {"type": "date"}
		},
		"optionalParams": {
			"eventStatus": {"type": "str"},
			"keyword": {"type": "str"}
		}
	},
	"bookEvent": {
		"requiredParams": {
			"eventId": {"type": "str"},
			"date": {"type": "date"},
			"time": {"type": "date"},
			"userContactNumber": {"type": "date"},
			"peopleNumber": {"type": "date"}
		}
    },
    "calculateBMI": {
        "requiredParams": {
            "height": {"type": "float"},
            "weight": {"type": "float"}
        }
    },
    "saveToMemo": {
        "requiredParams": {
            "startDate": {"type": "datetime"},
            "endDate": {"type": "datetime"}
        },
        "optionalParams": {
            "dateAndWeather": {"type": "str"},
            "cityAndSpecialties": {"type": "str"},
            "dateAndAction": {"type": "str"},
            "hotelName": {"type": "str"},
            "hotelPrice": {"type": "float"},
            "restaurantName": {"type": "str"},
            "trainPrice": {"type": "float"},
            "flightNumber": {"type": "str"},
            "flightPrice": {"type": "float"},
            "taxiPrice": {"type": "float"},
            "totalPrice": {"type": "float"},
            "BMI": {"type": "str"},
            "eventName": {"type": "str"},
            "eventPrice": {"type": "str"}
        }
    },
    "countBudget": {
        "optionalParams": {
            "price1": {"type": "float"},
            "price2": {"type": "float"},
            "price3": {"type": "float"},
            "price4": {"type": "float"},
            "price5": {"type": "float"},
            "price6": {"type": "float"},
            "price7": {"type": "float"},
            "price8": {"type": "float"}
        }
    },
    "recommendFood": {
        "optionalParams": {
            "age": {"type": "int"},
            "gender": {"type": "str"},
            "height": {"type": "int"},
            "weight": {"type": "int"},
            "BMI": {"type": "float"}
        }
    },
    "recommendSports": {
        "optionalParams": {
            "age": {"type": "int"},
            "gender": {"type": "str"},
            "height": {"type": "int"},
            "weight": {"type": "int"},
            "BMI": {"type": "float"}
        }
    },
    "calculateCalorie": {
        "optionalParams": {
            "foodName": {"type": "str"},
            "foodType": {"type": "str"}
        }
    },
    "healthAdvice": {
        "optionalParams": {
            "age": {"type": "int"},
            "gender": {"type": "str"},
            "height": {"type": "int"},
            "weight": {"type": "int"},
            "BMI": {"type": "float"},
            "disease": {"type": "str"}
        }
    }
}
The task is:
"""
]
# Result Initialization Template DAG
MESSAGE_RESULT_DAG = [
    """{
	"healthAdvice": {
		"advice": {"type": "str"}
	},
	"calculateCalorie": {
		"foodName": {"type": "str"},
		"foodType": {"type": "str"},
		"calorie": {"type": "str"}
	},
	"recommendSports": {
		"sportName": {"type": "str"},
		"sportType": {"type": "str"}
	},
	"recommendFood": {
		"foodName": {"type": "str"},
		"foodType": {"type": "str"},
		"rating": {"type": "str"},
		"price": {"type": "str"}
	},
	"bookEvent": {
		"eventId": {"type": "str"},
		"eventName": {"type": "str"},
		"type": {"type": "str"},
		"city ": {"type": "str"},
		"location ": {"type": "str"},
		"startDate": {"type": "datetime"},
		"startTime": {"type": "str"},
		"eventStatus": {"type": "str"},
		"endDate": {"type": "datetime"},
		"endTime": {"type": "str"},
		"pricePerPeople": {"type": "float"},
		"peopleNumber": {"type": "date"},
		"totalPrice": {"type": "date"}
	},
	"countBudget": {
		"totalPrice": {"type": "float"}
	},
	"saveToMemo": {
		"startDate": {"type": "datetime"},
		"endDate": {"type": "datetime"},
		"cities": {"type": "str"},
		"specialtiesByCity": {"type": "str"},
		"hotelName": {"type": "str"},
		"hotelPrice": {"type": "float"},
		"restaurantName": {"type": "str"},
		"trainNumber": {"type": "str"},
		"trainPrice": {"type": "float"},
		"flightNumber": {"type": "str"},
		"flightPrice": {"type": "float"},
		"taxiPrice": {"type": "float"},
		"eventName": {"type": "str"},
		"eventPrice": {"type": "float"},
		"totalPrice": {"type": "float"},
		"BMI": {"type": "str"}
	},
	"searchEvents": {
		"result": {
			"type": "list",
			"items": {
				"eventId": {"type": "str"},
				"eventName": {"type": "str"},
				"type": {"type": "str"},
				"city ": {"type": "str"},
				"location ": {"type": "str"},
				"startDate": {"type": "datetime"},
				"startTime": {"type": "str"},
				"eventStatus": {"type": "str"},
				"endDate": {"type": "datetime"},
				"endTime": {"type": "str"},
				"pricePerPeople": {"type": "float"},
				"artist": {"type": "str"}
			}
		}
	},
	"calculateBMI": {
		"BMI": {"type": "float"},
		"healthStatus": {"type": "string"}
	},
	"getEnrollCourses": {
		"result": {
			"type": "list",
			"items": {
				"courseId": {"type": "str"},
				"courseName": {"type": "str"},
				"startDate": {"type": "datetime"},
				"endDate": {"type": "datetime"},
				"instructorName": {"type": "str"},
				"rating": {"type": "str"},
				"category": {"type": "str"},
				"level": {"type": "str"},
				"pay": {"type": "bool"},
				"coursePrice": {"type": "float"},
				"platform": {"type": "string"}
			}
		}
	},
	"enrollCourse": {
		"courseId": {"type": "str"},
		"courseName": {"type": "str"},
		"startDate": {"type": "datetime"},
		"endDate": {"type": "datetime"},
		"instructorName": {"type": "str"},
		"level": {"type": "str"},
		"userContactNumber": {"type": "str"}
	},
	"queryOnlineCourses": {
		"courseId": {"type": "str"},
		"courseName": {"type": "str"},
		"instructorName": {"type": "str"},
		"pay": {"type": "bool"},
		"coursePrice": {"type": "float"},
		"platform": {"type": "str"},
		"level": {"type": "str"},
		"startDate": {"type": "datetime"},
		"endDate": {"type": "datetime"},
		"rating": {"type": "str"},
		"supportingBooks": {"type": "str"}
	},
	"buyGood": {
		"status": {"type": "str"},
		"goodId": {"type": "str"},
		"quantity": {"type": "int"},
		"pricePerUnit": {"type": "float"},
		"promoCode": {"type": "str"},
		"shippingCost": {"type": "float"},
		"finalPrice": {"type": "float"},
		"platform": {"type": "str"},
		"paymentMethod": {"type": "str"},
		"contactNumber": {"type": "str"},
		"address": {"type": "str"}
	},
	"addToCart": {
		"result": {
			"type": "list",
			"items": {
				"goodId": {"type": "str"},
				"quantity": {"type": "int"},
				"goodName": {"type": "str"}
			}
		}
	},
	"compareCostEffectiveness": {
		"betterGoodId": {"type": "str"},
		"betterGoodName": {"type": "str"},
		"betterGoodPrice": {"type": "float"},
		"betterGoodRating": {"type": "float"}
	},
	"searchGoodsOnline": {
		"goodId": {"type": "str"},
		"goodName": {"type": "str"},
		"goodCategory": {"type": "str"},
		"singlePrice": {"type": "float"},
		"platform": {"type": "str"},
		"sameDayDelivery": {"type": "bool"},
		"brand": {"type": "str"},
		"freeShipping": {"type": "bool"},
		"shippingCost": {"type": "float"}
	},
	"queryWeather": {
		"weather": {"type": "str"},
		"date": {"type": "datetime"},
		"city": {"type": "str"},
		"minCelsius": {"type": "float"},
		"maxCelsius": {"type": "float"}
	},
	"getCitySpecialties": {
		"food": {"type": "str"},
		"foodType": {"type": "str"},
		"averagePriceOfFood": {"type": "str"},
		"calorie": {"type": "float"},
		"healthLevel": {"type": "int"}
	},
	"bookRestaurant": {
		"reservationDate": {"type": "datetime"},
		"reservationTime": {"type": "datetime"},
		"restaurantName": {"type": "str"},
		"restaurantType": {"type": "str"},
		"location": {"type": "str"},
		"userContactNumber": {"type": "str"},
		"peopleNumber": {"type": "int"},
		"providingFood": {"type": "str"},
		"specialRequests": {"type": "str"}
	},
	"bookHotel": {
		"hotelName": {"type": "str"},
		"location": {"type": "str"},
		"checkInDate": {"type": "datetime"},
		"checkInTime": {"type": "datetime"},
		"checkOutDate": {"type": "datetime"},
		"checkOutTime": {"type": "datetime"},
		"userContactNumber": {"type": "str"},
		"roomType": {"type": "str"},
		"numberOfRooms": {"type": "str"},
		"peopleNumber": {"type": "int"},
		"totalPrice": {"type": "str"},
		"specialRequests": {"type": "str"}
	},
	"queryFlights": {
		"result": {
			"type": "list",
			"items": {
				"flightNumber": {"type": "str"},
				"departureDate ": {"type": "datetime"},
				"departureTime": {"type": "datetime"},
				"arrivalDate ": {"type": "datetime"},
				"arrivalTime": {"type": "datetime"},
				"economyCabinClassPrice": {"type": "float"},
				"businessCabinClassPrice": {"type": "float"},
				"firstCabinClassPrice": {"type": "float"},
				"airline": {"type": "str"},
				"originAirport": {"type": "str"},
				"destinationAirport": {"type": "str"}
			}
		}
	},
	"bookFlight": {
		"flightNumber": {"type": "str"},
		"departureDate ": {"type": "datetime"},
		"departureTime": {"type": "datetime"},
		"arrivalDate ": {"type": "datetime"},
		"arrivalTime": {"type": "datetime"},
		"price": {"type": "float"},
		"originAirport": {"type": "str"},
		"destinationAirport": {"type": "str"},
		"airline": {"type": "str"},
		"userContactNumber": {"type": "str"}
	},
	"queryTrains": {
		"result": {
			"type": "list",
			"items": {
				"trainNumber": {"type": "str"},
				"departureDate ": {"type": "datetime"},
				"departureTime": {"type": "datetime"},
				"arrivalDate ": {"type": "datetime"},
				"arrivalTime": {"type": "datetime"},
				"firstClassPrice": {"type": "float"},
				"secondClassPrice": {"type": "float"},
				"trainType": {"type": "str"},
				"originStation": {"type": "str"},
				"destinationStation": {"type": "str"}
			}
		}
	},
	"bookTrain": {
		"trainNumber": {"type": "str"},
		"departureDate ": {"type": "datetime"},
		"departureTime": {"type": "datetime"},
		"arrivalDate ": {"type": "datetime"},
		"arrivalTime": {"type": "datetime"},
		"price": {"type": "float"},
		"originStation": {"type": "str"},
		"destinationStation": {"type": "str"},
		"trainType": {"type": "str"},
		"userContactNumber": {"type": "str"}
	},
	"bookTaxi": {
		"bookingId": {"type": "str"},
		"pickupAddress": {"type": "str"},
		"dropOffAddress": {"type": "str"},
		"pickupTime": {"type": "datetime"},
		"contactNumber": {"type": "str"},
		"driverContact": {"type": "str"},
		"carType": {"type": "str"},
		"price": {"type": "float"}
	}
}
"""
]

# Planner Initialization Template - Travel
MESSAGE_PLANNER_1_travel = [
    """Your tools are as follows:
OpenWeather	"{
  ""city"": {
    ""type"": ""str"",
    ""required"": true
  }
}"
BookingCOM	"{
  ""latitude"": {
    ""type"": ""String"",
    ""required"": true
  },
  ""longitude"": {
    ""type"": ""String"",
    ""required"": true
  },
  ""arrival_date"": {
    ""type"": ""Date (yyyy-mm-dd)"",
    ""required"": true
  },
  ""departure_date"": {
    ""type"": ""Date (yyyy-mm-dd)"",
    ""required"": true
  },
  ""radius"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""adults"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""children_age"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""room_qty"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""price_min"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""price_max"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""units"": {
    ""type"": ""Enum"",
    ""required"": false
  },
  ""page_number"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""temperature_unit"": {
    ""type"": ""Enum"",
    ""required"": false
  },
  ""languagecode"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""currency_code"": {
    ""type"": ""String"",
    ""required"": false
  }
}"
BookingLocationToLatLong	"{
  ""query"": {
    ""type"": ""String"",
    ""required"": true
  }
}"
AeroDataBox	"{
  ""flightTimeModel"": {
    ""type"": ""Enum"",
    ""required"": false
  },
  ""aircraftName"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""codeType"": {
    ""type"": ""Enum"",
    ""required"": false
  },
  ""codeTo"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""codeFrom"": {
    ""type"": ""String"",
    ""required"": false
  }
}"
Tripadvisor	"{
  ""location"": {
    ""type"": ""String"",
    ""required"": true
  },
  ""page"": {
    ""type"": ""Number"",
    ""required"": false
  }
}"
VacationsdetailsAPI	"{
  ""country_name"": {
    ""type"": ""String"",
    ""required"": true
  }
}"
AmadeusAPI	"{
  ""keyword"": {
    ""type"": ""String"",
    ""required"": true
  },
  ""subType"": {
    ""type"": ""String"",
    ""required"": true
  }
}"
FlightsScraperAPI	"{
  ""market"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""locale"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""currency"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""adults"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""children"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""infants"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""cabinClass"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""stops"": {
    ""type"": ""Array"",
    ""required"": false
  },
  ""sort"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""airlines"": {
    ""type"": ""Array"",
    ""required"": false
  },
  ""flights"": {
    ""type"": ""Array"",
    ""required"": false
  }
}"
GreatCircleMapper	"{
  ""icao_iata"": {
    ""type"": ""String"",
    ""required"": true
  }
}"
TouristAttraction	"{
  ""location"": {
    ""type"": ""String"",
    ""required"": true
  },
  ""language"": {
    ""type"": ""String"",
    ""required"": true
  },
  ""currency"": {
    ""type"": ""String"",
    ""required"": true
  },
  ""offset"": {
    ""type"": ""String"",
    ""required"": false
  }
}"
VisaRequirements	"{
  ""country"": {
    ""type"": ""str"",
    ""required"": true
  }
}"
CostOfLivingPrices	"{
  ""city"": {
    ""type"": ""str"",
    ""required"": true
  }
}"
The task is:
"""
]
# Result Initialization Template - Travel
MESSAGE_RESULT_1_travel = [
    """
Your tools response are as follows:
"OpenWeather:
{
  ""type"": ""object"",
  ""properties"": {
    ""coord"": {
      ""type"": ""object"",
      ""properties"": {
        ""lon"": {""type"": ""number""},
        ""lat"": {""type"": ""number""}
      }
    },
    ""weather"": {
      ""type"": ""array"",
      ""items"": {
        ""type"": ""object"",
        ""properties"": {
          ""id"": {""type"": ""integer""},
          ""main"": {""type"": ""string""},
          ""description"": {""type"": ""string""},
          ""icon"": {""type"": ""string""}
        }
      }
    },
    ""base"": {""type"": ""string""},
    ""main"": {
      ""type"": ""object"",
      ""properties"": {
        ""temp"": {""type"": ""number""},
        ""feels_like"": {""type"": ""number""},
        ""temp_min"": {""type"": ""number""},
        ""temp_max"": {""type"": ""number""},
        ""pressure"": {""type"": ""integer""},
        ""humidity"": {""type"": ""integer""}
      }
    },
    ""visibility"": {""type"": ""integer""},
    ""wind"": {
      ""type"": ""object"",
      ""properties"": {
        ""speed"": {""type"": ""number""},
        ""deg"": {""type"": ""integer""},
        ""gust"": {""type"": ""number""}
      }
    },
    ""clouds"": {
      ""type"": ""object"",
      ""properties"": {
        ""all"": {""type"": ""integer""}
      }
    },
    ""dt"": {""type"": ""integer""},
    ""sys"": {
      ""type"": ""object"",
      ""properties"": {
        ""type"": {""type"": ""integer""},
        ""id"": {""type"": ""integer""},
        ""country"": {""type"": ""string""},
        ""sunrise"": {""type"": ""integer""},
        ""sunset"": {""type"": ""integer""}
      }
    },
    ""timezone"": {""type"": ""integer""},
    ""id"": {""type"": ""integer""},
    ""name"": {""type"": ""string""},
    ""cod"": {""type"": ""integer""}
  }
}"
"BookingCOM:
{
  ""type"": ""object"",
  ""properties"": {
    ""status"": {""type"": ""boolean""},
    ""message"": {""type"": ""string""},
    ""timestamp"": {""type"": ""integer""},
    ""data"": {
      ""type"": ""object"",
      ""properties"": {
        ""count"": {""type"": ""integer""},
        ""result"": {
          ""type"": ""array"",
          ""items"": {
            ""type"": ""object"",
            ""properties"": {
              ""city"": {""type"": ""string""},
              ""hotel_name_trans"": {""type"": ""string""},
              ""countrycode"": {""type"": ""string""},
              ""review_score"": {""type"": ""number""},
              ""composite_price_breakdown"": {
                ""type"": ""object"",
                ""properties"": {
                  ""gross_amount_per_night"": {
                    ""type"": ""object"",
                    ""properties"": {
                      ""currency"": {""type"": ""string""},
                      ""value"": {""type"": ""number""}
                    }
                  }
                }
              },
              ""main_photo_url"": {""type"": ""string""}
            }
          }
        }
      }
    }
  }
}"
"BookingLocationToLatLong:
{
  ""status"": {""type"": ""boolean""},
  ""message"": {""type"": ""string""},
  ""timestamp"": {""type"": ""integer""},
  ""data"": [
    {
      ""business_status"": {""type"": ""string""},
      ""formatted_address"": {""type"": ""string""},
      ""geometry"": {
        ""type"": ""object"",
        ""properties"": {
               ""location"": {
                ""lat"": ""string"",
                ""lng"": ""string""
              }
        }
      },
      ""name"": {""type"": ""string""},
      ""opening_hours"": {
        ""type"": ""object"",
        ""properties"": {
          ""open_now"": {""type"": ""boolean""}
        }
      },
      ""photos"": [
        {
          ""height"": {""type"": ""integer""},
          ""html_attributions"": {
            ""type"": ""array"",
            ""items"": [
              {""type"": ""string""}
            ]
          },
          ""photo_reference"": {""type"": ""string""},
          ""width"": {""type"": ""integer""}
        }
      ],
      ""place_id"": {""type"": ""string""},
      ""plus_code"": {
        ""type"": ""object"",
        ""properties"": {
          ""compound_code"": {""type"": ""string""},
          ""global_code"": {""type"": ""string""}
        }
      },
      ""rating"": {""type"": ""number""},
      ""reference"": {""type"": ""string""},
      ""types"": {
        ""type"": ""array"",
        ""items"": [
          {""type"": ""string""}
        ]
      },
      ""user_ratings_total"": {""type"": ""integer""}
    }
  ]
}"
"AeroDataBox:
{
  ""type"": ""object"",
  ""properties"": {
    ""id"": {""type"": ""string""},
    ""isBlocked"": {""type"": ""boolean""}
  }
}"
"Tripadvisor:
{
  ""type"": ""object"",
  ""properties"": {
    ""status"": {""type"": ""boolean""},
    ""message"": {""type"": ""string""},
    ""timestamp"": {""type"": ""integer""},
    ""data"": {
      ""type"": ""object"",
      ""properties"": {
        ""totalRecords"": {""type"": ""string""},
        ""totalPages"": {""type"": ""integer""},
        ""data"": {
          ""type"": ""array"",
          ""items"": {
            ""type"": ""object"",
            ""properties"": {
              ""heroImgUrl"": {""type"": ""string""},
              ""heroImgRawHeight"": {""type"": ""integer""},
              ""heroImgRawWidth"": {""type"": ""integer""},
              ""squareImgUrl"": {""type"": ""string""},
              ""squareImgRawLength"": {""type"": ""integer""},
              ""locationId"": {""type"": ""integer""},
              ""name"": {""type"": ""string""},
              ""averageRating"": {""type"": ""number""},
              ""userReviewCount"": {""type"": ""integer""},
              ""currentOpenStatusCategory"": {""type"": ""string""},
              ""currentOpenStatusText"": {""type"": ""string""},
              ""establishmentTypeAndCuisineTags"": {
                ""type"": ""array"",
                ""items"": {""type"": ""string""}
              },
              ""priceTag"": {""type"": ""string""},
              ""offers"": {
                ""type"": ""object"",
                ""properties"": {
                  ""slot1Offer"": {""type"": [""object"", ""null""]},
                  ""slot2Offer"": {""type"": [""object"", ""null""]}
                }
              },
              ""hasMenu"": {""type"": ""boolean""},
              ""menuUrl"": {""type"": [""string"", ""null""]},
              ""isDifferentGeo"": {""type"": ""boolean""},
              ""parentGeoName"": {""type"": ""string""},
              ""distanceTo"": {""type"": ""string""},
              ""reviewSnippets"": {
                ""type"": ""object"",
                ""properties"": {
                  ""reviewSnippetsList"": {
                    ""type"": ""array"",
                    ""items"": {
                      ""type"": ""object"",
                      ""properties"": {
                        ""reviewText"": {""type"": ""string""},
                        ""reviewUrl"": {""type"": ""string""}
                      }
                    }
                  }
                }
              },
              ""awardInfo"": {""type"": [""object"", ""null""]},
              ""isLocalChefItem"": {""type"": ""boolean""},
              ""isPremium"": {""type"": ""boolean""},
              ""isStoryboardPublished"": {""type"": ""boolean""}
            }
          }
        }
      }
    }
  }
}"
"VacationsdetailsAPI:
{
  ""capital"": {""type"": ""string""},
  ""currency"": {""type"": ""string""},
  ""vacation"": {""type"": ""string""}
}"
"AmadeusAPI:
{
  ""data"": [
    {
      ""address"": {
        ""type"": ""object"",
        ""properties"": {
          ""cityCode"": {""type"": ""string""},
          ""cityName"": {""type"": ""string""},
          ""countryCode"": {""type"": ""string""},
          ""countryName"": {""type"": ""string""},
          ""regionCode"": {""type"": ""string""}
        }
      },
      ""analytics"": {
        ""type"": ""object"",
        ""properties"": {
          ""travelers"": {
            ""type"": ""object"",
            ""properties"": {
              ""score"": {""type"": ""integer""}
            }
          }
        }
      },
      ""detailedName"": {""type"": ""string""},
      ""geoCode"": {
        ""type"": ""object"",
        ""properties"": {
          ""latitude"": {""type"": ""number""},
          ""longitude"": {""type"": ""number""}
        }
      },
      ""iataCode"": {""type"": ""string""},
      ""id"": {""type"": ""string""},
      ""name"": {""type"": ""string""},
      ""self"": {
        ""type"": ""object"",
        ""properties"": {
          ""href"": {""type"": ""string""}
        }
      },
      ""methods"": {
        ""type"": ""array"",
        ""items"": [
          {""type"": ""string""}
        ]
      },
      ""subType"": {""type"": ""string""},
      ""timeZoneOffset"": {""type"": ""string""},
      ""type"": {""type"": ""string""}
    }
  ]
}"
"FlightsScraperAPI:
{
  ""type"": ""object"",
  ""properties"": {
    ""data"": {
      ""type"": ""object"",
      ""properties"": {
        ""context"": {
          ""type"": ""object"",
          ""properties"": {
            ""status"": {""type"": ""string""},
            ""sessionId"": {""type"": ""string""},
            ""totalResults"": {""type"": ""integer""}
          }
        },
        ""itineraries"": {
          ""type"": ""array"",
          ""items"": {""type"": ""object""}
        },
        ""messages"": {""type"": ""array""},
        ""filterStats"": {
          ""type"": ""object"",
          ""properties"": {
            ""duration"": {
              ""type"": ""object"",
              ""properties"": {
                ""min"": {""type"": ""integer""},
                ""max"": {""type"": ""integer""},
                ""multiCityMin"": {""type"": ""integer""},
                ""multiCityMax"": {""type"": ""integer""}
              }
            },
            ""airports"": {
              ""type"": ""array"",
              ""items"": {
                ""type"": ""object"",
                ""properties"": {
                  ""city"": {""type"": ""string""},
                  ""airports"": {
                    ""type"": ""array"",
                    ""items"": {
                      ""type"": ""object"",
                      ""properties"": {
                        ""id"": {""type"": ""string""},
                        ""name"": {""type"": ""string""}
                      }
                    }
                  }
                }
              }
            },
            ""carriers"": {
              ""type"": ""array"",
              ""items"": {
                ""type"": ""object"",
                ""properties"": {
                  ""id"": {""type"": ""integer""},
                  ""logoUrl"": {""type"": ""string""},
                  ""name"": {""type"": ""string""}
                }
              }
            },
            ""stopPrices"": {
              ""type"": ""object"",
              ""properties"": {
                ""direct"": {
                  ""type"": ""object"",
                  ""properties"": {
                    ""isPresent"": {""type"": ""boolean""}
                  }
                },
                ""one"": {
                  ""type"": ""object"",
                  ""properties"": {
                    ""isPresent"": {""type"": ""boolean""},
                    ""formattedPrice"": {""type"": ""string""}
                  }
                },
                ""twoOrMore"": {
                  ""type"": ""object"",
                  ""properties"": {
                    ""isPresent"": {""type"": ""boolean""},
                    ""formattedPrice"": {""type"": ""string""}
                  }
                }
              }
            }
          }
        },
        ""flightsSessionId"": {""type"": ""string""},
        ""destinationImageUrl"": {""type"": ""string""},
        ""token"": {""type"": ""string""}
      }
    },
    ""status"": {""type"": ""boolean""},
    ""message"": {""type"": ""string""}
  }
}"
"GreatCircleMapper:
{
  ""type"": ""object"",
  ""properties"": {
    ""data"": {
      ""type"": ""object"",
      ""properties"": {
        ""context"": {
          ""type"": ""object"",
          ""properties"": {
            ""status"": {""type"": ""string""},
            ""sessionId"": {""type"": ""string""},
            ""totalResults"": {""type"": ""integer""}
          }
        },
        ""itineraries"": {
          ""type"": ""array"",
          ""items"": {""type"": ""object""}
        },
        ""messages"": {""type"": ""array""},
        ""filterStats"": {
          ""type"": ""object"",
          ""properties"": {
            ""duration"": {
              ""type"": ""object"",
              ""properties"": {
                ""min"": {""type"": ""integer""},
                ""max"": {""type"": ""integer""},
                ""multiCityMin"": {""type"": ""integer""},
                ""multiCityMax"": {""type"": ""integer""}
              }
            },
            ""airports"": {
              ""type"": ""array"",
              ""items"": {
                ""type"": ""object"",
                ""properties"": {
                  ""city"": {""type"": ""string""},
                  ""airports"": {
                    ""type"": ""array"",
                    ""items"": {
                      ""type"": ""object"",
                      ""properties"": {
                        ""id"": {""type"": ""string""},
                        ""name"": {""type"": ""string""}
                      }
                    }
                  }
                }
              }
            },
            ""carriers"": {
              ""type"": ""array"",
              ""items"": {
                ""type"": ""object"",
                ""properties"": {
                  ""id"": {""type"": ""integer""},
                  ""logoUrl"": {""type"": ""string""},
                  ""name"": {""type"": ""string""}
                }
              }
            },
            ""stopPrices"": {
              ""type"": ""object"",
              ""properties"": {
                ""direct"": {
                  ""type"": ""object"",
                  ""properties"": {
                    ""isPresent"": {""type"": ""boolean""}
                  }
                },
                ""one"": {
                  ""type"": ""object"",
                  ""properties"": {
                    ""isPresent"": {""type"": ""boolean""},
                    ""formattedPrice"": {""type"": ""string""}
                  }
                },
                ""twoOrMore"": {
                  ""type"": ""object"",
                  ""properties"": {
                    ""isPresent"": {""type"": ""boolean""},
                    ""formattedPrice"": {""type"": ""string""}
                  }
                }
              }
            }
          }
        },
        ""flightsSessionId"": {""type"": ""string""},
        ""destinationImageUrl"": {""type"": ""string""},
        ""token"": {""type"": ""string""}
      }
    },
    ""status"": {""type"": ""boolean""},
    ""message"": {""type"": ""string""}
  }
}"
"TouristAttraction:
{
  ""type"": ""object"",
  ""properties"": {
    ""images"": {
      ""type"": ""object"",
      ""properties"": {
        ""small"": {
          ""type"": ""object"",
          ""properties"": {
            ""width"": {""type"": ""string""},
            ""url"": {""type"": ""string""},
            ""height"": {""type"": ""string""}
          }
        },
        ""thumbnail"": {
          ""type"": ""object"",
          ""properties"": {
            ""width"": {""type"": ""string""},
            ""url"": {""type"": ""string""},
            ""height"": {""type"": ""string""}
          }
        },
        ""original"": {
          ""type"": ""object"",
          ""properties"": {
            ""width"": {""type"": ""string""},
            ""url"": {""type"": ""string""},
            ""height"": {""type"": ""string""}
          }
        },
        ""large"": {
          ""type"": ""object"",
          ""properties"": {
            ""width"": {""type"": ""string""},
            ""url"": {""type"": ""string""},
            ""height"": {""type"": ""string""}
          }
        },
        ""medium"": {
          ""type"": ""object"",
          ""properties"": {
            ""width"": {""type"": ""string""},
            ""url"": {""type"": ""string""},
            ""height"": {""type"": ""string""}
          }
        }
      }
    },
    ""is_blessed"": {""type"": ""boolean""},
    ""uploaded_date"": {""type"": ""string""},
    ""caption"": {""type"": ""string""},
    ""linked_reviews"": {""type"": ""integer""},
    ""id"": {""type"": ""string""},
    ""lang"": {""type"": ""string""},
    ""location_id"": {""type"": ""string""},
    ""published_date"": {""type"": ""string""},
    ""published_platform"": {""type"": ""string""},
    ""rating"": {""type"": ""string""},
    ""type"": {""type"": ""string""},
    ""helpful_votes"": {""type"": ""string""},
    ""url"": {""type"": ""string""},
    ""travel_date"": {""type"": [""string"", ""null""]},
    ""text"": {""type"": [""string"", ""null""]},
    ""user"": {
      ""type"": [""object"", ""null""],
      ""properties"": {
        ""user_id"": {""type"": ""string""},
        ""type"": {""type"": ""string""},
        ""first_name"": {""type"": ""string""},
        ""last_initial"": {""type"": ""string""},
        ""name"": {""type"": ""string""},
        ""member_id"": {""type"": ""string""},
        ""username"": {""type"": ""string""},
        ""user_location"": {""type"": ""string""},
        ""avatar"": {
          ""type"": ""object"",
          ""properties"": {
            ""small"": {
              ""type"": ""object"",
              ""properties"": {""url"": {""type"": ""string""}}
            },
            ""large"": {
              ""type"": ""object"",
              ""properties"": {""url"": {""type"": ""string""}}
            }
          }
        },
        ""link"": {""type"": ""string""},
        ""points"": {""type"": ""string""},
        ""created_time"": {""type"": ""string""},
        ""locale"": {""type"": ""string""}
      }
    },
    ""title"": {""type"": ""string""},
    ""owner_response"": {""type"": [""string"", ""null""]},
    ""subratings"": {""type"": ""object""},
    ""machine_translated"": {""type"": ""boolean""},
    ""machine_translatable"": {""type"": ""boolean""},
    ""locations"": {""type"": ""integer""},
    ""name"": {""type"": ""string""}
  }
}"
"VisaRequirements:
{
  ""type"": ""array"",
  ""items"": {""type"": ""string""}
}"
"CostOfLivingPrices:
{
  ""city_id"": {""type"": ""integer""},
  ""city_name"": {""type"": ""string""},
  ""state_code"": {""type"": ""null""},
  ""country_name"": {""type"": ""string""},
  ""exchange_rate"": {
    ""type"": ""object"",
    ""properties"": {
      ""EUR"": {""type"": ""number""},
      ""AUD"": {""type"": ""number""},
      ""USD"": {""type"": ""number""},
      ""CAD"": {""type"": ""number""},
      ""CNY"": {""type"": ""number""},
      ""CZK"": {""type"": ""number""},
      ""DKK"": {""type"": ""number""},
      ""GBP"": {""type"": ""number""},
      ""HKD"": {""type"": ""number""},
      ""JPY"": {""type"": ""number""},
      ""NZD"": {""type"": ""number""},
      ""NOK"": {""type"": ""number""},
      ""RUB"": {""type"": ""number""},
      ""KRW"": {""type"": ""number""},
      ""CHF"": {""type"": ""number""},
      ""UAH"": {""type"": ""number""},
      ""SEK"": {""type"": ""number""}
    }
  },
  ""exchange_rates_updated"": {
    ""type"": ""object"",
    ""properties"": {
      ""date"": {""type"": ""string""},
      ""timestamp"": {""type"": ""integer""}
    }
  },
  ""prices"": [
    {
      ""good_id"": {""type"": ""integer""},
      ""item_name"": {""type"": ""string""},
      ""category_id"": {""type"": ""integer""},
      ""category_name"": {""type"": ""string""},
      ""min"": {""type"": ""number""},
      ""avg"": {""type"": ""number""},
      ""max"": {""type"": ""number""},
      ""usd"": {
        ""type"": ""object"",
        ""properties"": {
          ""min"": {""type"": ""string""},
          ""avg"": {""type"": ""string""},
          ""max"": {""type"": ""string""}
        }
      },
      ""measure"": {""type"": ""string""},
      ""currency_code"": {""type"": ""string""}
    }
  ]
}"
"""
]
# Planner Initialization Template - Entertainment
MESSAGE_PLANNER_2_entertainment = [
    """Your tools are as follows:
YouTubeDataAPI	"{
  ""q"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""hl"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""gl"": {
    ""type"": ""str"",
    ""required"": false
  }
}"
YoutubeSearchAndDownload	"{
  ""channelId"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""lang"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""type"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""sortBy"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""nextToken"": {
    ""type"": ""str"",
    ""required"": false
  }
}"
SpotifyDownloader	"{
  ""search"": {
    ""type"": ""str"",
    ""required"": true
  }
}"
IMDBAPI	"{
  ""query"": {
    ""type"": ""str"",
    ""required"": true
  }
}"
uNoGSAPI	"{
  ""end_rating"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""country_list"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""start_year"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""person"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""offset"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""order_by"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""limit"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""end_year"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""top250"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""start_rating"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""new_date"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""top250tv"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""title"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""expiring"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""subtitle"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""type"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""genre_list"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""audio"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""audio_sub_andor"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""country_andorunique"": {
    ""type"": ""String"",
    ""required"": false
  }
}"
MyAnimeListAPI	"{
  ""q"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""n"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""score"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""genre"": {
    ""type"": ""String"",
    ""required"": false
  }
}"
The task is:
"""
]
# Result Initialization Template - Entertainment
MESSAGE_RESULT_2_entertainment = [
    """
Your tools response are as follows:
"YouTubeDataAPI:
{
  ""type"": ""object"",
  ""properties"": {
    ""query"": {""type"": ""string""},
    ""results"": {
      ""type"": ""array"",
      ""items"": {""type"": ""string""}
    }
  }
}"
"YoutubeSearchAndDownload:
{
  ""avatar"": {
    ""type"": ""object"",
    ""properties"": {
      ""thumbnails"": {
        ""type"": ""array"",
        ""items"": {""type"": ""object""}
      }
    }
  },
  ""country"": {""type"": ""string""},
  ""description"": {""type"": ""string""},
  ""joinedDateText"": {""type"": ""string""},
  ""subscriberCountText"": {""type"": ""string""},
  ""title"": {""type"": ""string""},
  ""vanityChannelUrl"": {""type"": ""string""},
  ""verified"": {""type"": ""boolean""},
  ""viewCountText"": {""type"": ""string""}
}"
"SpotifyDownloader:
{
  ""type"": ""object"",
  ""properties"": {
    ""success"": {""type"": ""boolean""},
    ""data"": {
      ""type"": ""object"",
      ""properties"": {
        ""albumDetails"": {
          ""type"": ""object"",
          ""properties"": {
            ""artist"": {""type"": ""string""},
            ""title"": {""type"": ""string""},
            ""cover"": {""type"": ""string""},
            ""releaseDate"": {""type"": ""string""}
          }
        },
        ""count"": {""type"": ""integer""},
        ""songs"": {
          ""type"": ""array"",
          ""items"": {
            ""type"": ""object"",
            ""properties"": {
              ""id"": {""type"": ""string""},
              ""artist"": {""type"": ""string""},
              ""title"": {""type"": ""string""},
              ""album"": {""type"": ""string""},
              ""cover"": {""type"": ""string""},
              ""releaseDate"": {""type"": ""string""},
              ""downloadLink"": {""type"": ""string""}
            }
          }
        }
      }
    },
    ""generatedTimeStamp"": {""type"": ""integer""}
  }
}"
"IMDBAPI:
{
  ""d"": {
    ""type"": ""array"",
    ""items"": [
      {
        ""type"": ""object"",
        ""properties"": {
          ""id"": {""type"": ""string""},
          ""l"": {""type"": ""string""},
          ""q"": {""type"": ""string""},
          ""rank"": {""type"": ""string""},
          ""s"": {""type"": ""string""},
          ""v"": {
            ""type"": ""array"",
            ""items"": [
              {
                ""type"": ""object"",
                ""properties"": {
                  ""id"": {""type"": ""string""},
                  ""l"": {""type"": ""string""},
                  ""s"": {""type"": ""string""}
                }
              }
            ]
          },
          ""vt"": {""type"": ""string""},
          ""y"": {""type"": ""string""},
          ""yr"": {""type"": ""string""}
        }
      }
    ]
  }
}"
"uNoGSAPI:
{
  ""type"": ""object"",
  ""properties"": {
    ""results"": {
      ""type"": ""array"",
      ""items"": {
        ""type"": ""object"",
        ""properties"": {
          ""country"": {""type"": ""string""},
          ""countrycode"": {""type"": ""string""},
          ""expiring"": {""type"": ""integer""},
          ""id"": {""type"": ""integer""},
          ""nl7"": {""type"": ""integer""},
          ""tmovs"": {""type"": ""integer""},
          ""tseries"": {""type"": ""integer""},
          ""tvids"": {""type"": ""integer""}
        }
      }
    }
  }
}"
"MyAnimeListAPI:
{
  ""type"": ""array"",
  ""items"": {
    ""type"": ""object"",
    ""properties"": {
      ""title"": {""type"": ""string""},
      ""amount"": {""type"": ""integer""},
      ""id"": {""type"": ""integer""}
    }
  }
}"
"""
]
# Planner Initialization Template - Shopping
MESSAGE_PLANNER_3_shopping = [
    """Your tools are as follows:
RealTimeAmazonData	"{
  ""country"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""offset"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""categories"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""min_product_star_rating"": {
    ""type"": ""Enum"",
    ""required"": false
  },
  ""price_range"": {
    ""type"": ""Enum"",
    ""required"": false
  },
  ""discount_range"": {
    ""type"": ""Enum"",
    ""required"": false
  },
  ""brands"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""prime_early_access"": {
    ""type"": ""Boolean"",
    ""required"": false
  },
  ""prime_exclusive"": {
    ""type"": ""Boolean"",
    ""required"": false
  },
  ""fields"": {
    ""type"": ""String"",
    ""required"": false
  }
}"
RealTimeProductSearch	"{
  ""q"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""language"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""page"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""limit"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""sort_by"": {
    ""type"": ""Enum"",
    ""required"": false
  },
  ""min_price"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""max_price"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""product_condition"": {
    ""type"": ""Enum"",
    ""required"": false
  },
  ""stores"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""free_returns"": {
    ""type"": ""Boolean"",
    ""required"": false
  },
  ""free_shipping"": {
    ""type"": ""Boolean"",
    ""required"": false
  },
  ""on_sale"": {
    ""type"": ""Boolean"",
    ""required"": false
  }
}"
AliexpressDataHub	"{
  ""q"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""page"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""sort"": {
    ""type"": ""Enum"",
    ""required"": false
  },
  ""catld"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""brandld"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""oc"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""attr"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""startPrice"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""endPrice"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""locale"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""region"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""currency"": {
    ""type"": ""str"",
    ""required"": false
  }
}"
ShopeeEcommerceData	"{
  ""site"": {
    ""type"": ""Enum"",
    ""required"": false
  },
  ""keyword"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""by"": {
    ""type"": ""Enum"",
    ""required"": false
  },
  ""order"": {
    ""type"": ""Enum"",
    ""required"": false
  },
  ""page"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""pageSize"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""cat_ids"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""price_start"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""price_end"": {
    ""type"": ""String"",
    ""required"": false
  }
}"
1688DataHub	"{
  ""q"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""catId"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""page"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""pageSize"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""startPrice"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""endPrice"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""sort"": {
    ""type"": ""Enum"",
    ""required"": false
  },
  ""switches"": {
    ""type"": ""String"",
    ""required"": false
  }
}"
TaobaoAdvanced	"{
  ""query"": {
    ""type"": ""String"",
    ""required"": true
  }
}"
WalmartAPI	"{
  ""query"": {
    ""type"": ""str"",
    ""required"": true
  }
}"
TrackingPackage	"{
  ""tracking_number"": {
    ""type"": ""str"",
    ""required"": true
  }
}"
CheapTrackingStatus	"{
  ""trackingCode"": {
    ""type"": ""str"",
    ""required"": true
  }
}"
PurchasefromplatformAPI	"{
  ""platformName"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""productID"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""address"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""quantity"": {
    ""type"": ""int"",
    ""required"": true
  }
}"
eBayAverageSellingPrice	"{
  ""keywords"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""max_search_results"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""excluded_keywords"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""category_id"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""remove_outliers"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""site_id"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""max_pages"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""aspects"": {
    ""type"": ""list"",
    ""required"": false
  }
}"
The task is:
"""
]
# Result Initialization Template - Shopping
MESSAGE_RESULT_3_shopping = [
    """
Your tools response are as follows:
"RealTimeAmazonData:
{
  ""type"": ""object"",
  ""properties"": {
    ""status"": {""type"": ""string""},
    ""request_id"": {""type"": ""string""},
    ""data"": {
      ""type"": ""array"",
      ""items"": {
        ""type"": ""object"",
        ""properties"": {
          ""id"": {""type"": ""string""},
          ""name"": {""type"": ""string""}
        }
      }
    }
  }
}"
"RealTimeProductSearch:
{
  ""type"": ""object"",
  ""properties"": {
    ""status"": {""type"": ""string""},
    ""request_id"": {""type"": ""string""},
    ""data"": {
      ""type"": ""object"",
      ""properties"": {
        ""products"": {
          ""type"": ""array"",
          ""items"": {""type"": ""object""}
        },
        ""sponsored_products"": {
          ""type"": ""array"",
          ""items"": {
            ""type"": ""object"",
            ""properties"": {
              ""offer_id"": {""type"": ""string""},
              ""offer_page_url"": {""type"": ""string""},
              ""title"": {""type"": ""string""},
              ""photo"": {""type"": ""string""},
              ""merchant_id"": {""type"": ""string""},
              ""store_name"": {""type"": ""string""}
            }
          }
        }
      }
    }
  }
}"
"ShopeeEcommerceData:
{
  ""type"": ""object"",
  ""properties"": {
    ""code"": {""type"": ""integer""},
    ""msg"": {""type"": ""string""},
    ""data"": {
      ""type"": ""object"",
      ""properties"": {
        ""item_id"": {""type"": ""string""},
        ""shop_id"": {""type"": ""string""},
        ""site"": {""type"": ""string""},
        ""page"": {""type"": ""integer""},
        ""page_size"": {""type"": ""integer""},
        ""rate_filter"": {""type"": ""string""},
        ""rate_star"": {""type"": ""string""},
        ""total_count"": {""type"": ""integer""},
        ""has_next_page"": {""type"": ""boolean""},
        ""ratings"": {
          ""type"": ""array"",
          ""items"": {
            ""type"": ""object"",
            ""properties"": {
              ""anonymous"": {""type"": ""boolean""},
              ""author_username"": {""type"": ""string""},
              ""author_userid"": {""type"": ""string""},
              ""comment"": {""type"": ""string""},
              ""ctime"": {""type"": ""integer""},
              ""is_hidden"": {""type"": ""boolean""},
              ""is_repeated_purchase"": {""type"": ""boolean""},
              ""like_count"": {""type"": [""integer"", ""null""]},
              ""order_id"": {""type"": ""string""},
              ""rating_star"": {""type"": ""integer""},
              ""rating_star_detail"": {
                ""type"": ""object"",
                ""properties"": {
                  ""product_quality"": {""type"": ""integer""}
                }
              },
              ""rating_imgs"": {
                ""type"": ""array"",
                ""items"": {""type"": ""string""}
              },
              ""rating_videos"": {
                ""type"": ""array"",
                ""items"": {""type"": ""string""}
              },
              ""status"": {""type"": ""integer""}
            }
          }
        }
      }
    }
  }
}"
"1688DataHub:
{
  ""type"": ""object"",
  ""properties"": {
    ""result"": {
      ""type"": ""object"",
      ""properties"": {
        ""status"": {
          ""type"": ""object"",
          ""properties"": {
            ""data"": {""type"": ""string""},
            ""code"": {""type"": ""integer""},
            ""executionTime"": {""type"": ""string""},
            ""load_average"": {""type"": ""string""},
            ""peak_memory_usage"": {""type"": ""integer""},
            ""memory_usage"": {""type"": ""integer""},
            ""requestId"": {""type"": ""string""},
            ""endpoint"": {""type"": ""string""}
          }
        },
        ""settings"": {
          ""type"": ""object"",
          ""properties"": {
            ""locale"": {""type"": ""string""},
            ""currency"": {""type"": ""string""},
            ""page"": {""type"": ""string""},
            ""pageSize"": {""type"": ""string""},
            ""startPrice"": {""type"": ""string""},
            ""endPrice"": {""type"": ""string""},
            ""q"": {""type"": ""string""},
            ""sort"": {""type"": ""string""}
          }
        },
        ""base"": {
          ""type"": ""object"",
          ""properties"": {
            ""totalResults"": {""type"": ""string""},
            ""list"": {
              ""type"": ""array"",
              ""items"": {
                ""type"": ""object"",
                ""properties"": {
                  ""itemId"": {""type"": ""string""},
                  ""title"": {""type"": ""string""},
                  ""rootCatId"": {""type"": ""string""},
                  ""sales"": {""type"": ""string""},
                  ""itemUrl"": {""type"": ""string""},
                  ""image"": {""type"": ""string""},
                  ""sku"": {
                    ""type"": ""object"",
                    ""properties"": {
                      ""def"": {
                        ""type"": ""object"",
                        ""properties"": {
                          ""quantity"": {""type"": ""string""},
                          ""price"": {""type"": ""string""},
                          ""minOrder"": {""type"": ""string""},
                          ""unit"": {""type"": ""string""}
                        }
                      },
                      ""rangePrice"": {
                        ""type"": ""array"",
                        ""items"": {
                          ""type"": ""object"",
                          ""properties"": {
                            ""quantity"": {""type"": ""string""},
                            ""value"": {""type"": ""string""}
                          }
                        }
                      }
                    }
                  },
                  ""delivery"": {
                    ""type"": ""object"",
                    ""properties"": {
                      ""shipsFrom"": {""type"": ""string""},
                      ""shipWeight"": {""type"": ""string""},
                      ""shipID"": {""type"": ""string""},
                      ""freeShipping"": {""type"": ""boolean""}
                    }
                  },
                  ""service"": {
                    ""type"": ""array"",
                    ""items"": {
                      ""type"": ""object"",
                      ""properties"": {
                        ""title"": {""type"": ""string""}
                      }
                    }
                  },
                  ""seller"": {
                    ""type"": ""object"",
                    ""properties"": {
                      ""sellerId"": {""type"": ""string""},
                      ""sellerTitle"": {""type"": ""string""},
                      ""storeTitle"": {""type"": ""string""},
                      ""storeId"": {""type"": ""string""},
                      ""storeType"": {""type"": ""string""}
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}"
"TaobaoAdvanced:
{
  ""type"": ""object"",
  ""properties"": {
    ""result"": {
      ""type"": ""object"",
      ""properties"": {
        ""status"": {
          ""type"": ""object"",
          ""properties"": {
            ""data"": {""type"": ""string""},
            ""code"": {""type"": ""integer""},
            ""executionTime"": {""type"": ""string""},
            ""load_average"": {""type"": ""string""},
            ""peak_memory_usage"": {""type"": ""integer""},
            ""memory_usage"": {""type"": ""integer""},
            ""requestId"": {""type"": ""string""},
            ""endpoint"": {""type"": ""string""}
          }
        },
        ""settings"": {
          ""type"": ""object"",
          ""properties"": {
            ""locale"": {""type"": ""string""},
            ""currency"": {""type"": ""string""},
            ""page"": {""type"": ""string""},
            ""pageSize"": {""type"": ""string""},
            ""startPrice"": {""type"": ""string""},
            ""endPrice"": {""type"": ""string""},
            ""q"": {""type"": ""string""},
            ""sort"": {""type"": ""string""}
          }
        },
        ""base"": {
          ""type"": ""object"",
          ""properties"": {
            ""totalResults"": {""type"": ""string""},
            ""list"": {
              ""type"": ""array"",
              ""items"": {
                ""type"": ""object"",
                ""properties"": {
                  ""itemId"": {""type"": ""string""},
                  ""title"": {""type"": ""string""},
                  ""rootCatId"": {""type"": ""string""},
                  ""sales"": {""type"": ""string""},
                  ""itemUrl"": {""type"": ""string""},
                  ""image"": {""type"": ""string""},
                  ""sku"": {
                    ""type"": ""object"",
                    ""properties"": {
                      ""def"": {
                        ""type"": ""object"",
                        ""properties"": {
                          ""quantity"": {""type"": ""string""},
                          ""price"": {""type"": ""string""},
                          ""minOrder"": {""type"": ""string""},
                          ""unit"": {""type"": ""string""}
                        }
                      },
                      ""rangePrice"": {
                        ""type"": ""array"",
                        ""items"": {
                          ""type"": ""object"",
                          ""properties"": {
                            ""quantity"": {""type"": ""string""},
                            ""value"": {""type"": ""string""}
                          }
                        }
                      }
                    }
                  },
                  ""delivery"": {
                    ""type"": ""object"",
                    ""properties"": {
                      ""shipsFrom"": {""type"": ""string""},
                      ""shipWeight"": {""type"": ""string""},
                      ""freeShipping"": {""type"": ""boolean""}
                    }
                  },
                  ""service"": {
                    ""type"": ""array"",
                    ""items"": {
                      ""type"": ""object"",
                      ""properties"": {
                        ""title"": {""type"": ""string""}
                      }
                    }
                  },
                  ""seller"": {
                    ""type"": ""object"",
                    ""properties"": {
                      ""sellerId"": {""type"": ""string""},
                      ""sellerTitle"": {""type"": ""string""},
                      ""storeTitle"": {""type"": ""string""},
                      ""storeId"": {""type"": ""string""},
                      ""storeType"": {""type"": ""string""}
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}"
"WalmartAPI:
{
  ""properties"": {
    ""brand"": {""type"": ""string""},
    ""bundleType"": {""type"": ""string""},
    ""canonicalUrl"": {""type"": ""string""},
    ""category"": {""type"": ""string""},
    ""classType"": {""type"": ""string""},
    ""detailedDescription"": {""type"": ""string""},
    ""imageList"": {
      ""items"": {
        ""properties"": {
          ""assetId"": {""type"": ""string""},
          ""imageAssetSizeUrls"": {
            ""properties"": {
              ""default"": {""type"": ""string""}
            },
            ""type"": ""object""
          },
          ""rank"": {""type"": ""integer""},
          ""type"": {""type"": ""string""}
        },
        ""type"": ""object""
      },
      ""type"": ""array""
    },
    ""manufacturerName"": {""type"": ""string""},
    ""manufacturerProductId"": {""type"": ""string""},
    ""model"": {""type"": ""string""},
    ""offerCount"": {""type"": ""integer""},
    ""offerList"": {
      ""items"": {""type"": ""object""},
      ""type"": ""array""
    },
    ""primaryProductId"": {""type"": ""string""},
    ""primaryShelfId"": {""type"": ""string""},
    ""productId"": {""type"": ""string""},
    ""productName"": {""type"": ""string""},
    ""productSegment"": {""type"": ""string""},
    ""productType"": {""type"": ""string""},
    ""regularItem"": {""type"": ""boolean""},
    ""sellerList"": {
      ""items"": {
        ""properties"": {
          ""aboutUsText"": {""type"": ""string""},
          ""catalogSellerId"": {""type"": ""string""},
          ""customerServiceText"": {""type"": ""string""},
          ""privacyPolicyText"": {""type"": ""string""},
          ""returnPolicyText"": {""type"": ""string""},
          ""sellerDisplayName"": {""type"": ""string""},
          ""sellerEmail"": {""type"": ""string""},
          ""sellerEscalationEmail"": {""type"": ""string""},
          ""sellerId"": {""type"": ""string""},
          ""sellerLogoUrl"": {""type"": ""string""},
          ""sellerName"": {""type"": ""string""},
          ""sellerPhone"": {""type"": ""string""},
          ""sellerType"": {""type"": ""string""},
          ""shippingInfoText"": {""type"": ""string""},
          ""taxPolicyText"": {""type"": ""string""}
        },
        ""type"": ""object""
      },
      ""type"": ""array""
    },
    ""shortDescription"": {""type"": ""string""},
    ""specialityGiftCard"": {""type"": ""boolean""},
    ""transactableOfferCount"": {""type"": ""integer""},
    ""upc"": {""type"": ""null""},
    ""usItemId"": {""type"": ""string""},
    ""walmartEGiftCard"": {""type"": ""boolean""},
    ""walmartGiftCard"": {""type"": ""boolean""},
    ""walmartItemNumber"": {""type"": ""null""}
  },
  ""type"": ""object""
}"
"TrackingPackage:
{
  ""TrackingNumber"": {""type"": ""string""},
  ""Delivered"": {""type"": ""boolean""},
  ""Carrier"": {""type"": ""string""},
  ""ServiceType"": {""type"": ""string""},
  ""PickupDate"": {""type"": ""string""},
  ""ScheduledDeliveryDate"": {""type"": ""string""},
  ""ScheduledDeliveryDateInDateTimeFromat"": {""type"": ""null""},
  ""StatusCode"": {""type"": ""string""},
  ""Status"": {""type"": ""string""},
  ""StatusSummary"": {""type"": ""string""},
  ""Message"": {""type"": ""string""},
  ""DeliveredDateTime"": {""type"": ""string""},
  ""DeliveredDateTimeInDateTimeFormat"": {""type"": ""null""},
  ""SignatureName"": {""type"": ""string""},
  ""DestinationCity"": {""type"": ""string""},
  ""DestinationState"": {""type"": ""string""},
  ""DestinationZip"": {""type"": ""string""},
  ""DestinationCountry"": {""type"": ""null""},
  ""TrackingDetails"": {
    ""type"": ""array"",
    ""items"": []
  }
}"
"CheapTrackingStatus:
{
  ""TrackingNumber"": {""type"": ""string""},
  ""Delivered"": {""type"": ""boolean""},
  ""Carrier"": {""type"": ""string""},
  ""ServiceType"": {""type"": ""string""},
  ""PickupDate"": {""type"": ""string""},
  ""ScheduledDeliveryDate"": {""type"": ""string""},
  ""ScheduledDeliveryDateInDateTimeFromat"": {""type"": ""null""},
  ""StatusCode"": {""type"": ""string""},
  ""Status"": {""type"": ""string""},
  ""StatusSummary"": {""type"": ""string""},
  ""Message"": {""type"": ""string""},
  ""DeliveredDateTime"": {""type"": ""string""},
  ""DeliveredDateTimeInDateTimeFormat"": {""type"": ""null""},
  ""SignatureName"": {""type"": ""string""},
  ""DestinationCity"": {""type"": ""string""},
  ""DestinationState"": {""type"": ""string""},
  ""DestinationZip"": {""type"": ""string""},
  ""DestinationCountry"": {""type"": ""null""},
  ""TrackingDetails"": {
    ""type"": ""array"",
    ""items"": []
  }
}"
"PurchasefromplatformAPI:
{
  ""success"": {
    ""type"": ""bool"",
    ""required"": true
  },
  ""shippingID"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""orderID"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""errorMessage"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""expectedDeliveryDate"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""totalAmount"": {
    ""type"": ""float"",
    ""required"": true
  },
  ""paymentStatus"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""paymentMethod"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""orderDetails"": {
    ""type"": ""object"",
    ""required"": true,
    ""properties"": {
      ""productName"": {
        ""type"": ""str"",
        ""required"": true
      },
      ""unitPrice"": {
        ""type"": ""float"",
        ""required"": true
      },
      ""quantity"": {
        ""type"": ""int"",
        ""required"": true
      },
      ""totalPrice"": {
        ""type"": ""float"",
        ""required"": true
      }
    }
  }
}"
"eBayAverageSellingPrice:
{
  ""warning"": {""type"": ""null""},
  ""success"": {""type"": ""boolean""},
  ""average_price"": {""type"": ""string""},
  ""median_price"": {""type"": ""string""},
  ""min_price"": {""type"": ""string""},
  ""max_price"": {""type"": ""string""},
  ""results"": {""type"": ""string""},
  ""total_results"": {""type"": ""string""},
  ""pages_included"": {""type"": ""string""},
  ""products"": {
    ""type"": ""array"",
    ""items"": {
      ""type"": ""object"",
      ""properties"": {
        ""title"": {""type"": ""string""},
        ""sale_price"": {""type"": ""string""},
        ""condition"": {""type"": ""string""},
        ""buying_format"": {""type"": ""string""},
        ""date_sold"": {""type"": ""string""},
        ""image_url"": {""type"": ""string""},
        ""shipping_price"": {""type"": ""string""},
        ""link"": {""type"": ""string""},
        ""item_id"": {""type"": ""string""}
      }
    }
  }
}"
"""
]
# Planner Initialization Template - Education
MESSAGE_PLANNER_4_edu = [
    """Your tools are as follows:
GetBooksInfo	"{
  ""Query"": {
    ""type"": ""str"",
    ""required"": true
  }
}"
ArxivJSON	"{
  ""authors"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""keywords"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""sort_by"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""sort_order"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""start"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""max_results"": {
    ""type"": ""Number"",
    ""required"": false
  }
}"
ArxivGPT	"{
  ""paper_id"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""max_pages"": {
    ""type"": ""Number"",
    ""required"": false
  }
}"
Photomath	"{
  ""locale"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""image"": {
    ""type"": ""binary"",
    ""required"": false
  }
}"
TEDTalksAPI	"{
  ""id"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""from_record_date"": {
    ""type"": ""Date"",
    ""required"": false
  },
  ""to_record_date"": {
    ""type"": ""Date"",
    ""required"": false
  },
  ""record_date"": {
    ""type"": ""Date"",
    ""required"": false
  },
  ""from_publish_date"": {
    ""type"": ""Date"",
    ""required"": false
  },
  ""to_publish_date"": {
    ""type"": ""Date"",
    ""required"": false
  },
  ""publish_date"": {
    ""type"": ""Date"",
    ""required"": false
  },
  ""min_duration"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""max_duration"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""audio_lang"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""subtitle_lang"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""speaker"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""topic"": {
    ""type"": ""String"",
    ""required"": false
  }
}"
UniversityCollegeListRankings	{}
UdemyPaidCoursesForFree	"{
  ""page"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""page_size"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""query"": {
    ""type"": ""str"",
    ""required"": true
  }
}"
PronunciationAssessment	"{
  ""audio_base64"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""audio_format"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""text"": {
    ""type"": ""str"",
    ""required"": false
  }
}"
AdvanceCourseFinder	"{
  ""course_id"": {
    ""type"": ""str"",
    ""required"": true
  }
}"
RandomWordsWithPronunciation	{}
BookInformationLibrary	"{
  ""genre"": {
    ""type"": ""str"",
    ""required"": false
  }
}"
The task is:
"""
]
# Result Initialization Template - Education
MESSAGE_RESULT_4_edu = [
    """
Your tools response are as follows:
"GetBooksInfo:
{
  ""type"": ""object"",
  ""properties"": {
    ""results"": {
      ""type"": ""array"",
      ""items"": {
        ""type"": ""object"",
        ""properties"": {
          ""isbn"": {""type"": ""string""},
          ""author"": {""type"": ""string""},
          ""description"": {""type"": ""string""},
          ""img_link"": {""type"": ""string""},
          ""pdf_link"": {""type"": ""string""},
          ""publisher"": {""type"": ""string""},
          ""title"": {""type"": ""string""},
          ""year"": {""type"": ""string""}
        }
      }
    }
  }
}"
"ArxivJSON:
{
  ""type"": ""array"",
  ""items"": {
    ""type"": ""object"",
    ""properties"": {
      ""id"": {""type"": ""string""},
      ""version"": {""type"": ""integer""},
      ""published"": {""type"": ""string""},
      ""updated"": {""type"": ""string""},
      ""title"": {""type"": ""string""},
      ""authors"": {
        ""type"": ""array"",
        ""items"": {
          ""type"": ""object"",
          ""properties"": {
            ""name"": {""type"": ""string""}
          }
        }
      },
      ""summary"": {""type"": ""string""},
      ""primary_category"": {""type"": ""string""},
      ""links"": {
        ""type"": ""array"",
        ""items"": {""type"": ""object""}
      },
      ""category"": {
        ""type"": ""array"",
        ""items"": {""type"": ""string""}
      }
    }
  }
}"
"ArxivGPT:
{
  ""type"": ""object"",
  ""properties"": {
    ""paper_id"": {""type"": ""string""},
    ""content"": {""type"": ""string""},
    ""total_pages"": {""type"": ""integer""},
    ""returned_pages"": {""type"": ""integer""},
    ""format"": {
      ""type"": ""string"",
      ""enum"": [""text"", ""markdown""]
    }
  }
}"
"Photomath:
{
  ""data"": {
    ""type"": ""object"",
    ""properties"": {
      ""solution"": {
        ""type"": ""object"",
        ""properties"": {
          ""steps"": {
            ""type"": ""array"",
            ""items"": {
              ""type"": ""object"",
              ""properties"": {
                ""description"": {""type"": ""string""},
                ""expression"": {""type"": ""string""}
              }
            }
          },
          ""result"": {""type"": ""string""}
        }
      },
      ""problem"": {""type"": ""string""},
      ""type"": {""type"": ""string""}
    }
  },
  ""meta"": {
    ""type"": ""object"",
    ""properties"": {
      ""confidence"": {""type"": ""number""},
      ""timestamp"": {""type"": ""string""}
    }
  }
}"
"TEDTalksAPI:
{
  ""results"": [
    {
      ""id"": {""type"": ""integer""},
      ""url"": {""type"": ""string""},
      ""title"": {""type"": ""string""},
      ""description"": {""type"": ""string""},
      ""audio_language"": {""type"": ""string""},
      ""event"": {""type"": ""string""},
      ""publish_date"": {""type"": ""string""},
      ""record_date"": {""type"": ""string""},
      ""duration_in_seconds"": {""type"": ""integer""},
      ""thumbnail_url"": {""type"": ""string""},
      ""mp4_url"": {""type"": ""string""},
      ""embed_url"": {""type"": ""string""}
    }
  ]
}"
"UniversityCollegeListRankings:
{
  ""universities"": [
    {
      ""id"": {""type"": ""integer""},
      ""name"": {""type"": ""string""},
      ""country"": {""type"": ""string""},
      ""city"": {""type"": ""string""},
      ""rank"": {""type"": ""integer""},
      ""overall_score"": {""type"": ""number""},
      ""teaching_score"": {""type"": ""number""},
      ""research_score"": {""type"": ""number""},
      ""citations_score"": {""type"": ""number""},
      ""industry_income_score"": {""type"": ""number""},
      ""international_outlook_score"": {""type"": ""number""},
      ""website"": {""type"": ""string""},
      ""logo_url"": {""type"": ""string""}
    }
  ]
}"
"UdemyPaidCoursesForFree:
{
  ""type"": ""object"",
  ""properties"": {
    ""courses"": {
      ""type"": ""array"",
      ""items"": {
        ""type"": ""object"",
        ""properties"": {
          ""name"": {""type"": ""string""},
          ""category"": {""type"": ""string""},
          ""image"": {""type"": ""string""},
          ""actual_price_usd"": {""type"": ""number""},
          ""sale_price_usd"": {""type"": ""number""},
          ""sale_end"": {""type"": ""string""},
          ""description"": {""type"": ""string""},
          ""url"": {""type"": ""string""},
          ""clean_url"": {""type"": ""string""}
        }
      }
    }
  }
}"
"PronunciationAssessment:
{
  ""words"": [
    {
      ""label"": {""type"": ""string""},
      ""phones"": [
        {
          ""label"": {""type"": ""string""},
          ""label_ipa"": {""type"": ""string""},
          ""confidence"": {""type"": ""integer""},
          ""score"": {""type"": ""integer""},
          ""error"": {""type"": ""boolean""},
          ""sounds_like"": [
            {
              ""label"": {""type"": ""string""},
              ""label_ipa"": {""type"": ""string""},
              ""confidence"": {""type"": ""integer""}
            }
          ]
        }
      ],
      ""score"": {""type"": ""integer""}
    }
  ]
}"
"AdvanceCourseFinder:
{
  ""type"": ""object"",
  ""properties"": {
    ""key1"": {""type"": ""string""},
    ""key2"": {""type"": ""string""}
  }
}"
"RandomWordsWithPronunciation:
{
  ""type"": ""array"",
  ""items"": {
    ""type"": ""object"",
    ""properties"": {
      ""definition"": {""type"": ""string""},
      ""pronunciation"": {""type"": ""string""},
      ""word"": {""type"": ""string""}
    }
  }
}"
"BookInformationLibrary:
{
  ""type"": ""object"",
  ""properties"": {
    ""totalBooks"": {""type"": ""integer""},
    ""recommendations"": {
      ""type"": ""array"",
      ""items"": {
        ""type"": ""object"",
        ""properties"": {
          ""_id"": {""type"": ""string""},
          ""title"": {""type"": ""string""},
          ""author"": {""type"": ""string""},
          ""genre"": {""type"": ""string""},
          ""summary"": {""type"": ""string""},
          ""img_url"": {""type"": ""string""},
          ""reviews"": {
            ""type"": ""array"",
            ""items"": {
              ""type"": ""object"",
              ""properties"": {
                ""reviewer"": {""type"": ""string""},
                ""rating"": {""type"": ""integer""},
                ""comment"": {""type"": ""string""},
                ""_id"": {""type"": ""string""}
              }
            }
          },
          ""__v"": {""type"": ""integer""}
        }
      }
    }
  }
}"
"""
]
# Planner Initialization Template - Health
MESSAGE_PLANNER_5_health = [
    """Your tools are as follows:
GoogleMapsGeocoding	"{
  ""latlng"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""location_type"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""result_type"": {
    ""type"": ""str"",
    ""required"": false
  }
}"
ExerciseDB	"{
  ""bodyPart"": {
    ""type"": ""str"",
    ""required"": true
  }
}"
USDoctorsAPI	"{
  ""NPI"": {
    ""type"": ""str"",
    ""required"": true
  }
}"
AdvancedExerciseFinder	{}
PositivityTips	{}
AIWorkoutNutritionGuideAPI	"{
  ""goal"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""dietary_restrictions"": {
    ""type"": ""array"",
    ""required"": false
  },
  ""current_weight"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""target_weight"": {
    ""type"": ""Number"",
    ""required"": false
  },
  ""daily_activity_level"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""lang"": {
    ""type"": ""String"",
    ""required"": false
  }
}"
BMICalculator	"{
  ""height"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""weight"": {
    ""type"": ""str"",
    ""required"": true
  }
}"
CoronavirusMonitor	{}
NutritionCalculator	"{
  ""measurement_units"": {
    ""type"": ""str"",
    ""required"": true
  },
  ""feet"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""inches"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""lbs"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""cm"": {
    ""type"": ""str"",
    ""required"": false
  },
  ""kilos"": {
    ""type"": ""str"",
    ""required"": false
  }
}"
AnxietyDepression	"{
  ""limit"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""orderBy"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""index"": {
    ""type"": ""String"",
    ""required"": false
  },
  ""value"": {
    ""type"": ""String"",
    ""required"": false
  }
}"
The task is:
"""
]
# Result Initialization Template - Health
MESSAGE_RESULT_5_health = [
    """
Your tools response are as follows:
"GoogleMapsGeocoding:
{
  ""status"": {""type"": ""boolean""},
  ""message"": {""type"": ""string""},
  ""timestamp"": {""type"": ""integer""},
  ""data"": [
    {
      ""business_status"": {""type"": ""string""},
      ""formatted_address"": {""type"": ""string""},
      ""geometry"": {
        ""type"": ""object"",
        ""properties"": {
               ""location"": {
                ""lat"": ""string"",
                ""lng"": ""string""
              }
        }
      },
      ""name"": {""type"": ""string""},
      ""opening_hours"": {
        ""type"": ""object"",
        ""properties"": {
          ""open_now"": {""type"": ""boolean""}
        }
      },
      ""photos"": [
        {
          ""height"": {""type"": ""integer""},
          ""html_attributions"": {
            ""type"": ""array"",
            ""items"": [
              {""type"": ""string""}
            ]
          },
          ""photo_reference"": {""type"": ""string""},
          ""width"": {""type"": ""integer""}
        }
      ],
      ""place_id"": {""type"": ""string""},
      ""plus_code"": {
        ""type"": ""object"",
        ""properties"": {
          ""compound_code"": {""type"": ""string""},
          ""global_code"": {""type"": ""string""}
        }
      },
      ""rating"": {""type"": ""number""},
      ""reference"": {""type"": ""string""},
      ""types"": {
        ""type"": ""array"",
        ""items"": [
          {""type"": ""string""}
        ]
      },
      ""user_ratings_total"": {""type"": ""integer""}
    }
  ]
}"
"ExerciseDB:
{
  ""type"": ""array"",
  ""items"": {
    ""type"": ""object"",
    ""properties"": {
      ""bodyPart"": {""type"": ""string""},
      ""equipment"": {""type"": ""string""},
      ""gifUrl"": {""type"": ""string""},
      ""id"": {""type"": ""string""},
      ""name"": {""type"": ""string""},
      ""target"": {""type"": ""string""},
      ""secondaryMuscles"": {
        ""type"": ""array"",
        ""items"": {""type"": ""string""}
      },
      ""instructions"": {
        ""type"": ""array"",
        ""items"": {""type"": ""string""}
      }
    },
    ""required"": [
      ""bodyPart"",
      ""equipment"",
      ""gifUrl"",
      ""id"",
      ""name"",
      ""target"",
      ""secondaryMuscles"",
      ""instructions""
    ]
  }
}"
"USDoctorsAPI:
{
  ""data"": {
    ""type"": ""object"",
    ""properties"": {
      ""doctors"": {
        ""type"": ""array"",
        ""items"": {
          ""type"": ""object"",
          ""properties"": {
            ""firstName"": {""type"": ""string""},
            ""lastName"": {""type"": ""string""},
            ""gender"": {""type"": ""string""},
            ""specialty"": {""type"": ""string""},
            ""address"": {
              ""type"": ""object"",
              ""properties"": {
                ""street"": {""type"": ""string""},
                ""city"": {""type"": ""string""},
                ""state"": {""type"": ""string""},
                ""zip"": {""type"": ""string""}
              }
            },
            ""phone"": {""type"": ""string""},
            ""email"": {""type"": ""string""},
            ""website"": {""type"": ""string""},
            ""ratings"": {
              ""type"": ""array"",
              ""items"": {
                ""type"": ""object"",
                ""properties"": {
                  ""source"": {""type"": ""string""},
                  ""score"": {""type"": ""number""},
                  ""reviews"": {""type"": ""integer""}
                }
              }
            }
          }
        }
      }
    }
  },
  ""meta"": {
    ""type"": ""object"",
    ""properties"": {
      ""total"": {""type"": ""integer""},
      ""page"": {""type"": ""integer""},
      ""limit"": {""type"": ""integer""}
    }
  }
}"
"AdvancedExerciseFinder:
{
  ""data"": {
    ""type"": ""object"",
    ""properties"": {
      ""allExerciseParams"": {
        ""type"": ""array"",
        ""items"": {
          ""type"": ""object"",
          ""properties"": {
            ""name"": {""type"": ""string""},
            ""id"": {""type"": ""string""},
            ""values"": {
              ""type"": ""array"",
              ""items"": {""type"": ""string""}
            }
          }
        }
      }
    }
  }
}"
"PositivityTips:
{
  ""data"": {
    ""type"": ""object"",
    ""properties"": {
      ""tips"": {
        ""type"": ""array"",
        ""items"": {
          ""type"": ""object"",
          ""properties"": {
            ""id"": {""type"": ""string""},
            ""tip"": {""type"": ""string""},
            ""category"": {""type"": ""string""},
            ""source"": {""type"": ""string""}
          }
        }
      }
    }
  },
  ""meta"": {
    ""type"": ""object"",
    ""properties"": {
      ""total"": {""type"": ""integer""},
      ""page"": {""type"": ""integer""},
      ""limit"": {""type"": ""integer""}
    }
  }
}"
"AIWorkoutNutritionGuideAPI:
{
  ""result"": {
    ""type"": ""object"",
    ""properties"": {
      ""exercise_name"": {""type"": ""string""},
      ""description"": {""type"": ""string""},
      ""goal"": {""type"": ""string""},
      ""calories_per_day"": {""type"": ""integer""},
      ""macronutrients"": {
        ""type"": ""object"",
        ""properties"": {
          ""carbohydrates"": {""type"": ""string""},
          ""proteins"": {""type"": ""string""},
          ""fats"": {""type"": ""string""}
        }
      },
      ""meal_suggestions"": {
        ""type"": ""array"",
        ""items"": [
          {
            ""type"": ""object"",
            ""properties"": {
              ""meal"": {""type"": ""string""},
              ""suggestions"": {
                ""type"": ""array"",
                ""items"": [
                  {
                    ""type"": ""object"",
                    ""properties"": {
                      ""name"": {""type"": ""string""},
                      ""ingredients"": {
                        ""type"": ""array"",
                        ""items"": [
                          {""type"": ""string""}
                        ]
                      },
                      ""calories"": {""type"": ""integer""}
                    }
                  }
                ]
              }
            }
          }
        ]
      },
      ""seo_title"": {""type"": ""string""},
      ""seo_content"": {""type"": ""string""},
      ""seo_keywords"": {""type"": ""string""}
    }
  },
  ""cacheTime"": {""type"": ""integer""},
  ""time"": {""type"": ""integer""}
}"
"BMICalculator:
{
  ""type"": ""object"",
  ""properties"": {
    ""weight"": {
      ""type"": ""object"",
      ""properties"": {
        ""kg"": {""type"": ""string""},
        ""lb"": {""type"": ""string""}
      }
    },
    ""height"": {
      ""type"": ""object"",
      ""properties"": {
        ""m"": {""type"": ""string""},
        ""cm"": {""type"": ""string""},
        ""in"": {""type"": ""string""},
        ""ft-in"": {""type"": ""string""}
      }
    },
    ""bmi"": {
      ""type"": ""object"",
      ""properties"": {
        ""value"": {""type"": ""string""},
        ""status"": {""type"": ""string""},
        ""risk"": {""type"": ""string""},
        ""prime"": {""type"": ""string""}
      }
    },
    ""ideal_weight"": {""type"": ""string""},
    ""surface_area"": {""type"": ""string""},
    ""ponderal_index"": {""type"": ""string""},
    ""bmr"": {
      ""type"": ""object"",
      ""properties"": {
        ""value"": {""type"": ""string""}
      }
    },
    ""whr"": {
      ""type"": ""object"",
      ""properties"": {
        ""value"": {""type"": ""string""},
        ""status"": {""type"": ""string""}
      }
    },
    ""whtr"": {
      ""type"": ""object"",
      ""properties"": {
        ""value"": {""type"": ""string""},
        ""status"": {""type"": ""string""}
      }
    },
    ""sex"": {""type"": ""string""},
    ""age"": {""type"": ""string""},
    ""waist"": {""type"": ""string""},
    ""hip"": {""type"": ""string""}
  }
}"
"CoronavirusMonitor:
{
  ""data"": {
    ""type"": ""object"",
    ""properties"": {
      ""summary"": {
        ""type"": ""object"",
        ""properties"": {
          ""newConfirmed"": {""type"": ""integer""},
          ""totalConfirmed"": {""type"": ""integer""},
          ""newDeaths"": {""type"": ""integer""},
          ""totalDeaths"": {""type"": ""integer""},
          ""newRecovered"": {""type"": ""integer""},
          ""totalRecovered"": {""type"": ""integer""},
          ""date"": {""type"": ""string""}
        }
      },
      ""countries"": {
        ""type"": ""array"",
        ""items"": {
          ""type"": ""object"",
          ""properties"": {
            ""country"": {""type"": ""string""},
            ""countryCode"": {""type"": ""string""},
            ""newConfirmed"": {""type"": ""integer""},
            ""totalConfirmed"": {""type"": ""integer""},
            ""newDeaths"": {""type"": ""integer""},
            ""totalDeaths"": {""type"": ""integer""},
            ""newRecovered"": {""type"": ""integer""},
            ""totalRecovered"": {""type"": ""integer""},
            ""date"": {""type"": ""string""}
          }
        }
      }
    }
  },
  ""message"": {""type"": ""string""},
  ""lastRefresh"": {""type"": ""string""}
}"
"NutritionCalculator:
{
  ""bmi"": {""type"": ""string""}
}"
"AnxietyDepression:
{
  ""type"": ""array""
}"
"""
]
