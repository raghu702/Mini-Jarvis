import re


# =========================================================
# SAH-AI — LOCAL MOCK MODE
# This version uses simple rules and makes NO API calls.
# =========================================================

conversation_state = {}


def get_state(conversation_id: str):
    """Create or retrieve state for a conversation."""

    if conversation_id not in conversation_state:
        conversation_state[conversation_id] = {
            "intent": None,
            "movie": None,
            "city": None,
            "date": None,
            "time": None,
            "tickets": None,
            "destination": None,
        }

    return conversation_state[conversation_id]


def reset_task(task: dict, intent: str):
    """Start a new task and clear information from the previous task."""

    task["intent"] = intent
    task["movie"] = None
    task["city"] = None
    task["date"] = None
    task["time"] = None
    task["tickets"] = None
    task["destination"] = None


def detect_new_intent(message: str):
    """Detect whether the user is starting a different task."""

    text = message.lower().strip()

    # Movie tickets
    if any(word in text for word in [
        "movie", "film", "cinema", "theatre", "theater",
        "movie ticket", "rajasab", "rajasaab"
    ]):
        if any(word in text for word in [
            "train", "railway", "rail", "bus", "hotel",
            "cab", "taxi", "bill payment"
        ]):
            pass
        else:
            return "book_movie_ticket"

    # Train search
    if any(word in text for word in [
        "train", "railway", "rail ticket", "train ticket"
    ]):
        return "search_train"

    # Hotel search
    if any(word in text for word in [
        "hotel", "room booking", "book a room", "stay"
    ]):
        return "search_hotel"

    # Bus search
    if any(word in text for word in [
        "bus ticket", "bus booking", "book a bus"
    ]):
        return "search_bus"

    # Cab search
    if any(word in text for word in [
        "cab", "taxi", "book a ride"
    ]):
        return "search_cab"

    return None


def extract_number(text: str):
    """Extract a ticket count from common text formats."""

    match = re.search(r"\b(\d+)\s*(?:tickets?|people|persons?)?\b", text.lower())

    if match:
        return int(match.group(1))

    word_numbers = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
    }

    for word, number in word_numbers.items():
        if re.search(rf"\b{word}\s*(?:tickets?|people|persons?)\b", text.lower()):
            return number

    return None


def update_task(task: dict, message: str):
    """Fill the next missing field using simple local rules."""

    text = message.strip()
    lower = text.lower()

    if task["intent"] == "book_movie_ticket":

        if task["movie"] is None:
            # Treat a short reply as a movie name.
            task["movie"] = text
            return

        if task["city"] is None:
            task["city"] = text
            return

        if task["date"] is None:
            task["date"] = text
            return

        if task["time"] is None:
            task["time"] = text
            return

        if task["tickets"] is None:
            number = extract_number(text)

            if number is not None:
                task["tickets"] = number
            return

    elif task["intent"] == "search_train":

        if task["destination"] is None:
            task["destination"] = text
            return

        if task["date"] is None:
            task["date"] = text
            return

    elif task["intent"] == "search_hotel":

        if task["city"] is None:
            task["city"] = text
            return

        if task["date"] is None:
            task["date"] = text
            return


def get_missing_information(task: dict):
    """Return the required fields that haven't been provided."""

    requirements = {
        "book_movie_ticket": [
            ("movie", "movie"),
            ("city", "city"),
            ("date", "date"),
            ("time", "show time"),
            ("tickets", "number of tickets"),
        ],
        "search_train": [
            ("destination", "destination"),
            ("date", "travel date"),
        ],
        "search_hotel": [
            ("city", "city"),
            ("date", "check-in date"),
        ],
    }

    fields = requirements.get(task["intent"], [])

    return [
        label
        for field, label in fields
        if task.get(field) is None
    ]


def generate_local_reply(task: dict, missing: list):
    """Generate a reply without using an external AI service."""

    intent = task["intent"]

    if intent == "book_movie_ticket":

        questions = {
            "movie": "Sure! 🎬 Which movie would you like to watch?",
            "city": f"Got it! Movie: {task['movie']}. Which city should I search in?",
            "date": f"Okay! {task['movie']} in {task['city']}. What date would you like to watch it?",
            "show time": f"Got it! Date: {task['date']}. What show time would you prefer?",
            "number of tickets": "What time works! How many tickets do you need?",
        }

        if missing:
            return questions.get(missing[0], "Could you provide a little more information?")

        return (
            "Here are the details you've provided! 🎬\n\n"
            f"Movie: {task['movie']}\n"
            f"City: {task['city']}\n"
            f"Date: {task['date']}\n"
            f"Show time: {task['time']}\n"
            f"Tickets: {task['tickets']}\n\n"
            "This is a test only. No tickets have been searched or booked. "
            "Would you like to proceed to the next step?"
        )

    if intent == "search_train":

        if missing:
            if "destination" in missing:
                return "Sure! 🚆 Where would you like to travel?"
            return f"Got it! Destination: {task['destination']}. What date would you like to travel?"

        return (
            f"Your train search details are ready!\n"
            f"Destination: {task['destination']}\n"
            f"Date: {task['date']}\n\n"
            "This is a test only. No live trains or availability have been checked."
        )

    if intent == "search_hotel":

        if missing:
            if "city" in missing:
                return "Sure! 🏨 Which city do you need a hotel in?"
            return f"Got it! City: {task['city']}. What is your check-in date?"

        return (
            f"Your hotel search details are ready!\n"
            f"City: {task['city']}\n"
            f"Check-in: {task['date']}\n\n"
            "This is a test only. No hotels or availability have been checked."
        )

    return (
        "I'm currently running in local test mode. "
        "Try asking me to book a movie ticket, search for a train, "
        "or find a hotel."
    )


def process_message(message: str, conversation_id: str):
    """Main entry point called by the FastAPI backend."""

    task = get_state(conversation_id)

    print("\n========== SAH-AI MOCK MODE ==========")
    print("User message:", message)

    new_intent = detect_new_intent(message)

    if new_intent is not None:
        reset_task(task, new_intent)

        # If the initial message already includes the movie name,
        # destination, city, or date, the simple mock may need
        # further improvements to extract multiple fields.
        if new_intent == "book_movie_ticket":
            if "rajasab" in message.lower() or "rajasaab" in message.lower():
                task["movie"] = "The Raja Saab"

        elif new_intent == "search_train":
            pass

    elif task["intent"] is None:
        print("No active task.")
        return (
            "Hi! 👋 I'm Sah-AI, currently in local test mode.\n"
            "Try: 'Movie ticket book cheyyali' or 'Train chudu'."
        )

    else:
        update_task(task, message)

    missing = get_missing_information(task)

    print("Current task:", task)
    print("Missing information:", missing)

    reply = generate_local_reply(task, missing)

    print("Sah-AI reply:", reply)
    print("=====================================\n")

    return reply