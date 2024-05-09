import abjad

noteString = "r4 r4 g'4 r4"
lastMeasure = "a'1"
container = abjad.Container(noteString)
container2 = abjad.Container(lastMeasure)

staff = abjad.Staff([container])
staff.append(lastMeasure)
repeat = abjad.Repeat()
abjad.attach(repeat, container)

key_signature = abjad.KeySignature(
    abjad.NamedPitchClass("e"), abjad.Mode("minor")
)
abjad.attach(key_signature, container[0])
abjad.show(staff)
