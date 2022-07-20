from dataclasses import dataclass

class regex_help:

    def __init__ (self, start_helper = True, helper_screen = 0):
        
        # from DataCamp course Regular Expressions in Python
        # https://www.datacamp.com/courses/regular-expressions-in-python#!

        self.start_helper = start_helper
        self.helper_screen = helper_screen
        
        self.helper_menu_1 = """

    Regular Expressions (RegEx) Helper
                    
    Input the number in the text box and press enter to visualize help and examples for a topic:

        1. regex basic theory and most common metacharacters
        2. regex quantifiers
        3. regex anchoring and finding
        4. regex greedy and non-greedy search
        5. regex grouping and capturing
        6. regex alternating and non-capturing groups
        7. regex backreferences
        8. regex lookaround
        9. print all topics at once
        10. Finish regex helper
        
        """
        
        # regex basic theory and most common metacharacters
        self.help_text_1 = """
    REGular EXpression or regex:
    String containing a combination of normal characters and special metacharacters that
    describes patterns to find text or positions within a text.

    Example:

    r'st\d\s\w{3,10}'
    - In Python, the r at the beginning indicates a raw string. It is always advisable to use it.
    - We said that a regex contains normal characters, or literal characters we already know. 
        - The normal characters match themselves. 
        - In the case shown above, 'st' exactly matches an 's' followed by a 't'.

    - Most important metacharacters:
        - \d: digit (number);
        - \D: non-digit;
        - \s: whitespace;
        - \s+: one or more consecutive whitespaces.
        - \S: non-whitespace;
        - \w: (word) character;
        - \W: non-word character.
        - {N, M}: indicates that the character on the left appears from N to M consecutive times.
            - \w{3,10}: a word character that appears 3, 4, 5,..., or 10 consecutive times.
        - {N}: indicates that the character on the left appears exactly N consecutive times.
            - \d{4}: a digit appears 4 consecutive times.
        - {N,}: indicates that the character appears at least N times.
            - \d{4,}: a digit appears 4 or more times.
            - phone_number = "John: 1-966-847-3131 Michelle: 54-908-42-42424"
            - re.findall(r"\d{1,2}-\d{3}-\d{2,3}-\d{4,}", phone_number) - returns: ['1-966-847-3131', '54-908-42-42424']

    ATTENTION: Using metacharacters in regular expressions will allow you to match types of characters such as digits. 
    - You can encounter many forms of whitespace such as tabs, space or new line. 
    - To make sure you match all of them always specify whitespaces as \s.

    re module: Python standard library module to search regex within individual strings.

    - .findall method: search all occurrences of the regex within the string, returning a list of strings.
    - Syntax: re.findall(r"regex", string)
        - Example: re.findall(r"#movies", "Love #movies! I had fun yesterday going to the #movies")
            - Returns: ['#movies', '#movies']

    - .split method: splits the string at each occurrence of the regex, returning a list of strings.
    - Syntax: re.split(r"regex", string)
        - Example: re.split(r"!", "Nice Place to eat! I'll come back! Excellent meat!")
            - Returns: ['Nice Place to eat', " I'll come back", ' Excellent meat', '']

    - .sub method: replace one or many matches of the regex with a given string (returns a replaced string).
    - Syntax: re.sub((r"regex", new_substring, original_string))
        - Example: re.sub(r"yellow", "nice", "I have a yellow car and a yellow house in a yellow neighborhood")
        - Returns: 'I have a nice car and a nice house in a nice neighborhood'

    - .search and .match methods: they have the same syntax and are used to find a match. 
        - Both methods return an object with the match found. 
        - The difference is that .match is anchored at the beginning of the string.
    - Syntax: re.search(r"regex", string) and re.match(r"regex", string)
        - Example 1: re.search(r"\d{4}", "4506 people attend the show")
        - Returns: <_sre.SRE_Match object; span=(0, 4), match='4506'>
        - re.match(r"\d{4}", "4506 people attend the show")
        - Returns: <_sre.SRE_Match object; span=(0, 4), match='4506'>
            - In this example, we use both methods to find a digit appearing four times. 
            - Both methods return an object with the match found.
        
        - Example 2: re.search(r"\d+", "Yesterday, I saw 3 shows")
        - Returns: <_sre.SRE_Match object; span=(17, 18), match='3'>
        - re.match(r"\d+","Yesterday, I saw 3 shows")
        - Returns: None
            - In this example,, we used them to find a match for a digit. 
            - In this case, .search finds a match, but .match does not. 
            - This is because the first characters do not match the regex.

    - .group method: detailed in Section 7 (Backreferences).
        - Retrieves the groups captured.
    - Syntax: searched_string = re.search(r"regex", string)
        re.group(N) - returns N-th group captured (group 0 is the regex itself).
        
        Example: text = "Python 3.0 was released on 12-03-2008."
        information = re.search('(\d{1,2})-(\d{2})-(\d{4})', text)
        information.group(3) - returns: '2008'
    - .group can only be used with .search and .match methods.

    Examples of regex:

    1. re.findall(r"User\d", "The winners are: User9, UserN, User8")
        ['User9', 'User8']
    2. re.findall(r"User\D", "The winners are: User9, UserN, User8")
        ['UserN']
    3. re.findall(r"User\w", "The winners are: User9, UserN, User8")
        ['User9', 'UserN', 'User8']
    4. re.findall(r"\W\d", "This skirt is on sale, only $5 today!")
        ['$5']
    5. re.findall(r"Data\sScience", "I enjoy learning Data Science")
        ['Data Science']
    6. re.sub(r"ice\Scream", "ice cream", "I really like ice-cream")
        'I really like ice cream'

    7. regex that matches the user mentions that starts with @ and follows the pattern @robot3!.

    regex = r"@robot\d\W"

    8. regex that matches the number of user mentions given as, for example: User_mentions:9.

    regex = r"User_mentions:\d"

    9. regex that matches the number of likes given as, for example, likes: 5.

    regex = r"likes:\s\d"

    10. regex that matches the number of retweets given as, for example, number of retweets: 4.

    regex = r"number\sof\sretweets:\s\d"

    11. regex that matches the user mentions that starts with @ and follows the pattern @robot3!.

    regex_sentence = r"\W\dbreak\W"

    12. regex that matches the pattern #newH

    regex_words = r"\Wnew\w"

    """

        # regex quantifiers
        self.help_text_2 = """
    Quantifiers: 
    A metacharacter that tells the regex engine how many times to match a character immediately to its left.

        1. +: Once or more times.
            - text = "Date of start: 4-3. Date of registration: 10-04."
            - re.findall(r"\d+-\d+", text) - returns: ['4-3', '10-04']
            - Again, \s+ represents one or more consecutive whitespaces.
        2. *: Zero times or more.
            - my_string = "The concert was amazing! @ameli!a @joh&&n @mary90"
            - re.findall(r"@\w+\W*\w+", my_string) - returns: ['@ameli!a', '@joh&&n', '@mary90']
        3. ?: Zero times or once: ?
            - text = "The color of this image is amazing. However, the colour blue could be brighter."
            - re.findall(r"colou?r", text) - returns: ['color', 'colour']
        
    The quantifier refers to the character immediately on the left:
    - r"apple+" : + applies to 'e' and not to 'apple'.

    Examples of regex:

    1. Most of the times, links start with 'http' and do not contain any whitespace, e.g. https://www.datacamp.com. 
    - regex to find all the matches of http links appearing:
        - regex = r"http\S+"
        - \S is very useful to use when you know a pattern does not contain spaces and you have reached the end when you do find one.

    2. User mentions in Twitter start with @ and can have letters and numbers only, e.g. @johnsmith3.
    - regex to find all the matches of user mentions appearing:
        - regex = r"@\w*\d*"

    3. regex that finds all dates in a format similar to 27 minutes ago or 4 hours ago.
    - regex = r"\d{1,2}\s\w+\sago"

    4. regex that finds all dates in a format similar to 23rd june 2018.
    - regex = r"\d{1,2}\w{2}\s\w+\s\d{4}"

    5. regex that finds all dates in a format similar to 1st september 2019 17:25.
    - regex = r"\d{1,2}\w{2}\s\w+\s\d{4}\s\d{1,2}:\d{2}"

    6. Hashtags start with a # symbol and contain letters and numbers but never whitespace.
    - regex that matches the described hashtag pattern.
        - regex = r"#\w+"
        
    """

        # regex anchoring and finding
        self.help_text_3 = """
    - Anchoring and Finding Metacharacters

        1. . (dot): Match any character (except newline).
            - my_links = "Just check out this link: www.amazingpics.com. It has amazing photos!"
            - re.findall(r"www.+com", my_links) - returns: ['www.amazingpics.com']
                - The dot . metacharacter is very useful when we want to match all repetitions of any character. 
                - However, we need to be very careful how we use it.
        2. ^: Anchoring on start of the string.
            - my_string = "the 80s music was much better that the 90s"
            - If we do re.findall(r"the\s\d+s", my_string) - returns: ['the 80s', 'the 90s']
            - Using ^: re.findall(r"^the\s\d+s", my_string) - returns: ['the 80s']
        3. $: Anchoring at the end of the string.
            - my_string = "the 80s music hits were much better that the 90s"
            - re.findall(r"the\s\d+s$", my_string) - returns: ['the 90s']
        4. \: Escape special characters.
            - my_string = "I love the music of Mr.Go. However, the sound was too loud."
                - re.split(r".\s", my_string) - returns: ['', 'lov', 'th', 'musi', 'o', 'Mr.Go', 'However', 'th', 'soun', 'wa', 'to', 'loud.']
                - re.split(r"\.\s", my_string) - returns: ['I love the music of Mr.Go', 'However, the sound was too loud.']
        5. |: OR Operator
            - my_string = "Elephants are the world's largest land animal! I would love to see an elephant one day"
            - re.findall(r"Elephant|elephant", my_string) - returns: ['Elephant', 'elephant']
        6. []: set of characters representing the OR Operator.
            Example 1 - my_string = "Yesterday I spent my afternoon with my friends: MaryJohn2 Clary3"
            - re.findall(r"[a-zA-Z]+\d", my_string) - returns: ['MaryJohn2', 'Clary3']
            Example 2 - my_string = "My&name&is#John Smith. I%live$in#London."
            - re.sub(r"[#$%&]", " ", my_string) - returns: 'My name is John Smith. I live in London.'
            
            Note 1: within brackets, the characters to be found should not be separated, as in [#$%&].
                - Whitespaces or other separators would be interpreted as characters to be found.
            Note 2: [a-z] represents all word characters from 'a' to 'z', lowercase.
                    - [A-Z] represents all word characters from 'A' to 'Z', uppercase.
                    - Since lower and uppercase are different, we must declare [a-zA-Z] or [A-Za-z] to capture all word characters.
                    - [0-9] represents all digits from 0 to 9.
                    - Something like [a-zA-Z0-9] or [a-z0-9A-Z] will search all word characters and all numbers.
        
        7. [^ ]: OR operator combined to ^ transforms the expression to negative.
            - my_links = "Bad website: www.99.com. Favorite site: www.hola.com"
            - re.findall(r"www[^0-9]+com", my_links) - returns: ['www.hola.com']

    Examples of regex:

    1. You want to find names of files that appear at the start of the string; 
        - always start with a sequence of 2 or 3 upper or lowercase vowels (a e i o u); 
        - and always finish with the txt ending.
            - Write a regex that matches the pattern of the text file names, e.g. aemyfile.txt.
            # . = match any character
            regex = r"^[aeiouAEIOU]{2,3}.+txt"

    2. When a user signs up on the company website, they must provide a valid email address.
        - The company puts some rules in place to verify that the given email address is valid:
        - The first part can contain: Upper A-Z or lowercase letters a-z; 
        - Numbers; Characters: !, #, %, &, *, $, . Must have @. Domain: Can contain any word characters;
        - But only .com ending is allowed. 
            - Write a regular expression to match valid email addresses.
            - Match the regex to the elements contained in emails, and print out the message indicating if it is a valid email or not 
        
        # Write a regex to match a valid email address
        regex = r"^[A-Za-z0-9!#%&*$.]+@\w+\.com"

        for example in emails:
            # Match the regex to the string
            if re.match(regex, example):
                # Complete the format method to print out the result
                print("The email {email_example} is a valid email".format(email_example=example))
            else:
                print("The email {email_example} is invalid".format(email_example=example))
        
        # Notice that we used the .match() method. 
        # The reason is that we want to match the pattern from the beginning of the string.

    3. Rules in order to verify valid passwords: it can contain lowercase a-z and uppercase letters A-Z;
        - It can contain numbers; it can contain the symbols: *, #, $, %, !, &, .
        - It must be at least 8 characters long but not more than 20.
            - Write a regular expression to check if the passwords are valid according to the description.
            - Search the elements in the passwords list to find out if they are valid passwords.
            - Print out the message indicating if it is a valid password or not, complete .format() statement.
        
        # Write a regex to check if the password is valid
        regex = r"[a-z0-9A-Z*#$%!&.]{8,20}"

        for example in passwords:
            # Scan the strings to find a match
            if re.match(regex, example):
                # Complete the format method to print out the result
                print("The password {pass_example} is a valid password".format(pass_example=example))
            else:
                print("The password {pass_example} is invalid".format(pass_example=example))

    """

        # regex greedy and non-greedy search
        self.help_text_4 = """
    There are two types of matching methods: greedy and non-greedy (also called lazy) operators. 

    Greedy operators
    - The standard quantifiers are greedy by default, meaning that they will attempt to match as many characters as possible.
        - Standard quantifiers: * , + , ? , {num, num}
        - Example: re.match(r"\d+", "12345bcada") - returns: <_sre.SRE_Match object; span=(0, 5), match='12345'>
        - We can explain this in the following way: our quantifier will start by matching the first digit found, '1'. 
        - Because it is greedy, it will keep going to find 'more' digits and stop only when no other digit can be matched, returning '12345'.
    - If the greedy quantifier has matched so many characters that can not match the rest of pattern, it will backtrack, giving up characters matched earlier one at a time and try again. 
    - Backtracking is like driving a car without a map. If you drive through a path and hit a dead end street, you need to backtrack along your road to an earlier point to take another street. 
        - Example: re.match(r".*hello", "xhelloxxxxxx") - returns: <_sre.SRE_Match object; span=(0, 6), match='xhello'>
        - We use the greedy quantifier .* to find anything, zero or more times, followed by the letters "h" "e" "l" "l" "o". 
        - We can see here that it returns the pattern 'xhello'. 
        - So our greedy quantifier will start by matching as much as possible, the entire string. 
        - Then, it tries to match the h, but there are no characters left. So it backtracks, giving up one matched character. 
        - Trying again, it still doesn't match the h, so it backtracks one more step repeatedly until it finally matches the h in the regex, and the rest of the characters.

    Non-greedy (lazy) operators
    - Because they have lazy behavior, non-greedy quantifiers will attempt to match as few characters as needed, returning the shortest match. 
    - To obtain non-greedy quantifiers, we can append a question mark at the end of the greedy quantifiers to convert them into lazy. 
        - Example: re.match(r"\d+?", "12345bcada") - returns: <_sre.SRE_Match object; span=(0, 1), match='1'>
        - Now, our non-greedy quantifier will return the pattern '1'. 
        - In this case, our quantifier will start by matching the first digit found, '1'. 
        - Because it is non-greedy, it will stop there, as we stated that we want 'one or more', and 1 is as few as needed.
    - Non-greedy quantifiers also backtrack. 
    - In this case, if they have matched so few characters that the rest of the pattern cannot match, they backtrack, expand the matched character one at a time, and try again. 
    - In the example above: this time we use the lazy quantifier .*?. Interestingly, we obtain the same match 'xhello'. 
    - But, how this match was obtained is different from the first time: the lazy quantifier first matches as little as possible, nothing, leaving the entire string unmatched. 
    - Then it tries to match the 'h', but it doesn't work. 
    - So, it backtracks, matching one more character, the 'x'. Then, it tries again, this time matching the 'h', and afterwards, the rest of the regex.

    - Even though greedy quantifiers lead to longer matches, they are sometimes the best option. 
    - Because lazy quantifiers match as few as possible, they return a shorter match than we expected.
        - Example: if you want to extract a word starting with 'a' and ending with 'e' in the string 'I like apple pie', you may think that applying the greedy regex r"a.+e" will return 'apple'. 
        - However, your match will be 'apple pie'. A way to overcome this is to make it lazy by using '?'' which will return 'apple'.
    - On the other hand, using greedy quantifiers always leads to longer matches that sometimes are not desired. 
        - Making quantifiers lazy by adding '?' to match a shorter pattern is a very important consideration to keep in mind when handling data for text mining.

    Examples of regex:

    1. You want to extract the number contained in the sentence 'I was born on April 24th'. 
        - A lazy quantifier will make the regex return 2 and 4, because they will match as few characters as needed. 
        - However, a greedy quantifier will return the entire 24 due to its need to match as much as possible.

        1.1. Use a lazy quantifier to match all numbers that appear in the variable sentiment_analysis:
        numbers_found_lazy = re.findall(r"[0-9]+?", sentiment_analysis)
        - Output: ['5', '3', '6', '1', '2']
        
        1.2. Now, use a greedy quantifier to match all numbers that appear in the variable sentiment_analysis.
        numbers_found_greedy = re.findall(r"[0-9]+", sentiment_analysis)
        - Output: ['536', '12']

    2.1. Use a greedy quantifier to match text that appears within parentheses in the variable sentiment_analysis.
        
        sentences_found_greedy = re.findall(r"\(.+\)", sentiment_analysis)
        - Output: ["(They were so cute) a few yrs ago. PC crashed, and now I forget the name of the site ('I'm crying)"]

    2.2. Now, use a lazy quantifier to match text that appears within parentheses in the variable sentiment_analysis.

        sentences_found_lazy = re.findall(r"\(.+?\)", sentiment_analysis)
        - Output: ["(They were so cute)", "('I'm crying)"]
        
    """

        # regex grouping and capturing
        self.help_text_5 = """
    Capturing groups in regular expressions
    - Let's say that we have the following text:
        
        text = "Clary has 2 friends who she spends a lot time with. Susan has 3 brothers while John has 4 sisters."
        
    - We want to extract information about a person, how many and which type of relationships they have. 
    - So, we want to extract Clary 2 friends, Susan 3 brothers and John 4 sisters.
    - If we do: re.findall(r'[A-Za-z]+\s\w+\s\d+\s\w+', text), the output will be: ['Clary has 2 friends', 'Susan has 3 brothers', 'John has 4 sisters']
        - The output is quite close, but we do not want the word 'has'.

    - We start simple, by trying to extract only the names. We can place parentheses to group those characters, capture them, and retrieve only that group:
        - re.findall(r'([A-Za-z]+)\s\w+\s\d+\s\w+', text) - returns: ['Clary', 'Susan', 'John']
    - Actually, we can place parentheses around the three groups that we want to capture. 
        - re.findall(r'([A-Za-z]+)\s\w+\s(\d+)\s(\w+)', text)
        
        - Each group will receive a number: 
            - The entire expression will always be group 0. 
            - The first group: 1; the second: 2; and the third: 3.
        
        - The result returned is: [('Clary', '2', 'friends'), ('Susan', '3', 'brothers'), ('John', '4', 'sisters')]
            - We got a list of tuples: 
                - The first element of each tuple is the match captured corresponding to group 1. 
                - The second, to group 2. The last, to group 3.
        
        - We can use capturing groups to match a specific subpattern in a pattern. 
        - We can use this information for retrieving the groups by numbers; or to organize data.
            - Example: pets = re.findall(r'([A-Za-z]+)\s\w+\s(\d+)\s(\w+)', "Clary has 2 dogs but John has 3 cats")
                        pets[0][0] == 'Clary'
                        - In the code, we placed the parentheses to capture the name of the owner, the number and which type of pets each one has. 
                        - We can access the information retrieved by using indexing and slicing as seen in the code. 
    
    - Capturing groups have one important feature. 
        - Remember that quantifiers apply to the character immediately to the left. 
        - So, we can place parentheses to group characters and then apply the quantifier to the entire group. 
        
        Example: re.search(r"(\d[A-Za-z])+", "My user name is 3e4r5fg")
            - returns: <_sre.SRE_Match object; span=(16, 22), match='3e4r5f'>
            - In the code, we have placed parentheses to match the group containing a number and any letter. 
            - We applied the plus quantifier to specify that we want this group repeated once or more times. 
        
    - ATTENTION: It's not the same to capture a repeated group AND to repeat a capturing group. 
        
        my_string = "My lucky numbers are 8755 and 33"
        - re.findall(r"(\d)+", my_string) - returns: ['5', '3']
        - re.findall(r"(\d+)", my_string) - returns: ['8755', '33']
        
        - In the first code, we use findall to match a capturing group containing one number. 
            - We want this capturing group to be repeated once or more times. 
            - We get 5 and 3 as an output, because these numbers are repeated consecutively once or more times. 
        - In the second code, we specify that we should capture a group containing one or more repetitions of a number. 

    - Placing a subpattern inside parenthesis will capture that content and stores it temporarily in memory. This can be later reused.

    Examples of regex:

    1. You want to extract the first part of the email. E.g. if you have the email marysmith90@gmail.com, you are only interested in marysmith90.
    - You need to match the entire expression. So you make sure to extract only names present in emails. Also, you are only interested in names containing upper (e.g. A,B, Z) or lowercase letters (e.g. a, d, z) and numbers.
    - regex to match the email capturing only the name part. The name part appears before the @.
        - regex_email = r"([a-z0-9A-Z]+)@\S+"

    2. Text follows a pattern: "Here you have your boarding pass LA4214 AER-CDB 06NOV."
    - You need to extract the information about the flight: 
        - The two letters indicate the airline (e.g LA); the 4 numbers are the flight number (e.g. 4214);
        - The three letters correspond to the departure (e.g AER); the destination (CDB); the date (06NOV) of the flight.
        - All letters are always uppercase.

    - Regular expression to match and capture all the flight information required.
    - Find all the matches corresponding to each piece of information about the flight. Assign it to flight_matches.
    - Complete the format method with the elements contained in flight_matches: 
        - In the first line print the airline and the flight number. 
        - In the second line, the departure and destination. In the third line, the date.

    # Import re
    import re

    # Write regex to capture information of the flight
    regex = r"([A-Z]{2})(\d{4})\s([A-Z]{3})-([A-Z]{3})\s(\d{2}[A-Z]{3})"

    # Find all matches of the flight information
    flight_matches = re.findall(regex, flight)
        
    #Print the matches
    print("Airline: {} Flight number: {}".format(flight_matches[0][0], flight_matches[0][1]))
    print("Departure: {} Destination: {}".format(flight_matches[0][2], flight_matches[0][3]))
    print("Date: {}".format(flight_matches[0][4]))

        - findall() returns a list of tuples. 
        - The nth element of each tuple is the element corresponding to group n. 
        - This provides us with an easy way to access and organize our data.

    """

        # regex alternating and non-capturing groups
        self.help_text_6 = """
    Alternating and non-capturing groups

    - Vertical bar or pipe operator
        - Suppose we have the following string, and we want to find all matches for pet names. 
        - We can use the pipe operator to specify that we want to match cat or dog or bird:
            - my_string = "I want to have a pet. But I don't know if I want a cat, a dog or a bird."
            - re.findall(r"cat|dog|bird", my_string) - returns: ['cat', 'dog', 'bird']
        
        - Now, we changed the string a little bit, and once more we want to find all the pet names, but only those that come after a number and a whitespace. 
        - So, if we specify this again with the pipe operator, we get the wrong output: 
            - my_string = "I want to have a pet. But I don't know if I want 2 cats, 1 dog or a bird."
            - re.findall(r"\d+\scat|dog|bird", my_string) - returns: ['2 cat', 'dog', 'bird']
        
        - That is because the pipe operator works by comparing everything that is to its left (digit whitespace cat) with everything to the right, dog.
        - In order to solve this, we can use alternation. 
            - In simpler terms, we can use parentheses again to group the optional characters:
            
            - my_string = "I want to have a pet. But I don't know if I want 2 cats, 1 dog or a bird."
            - re.findall(r"\d+\s(cat|dog|bird)", my_string) - returns: ['cat', 'dog']
            
            In the code, now the parentheses are added to group cat or dog or bird.
        
        - In the previous example, we may also want to match the number. 
        - In that case, we need to place parentheses to capture the digit group:
        
            - my_string = "I want to have a pet. But I don't know if I want 2 cats, 1 dog or a bird."
            - re.findall(r"(\d)+\s(cat|dog|bird)", my_string) - returns: [('2', 'cat'), ('1', 'dog')]
        
            - In the code, we now use two pair of parentheses and we use findall in the string, so we get a list with two tuples.
        
    - Non-capturing groups
        - Sometimes, we need to group characters using parentheses, but we are not going to reference back to this group. 
        - For these cases, there are a special type of groups called non-capturing groups. 
        - For using them, we just need to add question mark colon inside the parenthesis but before the regex.
        
        regex = r"(?:regex)"
        
        - Example: we have the following string, and we want to find all matches of numbers. 
        
            my_string = "John Smith: 34-34-34-042-980, Rebeca Smith: 10-10-10-434-425"
        
        - We see that the pattern consists of two numbers and dash repeated three times. After that, three numbers, dash, four numbers. 
        - We want to extract only the last part, without the first repeated elements. 
        - We need to group the first two elements to indicate repetitions, but we do not want to capture them. 
        - So, we use non-capturing groups to group \d repeated two times and dash. Then we indicate this group should be repeated three times. Then, we group \d repeated three times, dash, \d repeated three times:
        
            re.findall(r"(?:\d{2}-){3}(\d{3}-\d{3})", my_string) - returns: ['042-980', '434-425']
        
    - Alternation
        - We can combine non-capturing groups and alternation together. 
        - Remember that alternation implies using parentheses and the pipe operand to group optional characters. 
        - Let's suppose that we have the following string. We want to match all the numbers of the day. 
        
            my_date = "Today is 23rd May 2019. Tomorrow is 24th May 19."
        
        - We know that they are followed by 'th' or 'rd', but we only want to capture the number, and not the letters that follow it. 
        - We write our regex to capture inside parentheses \d repeated once or more times. Then, we can use a non-capturing group. 
        - Inside, we use the pipe operator to choose between 'th' or 'rd':
        
            re.findall(r"(\d+)(?:th|rd)", my_date) - returns: ['23', '24']

    - Non-capturing groups are very often used together with alternation. 
    - Sometimes, you have optional patterns and you need to group them. 
    - However, you are not interested in keeping them. It's a nice feature of regex.

    Examples of regex:

    1. Sentiment analysis project: firstly, you want to identify positive tweets about movies and concerts.
    - You plan to find all the sentences that contain the words 'love', 'like', or 'enjoy', and capture that word. 
    - You will limit the tweets by focusing on those that contain the words 'movie' or 'concert' by keeping the word in another group. 
    - You will also save the movie or concert name.
        - For example, if you have the sentence: 'I love the movie Avengers', you match and capture 'love'. 
        - You need to match and capture 'movie'. Afterwards, you match and capture anything until the dot.
        - The list sentiment_analysis contains the text of tweets.
    - Regular expression to capture the words 'love', 'like', or 'enjoy'; 
        - match and capture the words 'movie' or 'concert'; 
        - match and capture anything appearing until the '.'.

        regex_positive = r"(love|like|enjoy).+?(movie|concert)\s(.+?)\."

        - The pipe operator works by comparing everything that is to its left with everything to the right. 
        - Grouping optional patterns is the way to get the correct result.

    2. After finding positive tweets, you want to do it for negative tweets. 
    - Your plan now is to find sentences that contain the words 'hate', 'dislike' or 'disapprove'. 
    - You will again save the movie or concert name. 
    - You will get the tweet containing the words 'movie' or 'concert', but this time, you do not plan to save the word.
        - For example, if you have the sentence: 'I dislike the movie Avengers a lot.', you match and capture 'dislike'. 
        - You will match, but not capture, the word 'movie'. Afterwards, you match and capture anything until the dot.
    - Regular expression to capture the words 'hate', 'dislike' or 'disapprove'; 
        - Match, but do not capture, the words 'movie' or 'concert'; 
        - Match and capture anything appearing until the '.'.
        
        regex_negative = r"(hate|dislike|disapprove).+?(?:movie|concert)\s(.+?)\."
            
            """

        # regex backreferences
        self.help_text_7 = """
    Backreferences
    - How we can backreference capturing groups.

    Numbered groups
    - Imagine we come across this text, and we want to extract the date: 
        
        text = "Python 3.0 was released on 12-03-2008. It was a major revision of the language. Many of its major features were backported to Python 2.6.x and 2.7.x version series."
        
    - We want to extract only the numbers. So, we can place parentheses in a regex to capture these groups:
        
        regex = r"(\d{1,2})-(\d{1,2})-(\d{4})"

    - We have also seen that each of these groups receive a number. 
    - The whole expression is group 0; the first group, 1; and so on.

    - Let's use .search to match the pattern to the text. 
    - To retrieve the groups captured, we can use the method .group specifying the number of a group we want. 

    Again: .group method retrieves the groups captured.
        - Syntax: searched_string = re.search(r"regex", string)
        re.group(N) - returns N-th group captured (group 0 is the regex itself).

    Example: text = "Python 3.0 was released on 12-03-2008."

        information = re.search('(\d{1,2})-(\d{2})-(\d{4})', text)
        information.group(3) - returns: '2008'
        information.group(0) - returns: '12-03-2008' (regex itself, the entire expression).

    - .group can only be used with .search and .match methods.

    Named groups
    - We can also give names to our capturing groups. 
    - Inside the parentheses, we write '?P', and the name inside angle brackets:

        regex = r"(?P<name>regex)"

    - Let's say we have the following string, and we want to match the name of the city and zipcode in different groups. 
    - We can use capturing groups and assign them the name 'city' and 'zipcode'. 
    - We retrieve the information by using .group, and we indicate the name of the group. 
        
        text = "Austin, 78701"
        cities = re.search(r"(?P<city>[A-Za-z]+).*?(?P<zipcode>\d{5})", text)
        cities.group("city") - returns: 'Austin'
        cities.group("zipcode") - returns: '78701'

    Backreferences
    - There is another way to backreference groups. 
    - In fact, the matched group can be reused inside the same regex or outside for substitution. 
    - We can do this using backslash and the number of the group:

        regex = r'(\d{1,2})-(\d{2})-(\d{4})'
        
        - we can backreference the groups as:
            (\d{1,2}): (\1);
            (\d{2}): (\2)
            (\d{4}): (\3)

    - Example: we have the following string, and we want to find all matches of repeated words. 
    - In the code, we specify that we want to capture a sequence of word characters, then a whitespace.
    - Finally, we write \1. This will indicate that we want to match the first group captured again. 
    - In other words, it says: 'match that sequence of characters that was previously captured once more.' 
        
        sentence = "I wish you a happy happy birthday!"
        re.findall(r"(\w+)\s\1", sentence) - returns: ['happy'] 

    - We get the word 'happy' as an output: this was the repeated word in our string.

    - Now, we want to replace the repeated word with one occurrence of the same word. 
    - In the code, we use the same regex as before, but this time, we use the .sub method. 
    - In the replacement part, we can also reference back to the captured group: 
        - We write r"\1" to say: 'replace the entire expression match with the first captured group.' 
        
        re.sub(r"(\w+)\s\1", r"\1", sentence) - returns: 'I wish you a happy birthday!'
        - In the output string, we have only one occurrence of the word 'happy'.
        
    - We can also use named groups for backreferencing. 
    - To do this, we use ?P= the group name. 

        regex = r"(?P=name)"

    Example:
        sentence = "Your new code number is 23434. Please, enter 23434 to open the door."
        re.findall(r"(?P<code>\d{5}).*?(?P=code)", sentence) - returns: ['23434']

    - In the code, we want to find all matches of the same number. 
    - We use a capturing group and name it 'code'. 
    - Later, we reference back to this group, and we obtain the number as an output.

    - To reference the group back for replacement, we need to use \g and the group name inside angle brackets. 

        regex = r"(\g<name>)"

    Example:
        sentence = "This app is not working! It's repeating the last word word."
        re.sub(r"(?P<word>\w+)\s(?P=word)", r"\g<word>", sentence) - returns: 'This app is not working! It's repeating the last word.'
        
    - In the code, we want to replace repeated words by one occurrence of the same word. 
    - Inside the regex, we use the previous syntax. 
    - In the replacement field, we need to use this new syntax as seen in the code.
    - Backreferences are very helpful when you need to reuse part of the regex match inside the regex.
    - You should remember that the group zero stands for the entire expression matched. 
        - It is always helpful to keep that in mind. Sometimes you will need to use it.

    Examples of regex:

    1. Parsing PDF files: your company gave you some PDF files of signed contracts. The goal of the project is to create a database with the information you parse from them. 
    - Three of these columns should correspond to the day, month, and year when the contract was signed.
    - The dates appear as 'Signed on 05/24/2016' ('05' indicating the month, '24' the day). 
    - You decide to use capturing groups to extract this information. Also, you would like to retrieve that information so you can store it separately in different variables.
    - The variable contract contains the text of one contract.

    - Write a regex that captures the month, day, and year in which the contract was signed. 
    - Scan contract for matches.
    - Assign each captured group to the corresponding keys in the dictionary.
    - Complete the positional method to print out the captured groups. 
    - Use the values corresponding to each key in the dictionary.

        # Write regex and scan contract to capture the dates described
        regex_dates = r"Signed\son\s(\d{2})/(\d{2})/(\d{4})"
        dates = re.search(regex_dates, contract)

        # Assign to each key the corresponding match
        signature = {
            "day": dates.group(2),
            "month": dates.group(1),
            "year": dates.group(3)
        }
        # Complete the format method to print-out
        print("Our first contract is dated back to {data[year]}. Particularly, the day {data[day]} of the month {data[month]}.".format(data=signature))

    - Remember that each capturing group is assigned a number according to its position in the regex. 
    - Only if you use .search() and .match(), you can use .group() to retrieve the groups.

    2. The company is going to develop a new product which will help developers automatically check the code they are writing. 
    - You need to write a short script for checking that every HTML tag that is open has its proper closure.
    - You have an example of a string containing HTML tags: "<title>The Data Science Company</title>"
    - You learn that an opening HTML tag is always at the beginning of the string, and appears inside "<>". 
    - A closing tag also appears inside "<>", but it is preceded by "/".
    - The list html_tags, contains strings with HTML tags.

    - Regex to match closed HTML tags: find if there is a match in each string of the list html_tags. Assign the result to match_tag;
        - If a match is found, print the first group captured and saved in match_tag;
    - If no match is found, regex to match only the text inside the HTML tag. Assign it to notmatch_tag.
        - Print the first group captured by the regex and save it in notmatch_tag.
        - To capture the text inside <>, place parenthesis around the expression: r"<(text)>. To confirm that the same text appears in the closing tag, reference back to the m group captured by using '\m'.
        - To print the 'm' group captured, use .group(m).

        for string in html_tags:
            # Complete the regex and find if it matches a closed HTML tags
            match_tag =  re.match(r"<(\w+)>.*?</\1>", string)

            if match_tag:
                # If it matches print the first group capture
                print("Your tag {} is closed".format(match_tag.group(1))) 
            else:
                # If it doesn't match capture only the tag 
                notmatch_tag = re.match(r"<(\w+)>",string)
                # Print the first group capture
                print("Close your {} tag!".format(notmatch_tag.group(1)))

    3. Your task is to replace elongated words that appear in the tweets. 
    - We define an elongated word as a word that contains a repeating character twice or more times. 
        - e.g. "Awesoooome".
    - Replacing those words is very important since a classifier will treat them as a different term from the source words, lowering their frequency.
    - To find them, you will use capturing groups and reference them back using numbers. E.g \4.
    - If you want to find a match for 'Awesoooome', you firstly need to capture 'Awes'. 
        - Then, match 'o' and reference the same character back, and then, 'me'.
    - The list sentiment_analysis contains the text tweets.
    - Regular expression to match an elongated word as described.
    - Search the elements in sentiment_analysis list to find out if they contain elongated words. Assign the result to match_elongated.
    - Assign the captured group number zero to the variable elongated_word.
        - Print the result contained in the variable elongated_word.

        # Complete the regex to match an elongated word
        regex_elongated = r"\w*(\w)\1*me\w*"

        for tweet in sentiment_analysis:
            # Find if there is a match in each tweet 
            match_elongated = re.search(regex_elongated, tweet)

            if match_elongated:
                # Assign the captured group zero 
                elongated_word = match_elongated.group(0)

                # Complete the format method to print the word
                print("Elongated word found: {word}".format(word=elongated_word))
            else:
                print("No elongated word found") 

            """
        
        # regex lookaround
        self.help_text_8 = """
    Lookaround
    - There are specific types of non-capturing groups that help us look around an expression.
    - Look-around will look for what is behind or ahead of a pattern. 
    - Imagine that we have the following string:
        
        text = "the white cat sat on the chair"

    - We want to see what is surrounding a specific word. 
    - For example, we position ourselves in the word 'cat'. 
    - So look-around will let us answer the following problem: 
        - At my current position, look ahead and search if 'sat' is there. 
        - Or, look behind and search if 'white' is there.
        
    - In other words, looking around allows us to confirm that a sub-pattern is ahead or behind the main pattern.
    - "At my current position in the matching process, look ahead or behind and examine whether some pattern matches or not match before continuing."
    - In the previous example, we are looking for the word 'cat'. 
    - The look ahead expression can be either positive or negative. For positive we use ?=. For negative, ?!.
        - positive: (?=sat)
        - negative: (?!run)

    - Look-ahead
    - This non-capturing group checks whether the first part of the expression is followed or not by the lookahead expression. 
    - As a consequence, it will return the first part of the expression. 
        - Let's imagine that we have a string containing file names and the status of that file. 
        - We want to extract only those files that are followed by the word 'transferred'. 
        - So we start building the regex by indicating any word character followed by .txt.
        - We now indicate we want the first part to be followed by the word transferred. 
        - We do so by writing ?= and then whitespace transferred all inside the parenthesis:
        
        my_text ="tweets.txt transferred, mypass.txt transferred, keywords.txt error"
        re.findall(r"\w+\.txt(?=\stransferred)", my_text) - returns: ['tweets.txt', 'mypass.txt']

    - Negative look-ahead
        - Now, let's use negative lookahead in the same example.
        - In this case, we will say that we want those matches that are NOT followed by the expression 'transferred'. 
        - We use, instead, ?! inside parenthesis:

        my_text = "tweets.txt transferred, mypass.txt transferred, keywords.txt error"
        re.findall(r"\w+\.txt(?!\stransferred)", my_text) - returns: ['keywords.txt']

    - Look-behind
    - The non-capturing group look-behind gets all matches that are preceded or not by a specific pattern.
    - As a consequence, it will return the matches after the look expression.
    - Look behind expression can also be either positive or negative. 
        - For positive, we use ?<=. For negative, ?<!.
        - So, we add an intermediate '<' (angle bracket) sign. In the previous example, we can look before the word 'cat': 
            - positive: (?<=white)
            - negative: (?<!brown)
        
    - Positive look-behind
        - Let's look at the following string, in which we want to find all matches of the names that are preceded by the word 'member'. 
        - We construct our regex with positive look-behind. 
        - At the end of the regex, we indicate that we want a sequence of word characters whitespace another sequence of word characters:
        
        my_text = "Member: Angus Young, Member: Chris Slade, Past: Malcolm Young, Past: Cliff Williams."
        re.findall(r"(?<=Member:\s)\w+\s\w+", my_text) - returns: ['Angus Young', 'Chris Slade']
        
        - Pay attention to the code: the look-behind expression goes before that expression. 
        - We indicate ?<= followed by member, colon, and whitespace. All inside parentheses. 
        - In that way we get the two names that were preceded by the word member, as shown in the output.

    - Negative look-behind
    - Now, we have other string, in which will use negative look-behind. 
    - We will find all matches of the word 'cat' or 'dog' that are not preceded by the word 'brown'. 
    - In this example, we use ?<!, followed by brown, whitespace. All inside the parenthesis. 
    - Then, we indicate our alternation group: 'cat' or 'dog'. 

        my_text = "My white cat sat at the table. However, my brown dog was lying on the couch."
        re.findall(r"(?<!brown\s)(cat|dog)", my_text) - returns: ['cat']

        - Consequently, we get 'cat' as an output, the 'cat' or 'dog' word that is not after the word 'brown'.

    In summary:
    - Positive lookahead (?=) makes sure that first part of the expression is followed by the lookahead expression. 
    - Positive lookbehind (?<=) returns all matches that are preceded by the specified pattern.
    - It is important to know that positive lookahead will return the text matched by the first part of the expression after asserting that it is followed by the lookahead expression,
        - while positive lookbehind will return all matches that follow a specific pattern.
    - Negative lookarounds work in a similar way to positive lookarounds. 
        - They are very helpful when we are looking to exclude certain patterns from our analysis.

    Examples of regex:

    1. You are interested in the words surrounding 'python'. You want to count how many times a specific words appears right before and after it.
    - The variable sentiment_analysis contains the text of one tweet.
    - Get all the words that are followed by the word 'python' in sentiment_analysis. 
    - Print out the word found.
        - In re.findall(). Use \w+ to match the words followed by the word 'python';
        - In re.findall() first argument, include \spython within parentheses to indicate that everything after the word 'python' should be matched.

        # Positive lookahead
        look_ahead = re.findall(r"\w+(?=\spython)", sentiment_analysis)

        # Print out
        print(look_ahead)
    
    1.2. Get all the words that are preceded by the word 'python' or 'Python' in sentiment_analysis. Print out the words found.
    - In re.findall() first argument, include [Pp]ython\s within parentheses to indicate that everything before the word 'python' (or 'Python') should be matched.

        # Positive lookbehind
        look_behind = re.findall(r"(?<=[pP]ython\s)\w+", sentiment_analysis)

        # Print out
        print(look_behind)

    2. You need to write a script for a cell-phone searcher. 
    - It should scan a list of phone numbers and return those that meet certain characteristics.
    - The phone numbers in the list have the structure:
        - Optional area code: 3 numbers
        - Prefix: 4 numbers
        - Line number: 6 numbers
        - Optional extension: 2 numbers
        - E.g. 654-8764-439434-01.
    - You decide to use .findall() and the non-capturing group's negative lookahead (?!) and negative lookbehind (?<!).
    - The list cellphones, contains three phone numbers:
        cellphones = ['4564-646464-01', '345-5785-544245', '6476-579052-01']

    - Get all cell phones numbers that are not preceded by the optional area code.
        - In re.findall() first argument, you use a negative lookbehind ?<! within parentheses () indicating the optional area code.

        for phone in cellphones:
            # Get all phone numbers not preceded by area code
            number = re.findall(r"(?<!\d{3}-)\d{4}-\d{6}-\d{2}", phone)
            print(number)
    
    2.1. Get all the cell phones numbers that are not followed by the optional extension.
        - In re.findall() first argument, you use a negative lookahead ?! within parentheses () indicating the optional extension.

        for phone in cellphones:
            # Get all phone numbers not followed by optional extension
            number = re.findall(r"\d{3}-\d{4}-\d{6}(?!-\d{2})", phone)
            print(number)
        
            """
        
    def show_screen (self):
            
        helper_screen = self.helper_screen
        helper_menu_1 = self.helper_menu_1
            
        if (helper_screen == 0):
                
            # Start screen
            print(self.helper_menu_1)
            print("\n")
            # For the input, strip all whitespaces and, and so convert it to integer:
            helper_screen = int(str(input("Next screen:")).strip())
                
            # the object.__dict__ method returns all attributes from an object as a dictionary.
            # Analogously, the vars function applied to an object vars(object) returns the same
            # dictionary. We can access an attribute from the object by passing the key of this
            # dictionary:
            # vars(object)['key']
                
            while (helper_screen != 10):
                    
                if (helper_screen not in range(0, 11)):
                    # range (0, 11): integers from 0 to 10
                        
                    helper_screen = int(str(input("Input a valid number, from 0 to 10:")).strip())
                    
                else:
                        
                    if (helper_screen == 9):
                        # print all at once:
                        for screen_number in range (1, 9):
                            # integers from 1 to 8
                            key = "help_text_" + str(screen_number)
                            # apply the vars function to get the dictionary of attributes, and call the
                            # attribute by passing its name as key from the dictionary:
                            screen_text = vars(self)[key]
                            # Notice that we cannot directly call the attribute as a string. We would have to
                            # create an if else for each of the 8 attributes.
                            print(screen_text)
                            
                        # Now, make helper_screen = 10 for finishing this step:
                        helper_screen = 10
                        
                    else:
                        key = "help_text_" + str(helper_screen)
                        screen_text = vars(self)[key]
                        print(screen_text)
                        helper_screen = int(str(input("Next screen:")).strip())
            
        print("Finishing regex assistant.\n")
            
        return self


