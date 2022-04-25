import logic.chords_new as chords
from pprint import pprint
import logic.classes as classes
import math

from scipy import spatial


def find_base(notes):
    if(notes):
        bottom = sorted(notes, key=lambda x:x.note)[0]

    base_note = []
    for n in notes:
        for m in notes:
            if(m != n and n.note_number == bottom.note_number):
                if(n.note_number == m.note_number and n.note - m.note >= 12):
                    if(n.note_number not in base_note):
                        base_note.append(n.note_number)
    return base_note

def match_chords_old(notes, key):
    # find base
    base_note = find_base(notes)
    print(base_note)

    # find scale
    scale = chords.getScaleByKey(key)
    #pprint(scale)

    # find unique
    unique_note = []
    for n in notes:
        # unique_note.append(n.note_number)
        if n.note_number not in unique_note:
            unique_note.append(n.note_number)

    # print("base_note")
    # pprint(base_note)
    # print("unique")
    # pprint(unique_note)
    # pprint(chords.Chords.getAllChords())

    all_chords = chords.getAllChords()
    # print(all_chords, '\n')
    score_keys = []
    for chord_key in all_chords: # each key: 0, 1, 2..
        chords_dict = {}
        for chord in chord_key['chords']: # each chord: major, minor, augmented..
            # chord[0] = chord's name, chord[1] = chord's notes number
            chord_match = 0
            chord_length = len(chord[1])
            for note_number in chord[1]: # each number in chord
                if(note_number in unique_note):

                    chord_match += 1
                    if(note_number not in scale):
                        chord_match -= 0.5
                    if(note_number in base_note and note_number in scale):
                        chord_match += 1

                    # score = 1
                    # if(note_number in base_note):
                    #     score = 2
                    # if(chord[0] in chords_dict):
                    #     chords_dict[chord[0]] += score
                    # else:
                    #     chords_dict[chord[0]] = score
            if (chord_match != 0):
                chords_dict[chord[0]] = chord_match/chord_length
        score_keys.append((chord_key['key'], chords_dict))

    # pprint(score_keys)

    # Generate final score
    scores = {}
    for key in range(0, 12):
        scores[key] = 0

    #pprint(scores)

    scores_chord_name = {}
    scores_chord_name = []
    for score_key in score_keys:
        length = len(score_key[1])
        base_bonus = 0
        # if(score_key[0] in base_note): base_bonus = 1
        max = ('NOT_FOUND', 0)
        score = 0
        for chord_name in score_key[1].items():
            #print(chord_name)
            score += chord_name[1]
            if(chord_name[1] > max[1]):
                max = chord_name
        #print('\n')
        #scores_chord_name[chords.Chords.getSign(score_key[0]) + max[0]] = (max[1]+base_bonus)*length
        #scores_chord_name[chords.Chords.getSign(score_key[0]) + max[0]] = (classes.Chord(score_key[0], max[0]), score)
        scores_chord_name.append((classes.Chord(score_key[0], max[0]), score))

    result = list(reversed(sorted(scores_chord_name, key=lambda x:x[1])))[:5]
    return result




def match_chords_new(notes, key):
    # find base
    base_note = find_base(notes)
    #print(base_note)

    # find scale
    # scale = chords.getScaleByKey(key)
    #pprint(list(map(chords.getSign, scale)))

    notes_in_numbers = []
    for n in notes:
        notes_in_numbers.append(n.note_number)

    notes_vector = getNotesVector(notes, base_note)

    all_chords_vector = chords.getAllChordsVector(key)

    # similarity = 1 - spatial.distance.cosine(notes_vector, all_chords_vector)


    chord_scores = []
    for key_to_chords in all_chords_vector:
        key = key_to_chords['key']
        subchords = key_to_chords['chords'] # list of all major, minor.. chords under this key

        for subchord in subchords:
            subchord_name = subchord[0]
            subchord_vector = subchord[1] # list of note numbers of this chord

            subchord_score = 1 - spatial.distance.cosine(notes_vector, subchord_vector)
            chord_scores.append({'key': key, 'subchord': subchord_name, 'subchord_score': subchord_score})





    # compute best chord
    best_chords = sorted(chord_scores, key=lambda x:x["subchord_score"], reverse=True)[0:5]
    return best_chords




def getNotesVector(notes, base_note):
    vector = [0] * 12
    for note in notes:
        vector[note.note_number] += 1
    for note_number in base_note:
        vector[note_number] += 0
    # print(vector)
    return vector
