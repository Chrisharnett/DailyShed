import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Navigation from "../components/NavBar";
import "bootstrap/dist/css/bootstrap.min.css";
import Button from "react-bootstrap/Button";
import axios from "axios";
import useUser from "../hooks/useUser";
import CurrentExercise from "../components/CurrentExercise";
import SmallExercise from "../components/SmallExercise";

const ExerciseTestPage = () => {
  const [student, setStudent] = useState({
    name: "Chris",
    exerciseHistory: [
      {
        exercise: {
          exerciseName: "g_major_0_tone_0",
          pitchPattern: {
            notePatternId: 0,
            notePatternType: "tone",
            notePattern: [1],
            rhythmMatcher: "tone",
            description: "on the 1",
            dynamic: "",
            direction: "static",
            repeatMe: true,
            holdLastNote: false,
          },
          rhythmPattern: {
            rhythmId: "tone_0",
            rhythmType: "tone",
            rhythmDescription: "one note long tone",
            rhythmPattern: [["1"]],
            timeSignature: [4, 4],
            articulation: [
              {
                articulation: "fermata",
                index: 0,
                name: "fermata",
              },
            ],
            noteLength: 1,
          },
          key: "g",
          mode: "major",
          imageFileName: "g_major_0_tone_0.cropped.png",
          imageURL:
            "https://mysaxpracticeexercisebucket.s3.amazonaws.com/g_major_0_tone_0",
          description: "g major 0  [1] tone on the 1  in 4 / 4.",
        },
        assessment: 2,
        playCount: 1,
      },
      {
        exercise: {
          exerciseName: "g_major_1_tone_0",
          pitchPattern: {
            notePatternId: 1,
            notePatternType: "tone",
            notePattern: [2],
            rhythmMatcher: "tone",
            description: "on the 2",
            dynamic: "",
            direction: "static",
            repeatMe: true,
            holdLastNote: false,
          },
          rhythmPattern: {
            rhythmId: "tone_0",
            rhythmType: "tone",
            rhythmDescription: "one note long tone",
            rhythmPattern: [["1"]],
            timeSignature: [4, 4],
            articulation: [
              {
                articulation: "fermata",
                index: 0,
                name: "fermata",
              },
            ],
            noteLength: 1,
          },
          key: "g",
          mode: "major",
          imageFileName: "g_major_1_tone_0.cropped.png",
          imageURL:
            "https://mysaxpracticeexercisebucket.s3.amazonaws.com/g_major_1_tone_0",
          description: "g major 1  [2] tone on the 2  in 4 / 4.",
        },
        assessment: 4,
        playCount: 1,
      },
      {
        exercise: {
          exerciseName: "g_major_8_r1",
          pitchPattern: {
            notePatternId: 8,
            notePatternType: "scale",
            notePattern: [1, 2],
            rhythmMatcher: "general",
            description: "to the 2",
            dynamic: "",
            direction: "ascending",
            repeatMe: true,
            holdLastNote: true,
          },
          rhythmPattern: {
            rhythmId: "r1",
            rhythmType: "general",
            rhythmDescription: "quarter note",
            rhythmPattern: [["4"], ["r4"], ["r4"], ["r4"]],
            timeSignature: [4, 4],
            articulation: null,
            noteLength: 1,
          },
          key: "g",
          mode: "major",
          imageFileName: "g_major_8_r1.cropped.png",
          imageURL:
            "https://mysaxpracticeexercisebucket.s3.amazonaws.com/g_major_8_r1",
          description:
            "g major 8  [1, 2] scale to the 2 quarter note rhythm, in 4 / 4.",
        },
        assessment: 5,
        playCount: 1,
      },
      {
        exercise: {
          exerciseName: "g_major_9_r5",
          pitchPattern: {
            notePatternId: 9,
            notePatternType: "scale",
            notePattern: [1, 2, 3],
            rhythmMatcher: "general",
            description: "to the 3",
            dynamic: "",
            direction: "ascending",
            repeatMe: true,
            holdLastNote: true,
          },
          rhythmPattern: {
            rhythmId: "r5",
            rhythmType: "general",
            rhythmDescription: "quarter note",
            rhythmPattern: [["4"], ["4"], ["r4"], ["r4"]],
            timeSignature: [4, 4],
            articulation: null,
            noteLength: 2,
          },
          key: "g",
          mode: "major",
          imageFileName: "g_major_9_r5.cropped.png",
          imageURL:
            "https://mysaxpracticeexercisebucket.s3.amazonaws.com/g_major_9_r5",
          description:
            "g major 9  [1, 2, 3] scale to the 3 quarter note rhythm, in 4 / 4.",
        },
        assessment: 5,
        playCount: 1,
      },
    ],
    currentStatus: {
      setPattern: [
        {
          type: "tone",
          reviewBool: 1,
          key: "g",
          mode: "major",
        },
        {
          type: "tone",
          reviewBool: 0,
          key: "g",
          mode: "major",
        },
        {
          type: "ninthScale1",
          reviewBool: 1,
          key: "g",
          mode: "major",
        },
        {
          type: "ninthScale1",
          reviewBool: 0,
          key: "g",
          mode: "major",
        },
      ],
      currentIndex: {
        tone: {
          index: 1,
          currentKey: "g",
          currentMode: "major",
        },
        ninthScale1: {
          index: 1,
          currentKey: "g",
          currentMode: "major",
        },
      },
    },
    previousSet: [
      {
        exerciseName: "g_major_0_tone_0",
        pitchPattern: {
          notePatternId: 0,
          notePatternType: "tone",
          notePattern: [1],
          rhythmMatcher: "tone",
          description: "on the 1",
          dynamic: "",
          direction: "static",
          repeatMe: true,
          holdLastNote: false,
        },
        rhythmPattern: {
          rhythmId: "tone_0",
          rhythmType: "tone",
          rhythmDescription: "one note long tone",
          rhythmPattern: [["1"]],
          timeSignature: [4, 4],
          articulation: [
            {
              articulation: "fermata",
              index: 0,
              name: "fermata",
            },
          ],
          noteLength: 1,
        },
        key: "g",
        mode: "major",
        imageFileName: "g_major_0_tone_0.cropped.png",
        imageURL:
          "https://mysaxpracticeexercisebucket.s3.amazonaws.com/g_major_0_tone_0",
        description: "g major 0  [1] tone on the 1  in 4 / 4.",
      },
      {
        exerciseName: "g_major_1_tone_0",
        pitchPattern: {
          notePatternId: 1,
          notePatternType: "tone",
          notePattern: [2],
          rhythmMatcher: "tone",
          description: "on the 2",
          dynamic: "",
          direction: "static",
          repeatMe: true,
          holdLastNote: false,
        },
        rhythmPattern: {
          rhythmId: "tone_0",
          rhythmType: "tone",
          rhythmDescription: "one note long tone",
          rhythmPattern: [["1"]],
          timeSignature: [4, 4],
          articulation: [
            {
              articulation: "fermata",
              index: 0,
              name: "fermata",
            },
          ],
          noteLength: 1,
        },
        key: "g",
        mode: "major",
        imageFileName: "g_major_1_tone_0.cropped.png",
        imageURL:
          "https://mysaxpracticeexercisebucket.s3.amazonaws.com/g_major_1_tone_0",
        description: "g major 1  [2] tone on the 2  in 4 / 4.",
      },
      {
        exerciseName: "g_major_8_r1",
        pitchPattern: {
          notePatternId: 8,
          notePatternType: "scale",
          notePattern: [1, 2],
          rhythmMatcher: "general",
          description: "to the 2",
          dynamic: "",
          direction: "ascending",
          repeatMe: true,
          holdLastNote: true,
        },
        rhythmPattern: {
          rhythmId: "r1",
          rhythmType: "general",
          rhythmDescription: "quarter note",
          rhythmPattern: [["4"], ["r4"], ["r4"], ["r4"]],
          timeSignature: [4, 4],
          articulation: null,
          noteLength: 1,
        },
        key: "g",
        mode: "major",
        imageFileName: "g_major_8_r1.cropped.png",
        imageURL:
          "https://mysaxpracticeexercisebucket.s3.amazonaws.com/g_major_8_r1",
        description:
          "g major 8  [1, 2] scale to the 2 quarter note rhythm, in 4 / 4.",
      },
      {
        exerciseName: "g_major_9_r5",
        pitchPattern: {
          notePatternId: 9,
          notePatternType: "scale",
          notePattern: [1, 2, 3],
          rhythmMatcher: "general",
          description: "to the 3",
          dynamic: "",
          direction: "ascending",
          repeatMe: true,
          holdLastNote: true,
        },
        rhythmPattern: {
          rhythmId: "r5",
          rhythmType: "general",
          rhythmDescription: "quarter note",
          rhythmPattern: [["4"], ["4"], ["r4"], ["r4"]],
          timeSignature: [4, 4],
          articulation: null,
          noteLength: 2,
        },
        key: "g",
        mode: "major",
        imageFileName: "g_major_9_r5.cropped.png",
        imageURL:
          "https://mysaxpracticeexercisebucket.s3.amazonaws.com/g_major_9_r5",
        description:
          "g major 9  [1, 2, 3] scale to the 3 quarter note rhythm, in 4 / 4.",
      },
    ],
  });
  const [currentSet, setCurrentSet] = useState(null);

  useEffect(() => {
    const getSet = async () => {
      try {
        let response = await axios.post("/api/generateSet", student);
        console.log("Practice set data received:", response.data);
        setCurrentSet(response.data);
      } catch (error) {
        console.error("Error: ", error);
      }
    };
    getSet();
  }, [student]);

  if (currentSet) {
    return (
      <>
        <Navigation />
        <h1>Student Test Set Page</h1>
        {currentSet.map((ex, index) => {
          return (
            <>
              <SmallExercise key={index} exercise={ex} />
            </>
          );
        })}
      </>
    );
  }
};

export default ExerciseTestPage;
