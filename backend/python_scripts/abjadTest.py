
import abjad

def abjadTest():
    staff = abjad.Staff("c'4")
    # score = abjad.Score([staff])
    score = abjad.Score("{ { { { g'1 } { g'1 } } } }", name='Score', simultaneous=True)
    # Create a LilyPond file and add a simple note
    lilypond_file = abjad.LilyPondFile(items=[r"#(set-global-staff-size 28)", score])

    # Save the score to a PNG file
    abjad.persist.as_png(lilypond_file, 'simple_score.png', flags="-dcrop", resolution=300)

def main():
    abjadTest()

if __name__ == '__main__':
    main()