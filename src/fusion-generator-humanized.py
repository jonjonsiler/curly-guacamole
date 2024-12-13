import os
import random
import hashlib
from mido import MidiFile, MidiTrack, Message

# Function to create a unique hash-based filename
def generate_unique_filename(seed):
    random.seed(seed)
    seed_str = str(seed).encode()
    hash_str = hashlib.md5(seed_str).hexdigest()[:6]
    return f"fusion-dynamic-improvised-{hash_str}.mid"

# Ensure the compositions folder exists
output_folder = "compositions"
os.makedirs(output_folder, exist_ok=True)

# Function to find the note closest to the melody in frequency
def closest_note_to_melody(chord, melody_note):
    return min(chord, key=lambda x: abs(x - melody_note))

# Function to add chords with nuanced dynamics
def add_dynamic_chords(track, chords, base_duration, repetitions, melody_notes):
    melody_index = 0
    for _ in range(repetitions):
        for chord in chords:
            # Pick the melody note for this chord
            melody_note = melody_notes[melody_index % len(melody_notes)]
            melody_index += 1
            
            # Find the chord note closest to the melody
            emphasized_note = closest_note_to_melody(chord, melody_note)
            
            for note in chord:
                velocity = random.randint(50, 70)  # Base velocity variation
                if note == emphasized_note:
                    velocity += 20  # Boost emphasis note
                track.append(Message('note_on', note=note, velocity=velocity, time=0))
            track.append(Message('note_off', note=chord[0], velocity=64, time=base_duration))
            for note in chord:
                track.append(Message('note_off', note=note, velocity=64, time=0))

# Function to add improvisational melody
def add_improvised_melody(track, base_scale, base_duration, bars, notes_per_bar):
    melody = []
    for _ in range(bars):
        for _ in range(notes_per_bar):
            note = random.choice(base_scale)  # Randomly pick a note from the scale
            duration = random.choice([base_duration, base_duration // 2])  # Randomize note duration
            velocity = random.randint(70, 90)  # Dynamic velocity for expressiveness
            track.append(Message('note_on', note=note, velocity=velocity, time=0))
            track.append(Message('note_off', note=note, velocity=64, time=duration))
            melody.append(note)
    return melody

# Chord progression (E Lydian)
chords = [
    [64, 67, 71, 74],  # Emaj7
    [66, 69, 73, 76],  # F#m7
    [68, 71, 74, 77],  # G#m7(11)
    [69, 72, 76, 79],  # Amaj7(#11)
]

# Lead melody/solo scale (E Lydian scale)
lead_scale = [64, 66, 68, 69, 71, 73, 76]

# Initialize MIDI file
mid = MidiFile()
rhythm_guitar = MidiTrack()
bass_guitar = MidiTrack()
lead_guitar = MidiTrack()
synth = MidiTrack()
rhythm_guitar.name = "Rhythm Guitar"
bass_guitar.name = "Bass Guitar"
lead_guitar.name = "Lead Guitar"
synth.name = "Synth Pad"
mid.tracks.extend([rhythm_guitar, bass_guitar, lead_guitar, synth])

# Generate a seed for randomization
seed = random.randint(0, 99999)
filename = generate_unique_filename(seed)
output_path = os.path.join(output_folder, filename)

# Lead Guitar Solo: 24 bars with improvisation
lead_melody = add_improvised_melody(lead_guitar, lead_scale, 240, 24, 5)  # Improvisation within E Lydian

# Intro: Rhythm guitar chords for 16 bars with nuanced dynamics
add_dynamic_chords(rhythm_guitar, chords, 600, 16, lead_melody)

# Bassline accompaniment
add_improvised_melody(bass_guitar, [40, 42, 44, 45], 300, 16, 5)  # Syncopated bass groove

# Synth Pads: Background chords with nuanced dynamics
add_dynamic_chords(synth, chords, 600, 16, lead_melody)

# Save the MIDI file
mid.save(output_path)
print(f"Saved to {output_path}")
