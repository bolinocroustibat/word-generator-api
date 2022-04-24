import re
from typing import Iterator, Match


def add_to_text_fr(text: str, string: str) -> str:
    try:
        if text[-1] not in ["'", "’", "-"] and string[0] not in [".", ",", "-"]:
            return text + " " + string
    except IndexError:
        pass
    return text + string


def correct_text_fr(text: str) -> str:
    # TODO: use regexes
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
        " du a": " de l'a",
        " du e": " de l'e",
        " du é": " de l'é",
        " du è": " de l'è",
        " du ê": " de l'ê",
        " du i": " de l'i",
        " du î": " de l'î",
        " du o": " de l'o",
        " du u": " de l'u",
        " du h": " de l'h",
        " du A": " de l'A",
        " du E": " de l'E",
        " du I": " de l'I",
        " du Î": " de l'Î",
        " du O": " de l'O",
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
        "La a": "L'a",
        "La à": "L'à",
        "La e": "L'e",
        "La é": "L'é",
        "La è": "L'è",
        "La ê": "L'ê",
        "La i": "L'i",
        "La î": "L'î",
        "La o": "L'o",
        "La ô": "L'ô",
        "La u": "L'u",
        "Le a": "L'a",
        "Le à": "L'à",
        "Le e": "L'e",
        "Le é": "L'é",
        "Le è": "L'è",
        "Le ê": "L'ê",
        "Le i": "L'i",
        "Le î": "L'î",
        "Le o": "L'o",
        "Le ô": "L'ô",
        "Le u": "L'u",
        "La A": "L'A",
        "La À": "L'À",
        "La E": "L'E",
        "La É": "L'É",
        "La È": "L'È",
        "La Ê": "L'Ê",
        "La I": "L'I",
        "La Î": "L'Î",
        "La O": "L'O",
        "La Ô": "L'Ô",
        "La U": "L'U",
        "Le A": "L'A",
        "Le À": "L'À",
        "Le E": "L'E",
        "Le É": "L'É",
        "Le È": "L'È",
        "Le Ê": "L'Ê",
        "Le I": "L'I",
        "Le Î": "L'Î",
        "Le O": "L'O",
        "Le Ô": "L'Ô",
        "Le U": "L'U",
        "Le la ": "La ",
        "Le le ": "Le ",
        "Le les ": "Les ",
        " un l'": " un ",
        " un l'": " un ",
        " un la ": " une ",
        " un le ": " un ",
        " un les ": " des ",
        "Un l'": "Un ",
        "Un l'": "Un ",
        "Un la ": "Une ",
        "Un le ": "Un ",
        "Un les ": " des ",
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
