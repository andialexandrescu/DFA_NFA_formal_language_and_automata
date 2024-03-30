def inputDataProcessing():
    global no_states, Lstates, no_symbols, Lsymbols, initial_state, no_accepted_states, Laccepted_states, no_transitions, dict_transitions_nfa, no_words, Lwords

    f = open("date_nfa.in")
    no_states = int(f.readline().strip()) # number (no.) of states
    Lstates = [int(x) for x in f.readline().strip().split()] # in ac mom nu conteaza nr de stari, din moment ce toate sunt scrise pe o linie
    no_symbols = int(f.readline().strip())
    Lsymbols = [ch for ch in f.readline().strip().split()] # implicit e un sir de caractere
    initial_state = int(f.readline().strip())
    no_accepted_states = int(f.readline().strip())
    Laccepted_states = [int(x) for x in f.readline().strip().split()]

    dict_transitions_nfa = dict() # initializare dictionar de forma {key=current_state : {symbol1: [target_state1, target_state2], symbol2: [target_state2], ...} }
    no_transitions = int(f.readline().strip())
    for i in range(no_transitions):
        line_transition = f.readline().strip().split() # fiecare linie reprezinta de fapt o tranzitie vazuta ca un tuplu care poate fi despachetat, de forma (current_state, symbol, target_state)
        # despachetare:
        current_state, symbol, target_state = int(line_transition[0]), line_transition[1], int(line_transition[2])
        if current_state not in dict_transitions_nfa:
            dict_transitions_nfa[current_state] = {}
        if symbol not in dict_transitions_nfa[current_state]:
            dict_transitions_nfa[current_state][symbol] = [target_state]
        else:
            dict_transitions_nfa[current_state][symbol].append(target_state) # lista de target states

    no_words = int(f.readline().strip())
    Lwords = list()
    for cuv in range(no_words):
        Lwords.append(f.readline().strip())

    #print(no_states, Lstates, no_symbols, Lsymbols, initial_state, no_accepted_states, Laccepted_states, no_transitions, dict_transitions_nfa, no_words, Lwords, sep="\n")
    f.close()

def NFA_to_DFA():
    global dict_transitions_nfa, dict_transitions_dfa, initial_state, Lsymbols, Laccepted_states, L_dfa_accepted_states

    L_dfa_states = [frozenset([initial_state])] # !!!frozenset functioneaza doar pt obiecte iterabile
    L_dfa_accepted_states = []
    dict_transitions_dfa = dict()
    # e necesar a crea o lista de stari ale automatului DFA care trebuie creat, ele putand sa fie unitare (in sensul ca exista deja ca stari ale NFA-ului) sau reprezentate ca o multime imutabila de stari din NFA (multimea in sine reprezinta o noua stare reinterpretata in DFA)
    # exemplu exprimare anterioara: STARE UNITARA (are cardinalul 1, un singur element): frozenset({3499})/ STARE MULTIME: frozenset({7571, 6107, 7814})
    # asadar dictionarul care corespunde DFA-ului va reprezenta un dictionar de dictionare de forma {key=frozenset({state1, state2, ...}): {symbol1: frozenset({state3, state4, ...}), symbol2: frozenset(...), ...}, ...}

    for new_state in L_dfa_states: # noua stare reprezinta de fapt o multime imutabila (frozenset) deoarece se doreste reuniunea elementelor din NFA (fara duplicate)
        # se itereaza prin fiecare noua stare adaugata la lista noilor stari reintrepretate pt DFA (linia 53)
        if new_state not in dict_transitions_dfa: # doar daca nu exista o noua stare in dictionarul principal, inseamna ca nu a fost initializat niciun subdictionar corespunzator
            dict_transitions_dfa[new_state] = {}
        # else: este inutil sa fie tratat cazul de else din moment ce sunt specificate toate tranzitiile corespunzatoare starii noi dupa ce se itereaza prin intreaga lista de simboluri NFA (linia 51)

        # !pt usurinta voi parcurge simbolurile mai intai, dupa starile continute in multimea new_state, din moment ce un target_state depinde in primul rand de muchia asociata unui simbol din limbaj
        for symbol in Lsymbols: # un nou target state de tip frozenset va fi determinat pt fiecare simbol existent in limbaj
            target_state = set() # momentan target_state e multime mutabila pt a avea posibilitatea de a adauga elemente, ulterior va fi prelucrata ca imutabila, din moment ce va reprezenta o noua cheie in dictionarul principal
            for state in new_state: # se parcurge fiecare stare continuta in frozenset-ul new_state definit in lista de stari noi DFA
                if state in dict_transitions_nfa:
                    target_state.update(dict_transitions_nfa[state].get(symbol, set())) # reuniune
                    # get gaseste valoarea asociata cheii symbol (cheia subdictionarului), daca valoarea symbol nu exista in subdictionar, inseamna ca nu exista o tranzitie valida, deci multimea care ar trebui intoarsa este vida, set() (default parameter pt get)
            if target_state: # daca multimea nu e vida, va fi retinuta tranzitia in dictionarul DFA-ului de tranzitii
                dict_transitions_dfa[new_state][symbol] = frozenset(target_state)
                if frozenset(target_state) not in L_dfa_states: # se adauga noi stari de tip frozenset la lista noilor stari, doar daca ele nu au fost gasite anterior pasului curent, altfel e redundant
                    L_dfa_states.append(frozenset(target_state))

    # noile stari DFA acceptate ca fiind finale, presupun sa existe cel putin una din starile acceptate NFA in componenta multimii imutabile new_state
    for new_state in L_dfa_states:
        for state in new_state: # fiecare stare unitara din multimea imutabila
            if state in Laccepted_states and new_state not in L_dfa_accepted_states: # se adauga in lista starilor noi acceptate de DFA doar acele multimi care nu exista deja
                L_dfa_accepted_states.append(new_state)

    #for key, value in dict_transitions_dfa.items(): # despachetare dictionar principal pt vizualizare rezultate
        #print(f"{key}: {value}")
    #print()
    #print(*L_dfa_accepted_states, sep='\n')

def DFA_wrdsProcessing():
    global Lwords, dict_transitions_dfa, initial_state, L_dfa_accepted_states
    #Laccepted_words = list()

    # starea curenta e o multime imutabila
    for wrd in Lwords:
        current_state = frozenset([initial_state])
        for ch in wrd:
            if current_state in dict_transitions_dfa.keys():
                if ch in dict_transitions_dfa[current_state].keys():
                    current_state = dict_transitions_dfa[current_state][ch] # noua stare curenta e cea determinata ca un target state
                else:
                    print("NU")
                    break
            # else: ac conditie nu are sens pentru ca toate starile vor fi apartine listei cheilor dictionarului dict_transitions
        else: # daca for-ul se termina natural, adica toate literele sunt procesate si ajung in stari valide, bazat pe functia de tranzitie definita in dict_transitions, inseamna ca trebuie verificata daca target_state coincide cu una dintre starile finale posibile
            if current_state in L_dfa_accepted_states:
                print("DA")
                # Laccepted_words.append(wrd)
            else: # ne aflam la finalul cuv, insa cu toate ca drumul (privit in graf) exista, ultima litera nu apartine unei stari finale
                print("NU")
    #print(Laccepted_words)

inputDataProcessing()
NFA_to_DFA()
DFA_wrdsProcessing()