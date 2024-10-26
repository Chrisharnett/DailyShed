import { useState, useEffect } from "react";
import Container from "react-bootstrap/esm/Container";

// export function ExerciseList({ exList }) {
//   return exList.map((exList, i) => {
//     return (
//       <Exercise
//         key={i}
//         title={exList.exerciseName}
//         description={exList.description}
//         src={exList.imageURL}
//         height={50}
//       />
//     );
//   });
// }

// export function ExSelection({ exList, onNewProgramSequenceChange }) {
//   const [checked, setChecked] = useState([]);
//   const [patternTypes, setPatternTypes] = useState(null);
//   const [uniqueKeys, setUniqueKeys] = useState([]);
//   const [uniqueModes, setUniqueModes] = useState([]);
//   const [keys, setKeys] = useState([]);
//   const [modes, setModes] = useState([]);
//   const [sampleExercises, setSampleExercises] = useState([]);
//   const [newProgramSequence, setNewProgramSequence] = useState([]);
//   const [selectedExercises, setSelectedExercises] = useState([]);

//   useEffect(() => {
//     if (exList) {
//       // Get unique patternTypes
//       const types = exList.map((exercise) => {
//         return exercise.patternType;
//       });
//       const uniquePatternTypes = [...new Set(types)];

//       // Get unique keys
//       const keys = exList.map((ex) => {
//         return ex.key;
//       });
//       const uKeys = [...new Set(keys)];

//       //Get unique modes
//       const modes = exList.map((ex) => {
//         return ex.mode;
//       });
//       const uModes = [...new Set(modes)];

//       setPatternTypes(uniquePatternTypes);
//       setUniqueKeys(uKeys);
//       setUniqueModes(uModes);
//     }
//   }, [exList]);

//   useEffect(() => {
//     if (exList && patternTypes) {
//       const filteredExercises = exList.filter((ex) => {
//         return ex.key === "g" && ex.mode === "major";
//       });
//       setSampleExercises(filteredExercises);
//     }
//   }, [exList, patternTypes]);

//   const handleCheck = (event, exercise) => {
//     const exerciseId = exercise.exerciseId;
//     const isChecked = event.target.checked;

//     const newSelectedExercises = { ...selectedExercises };
//     const newKeys = { ...keys };
//     const newModes = { ...modes };

//     if (isChecked) {
//       newKeys[exerciseId] = exercise.key;
//       newModes[exerciseId] = exercise.mode;
//     } else {
//       delete newKeys[exerciseId];
//       delete newModes[exerciseId];
//     }

//     if (Object.keys(newSelectedExercises).length === 0) {
//       newKeys[exerciseId] = "g";
//       newModes[exerciseId] = "major";
//     }

//     newSelectedExercises[exerciseId] = exercise;

//     setSelectedExercises(newSelectedExercises);
//     setKeys(newKeys);
//     setModes(newModes);

//     if (isChecked) {
//       setChecked([...checked, exercise]);
//     } else {
//       const updatedChecked = checked.filter(
//         (ex) => ex.exerciseId !== exerciseId
//       );
//       setChecked(updatedChecked);
//     }
//   };

//   useEffect(() => {
//     if (checked.length > 0) {
//       // Map over the values in keys to create an array of exercises.
//       const updatedProgramSequence = Object.values(keys).map((key, index) => ({
//         patternId: checked[index].patternId,
//         key: key,
//         mode: modes[checked[index].exerciseId],
//       }));
//       setNewProgramSequence(updatedProgramSequence);
//     }
//   }, [checked, keys, modes]);

//   useEffect(() => {
//     onNewProgramSequenceChange(newProgramSequence);
//   }, [newProgramSequence, onNewProgramSequenceChange]);

//   const isChecked = (exerciseId) =>
//     Boolean(keys[exerciseId]) && Boolean(modes[exerciseId])
//       ? "checked-item"
//       : "not-checked-item";

//   const handlePatternFilter = (pType) => {
//     if (pType === "all") {
//       setSampleExercises(
//         exList.filter((ex) => {
//           return ex.key === "g" && ex.mode === "major";
//         })
//       );
//     } else {
//       let filteredExercises = exList.filter((ex) => {
//         return ex.patternType === pType;
//       });
//       setSampleExercises(filteredExercises);
//     }
//   };

