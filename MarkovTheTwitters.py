import random
from twython import Twython, exceptions
import config
        
def createDictionary( text ):
    """Returns a dictionary of all the non-URL words and what follows them in the text"""
    listOfWords = text.split()

    dictionary = {}
    previousWord = '$'

    for word in listOfWords:
#         URLS clutter the final result and are best removed
        if word[:4] == "http":
            previousWord = '$'
            
        else:
            if previousWord not in dictionary:
                dictionary[previousWord] = [word]
    
            else:
                dictionary[previousWord] += [word]
    
            if word[-1] == '.' or word[-1] == '?' or word[-1] == '!':
                previousWord = '$'
    
            else:
                previousWord = word
                
    return dictionary

def generateText( dictionary, n ):
    """Uses a dictionary to generate a string of n words"""
    listOfWords = []
    
#     Start the list with a random word from the text
    listOfWords += [random.choice(dictionary['$'])]
    
    while len(listOfWords) != n:
        
#         Start with the last word in the list
        word = listOfWords[-1]
        
        try:
#             If there's punctuation, start a new sentence.
            if word[-1] == '.' or word[-1] == '?' or word[-1] == '!':
                listOfWords += [random.choice(dictionary['$'])]
#             Otherwise find a word that has come after the last word.
            else:
                listOfWords += [random.choice(dictionary[listOfWords[-1]])]
                
#         Allows generation to continue if there is a non-word in the text
        except KeyError:
            listOfWords += [random.choice(dictionary['$'])]
            
#     Convert to string and return
    string = ' '.join(listOfWords)
    return string

def main():
#     Error handling to make sure authentication is working
    try:
        twitter = Twython(config.OAUTH_KEY, config.OAUTH_SECRET, oauth_version=2)
        accessToken = twitter.obtain_access_token()
        twitter = Twython(config.OAUTH_KEY, access_token=accessToken)
    except AttributeError:
        print "ERROR: Please set up your key and secret as per the README."
        return
    except exceptions.TwythonError:
        print "ERROR: Please set up your key and secret as per the README."
        return
    
#     Get user query and search twitter
    userSearch = raw_input('What would you like to search for today? ')
    searchResults = twitter.search(q=userSearch, lang="en", count=100)
    
#     Parse twitter search results
    twitterPosts = searchResults.get("statuses")
    
    listOfTweets = ""
    for tweet in twitterPosts:
        listOfTweets = listOfTweets + tweet["text"] + ". "
    
    print ""
    
#     A lack of results ultimately returns a KeyError
#     This checks for results before continuing
    if listOfTweets == "":
        print "No tweets found, please try a new search."
    else:
        dictionary = createDictionary(listOfTweets)
        NewTweet0 = generateText(dictionary, 30)
        print NewTweet0[:140]
        
    print ""
        
    again = raw_input('Would you like to try again? (y/n) ')
    if again == 'y':
        main()
    elif again == 'n':
        "kthxbai"
        return
    else:
        print "try following directions next time!"
        return    

main()