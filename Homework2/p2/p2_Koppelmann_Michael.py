# Question 2
pythagorean_pairs = [(a, b, c, d)
                     for a in range (1, 11)
                     for b in range (1, 11)
                     for c in range (1, 11)
                     for d in range (1, 11)
                     if len({a, b, c, d}) == 4 and a**2 + b**2 == c**2 + d**2]

words = ['One', 'SEVEN', 'three', 'two', 'Ten']
short_words = [(w.lower(), len(w)) for w in words if len(w) < 5]
names = ['Christopher Aston Kutcher', 'Elizabeth Stamnatina Fey']
abbreviated = [f"{first} {middle[0]} {last}"
               for first, middle, last in (name.split() for name in names)]

list1 = ["Spams", "Trams", "Elbows", "Tops", "Astral"]
list2 = ["Bowels", "Sample", "Atlars", "Stop", "Course", "Smart"]

anagrams = [(w1, w2)
            for w1 in list1
            for w2 in list2
            if sorted(w1.lower()) == sorted(w2.lower())]

s = ['one', 'two', 'three']
lengths = {w: len(w) for w in s}
text = "Hello World"
vowel_positions = {i: c for i, c in enumerate(text) if c.lower () in "aeiou"}

print("a)", pythagorean_pairs)
print("b)", short_words)
print("c)", names)
print("d)", anagrams)
print("e)", lengths)
print("f)", vowel_positions)
