import { useEffect, useRef, useState } from 'react';

import * as faceapi from 'face-api.js';
import Webcam from 'react-webcam';
import Ai from './Ai';

const App = () => {

	let [ready, setReady] = useState(false);

	const loadModels = () => {
		const MODEL_URL = `${process.env.PUBLIC_URL}/models`;

		let p = Promise.all([
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

	return (
		<div className="app">
			{/* <button>Activate</button>
			<button>Deactivate</button> */}
			{
				ready ? <Ai /> : 'loading...'
			}
		</div>
	);
}; export default App;