//   const handleKeyChange = (event, exerciseId) => {
//     const newKeys = { ...keys };
//     newKeys[exerciseId] = event.target.value;
//     setKeys(newKeys);
//   };

//   const handleModeChange = (event, exerciseId) => {
//     const newModes = { ...modes };
//     newModes[exerciseId] = event.target.value;
//     setModes(newModes);
//   };

//   if (patternTypes && keys && modes && sampleExercises) {
//     return (
//       <div className="checkList">
//         <h3>Selected Exercises</h3>
//         <div className="d-inline-flex">
//           {Object.values(selectedExercises).map((ex, index) => (
//             <div id={ex.exerciseId} key={index} className="m-3">
//               <p>
//                 {index + 1}. {ex.exerciseName}
//               </p>
//               <img src={ex.imageURL} alt={ex.exerciseName} height={35} />
//               <p>Key</p>
//               <select
//                 title="Exercise Key"
//                 value={keys[ex.exerciseId] || ""}
//                 onChange={(event) => {
//                   handleKeyChange(event, ex.exerciseId);
//                 }}
//                 id={ex.exerciseId + "_exerciseKeySelector"}
//               >
//                 {" "}
//                 {uniqueKeys.map((key, keyIndex) => {
//                   return (
//                     <option
//                       key={keyIndex}
//                       id={"key_" + ex.exerciseId + "_" + keyIndex}
//                       value={key}
//                     >
//                       {" "}
//                       {key}
//                     </option>
//                   );
//                 })}
//               </select>
//               <p>Mode</p>
//               <select
//                 title="Exercise Mode"
//                 value={modes[ex.exerciseId] || ""}
//                 onChange={(event) => {
//                   handleModeChange(event, ex.exerciseId);
//                 }}
//                 id={ex.exerciseId + "_exerciseModeSelector"}
//               >
//                 {uniqueModes.map((mode, modeIndex) => {
//                   return (
//                     <option
//                       id={"mode_" + ex.exerciseId + "_" + modeIndex}
//                       key={modeIndex}
//                       value={mode}
//                     >
//                       {" "}
//                       {mode.replace("_", " ")}
//                     </option>
//                   );
//                 })}
//               </select>
//             </div>
//           ))}
//         </div>
//         <hr></hr>
//         <Container className="inline">
//           <h3>Exercise List</h3>
//           <h4>Filter</h4>
//           <select
//             id="patternFilter"
//             variant="success"
//             title="Pattern Type"
//             onChange={(event) => handlePatternFilter(event.target.value)}
//           >
//             <option value="all">Show All</option>
//             {patternTypes.map((patternType, index) => {
//               return (
//                 <option id={index} key={patternType}>
//                   {" "}
//                   {patternType}
//                 </option>
//               );
//             })}
//           </select>
//         </Container>
//         <div>
//           {sampleExercises.map((ex, index) => (
//             <div key={index} className="form-check mb-3">
//               <input
//                 id={ex.imageURL}
//                 value={index}
//                 name={ex.exerciseName}
//                 type="checkbox"
//                 onChange={(event) => handleCheck(event, ex)}
//                 checked={
//                   Boolean(keys[ex.exerciseId]) && Boolean(modes[ex.exerciseId])
//                 }
//               />
//               <h4 className={isChecked(ex.exerciseId)}>{ex.exerciseName} </h4>
//               <img src={ex.imageURL} alt={ex.description} height={50}></img>
//             </div>
//           ))}
//         </div>
//       </div>
//     );
//   }
// }

// export function Routines({ studentRoutines }) {
//   return (
//     <div>
//       {studentRoutines && studentRoutines.length > 0 ? (
//         <div>
//           {studentRoutines.map((routine, index) => (
//             <div id={index} key={index}>
//               <p>
//                 {index + 1}. Student: {routine.student}
//               </p>
//             </div>
//           ))}
//         </div>
//       ) : (
//         <p>No routines available.</p>
//       )}
//     </div>
//   );
// }

// export function Exercise(props) {
//   return (
//     <>
//       <h4>{props.exerciseName}</h4>
//       <img src={props.src} alt={props.description} height={props.height}></img>
//       <p>{props.description}</p>
//     </>
//   );
// }
