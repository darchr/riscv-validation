from glob import glob


def parser (str, letter):
    global city1
    global city2
    letter1 = str[letter]
    letter2 = str[letter+1]
    city1 = city1 + letter1
    city2 = city2 + letter2
    return city1,city2

strs = ["My boss just pushed me over the limit", "I ain't had a day off now, in over a year", "Pour me something tall and strong, make it a hurricane, before I go insane", "Tomorrow morning I know there'll be hell to pay hey, but that's all right", "I could pay off my tab, pour myself in a cab and be back to work before two", "(And I don't care) It's five o'clock somewhere", "I'd like to call him something, think I'll just call it a day", "Pour me something tall and strong, make it a hurricane, before I go insane", "If the phone's for me you can just tell them I just sailed away", "It's only half past twelve. But I don't care", "My Jamaican vacation's gonna start right here", "Pour me something tall and strong, make it a hurricane, before I go insane", "This lunch break is gonna take all afternoon, half the night", "The sun is hot and that old clock is movin' slow, and so am I"]
letters = [0, 35,42,15,20,27,3,28,21,36,36,23,33,11]
city1 = ""
city2= ""

for i in range(len(strs)):
    city1,city2 = parser(strs[i],letters[i])

print(city1, "\n", city2)