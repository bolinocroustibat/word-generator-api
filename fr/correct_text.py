import re
from typing import Iterator, Match


def correct_text_fr(text: str) -> str:

    # matches: Iterator[Match] = re.search(
    #     "(l'[bcdfghjklmnpqrstvwxz])+", string
    # )
    # for m in matches:
    #     string = string[: m.start(1)] + " " + string[m.end(1) :]
    #     return string


    CORRECTIONS = {  # we could also use "replace(old, new)"
        "( ": "(",
        " )": ")",
        " à le ": " au ",
        " à les ": " aux ",
        " de a": " d'a",
        " de e": " d'e",
        " de é": " d'é",
        " de è": " d'è",
        " de ê": " d'ê",
        " de i": " d'i",
        " de î": " d'î",
        " de o": " d'o",
        " de u": " d'u",
        " de h": " d'h",
        " de A": " d'A",
        " de E": " d'E",
        " de I": " d'I",
        " de Î": " d'Î",
        " de O": " d'O",
        " de de ": " de ",
        " de des ": " des ",
        " de le ": " du ",
        " de les ": " des ",
        " en la ": " en ",
        " en le ": " en ",
        " en les ": " en ",
        " la a": " l'a",
        " la à": " l'à",
        " la e": " l'e",
        " la é": " l'é",
        " la è": " l'è",
        " la ê": " l'ê",
        " la i": " l'i",
        " la î": " l'î",
        " la o": " l'o",
        " la ô": " l'ô",
        " la u": " l'u",
        " le a": " l'a",
        " le à": " l'à",
        " le e": " l'e",
        " le é": " l'é",
        " le è": " l'è",
        " le ê": " l'ê",
        " le i": " l'i",
        " le î": " l'î",
        " le o": " l'o",
        " le ô": " l'ô",
        " le u": " l'u",
        " la A": " l'A",
        " la À": " l'À",
        " la E": " l'E",
        " la É": " l'É",
        " la È": " l'È",
        " la Ê": " l'Ê",
        " la I": " l'I",
        " la Î": " l'Î",
        " la O": " l'O",
        " la Ô": " l'Ô",
        " la U": " l'U",
        " le A": " l'A",
        " le À": " l'À",
        " le E": " l'E",
        " le É": " l'É",
        " le È": " l'È",
        " le Ê": " l'Ê",
        " le I": " l'I",
        " le Î": " l'Î",
        " le O": " l'O",
        " le Ô": " l'Ô",
        " le U": " l'U",
        " le la ": " la ",
        " le le ": " le ",
        " le les ": " les ",
        " un l'": " un ",
        " un l'": " un ",
        " un la ": " une ",
        " un le ": " un ",
        " un les ": " des ",
        " son la ": " sa ",
        " son le ": " son ",
        " son l'": " son ",
        " son l'": " son ",
        " son les ": " ses ",
        " que a": " qu'a",
        " que à": " qu'à",
        " que e": " qu'e",
        " que é": " qu'é",
        " que è": " qu'è",
        " que ê": " qu'ê",
        " que i": " qu'i",
        " que î": " qu'î",
        " que u": " qu'u",
        " que A": " qu'A",
        " que E": " qu'E",
        " que I": " qu'I",
        " que Î": " qu'Î",
        " que U": " qu'U",
        " ,": ",",
    }
    return _strtr(text, CORRECTIONS)


def _strtr(string: str, corrections: dict) -> str:
    buffer = []
    i, n = 0, len(string)
    while i < n:
        match = False
        for s, r in corrections.items():
            if string[i : len(s) + i] == s:
                buffer.append(r)
                i = i + len(s)
                match = True
                break
        if not match:
            buffer.append(string[i])
            i = i + 1
    return "".join(buffer)
