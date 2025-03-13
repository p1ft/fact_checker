# Fact Checker

A fact-checking program that verifies user claims by 
comparing Gemini API responses with Wikipedia data.
_____
## Description:
This script takes a factual claim from a user, processes it 
through Google's Gemini API to get a True/False response, then finds 
this information on Wikipedia using the Wikipedia API and 
compares Wiki and Gemini responses using the Gemini API again.


1. User enters a claim
2. Gemini API analyzes the claim and returns a True/False answer with a short explanation
3. Wikipedia API finds a relevant article and retrieves information, using the keywords found for it
4. A second Gemini query сhecks the claim using the earlier given Wikipedia info and returns True/False and an explanation
5. Program makes a final decision:
   - TRUE (if LLM and Wikipedia agree)
   - FALSE (if LLM and Wikipedia contradict)
   - UNCERTAIN (if Wikipedia lacks relevant information)

## Repository Structure

```
fact_checker/
├── .env                # API KEY
├── README.md           # INSTRUCTIONS
├── main.py             # MAIN CODE
└── requirements.txt    # REQUIRMENTS
```

## How to use:

1. Enter a factual claim when prompted
2. Check the result in the console

_______
Example 1:
```
   Write the claim: The Eiffel Tower is 330 metres tall, including antenna

   Gemini response: True. The Eiffel Tower's official height, including its antenna, is 330 meters.

   Wikipedia info:, ['The Eiffel Tower (  EYE-fəl; French: Tour Eiffel [tuʁ ɛfɛl] ) is a wrought-iron lattice tower on the Champ de Mars in Paris, France', 'It is named after the engineer Gustave Eiffel, whose company designed and built the tower from 1887 to 1889.\nLocally nicknamed "La dame de fer" (French for "Iron Lady"), it was constructed as the centerpiece of the 1889 World\'s Fair, and to crown the centennial anniversary of the French Revolution', "Although initially criticised by some of France's leading artists and intellectuals for its design, it has since become a global cultural icon of France and one of the most recognisable structures in the world", 'The tower received 5,889,000 visitors in 2022', 'The Eiffel Tower is the most visited monument with an entrance fee in the world: 6.91 million people ascended it in 2015', 'It was designated a monument historique in 1964, and was named part of a UNESCO World Heritage Site ("Paris, Banks of the Seine") in 1991.\nThe tower is 330 metres (1,083 ft) tall, about the same height as an 81-storey building, and the tallest structure in Paris', 'Its base is square, measuring 125 metres (410 ft) on each side'] 

   Final Decision: TRUE (LLM and Wikipedia agree)
```

Example 2:
```
  Write the claim: Honey never spoils

    Gemini response: True. Honey is hygroscopic and has a low pH, both of which inhibit bacterial growth, preventing spoilage.

    Wikipedia info:, ['Jessica Marie Alba ( AL-bə; born April 28, 1981) is an American actress, businesswoman, and entrepreneur', 'She began her acting career at age 13 in Camp Nowhere, followed up by The Secret World of Alex Mack (both 1994), and rose to prominence at age 19 as the lead actress of the television series Dark Angel (2000–2002), for which she received a Golden Globe nomination.\nHer big screen breakthrough came in Honey (2003)', "She soon established herself as a Hollywood actress, and has starred in numerous box office hits throughout her career, including Fantastic Four (2005), Fantastic Four: Rise of the Silver Surfer (2007), Good Luck Chuck (2007), The Eye (2008), Valentine's Day (2010), Little Fockers (2010), and Mechanic: Resurrection (2016)", 'She is a frequent collaborator with director Robert Rodriguez, having starred in Sin City (2005), Machete (2010), Spy Kids: All the Time in the World (2011), Machete Kills (2013), and Sin City: A Dame to Kill For (2014)', "From 2019 to 2020, Alba starred in the Spectrum action crime series L.A.'s Finest.\nIn 2011, Alba co-founded The Honest Company, a consumer goods company that sells baby, personal and household products", "A number of magazines, including Men's Health, Vanity Fair and FHM, have included Alba on their lists of the world's most beautiful women."] 

    Final Decision: UNCERTAIN (Missing or unclear information)
```

Example 3:
```
  Write the claim: The Moon is made of green cheese

    Gemini response: False. Scientific evidence confirms the Moon is composed of rock, metals, and minerals, not cheese.

    Wikipedia info:, ["The Moon is Earth's only natural satellite, orbiting at an average distance of 384399 km (238,854 mi; about 30 times Earth's diameter)", 'It faces Earth always with the same side', "This is a result of Earth's gravitational pull having synchronized the Moon's rotation period (lunar day) with its orbital period (lunar month) of 29.5 Earth days", "The Moon's pull on Earth is the main driver of Earth's tides.\nIn geophysical terms, the Moon is a planetary-mass object or satellite planet", "Its mass is 1.2% that of the Earth, and its diameter is 3,474 km (2,159 mi), roughly one-quarter of Earth's (about as wide as the contiguous United States)", 'Within the Solar System, it is the largest and most massive satellite in relation to its parent planet, the fifth-largest and fifth-most massive moon overall, and larger and more massive than all known dwarf planets', "Its surface gravity is about one-sixth of Earth's, about half that of Mars, and the second-highest among all moons in the Solar System, after Jupiter's moon Io"] 

    Final Decision: TRUE (LLM and Wikipedia agree)
```
Example 4:
```
  Write the claim: The city of Eldoria was founded in 1000

  Gemini response: False. The prompt doesn't provide any information about when Eldoria was founded, so we cannot assume it was 1000.

  Wikipedia info:, No Wikipedia data found. 

  Final Decision: UNCERTAIN (Missing or unclear information)
```

Example 5:
```
  Write the claim: Kyiv is the capital of Ukraine

  Gemini response: True. Kyiv is the capital and largest city of Ukraine.

  Wikipedia info:, ['Kyiv (also Kiev) is the capital and most populous city of Ukraine', 'It is in north-central Ukraine along the Dnieper River', 'As of 1 January 2022, its population was 2,952,301, making Kyiv the seventh-most populous city in Europe', 'Kyiv is an important industrial, scientific, educational, and cultural center in Eastern Europe', 'It is home to many high-tech industries, higher education institutions, and historical landmarks', "The city has an extensive system of public transport and infrastructure, including the Kyiv Metro.\nThe city's name is said to derive from the name of Kyi, one of its four legendary founders", 'During its history, Kyiv, one of the oldest cities in Eastern Europe, passed through several stages of prominence and obscurity'] 

  Final Decision: TRUE (LLM and Wikipedia agree)
```
-----
## Issues:

1. **Keywords Extraction**: The current method for extracting the main words from the claim is simple and might have problems with complex claims. Also it extracts not only one sentence that contains numerical or factual data, but a few (3-7) for a better Gemini check.


2. **Wikipedia Data Retrieval**: The system sometimes struggles to find the exact Wikipedia page for the entity in the claim, which can lead to UNCERTAIN results even for verifiable claims.


3. **Error Handling**: Basic error handling is implemented, but more complex errors such as API failures, network issues are not.

