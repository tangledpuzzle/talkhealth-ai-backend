import { useEffect, useRef, useState } from 'react';

import * as faceapi from 'face-api.js';
import Webcam from 'react-webcam';
import Ai from '../Ai/Ai';
import './App.css';

const App = () => {

	let [ready, setReady] = useState<boolean>(false);

	const loadModels = () => {
		const MODEL_URL = `${process.env.PUBLIC_URL}/models`;

		let p: Promise<Array<any>> = Promise.all([
			faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
			faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
			faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
			faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL),
			faceapi.nets.ageGenderNet.loadFromUri(MODEL_URL),
		]);
		return p;

	};
	useEffect(() => {
		loadModels();
		setReady(true);
		console.log('models loaded')
	}, [])

	let emotions = [
		'neutral',
		'happy',
		'sad',
		'angry',
		'fearful',
		'disgusted',
		'surprised'
	]

	let [currentEmotion, setCurrentEmotion] = useState<string>('neutral');
	let [hasResult, setHasResult] = useState<boolean>(false);

	function handleGradient(results: any) {

		if (results === undefined) {
			setHasResult(false);
			return;
		} else {
			setHasResult(true);
		}

		console.log(results)
		let expressions = results[0].expressions;
		console.log(expressions)
		let emotion = Object.keys(expressions).reduce((a, b) => expressions[a] > expressions[b] ? a : b);
		console.log(emotion)
		setCurrentEmotion(emotion);
	}

	return (
		<>
			<div className={`gradient t ${currentEmotion as string}`}></div>
			<div className="app">
				<div className='emotion'>
					{
						hasResult ? currentEmotion : 'emotion ai'
					}
				</div>
				{
					ready ? <Ai gradientCallback={handleGradient}/> : 'loading...'
				}
			</div>
		</>
	);
}; export default App;