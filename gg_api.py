'''Version 0.35'''
import nominees as noms
import winners as wins
import findHost as host_s
import presenters as present
from multiprocessing import Process, Queue

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

answers = Queue()
final_answers = dict()

def host(year):
    hosts = host_s.runHosts(year)
    answers.put(('hosts', hosts))

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    hosts = final_answers['hosts']
    return hosts

def award(year): #put awards array call in place of the empty array here
    awards = []
    answers.put(('awards', awards))

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    awards = final_answers['awards']
    return awards

def nominee(year):
    nominees = noms.get_nominees(year)
    answers.put(('nominees', nominees))

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    nominees = final_answers['nominees']
    return nominees

def winner(year):
    winners = wins.get_winners(year)
    answers.put(('winners', winners))

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    winners = final_answers['winners']
    return winners

def presenter(year):
    presenters = present.get_presenters(year)
    answers.put(('presenters', presenters))

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    presenters = final_answers['presenters']
    return presenters

def handle_answers():
    print('length of answers:', len(answers))
    while len(answers) > 0:
        set = answers.get()
        final_answers[set[0]] = set[1]

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    functions = []
    functions.append(Process(target=host, args=(2013,)))
    functions.append(Process(target=presenter, args=(2013,)))
    functions.append(Process(target=nominee, args=(2013,)))
    functions.append(Process(target=winner, args=(2013,)))
    # functions.append(Process(target=award, args=(2013,))) #uncomment this line when the award() func is done
    for job in functions:
        job.start()
    for job in functions:
        job.join()
    handle_answers()
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    hosts = get_hosts(2013)
    presenters = get_presenters(2013)
    winners = get_winner(2013)
    nominees = get_nominees(2013)
    nominees['cecil b. demille award'] = winners['cecil b. demille award']
    print(list(answers.queue))
    print('Hosting: '.join(hosts))

    for award in OFFICIAL_AWARDS_1315:
        print("Award: ", award)
        print('Presenters: ', presenters[award])
        print('Nominees: ', nominees[award])
        print('Winner: ', winners[award])
    return

if __name__ == '__main__':
    pre_ceremony()
    main()
