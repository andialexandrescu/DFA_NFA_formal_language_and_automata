def inputDataProcessingDFA():
    global no_states, Lstates, no_symbols, Lsymbols, initial_state, no_accepted_states, Laccepted_states, no_transitions, dict_transitions, no_words, Lwords

    f = open("date_dfa.in")
    no_states = int(f.readline().strip()) # number (no.) of states
    Lstates = [int(x) for x in f.readline().strip().split()] # in ac mom nu conteaza nr de stari, din moment ce toate sunt scrise pe o linie
    no_symbols = int(f.readline().strip())
    Lsymbols = [ch for ch in f.readline().strip().split()] # implicit e un sir de caractere
    initial_state = int(f.readline().strip())
    no_accepted_states = int(f.readline().strip())
    Laccepted_states = [int(x) for x in f.readline().strip().split()]

    dict_transitions = dict() # initializare dictionar de forma {key=current_state : {symbol1: target_state1, symbol2: target_state2, ...} }
    no_transitions = int(f.readline().strip())
    for i in range(no_transitions):
        line_transition = f.readline().strip().split() # fiecare linie reprezinta de fapt o tranzitie vazuta ca un tuplu care poate fi despachetat, de forma (current_state, symbol, target_state)
        # despachetare:
        current_state, symbol, target_state = int(line_transition[0]), line_transition[1], int(line_transition[2])
        if current_state not in dict_transitions.keys():
            dict_transitions[current_state] = dict({symbol: target_state}) # initializare dictionar auxiliar
        else:
            dict_transitions[current_state][symbol] = target_state

    no_words = int(f.readline().strip())
    Lwords = list()
    for cuv in range(no_words):
        Lwords.append(f.readline().strip())

    #print(no_states, Lstates, no_symbols, Lsymbols, initial_state, no_accepted_states, Laccepted_states, no_transitions, dict_transitions, no_words, Lwords, sep="\n")
    f.close()

def DFA_wrdsProcessing():
    global Lwords, dict_transitions, initial_state, Laccepted_states
    #Laccepted_words = list()

    target_state = None
    for wrd in Lwords:
        current_state = None
        for ch in wrd:
            if current_state is None:
                current_state = initial_state
            else:
                current_state = target_state # interpretat drept un previous_state in acest caz
            if current_state in dict_transitions.keys():
                if ch in dict_transitions[current_state].keys():
                    target_state = dict_transitions[current_state][ch]
                else:
                    print("NU")
                    break
            # else: ac conditie nu are sens pentru ca toate starile vor fi apartine listei cheilor dictionarului dict_transitions
        else: # daca for-ul se termina natural, adica toate literele sunt procesate si ajung in stari valide, bazat pe functia de tranzitie definita in dict_transitions, inseamna ca trebuie verificata daca target_state coincide cu una dintre starile finale posibile
            if target_state in Laccepted_states:
                print("DA")
                #Laccepted_words.append(wrd)
            else: # ne aflam la finalul cuv, insa cu toate ca drumul privit in graf exista, ultima litera nu apartine unei stari finale
                print("NU")
    #print(Laccepted_words)

inputDataProcessingDFA()
DFA_wrdsProcessing()