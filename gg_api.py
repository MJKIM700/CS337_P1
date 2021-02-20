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
    for answer in list(answers.queue):
        if answer[0] == 'hosts':
            hosts = answer[1]
    return hosts

def award(year):
    awards = []
    answers.put(('awards', awards))

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    for answer in list(answers.queue):
        if answer[0] == 'hosts':
            hosts = answer[1]
            break
    return hosts

def nominee(year):
    nominees = noms.get_nominees(year)
    answers.put(('nominees', nominees))

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    for answer in list(answers.queue):
        if answer[0] == 'nominees':
            nominees = answer[1]
            break
    return nominees

def winner(year):
    winners = wins.get_winners(year)
    answers.put(('winners', winners))

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    for answer in list(answers.queue):
        if answer[0] == 'winners':
            winners = answer[1]
            break
    return winners

def presenter(year):
    presenters = present.get_presenters(year)
    answers.put(('presenters', presenters))

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    for answer in list(answers.queue):
        if answer[0] == 'presenters':
            presenters = answer[1]
            break
    return presenters

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
    for job in functions:
        job.start()
    for job in functions:
        job.join()

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
