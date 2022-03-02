from typing import Tuple


def classify_fr(word: str) -> dict:
    """
    Classify french word
	if (mb_substr($string, -1) == 'é') {
		$type = 'past-participle';
		$gender = 'm';
		$number = 's';
	} elseif (mb_substr($string, -2) == 'ée') {
		$type = 'past-participle';
		$gender = 'f';
		$number = 's';
	} elseif (mb_substr($string, -2) == 'és') {
		$type = 'past-participle';
		$gender = 'm';
		$number = 'p';
	} elseif (mb_substr($string, -3) == 'ées') {
		$type = 'past-participle';
		$gender = 'f';
		$number = 'p';
	} elseif ((substr($string, -2) == 'er') or (substr($string, -2) == 'ir')) {
		$type = 'verb';
		$tense = 'infinitive';
	} elseif (substr($string, -3) == 'ons') {
		$type = 'verb';
		$tense = 'present';
		$conjug = '4';
	} elseif (substr($string, -2) == 'ez') {
		$type = 'verb';
		$tense = 'present';
		$conjug = '5';
	} elseif ((substr($string, -3)) == 'ent') {
		$type = 'verb';
		$tense = 'present';
		$conjug = '6';
	} elseif (substr($string, -3) == 'ais') {
		$type = 'verb';
		$tense = 'present';
		$conjug = '1';
	} elseif (substr($string, -2) == 'as') {
		$type = 'verb';
		$tense = 'present';
		$conjug = '2';
	} elseif (substr($string, -3) == 'ait') {
		$type = 'verb';
		$tense = 'present';
		$conjug = '3';
	} elseif (substr($string, -5) == 'aient') {
		$type = 'verb';
		$tense = 'past';
		$conjug = '6';
	} elseif (substr($string, -2) == 'ra') {
		$type = 'verb';
		$tense = 'future';
		$conjug = '1';
	} elseif (substr($string, -3) == 'ras') {
		$type = 'verb';
		$tense = 'future';
		$conjug = '2';
	} elseif (substr($string, -3) == 'ont') {
		$type = 'verb';
		$tense = 'future';
		$conjug = '6';
	} elseif (substr($string, -2) == 'if') {
		$type = 'adjective';
		$gender = 'm';
		$number = 's';
	} elseif (substr($string, -3) == 'ive') {
		$type = 'adjective';
		$gender = 'f';
		$number = 's';
	} elseif (substr($string, -3) == 'eux') {
		$type = 'adjective';
		$gender = 'm';
		$number = 'p';
	} elseif (substr($string, -4) == 'euse') {
		$type = 'adjective';
		$gender = 'f';
		$number = 'p';
	} elseif (substr($string, -4) == 'ique') {
		$type = 'adjective';
		$gender = 'm';
		$number = 's';
	} elseif (substr($string, -2) == 'es') {
		$type = 'noun';
		$gender = 'f';
		$number = 'p';
	} elseif (substr($string, -1) == 'e') {
		$type = 'noun';
		$gender = 'f';
		$number = 's';
	} elseif (substr($string, -1) == 's') {
		$type = 'noun';
		$gender = 'm';
		$number = 'p';
	} else {
		$type = 'noun';
		$gender = 'm';
		$number = 's';
    """
    type = None
    gender = None
    number = None
    tense = None
    conjug = None

    # TODO

    return {
        "type": type,
        "gender": gender,
        "number": number,
        "tense": tense,
        "conjug": conjug,
    }
