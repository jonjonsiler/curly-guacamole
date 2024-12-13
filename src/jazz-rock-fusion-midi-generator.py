from mido import Message, MidiFile, MidiTrack

# Create a new MIDI file
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Add Chords
chord_progression = [
    (64, 67, 71, 74),  # Emaj7
    (66, 69, 73, 76),  # F#m7
    (68, 71, 74, 77),  # G#m7(11)
    (69, 72, 76, 79),  # Amaj7(#11)
]

time_interval = 480  # Quarter note duration

for chord in chord_progression:
    for note in chord:
        track.append(Message('note_on', note=note, velocity=64, time=0))
    track.append(Message('note_off', note=chord[0], velocity=64, time=time_interval))
    for note in chord:
        track.append(Message('note_off', note=note, velocity=64, time=0))

# Add Bassline
bassline = [40, 42, 44, 45]  # Bass notes for funk rhythm
for note in bassline:
    track.append(Message('note_on', note=note, velocity=64, time=240))
    track.append(Message('note_off', note=note, velocity=64, time=240))

# Save the MIDI file
mid.save("JazzRockFusion_Composition.mid")

