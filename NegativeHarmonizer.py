import argparse
import os
import mido

def get_mirror_line(tonic):
    return tonic + 3.5

def mirror_note_over_line(note, line):
    original_distance = line - note
    return int(line + original_distance)

def mirror_pitch_bend_over_line(pitch_bend, line):
    original_distance = line - pitch_bend
    mirrored_value = int(line + original_distance)
    return max(min(mirrored_value, 8191), -8192)

def find_average_track_notes(track):
    notes = [message.note for message in track if message.type == 'note_on']
    return sum(notes) / len(notes) if notes else None

def mirror_all_notes_in_track(track, line, ignored_channels):
    for message in track:
        if message.type in ('note_on', 'note_off') and message.channel not in ignored_channels:
            message.note = mirror_note_over_line(message.note, line)
        elif message.type == 'pitchwheel' and message.channel not in ignored_channels:
            message.pitch = mirror_pitch_bend_over_line(message.pitch, line)

def transpose_to_original_octaves(track, original_notes, new_notes, ignored_channels):
    if original_notes is not None and new_notes is not None:
        notes_distance = original_notes - new_notes
        octaves_to_transpose = round(notes_distance / 12)
        for message in track:
            if message.type in ('note_on', 'note_off') and message.channel not in ignored_channels:
                transposed_note = message.note + (octaves_to_transpose * 12)
                message.note = max(0, min(transposed_note, 127))

def invert_tonality(midi_file, tonic, ignored_channels, adjust_octaves):
    mirror_line = get_mirror_line(tonic)

    original_track_notes = {}
    new_track_notes = {}

    for i, track in enumerate(midi_file.tracks):
        original_track_notes[i] = find_average_track_notes(track)
        mirror_all_notes_in_track(track, mirror_line, ignored_channels)
        new_track_notes[i] = find_average_track_notes(track)
        transpose_to_original_octaves(track, original_track_notes[i], new_track_notes[i], ignored_channels)

def main(input_file, tonic, ignored_channels, adjust_octaves):
    root, ext = os.path.splitext(input_file)
    midi_file = mido.MidiFile(input_file)

    invert_tonality(midi_file, tonic, ignored_channels, adjust_octaves)
    midi_file.save(root + "_negative" + ext)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Negative Harmonize a midi file.')

    parser.add_argument('file', metavar='f', help='the input midi file (with no extension .mid)')
    parser.add_argument('--tonic', type=int, default=60, help='the tonic')
    parser.add_argument('--ignore', type=int, nargs="+", default=[],
                        help='the midi channels to ignore (usually 9 for drums)')
    parser.add_argument('--adjust-octaves', dest='adjust_octaves', action='store_true',
                        help='transpose octaves to keep bass instruments low')
    parser.set_defaults(adjust_octaves=False)

    args = parser.parse_args()

    main(input_file=args.file, tonic=args.tonic, ignored_channels=args.ignore, adjust_octaves=args.adjust_octaves)
