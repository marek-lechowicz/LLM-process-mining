# Plan pracy

## Projekt - Done:

1. Generator workflow log

## Projekt - ToDo:

1. [MUST HAVE] Testy doświadczalne generatora workflow log
   - więcej przykładów danych wejściowych
1. [MUST HAVE] Process mining
   - zastosowanie algorytmu alpha - https://github.com/harrywang/pyprom
   - algorytm alpha generujący bezpośrednio diagramy BPMN
   - [COULD HAVE] ewentualnie inne algorytmy
   - PetriNet -> BPMN - Anna Kalenkova "Process mining using BPMN: event log"
1. [COULD HAVE] Generowanie logu procesu do formatu XES
   - przy użyciu biblioteki opyenxes - https://pypi.org/project/opyenxes/
1. [MUST HAVE] Rysowanie diagramu BPMN
   - korzystając z biblioteki https://github.com/KrzyHonk/bpmn-python
1. [SHOULD HAVE] Interfejs CLI
1. [COULD HAVE] Obrazy dockera z zainstalowanymi zależnościami projektu

## Praca:

1. Opis problemu, motywacja (do czego to sluzy), struktura pracy
1. Metoda generowania modeli procesow 
   - Opis zaimplementowanej metody (na podstawie artykułów), opis modyfikacji. (bazowac na artykule, bibliografia i odnosniki)
   - rysunek ilustrujacy metode
   1. Wykorzystane techniki i technologie
      1. Constraint Programming
      1. Process mining (odkrywanie procesow, eksploracja procesow)
      1. BPMN
1. Projekt systemu/narzędzia
   1. Wymagania na system (funkcjonalne/niefunkcjonalne)
   2. Architektura (?)
      - diagram struktury projektu 
      - diagram zachowania (najwazniejsze funkcje) 
      - opis musi byc 
1. Szczegóły implementacji
   1. jezyk, uzyte biblioteki, zaleznosci itp.
   1. Silniki wnioskujące (Mistral, Gecode, etc.)
   1. fragmenty kodu 
   1. link do repozytorium, screen z repozytorium (z lista plikow, ew. drzewo plikow)
1. Ewaluacja 
   1. sposob uzycia (user guide)
   1. use cases np. bank (1 przyklad roznorodny opisac dokladniej, a pozostale tylko wymienic)
   1. testy (jesli beda to opisac) X 
1. Wnioski, podsumowanie, mozliwosci rozbudowy aplikacji

---
liczba stron: minimum 30, max 60

---

- 20. lutego - wysłać maila
- 21. lutego, po południu (17, 18) - konsultacje, wersja alpha gotowej pracy
- 25. lutego - poprawki
- 27. lutego

bibtex

W pracy~\cite{wisniewski2018approach} zaproponowano metode...
rysunki \label -> \ref


### Elementy BPMN:

1. Bramki
   - XOR
   - AND
1. Aktywności
1. Start / Stop
