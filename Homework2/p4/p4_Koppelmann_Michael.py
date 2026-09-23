# Question 4
import csv, os
FOLDER = os.path.dirname(os.path.abspath(__file__))

TOP_RATED_FILE = 'imdb-top-rated-csv'
TOP_GROSSING_FILE = 'lmdb-top-grossing.csv'
TOP_CASTS_FILE = 'imdb-top-casts.csv'

def read_csv(filename, header):
    with open(os.path.join(FOLDER, filename), 'r', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    return rows[1:] if header else rows

def get_casts():
    return{(r[0], r[1]): (r[2], r[3:]) for r in read_csv('imdb-top-casts.csv', False)}

def display_top_collaborations(n=20):
    casts = get_casts()
    counts = {}
    for row in read_csv('imdb-top-rated.csv', True):
        if (row[1], row[2]) in casts:
            director, actors = casts[(row[1], row[2])]
            for actor in actors:
                counts[(director, actor)] = counts.get((director, actor), 0) + 1

    ranking = sorted(counts.items(), key=lambda p: p[1], reverse=True)
    print('Director-actor collaborations in top rated movies')
    for rank, ((director, actor), count) in enumerate(ranking[:n], 1):
        print(f'{rank:>4} {director:>25} {actor:>25} {count:>3}')
    print()

def display_top_actors(n=20):
    casts = get_casts()
    totals = {}
    for row in read_csv('imdb-top-grossing.csv', True):
        if (row[1], row[2]) in casts:
            for actor in casts[(row[1], row[2])][1]:
                totals[actor] = totals.get(actor, 0) + int(row[3])
    ranking = sorted(totals.items(), key=lambda p: p[1], reverse=True)
    print('Actors by total USA box office in top grossing movies')
    for rank, (actor, money) in enumerate(ranking[:n], 1):
        print(f'{rank:>4} {actor:<25} {money:>16}')
        print()

def main():
    display_top_collaborations()
    display_top_actors()

if __name__ == '__main__':
    main()