@dataclass
class text_extraction:


    def trim_spaces_or_characters (string_or_list_of_strings, new_variable_type = None, method = 'trim', substring_to_eliminate = None):
        
        import numpy as np
        
        # string_or_list_of_strings: string or list of strings (inside quotes), 
        # that will be analyzed. 
        # e.g. string_or_list_of_strings = "column1" will analyze 'column1', whereas 
        # string_or_list_of_strings = ['col1', 'col2'] will process both 'col1' and 'col2'.
        
        # new_variable_type = None. String (in quotes) that represents a given data type for the variables
        # after transformation. Set:
        # - new_variable_type = 'int' to convert the column to integer type after the transform;
        # - new_variable_type = 'float' to convert the column to float (decimal number);
        # - new_variable_type = 'datetime' to convert it to date or timestamp;
        
        # method = 'trim' will eliminate trailing and leading white spaces from the strings in
        # column_to_analyze.
        # method = 'substring' will eliminate a defined trailing and leading substring from
        # column_to_analyze.
        
        # substring_to_eliminate = None. Set as a string (in quotes) if method = 'substring'.
        # e.g. suppose column_to_analyze contains time information: each string ends in " min":
        # "1 min", "2 min", "3 min", etc. If substring_to_eliminate = " min", this portion will be
        # eliminated, resulting in: "1", "2", "3", etc. If new_variable_type = None, these values will
        # continue to be strings. By setting new_variable_type = 'int' or 'float', the series will be
        # converted to a numeric type.
        
        
        # Check if a string was passed. If it was, convert it to list of single element:
        if (type(string_or_list_of_strings) == str):
            list_of_strings = [string_or_list_of_strings]
        
        else: # simply convert the iterable to the new standard name:
            list_of_strings = list(string_or_list_of_strings)
        
        # Now, we have a local copy as a list.
        # As we are dealing with strings and not Pandas dataframes, we do not call the str attribute.
        
        if (method == 'substring'):
            
            if (substring_to_eliminate is None):
                
                method = 'trim'
                print("No valid substring input. Modifying method to \'trim\'.\n")
        
        if (method == 'substring'):
            
            print("ATTENTION: Operations of string strip (removal) or replacement are all case-sensitive. There must be correct correspondence between cases and spaces for the strings being removed or replaced.\n")
            
            new_series = [string.strip(substring_to_eliminate) for string in list_of_strings]
        
        else:
            
            new_series = [string.strip() for string in list_of_strings]
        
        # Check if a the series type should be modified:
        if (new_variable_type is not None):
            # try converting the type:
            try:
                if (new_variable_type == 'int'):

                    new_series = np.int64(new_series)

                elif (new_variable_type == 'float'):

                    new_series = np.float64(new_series)

                elif (new_variable_type == 'datetime'):

                    new_series = np.datetime64(new_series)
            
                print(f"Successfully converted the strings to the type {new_variable_type}.\n")
            
            except:
                pass

        # Now, we are in the main code.
        print("Finished removing leading and trailing spaces or characters (substrings).")
        print("Check the 10 first strings:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(new_series[:10])
                
        except: # regular mode
            print(new_series[:10])
        
        return new_series


    def capitalize_or_lower_string_case (string_or_list_of_strings, method = 'lowercase'):
        
        import numpy as np
        
        # string_or_list_of_strings: string or list of strings (inside quotes), 
        # that will be analyzed. 
        # e.g. string_or_list_of_strings = "column1" will analyze 'column1', whereas 
        # string_or_list_of_strings = ['col1', 'col2'] will process both 'col1' and 'col2'.
        
        # method = 'capitalize' will capitalize all letters from the input string 
        # (turn them to upper case).
        # method = 'lowercase' will make the opposite: turn all letters to lower case.
        # e.g. suppose string_or_list_of_strings contains strings such as 'String One', 'STRING 2',  and
        # 'string3'. If method = 'capitalize', the output will contain the strings: 
        # 'STRING ONE', 'STRING 2', 'STRING3'. If method = 'lowercase', the outputs will be:
        # 'string one', 'string 2', 'string3'.
        
        
        # Check if a string was passed. If it was, convert it to list of single element:
        if (type(string_or_list_of_strings) == str):
            list_of_strings = [string_or_list_of_strings]
        
        else: # simply convert the iterable to the new standard name:
            list_of_strings = list(string_or_list_of_strings)
        
        # Now, we have a local copy as a list.
        # As we are dealing with strings and not Pandas dataframes, we do not call the str attribute.
        
        if (method == 'capitalize'):
            
            print("Capitalizing the string (moving all characters to upper case).\n")
            new_series = [string.upper() for string in list_of_strings]
        
        else:
            
            print("Lowering the string case (moving all characters to lower case).\n")
            new_series = [string.lower() for string in list_of_strings]
        
        # Now, we are in the main code.
        print(f"Finished homogenizing the string cases, giving value consistency.")
        print("Check the 10 first strings:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(new_series[:10])
                
        except: # regular mode
            print(new_series[:10])
        
        return new_series


    def add_contractions_to_library (list_of_contractions = [{'contracted_expression': None, 'correct_expression': None}, {'contracted_expression': None, 'correct_expression': None}, {'contracted_expression': None, 'correct_expression': None}, {'contracted_expression': None, 'correct_expression': None}]):
        
        import contractions
        # contractions library: https://github.com/kootenpv/contractions
        
        # list_of_contractions = 
        # [{'contracted_expression': None, 'correct_expression': None}]
        # This is a list of dictionaries, where each dictionary contains two key-value pairs:
        # the first one contains the form as the contraction is usually observed; and the second one 
        # contains the correct (full) string that will replace it.
        # Since contractions can cause issues when processing text, we can expand them with these functions.
        
        # The object list_of_contractions must be declared as a list, 
        # in brackets, even if there is a single dictionary.
        # Use always the same keys: 'contracted_expression' for the contraction; and 'correct_expression', 
        # for the strings with the correspondent correction.
        
        # If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
        # and you can also add more elements (dictionaries) to the lists, if you want to add more elements
        # to the contractions library.
        # Simply put a comma after the last element from the list and declare a new dictionary, keeping the
        # same keys: {'contracted_expression': original_str, 'correct_expression': new_str}, 
        # where original_str and new_str represent the contracted and expanded strings
        # (If one of the keys contains None, the new dictionary will be ignored).
        
        # Example:
        # list_of_contractions = [{'contracted_expression': 'mychange', 'correct_expression': 'my change'}]
        
        
        for dictionary in list_of_contractions:
            
            contraction = dictionary['contracted_expression']
            correction = dictionary['correct_expression']
            
            if ((contraction is not None) & (correction is not None)):
        
                contractions.add(contraction, correction)
                print(f"Successfully included the contracted expression {contraction} to the contractions library.")

        print("Now, the function for contraction correction will be able to process it within the strings.\n")


    def correct_contracted_strings (string_or_list_of_strings):
        
        import numpy as np
        import contractions
        
        # contractions library: https://github.com/kootenpv/contractions
        
        # string_or_list_of_strings: string or list of strings (inside quotes), 
        # that will be analyzed. 
        # e.g. string_or_list_of_strings = "column1" will analyze 'column1', whereas 
        # string_or_list_of_strings = ['col1', 'col2'] will process both 'col1' and 'col2'.
        
        # Check if a string was passed. If it was, convert it to list of single element:
        if (type(string_or_list_of_strings) == str):
            list_of_strings = [string_or_list_of_strings]
        
        else: # simply convert the iterable to the new standard name:
            list_of_strings = list(string_or_list_of_strings)
        
        # Now, we have a local copy as a list.
        # As we are dealing with strings and not Pandas dataframes, we do not call the str attribute.
        
        # Contractions operate at one string at once:
        correct_contractions_list = [contractions.fix(string, slang = True) for string in list_of_strings]

        # Now, we are in the main code.
        print(f"Finished correcting the contracted strings.")
        print("Check the 10 first strings:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(correct_contractions_list[:10])
                
        except: # regular mode
            print(correct_contractions_list[:10])
        
        return correct_contractions_list


    def replace_substring (string_or_list_of_strings, substring_to_be_replaced = None, new_substring_for_replacement = ''):
        
        import numpy as np
        
        # string_or_list_of_strings: string or list of strings (inside quotes), 
        # that will be analyzed. 
        # e.g. string_or_list_of_strings = "column1" will analyze 'column1', whereas 
        # string_or_list_of_strings = ['col1', 'col2'] will process both 'col1' and 'col2'.
        
        # substring_to_be_replaced = None; new_substring_for_replacement = ''. 
        # Strings (in quotes): when the sequence of characters substring_to_be_replaced was
        # found in the strings from column_to_analyze, it will be substituted by the substring
        # new_substring_for_replacement. If None is provided to one of these substring arguments,
        # it will be substituted by the empty string: ''
        # e.g. suppose column_to_analyze contains the following strings, with a spelling error:
        # "my collumn 1", 'his collumn 2', 'her column 3'. We may correct this error by setting:
        # substring_to_be_replaced = 'collumn' and new_substring_for_replacement = 'column'. The
        # function will search for the wrong group of characters and, if it finds it, will substitute
        # by the correct sequence: "my column 1", 'his column 2', 'her column 3'.
        
        
        # Check if a string was passed. If it was, convert it to list of single element:
        if (type(string_or_list_of_strings) == str):
            list_of_strings = [string_or_list_of_strings]
        
        else: # simply convert the iterable to the new standard name:
            list_of_strings = list(string_or_list_of_strings)
        
        # Now, we have a local copy as a list.
        # As we are dealing with strings and not Pandas dataframes, we do not call the str attribute.
        
        print("ATTENTION: Operations of string strip (removal) or replacement are all case-sensitive. There must be correct correspondence between cases and spaces for the strings being removed or replaced.\n")
            
        # If one of the input substrings is None, make it the empty string:
        if (substring_to_be_replaced is None):
            substring_to_be_replaced = ''
        
        if (new_substring_for_replacement is None):
            new_substring_for_replacement = ''
        
        # Guarantee that both were read as strings (they may have been improperly read as 
        # integers or floats):
        substring_to_be_replaced = str(substring_to_be_replaced)
        new_substring_for_replacement = str(new_substring_for_replacement)
        
        new_series = [string.replace(substring_to_be_replaced, new_substring_for_replacement) for string in list_of_strings]
        
        # Now, we are in the main code.
        print(f"Finished replacing the substring {substring_to_be_replaced} by {new_substring_for_replacement}.")
        print("Check the 10 first strings:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(new_series[:10])
                
        except: # regular mode
            print(new_series[:10])
        
        return new_series


    def invert_strings (string_or_list_of_strings):
        
        import numpy as np
        
        # string_or_list_of_strings: string or list of strings (inside quotes), 
        # that will be analyzed. 
        # e.g. string_or_list_of_strings = "column1" will analyze 'column1', whereas 
        # string_or_list_of_strings = ['col1', 'col2'] will process both 'col1' and 'col2'.
        
        
        # Check if a string was passed. If it was, convert it to list of single element:
        if (type(string_or_list_of_strings) == str):
            list_of_strings = [string_or_list_of_strings]
        
        else: # simply convert the iterable to the new standard name:
            list_of_strings = list(string_or_list_of_strings)
        
        # Now, we have a local copy as a list.
        # As we are dealing with strings and not Pandas dataframes, we do not call the str attribute.
        
        # Pandas slice: start from -1 (last character) and go to the last element with -1 step
        # walk through the string 'backwards':
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.slice.html
        
        new_series = [string[::-1] for string in list_of_strings]
        

        # Now, we are in the main code.
        print(f"Finished inversion of the strings.")
        print("Check the 10 first strings:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(new_series[:10])
                
        except: # regular mode
            print(new_series[:10])
        
        return new_series


    def slice_strings (string_or_list_of_strings, first_character_index = None, last_character_index = None, step = 1):
        
        import numpy as np
        
        # string_or_list_of_strings: string or list of strings (inside quotes), 
        # that will be analyzed. 
        # e.g. string_or_list_of_strings = "column1" will analyze 'column1', whereas 
        # string_or_list_of_strings = ['col1', 'col2'] will process both 'col1' and 'col2'.
        
        # first_character_index = None - integer representing the index of the first character to be
        # included in the new strings. If None, slicing will start from first character.
        # Indexing of strings always start from 0. The last index can be represented as -1, the index of
        # the character before as -2, etc (inverse indexing starts from -1).
        # example: consider the string "idsw", which contains 4 characters. We can represent the indices as:
        # 'i': index 0; 'd': 1, 's': 2, 'w': 3. Alternatively: 'w': -1, 's': -2, 'd': -3, 'i': -4.
        
        # last_character_index = None - integer representing the index of the last character to be
        # included in the new strings. If None, slicing will go until the last character.
        # Attention: this is effectively the last character to be added, and not the next index after last
        # character.
        
        # in the 'idsw' example, if we want a string as 'ds', we want the first_character_index = 1 and
        # last_character_index = 2.
        
        # step = 1 - integer representing the slicing step. If step = 1, all characters will be added.
        # If step = 2, then the slicing will pick one element of index i and the element with index (i+2)
        # (1 index will be 'jumped'), and so on.
        # If step is negative, then the order of the new strings will be inverted.
        # Example: step = -1, and the start and finish indices are None: the output will be the inverted
        # string, 'wsdi'.
        # first_character_index = 1, last_character_index = 2, step = 1: output = 'ds';
        # first_character_index = None, last_character_index = None, step = 2: output = 'is';
        # first_character_index = None, last_character_index = None, step = 3: output = 'iw';
        # first_character_index = -1, last_character_index = -2, step = -1: output = 'ws';
        # first_character_index = -1, last_character_index = None, step = -2: output = 'wd';
        # first_character_index = -1, last_character_index = None, step = 1: output = 'w'
        # In this last example, the function tries to access the next element after the character of index
        # -1. Since -1 is the last character, there are no other characters to be added.
        # first_character_index = -2, last_character_index = -1, step = 1: output = 'sw'.
        
        
        # Check if a string was passed. If it was, convert it to list of single element:
        if (type(string_or_list_of_strings) == str):
            list_of_strings = [string_or_list_of_strings]
        
        else: # simply convert the iterable to the new standard name:
            list_of_strings = list(string_or_list_of_strings)
        
        # Now, we have a local copy as a list.
        # As we are dealing with strings and not Pandas dataframes, we do not call the str attribute.
        
        if (step is None):
            # set as 1
            step = 1
        
        if (last_character_index is not None):
            if (last_character_index == -1):
                # In this case, we cannot sum 1, because it would result in index 0 (1st character).
                # So, we will proceed without last index definition, to stop only at the end.
                last_character_index = None
        
        # Now, make the checking again:
                
        if ((first_character_index is None) & (last_character_index is None)):
            
            new_series = [string[::step] for string in list_of_strings]
            
        elif (first_character_index is None):
            # Only this is None:
            new_series = [string[:(last_character_index + 1):step] for string in list_of_strings]
            
        elif (last_character_index is None):
            new_series = [string[first_character_index::step] for string in list_of_strings]
        
        else:
            new_series = [string[first_character_index:(last_character_index + 1):step] for string in list_of_strings]
            
        # Slicing from index i to index j includes index i, but does not include 
        # index j (ends in j-1). So, we add 1 to the last index to include it.
        # automatically included.

        # Now, we are in the main code.
        print(f"Finished slicing the strings from character {first_character_index} to character {last_character_index}.")
        print("Check the 10 first strings:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(new_series[:10])
                
        except: # regular mode
            print(new_series[:10])
        
        return new_series


    def left_characters (string_or_list_of_strings, number_of_characters_to_retrieve = 1, new_variable_type = None):
        
        import numpy as np
        
        # string_or_list_of_strings: string or list of strings (inside quotes), 
        # that will be analyzed. 
        # e.g. string_or_list_of_strings = "column1" will analyze 'column1', whereas 
        # string_or_list_of_strings = ['col1', 'col2'] will process both 'col1' and 'col2'.
        
        # number_of_characters_to_retrieve = 1 - integer representing the total of characters that will
        # be retrieved. Here, we will retrieve the leftest characters. If number_of_characters_to_retrieve = 1,
        # only the leftest (last) character will be retrieved.
        # Consider the string 'idsw'.
        # number_of_characters_to_retrieve = 1 - output: 'w';
        # number_of_characters_to_retrieve = 2 - output: 'sw'.
        
        # new_variable_type = None. String (in quotes) that represents a given data type for the column
        # after transformation. Set:
        # - new_variable_type = 'int' to convert the extracted column to integer;
        # - new_variable_type = 'float' to convert the column to float (decimal number);
        # - new_variable_type = 'datetime' to convert it to date or timestamp;
    
        # So, if the last part of the strings is a number, you can use this argument to directly extract
        # this part as numeric variable.
        
        
        # Check if a string was passed. If it was, convert it to list of single element:
        if (type(string_or_list_of_strings) == str):
            list_of_strings = [string_or_list_of_strings]
        
        else: # simply convert the iterable to the new standard name:
            list_of_strings = list(string_or_list_of_strings)
        
        # Now, we have a local copy as a list.
        # As we are dealing with strings and not Pandas dataframes, we do not call the str attribute.
        
        # Pandas slice:
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.slice.html
        
        if (number_of_characters_to_retrieve is None):
            # set as 1
            number_of_characters_to_retrieve = 1
        
        # last_character_index = -1 would be the index of the last character.
        # If we want the last N = 2 characters, we should go from index -2 to -1, -2 = -1 - (N-1);
        # If we want the last N = 3 characters, we should go from index -3 to -1, -2 = -1 - (N-1);
        # If we want only the last (N = 1) character, we should go from -1 to -1, -1 = -1 - (N-1).
        
        # N = number_of_characters_to_retrieve
        first_character_index = -1 - (number_of_characters_to_retrieve - 1)
        
        # Perform the slicing without setting the limit, to slice until the end of the string:
        new_series = [string[first_character_index:] for string in list_of_strings]
        # If no step is specified, step = 1
        
        # Check if a the series type should be modified:
        if (new_variable_type is not None):
            # try converting the type:
            try:
                if (new_variable_type == 'int'):

                    new_series = np.int64(new_series)

                elif (new_variable_type == 'float'):

                    new_series = np.float64(new_series)

                elif (new_variable_type == 'datetime'):

                    new_series = np.datetime64(new_series)
            
                print(f"Successfully converted the strings to the type {new_variable_type}.\n")
            
            except:
                pass
        
        
        # Now, we are in the main code.
        print(f"Finished extracting the {number_of_characters_to_retrieve} leftest characters.")
        print("Check the 10 first strings:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(new_series[:10])
                
        except: # regular mode
            print(new_series[:10])
        
        return new_series


    def right_characters (string_or_list_of_strings, number_of_characters_to_retrieve = 1, new_variable_type = None):
        
        import numpy as np
        
        # string_or_list_of_strings: string or list of strings (inside quotes), 
        # that will be analyzed. 
        # e.g. string_or_list_of_strings = "column1" will analyze 'column1', whereas 
        # string_or_list_of_strings = ['col1', 'col2'] will process both 'col1' and 'col2'.
        
        # number_of_characters_to_retrieve = 1 - integer representing the total of characters that will
        # be retrieved. Here, we will retrieve the rightest characters. If number_of_characters_to_retrieve = 1,
        # only the rightest (first) character will be retrieved.
        # Consider the string 'idsw'.
        # number_of_characters_to_retrieve = 1 - output: 'i';
        # number_of_characters_to_retrieve = 2 - output: 'id'.
        
        # new_variable_type = None. String (in quotes) that represents a given data type for the column
        # after transformation. Set:
        # - new_variable_type = 'int' to convert the extracted column to integer;
        # - new_variable_type = 'float' to convert the column to float (decimal number);
        # - new_variable_type = 'datetime' to convert it to date or timestamp;
        
        # So, if the first part of the strings is a number, you can use this argument to directly extract
        # this part as numeric variable.
        
        
        # Check if a string was passed. If it was, convert it to list of single element:
        if (type(string_or_list_of_strings) == str):
            list_of_strings = [string_or_list_of_strings]
        
        else: # simply convert the iterable to the new standard name:
            list_of_strings = list(string_or_list_of_strings)
        
        # Now, we have a local copy as a list.
        # As we are dealing with strings and not Pandas dataframes, we do not call the str attribute.
        
        # Pandas slice:
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.slice.html
        
        if (number_of_characters_to_retrieve is None):
            # set as 1
            number_of_characters_to_retrieve = 1
        
        # first_character_index = 0 would be the index of the first character.
        # If we want the last N = 2 characters, we should go from index 0 to 1, 1 = (N-1);
        # If we want the last N = 3 characters, we should go from index 0 to 2, 2 = (N-1);
        # If we want only the last (N = 1) character, we should go from 0 to 0, 0 = (N-1).
        
        # N = number_of_characters_to_retrieve
        last_character_index = number_of_characters_to_retrieve - 1
        
        # Perform the slicing without setting the limit, to slice from the 1st character:
        new_series = [string[:(last_character_index + 1)] for string in list_of_strings]
        # If no step is specified, step = 1
        
        # Check if a the series type should be modified:
        if (new_variable_type is not None):
            # try converting the type:
            try:
                if (new_variable_type == 'int'):

                    new_series = np.int64(new_series)

                elif (new_variable_type == 'float'):

                    new_series = np.float64(new_series)

                elif (new_variable_type == 'datetime'):

                    new_series = np.datetime64(new_series)
            
                print(f"Successfully converted the strings to the type {new_variable_type}.\n")
            
            except:
                pass
        

        # Now, we are in the main code.
        print(f"Finished extracting the {number_of_characters_to_retrieve} rightest characters.")
        print("Check the 10 first strings:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(new_series[:10])
                
        except: # regular mode
            print(new_series[:10])
        
        return new_series


    def join_list_of_strings (string_or_list_of_strings, separator = " "):
        
        import numpy as np
        
        # string_or_list_of_strings: string or list of strings (inside quotes), 
        # that will be analyzed. 
        # e.g. string_or_list_of_strings = "column1" will analyze 'column1', whereas 
        # string_or_list_of_strings = ['col1', 'col2'] will process both 'col1' and 'col2'.
        
        # separator = " " - string containing the separator. Suppose the column contains the
        # strings: 'a', 'b', 'c', 'd'. If the separator is the empty string '', the output will be:
        # 'abcd' (no separation). If separator = " " (simple whitespace), the output will be 'a b c d'
        
        
        if (separator is None):
            # make it a whitespace:
            separator = " "
        
        # Check if a string was passed. If it was, convert it to list of single element:
        if (type(string_or_list_of_strings) == str):
            list_of_strings = [string_or_list_of_strings]
        
        else: # simply convert the iterable to the new standard name:
            list_of_strings = list(string_or_list_of_strings)
        
        # Now, we have a local copy as a list.
        # As we are dealing with strings and not Pandas dataframes, we do not call the str attribute.
        
        concat_string = separator.join(list_of_strings)
        # sep.join(list_of_strings) method: join all the strings, separating them by sep.

        # Now, we are in the main code.
        print(f"Finished joining strings.")
        print("Check the 10 first characters of the new string:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(concat_string[:10])
                
        except: # regular mode
            print(concat_string[:10])
        
        return concat_string


    def split_strings (string_or_list_of_strings, separator = " "):
        
        import numpy as np
        
        # string_or_list_of_strings: string or list of strings (inside quotes), 
        # that will be analyzed. 
        # e.g. string_or_list_of_strings = "column1" will analyze 'column1', whereas 
        # string_or_list_of_strings = ['col1', 'col2'] will process both 'col1' and 'col2'.
    
        # separator = " " - string containing the separator. Suppose the column contains the
        # string: 'a b c d' on a given row. If the separator is whitespace ' ', 
        # the output will be a list: ['a', 'b', 'c', 'd']: the function splits the string into a list
        # of strings (one list per row) every time it finds the separator.
        
        
        if (separator is None):
            # make it a whitespace:
            separator = " "
            
        # Check if a string was passed. If it was, convert it to list of single element:
        if (type(string_or_list_of_strings) == str):
            list_of_strings = [string_or_list_of_strings]
        
        else: # simply convert the iterable to the new standard name:
            list_of_strings = list(string_or_list_of_strings)
        
        # Now, we have a local copy as a list.
        # As we are dealing with strings and not Pandas dataframes, we do not call the str attribute.
        
        # Split the strings from new_series, getting a list of strings:
        new_series = [string.split(sep = separator) for string in list_of_strings]

        # Now, we are in the main code.
        print(f"Finished splitting strings.")
        print("Check the 10 first strings:\n")
        
        try:
            # only works in Jupyter Notebook:
            from IPython.display import display
            display(new_series[:10])
                
        except: # regular mode
            print(new_series[:10])
        
        return new_series


    def switch_strings (string_or_list_of_strings, list_of_dictionaries_with_original_strings_and_replacements = [{'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}, {'original_string': None, 'new_string': None}]):
        
        import numpy as np
        
        # string_or_list_of_strings: string or list of strings (inside quotes), 
        # that will be analyzed. 
        # e.g. string_or_list_of_strings = "column1" will analyze 'column1', whereas 
        # string_or_list_of_strings = ['col1', 'col2'] will process both 'col1' and 'col2'.
        
        # list_of_dictionaries_with_original_strings_and_replacements = 
        # [{'original_string': None, 'new_string': None}]
        # This is a list of dictionaries, where each dictionary contains two key-value pairs:
        # the first one contains the original string; and the second one contains the new string
        # that will substitute the original one. The function will loop through all dictionaries in
        # this list, access the values of the keys 'original_string', and search these values on the strings
        # in column_to_analyze. When the value is found, it will be replaced (switched) by the correspondent
        # value in key 'new_string'.
        
        # The object list_of_dictionaries_with_original_strings_and_replacements must be declared as a list, 
        # in brackets, even if there is a single dictionary.
        # Use always the same keys: 'original_string' for the original strings to search on the column 
        # column_to_analyze; and 'new_string', for the strings that will replace the original ones.
        # Notice that this function will not search substrings: it will substitute a value only when
        # there is perfect correspondence between the string in 'column_to_analyze' and 'original_string'.
        # So, the cases (upper or lower) must be the same.
        
        # If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
        # and you can also add more elements (dictionaries) to the lists, if you need to replace more
        # values.
        # Simply put a comma after the last element from the list and declare a new dictionary, keeping the
        # same keys: {'original_string': original_str, 'new_string': new_str}, 
        # where original_str and new_str represent the strings for searching and replacement 
        # (If one of the keys contains None, the new dictionary will be ignored).
        
        # Example:
        # Suppose the column_to_analyze contains the values 'sunday', 'monday', 'tuesday', 'wednesday',
        # 'thursday', 'friday', 'saturday', but you want to obtain data labelled as 'weekend' or 'weekday'.
        # Set: list_of_dictionaries_with_original_strings_and_replacements = 
        # [{'original_string': 'sunday', 'new_string': 'weekend'},
        # {'original_string': 'saturday', 'new_string': 'weekend'},
        # {'original_string': 'monday', 'new_string': 'weekday'},
        # {'original_string': 'tuesday', 'new_string': 'weekday'},
        # {'original_string': 'wednesday', 'new_string': 'weekday'},
        # {'original_string': 'thursday', 'new_string': 'weekday'},
        # {'original_string': 'friday', 'new_string': 'weekday'}]
        
        
        # Check if a string was passed. If it was, convert it to list of single element:
        if (type(string_or_list_of_strings) == str):
            list_of_strings = [string_or_list_of_strings]
        
        else: # simply convert the iterable to the new standard name:
            list_of_strings = list(string_or_list_of_strings)
        
        # Now, we have a local copy as a list.
        # As we are dealing with strings and not Pandas dataframes, we do not call the str attribute.
        
        print("ATTENTION: Operations of string strip (removal) or replacement are all case-sensitive. There must be correct correspondence between cases and spaces for the strings being removed or replaced.\n")
        
        # Create the mapping dictionary for the str.replace method:
        mapping_dict = {}
        # The key of the mapping dict must be an string, whereas the value must be the new string
        # that will replace it.
            
        # Loop through each element on the list list_of_dictionaries_with_original_strings_and_replacements:
        
        for i in range (0, len(list_of_dictionaries_with_original_strings_and_replacements)):
            # from i = 0 to i = len(list_of_dictionaries_with_original_strings_and_replacements) - 1, index of the
            # last element from the list
                
            # pick the i-th dictionary from the list:
            dictionary = list_of_dictionaries_with_original_strings_and_replacements[i]
                
            # access 'original_string' and 'new_string' keys from the dictionary:
            original_string = dictionary['original_string']
            new_string = dictionary['new_string']
            
            # check if they are not None:
            if ((original_string is not None) & (new_string is not None)):
                
                #Guarantee that both are read as strings:
                original_string = str(original_string)
                new_string = str(new_string)
                
                # add them to the mapping dictionary, using the original_string as key and
                # new_string as the correspondent value:
                mapping_dict[original_string] = new_string
        
        # Now, the input list was converted into a dictionary with the correct format for the method.
        # Check if there is at least one key in the dictionary:
        if (len(mapping_dict) > 0):
            # len of a dictionary returns the amount of key:value pairs stored. If nothing is stored,
            # len = 0. dictionary.keys() method (no arguments in parentheses) returns an array containing
            # the keys; whereas dictionary.values() method returns the arrays of the values.
            
            for original_string, new_string in mapping_dict.items():
                
                # For strings, we must perform one substitution by call of the replace method.
                # It is different from pd.str.replace, where a simple call performs this work.
                # So, let's re-create the lists for each key value pair
                # https://www.w3schools.com/python/ref_string_replace.asp
                list_of_strings = [string.replace(original_string, new_string) for string in list_of_strings]
            
            # Now, we are in the main code.
            print(f"Finished replacing the substrings accordingly to the mapping: {mapping_dict}.")
            print("Check the 10 first strings:\n")
        
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(list_of_strings[:10])

            except: # regular mode
                print(list_of_strings[:10])

            return list_of_strings
        
        else:
            print("Input at least one dictionary containing a pair of original string, in the key \'original_string\', and the correspondent new string as key \'new_string\'.")
            print("The dictionaries must be elements from the list list_of_dictionaries_with_original_strings_and_replacements.\n")
            
            return "error"


    def string_replacement_ml (string_or_list_of_strings, mode = 'find_and_replace', threshold_for_percent_of_similarity = 80.0, list_of_dictionaries_with_standard_strings_for_replacement = [{'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}, {'standard_string': None}]):
        
        import numpy as np
        from fuzzywuzzy import process
        
        # string_or_list_of_strings: string or list of strings (inside quotes), 
        # that will be analyzed. 
        # e.g. string_or_list_of_strings = "column1" will analyze 'column1', whereas 
        # string_or_list_of_strings = ['col1', 'col2'] will process both 'col1' and 'col2'.
        
        # mode = 'find_and_replace' will find similar strings; and switch them by one of the
        # standard strings if the similarity between them is higher than or equals to the threshold.
        # Alternatively: mode = 'find' will only find the similar strings by calculating the similarity.
        
        # threshold_for_percent_of_similarity = 80.0 - 0.0% means no similarity and 100% means equal strings.
        # The threshold_for_percent_of_similarity is the minimum similarity calculated from the
        # Levenshtein (minimum edit) distance algorithm. This distance represents the minimum number of
        # insertion, substitution or deletion of characters operations that are needed for making two
        # strings equal.
        
        # list_of_dictionaries_with_standard_strings_for_replacement =
        # [{'standard_string': None}]
        # This is a list of dictionaries, where each dictionary contains a single key-value pair:
        # the key must be always 'standard_string', and the value will be one of the standard strings 
        # for replacement: if a given string on the column_to_analyze presents a similarity with one 
        # of the standard string equals or higher than the threshold_for_percent_of_similarity, it will be
        # substituted by this standard string.
        # For instance, suppose you have a word written in too many ways, making it difficult to use
        # the function switch_strings: "EU" , "eur" , "Europ" , "Europa" , "Erope" , "Evropa" ...
        # You can use this function to search strings similar to "Europe" and replace them.
        
        # The function will loop through all dictionaries in
        # this list, access the values of the keys 'standard_string', and search these values on the strings
        # in column_to_analyze. When the value is found, it will be replaced (switched) if the similarity
        # is sufficiently high.
        
        # The object list_of_dictionaries_with_standard_strings_for_replacement must be declared as a list, 
        # in brackets, even if there is a single dictionary.
        # Use always the same keys: 'standard_string'.
        # Notice that this function performs fuzzy matching, so it MAY SEARCH substrings and strings
        # written with different cases (upper or lower) when this portions or modifications make the
        # strings sufficiently similar to each other.
        
        # If you want, you can remove elements (dictionaries) from the list to declare fewer elements;
        # and you can also add more elements (dictionaries) to the lists, if you need to replace more
        # values.
        # Simply put a comma after the last element from the list and declare a new dictionary, keeping the
        # same key: {'standard_string': other_std_str}, 
        # where other_std_str represents the string for searching and replacement 
        # (If the key contains None, the new dictionary will be ignored).
        
        # Example:
        # Suppose the column_to_analyze contains the values 'California', 'Cali', 'Calefornia', 
        # 'Calefornie', 'Californie', 'Calfornia', 'Calefernia', 'New York', 'New York City', 
        # but you want to obtain data labelled as the state 'California' or 'New York'.
        # Set: list_of_dictionaries_with_standard_strings_for_replacement = 
        # [{'standard_string': 'California'},
        # {'standard_string': 'New York'}]
        
        # ATTENTION: It is advisable for previously searching the similarity to find the best similarity
        # threshold; set it as high as possible, avoiding incorrect substitutions in a gray area; and then
        # perform the replacement. It will avoid the repetition of original incorrect strings in the
        # output dataset, as well as wrong replacement (replacement by one of the standard strings which
        # is not the correct one).
        
        
        print("Performing fuzzy replacement based on the Levenshtein (minimum edit) distance algorithm.")
        print("This distance represents the minimum number of insertion, substitution or deletion of characters operations that are needed for making two strings equal.\n")
        
        print("This means that substrings or different cases (upper or higher) may be searched and replaced, as long as the similarity threshold is reached.\n")
        
        print("ATTENTION!\n")
        print("It is advisable for previously searching the similarity to find the best similarity threshold.\n")
        print("Set the threshold as high as possible, and only then perform the replacement.\n")
        print("It will avoid the repetition of original incorrect strings in the output dataset, as well as wrong replacement (replacement by one of the standard strings which is not the correct one.\n")
        
        # Check if a string was passed. If it was, convert it to list of single element:
        if (type(string_or_list_of_strings) == str):
            list_of_strings = [string_or_list_of_strings]
        
        else: # simply convert the iterable to the new standard name:
            list_of_strings = list(string_or_list_of_strings)
        
        # Now, we have a local copy as a list.
        # As we are dealing with strings and not Pandas dataframes, we do not call the str attribute.

        # Get the unique values present in column_to_analyze:
        # Convert the list to a set: sets accepts only unique elements. These objects are based on the
        # sets mathematical theory
        unique_types = set(list_of_strings)
        
        # Create the summary_list:
        summary_list = []
            
        # Loop through each element on the list list_of_dictionaries_with_original_strings_and_replacements:
        
        for i in range (0, len(list_of_dictionaries_with_standard_strings_for_replacement)):
            # from i = 0 to i = len(list_of_dictionaries_with_standard_strings_for_replacement) - 1, index of the
            # last element from the list
                
            # pick the i-th dictionary from the list:
            dictionary = list_of_dictionaries_with_standard_strings_for_replacement[i]
                
            # access 'standard_string' key from the dictionary:
            standard_string = dictionary['standard_string']
            
            # check if it is not None:
            if (standard_string is not None):
                
                # Guarantee that it was read as a string:
                standard_string = str(standard_string)
                
                # Calculate the similarity between each one of the unique_types and standard_string:
                similarity_list = process.extract(standard_string, unique_types, limit = len(unique_types))
                
                # Add the similarity list to the dictionary:
                dictionary['similarity_list'] = similarity_list
                # This is a list of tuples with the format (tested_string, percent_of_similarity_with_standard_string)
                # e.g. ('asiane', 92) for checking similarity with string 'asian'
                
                if (mode == 'find_and_replace'):
                    
                    # If an invalid value was set for threshold_for_percent_of_similarity, correct it to 80% standard:
                    
                    if(threshold_for_percent_of_similarity is None):
                        threshold_for_percent_of_similarity = 80.0
                    
                    if((threshold_for_percent_of_similarity == np.nan) | (threshold_for_percent_of_similarity < 0)):
                        threshold_for_percent_of_similarity = 80.0
                    
                    list_of_replacements = []
                    # Let's replace the matches in the series by the standard_string:
                    # Iterate through the list of matches
                    for match in similarity_list:
                        # Check whether the similarity score is greater than or equal to threshold_for_percent_of_similarity.
                        # The similarity score is the second element (index 1) from the tuples:
                        if (match[1] >= threshold_for_percent_of_similarity):
                            # If it is, select all rows where the column_to_analyze is spelled as
                            # match[0] (1st Tuple element), and set it to standard_string:
                            list_of_strings = [string.replace(match[0], standard_string) for string in list_of_strings]
            
                            print(f"Found {match[1]}% of similarity between {match[0]} and {standard_string}.")
                            print(f"Then, {match[0]} was replaced by {standard_string}.\n")
                            
                            # Add match to the list of replacements:
                            list_of_replacements.append(match)
                    
                    # Add the list_of_replacements to the dictionary, if its length is higher than zero:
                    if (len(list_of_replacements) > 0):
                        dictionary['list_of_replacements_by_std_str'] = list_of_replacements
                
                # Add the dictionary to the summary_list:
                summary_list.append(dictionary)
        
        # Now, let's replace the original column or create a new one if mode was set as replace:
        if (mode == 'find_and_replace'):
        
            # Now, we are in the main code.
            print(f"Finished replacing the strings by the provided standards. Returning the new list and a summary list.\n")
            print("In summary_list, you can check the calculated similarities in keys \'similarity_list\' from the dictionaries.\n")
            print("The similarity list is a list of tuples, where the first element is the string compared against the value on key \'standard_string\'; and the second element is the similarity score, the percent of similarity between the tested and the standard string.\n")
            print("Check the 10 first strings:\n")
        
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(list_of_strings[:10])

            except: # regular mode
                print(list_of_strings[:10])
        
        else:
            
            print("Finished mapping similarities. Returning the original list and a summary list.\n")
            print("Check the similarities below, in keys \'similarity_list\' from the dictionaries.\n")
            print("The similarity list is a list of tuples, where the first element is the string compared against the value on key \'standard_string\'; and the second element is the similarity score, the percent of similarity between the tested and the standard string.\n")
            
            try:
                display(summary_list)
            except:
                print(summary_list)
        
        return list_of_strings, summary_list


    def regex_search (string_or_list_of_strings, regex_to_search = r"", show_regex_helper = False):
        
        import re
        import numpy as np
        
        # string_or_list_of_strings: string or list of strings (inside quotes), 
        # that will be analyzed. 
        # e.g. string_or_list_of_strings = "column1" will analyze 'column1', whereas 
        # string_or_list_of_strings = ['col1', 'col2'] will process both 'col1' and 'col2'.
        
        # regex_to_search = r"" - string containing the regular expression (regex) that will be searched
        # within each string from the column. Declare it with the r before quotes, indicating that the
        # 'raw' string should be read. That is because the regex contain special characters, such as \,
        # which should not be read as scape characters.
        # example of regex: r'st\d\s\w{3,10}'
        # Use the regex helper to check: basic theory and most common metacharacters; regex quantifiers;
        # regex anchoring and finding; regex greedy and non-greedy search; regex grouping and capturing;
        # regex alternating and non-capturing groups; regex backreferences; and regex lookaround.
        
        ## ATTENTION: This function returns ONLY the capturing groups from the regex, i.e., portions of the
        # regex explicitly marked with parentheses (check the regex helper for more details, including how
        # to convert parentheses into non-capturing groups). If no groups are marked as capturing, the
        # function will raise an error.

        # show_regex_helper: set show_regex_helper = True to show a helper guide to the construction of
        # the regular expression. After finishing the helper, the original dataset itself will be returned
        # and the function will not proceed. Use it in case of not knowing or not certain on how to input
        # the regex.
        
        
        if (show_regex_helper): # run if True
            
            # Create an instance (object) from class regex_help:
            helper = regex_help()
            # Run helper object:
            helper = helper.show_screen()
            print("Interrupting the function and returning the dataframe itself.")
            print("Use the regex helper instructions to obtain the regex.")
            print("Do not forget to declare it as r'regex', with the r before quotes.")
            print("It indicates a raw expression. It is important for not reading the regex metacharacters as regular string scape characters.")
            print("Also, notice that this function returns only the capturing groups (marked with parentheses).")
            print("If no groups are marked as capturing groups (with parentheses) within the regex, the function will raise an error.\n")
            
            return df
        
        else:
            
            # Check if a string was passed. If it was, convert it to list of single element:
            if (type(string_or_list_of_strings) == str):
                list_of_strings = [string_or_list_of_strings]

            else: # simply convert the iterable to the new standard name:
                list_of_strings = list(string_or_list_of_strings)

            # Now, we have a local copy as a list.
            # As we are dealing with strings and not Pandas dataframes, we do not call the str attribute.
            
            # Search for the regex within the list:
            new_series = [re.findall(regex_to_search, string) for string in list_of_strings]
            

            # Now, we are in the main code.
            print(f"Finished searching the regex {regex_to_search} within the list of strings.")
            print("Check the 10 first strings:\n")
        
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(new_series[:10])

            except: # regular mode
                print(new_series[:10])

            return new_series


    def regex_replacement (string_or_list_of_strings, regex_to_search = r"", string_for_replacement = "", show_regex_helper = False):
        
        import re
        import numpy as np
        
        # string_or_list_of_strings: string or list of strings (inside quotes), 
        # that will be analyzed. 
        # e.g. string_or_list_of_strings = "column1" will analyze 'column1', whereas 
        # string_or_list_of_strings = ['col1', 'col2'] will process both 'col1' and 'col2'.
        
        # regex_to_search = r"" - string containing the regular expression (regex) that will be searched
        # within each string from the column. Declare it with the r before quotes, indicating that the
        # 'raw' string should be read. That is because the regex contain special characters, such as \,
        # which should not be read as scape characters.
        # example of regex: r'st\d\s\w{3,10}'
        # Use the regex helper to check: basic theory and most common metacharacters; regex quantifiers;
        # regex anchoring and finding; regex greedy and non-greedy search; regex grouping and capturing;
        # regex alternating and non-capturing groups; regex backreferences; and regex lookaround.
        
        # string_for_replacement = "" - regular string that will replace the regex_to_search: 
        # whenever regex_to_search is found in the string, it is replaced (substituted) by 
        # string_or_regex_for_replacement. 
        # Example string_for_replacement = " " (whitespace).
        # If string_for_replacement = None, the empty string will be used for replacement.
        
        ## ATTENTION: This function process a single regex by call.
        
        # show_regex_helper: set show_regex_helper = True to show a helper guide to the construction of
        # the regular expression. After finishing the helper, the original dataset itself will be returned
        # and the function will not proceed. Use it in case of not knowing or not certain on how to input
        # the regex.
        
        
        if (show_regex_helper): # run if True
            
            # Create an instance (object) from class regex_help:
            helper = regex_help()
            # Run helper object:
            helper = helper.show_screen()
            print("Interrupting the function and returning the dataframe itself.")
            print("Use the regex helper instructions to obtain the regex.")
            print("Do not forget to declare it as r'regex', with the r before quotes.")
            print("It indicates a raw expression. It is important for not reading the regex metacharacters as regular string scape characters.\n")
            
            return df
        
        else:
            
            if (string_for_replacement is None):
                # make it the empty string
                string_for_replacement = ""
            
            # Check if a string was passed. If it was, convert it to list of single element:
            if (type(string_or_list_of_strings) == str):
                list_of_strings = [string_or_list_of_strings]

            else: # simply convert the iterable to the new standard name:
                list_of_strings = list(string_or_list_of_strings)

            # Now, we have a local copy as a list.
            # As we are dealing with strings and not Pandas dataframes, we do not call the str attribute.
            # Search for the regex within the list and replace (substitute it):
            new_series = [re.sub(regex_to_search, string_for_replacement, string) for string in list_of_strings]
            

            # Now, we are in the main code.
            print(f"Finished searching the regex {regex_to_search} within the input strings.")
            print("Check the 10 first strings:\n")
        
            try:
                # only works in Jupyter Notebook:
                from IPython.display import display
                display(new_series[:10])

            except: # regular mode
                print(new_series[:10])

            return new_series

