import { MutableRefObject, RefObject, useEffect, useRef, useState } from 'react';

import * as faceapi from 'face-api.js';
import Webcam from 'react-webcam';

import './Ai.css';

const Ai = () => {
	const videoRef = useRef<HTMLVideoElement>(null);
	const cameraCanvas: any = useRef();

	const [results, setResults]: any = useState([]);
	const detectFaces = async (image: HTMLVideoElement) => {
		if (!image) {
            console.log('no image')
			return;
		}

		const imgSize = image.getBoundingClientRect();
		const displaySize = { width: imgSize.width, height: imgSize.height };
		if (displaySize.height === 0) {
            console.log('image size err')
			return;
		}

		const faces = await faceapi
			.detectAllFaces(image, new faceapi.TinyFaceDetectorOptions({ inputSize: 320 }))
			.withFaceLandmarks()
			.withFaceExpressions()
			.withAgeAndGender();

		return faceapi.resizeResults(faces, displaySize);
	};
	const drawResults = async (image:any, canvas:any, results:any) => {
		if (image && canvas && results) {
			const imgSize = image.getBoundingClientRect();
			const displaySize = { width: imgSize.width, height: imgSize.height };
			faceapi.matchDimensions(canvas, displaySize);
			canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
			const resizedDetections = faceapi.resizeResults(results, displaySize);
            faceapi.draw.drawDetections(canvas, resizedDetections);
            faceapi.draw.drawFaceExpressions(canvas, resizedDetections);
            faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
		}
        else {
            console.log('no image, canvas, or results')
        }
	};

	const getFaces = async () => {
		if (videoRef.current !== null && videoRef.current !== undefined) {
			const faces = await detectFaces(videoRef.current/* .video */);
			await drawResults(videoRef.current/* .video */, cameraCanvas.current, faces);
			setResults(faces);
		}
	};

	const clearOverlay = (canvas: any) => {
		canvas.current.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
	};

    const [captureVideo, setCaptureVideo] = useState(false);
    function startCamera() {
        setCaptureVideo(true);
        navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
            videoRef!.current!.srcObject = stream;
        }).catch((err) => {
            console.log(err)
        });
        console.log('camera started')
    }

    function stopCamera() {
        videoRef.current!.pause();
        videoRef.current!.srcObject = null;
        setCaptureVideo(false);
        clearOverlay(cameraCanvas);
    }

    const intervalRef = useRef<any>(null)
	useEffect(() => {
        if (captureVideo) {
            console.log('ping')

            if (videoRef !== null && videoRef !== undefined) {

                intervalRef.current = setInterval(async () => {
                    await getFaces();
                    console.log(captureVideo);
                }, 100);
                console.log(intervalRef.current)
                /* return () => {
                    clearOverlay(cameraCanvas);
                    clearInterval(ticking);
                }; */
            } /* else {
                clearInterval(ticking);
                return clearOverlay(cameraCanvas);
            } */
        } else {
            console.log('pong')
            console.log(captureVideo)
            console.log(intervalRef.current)
            clearInterval(intervalRef.current);
            intervalRef.current = null;
        }

	}, [captureVideo]);

	return (
		<div className="ai">
			
			<div className='viewer'>
                {
                    captureVideo ?
                    <div className="camera">
                        {videoRef == undefined ? 'no video ref' : ''}
                        <video ref={videoRef} width="480px" height="365px" autoPlay></video>
                        <canvas className={'webcam-overlay'} ref={cameraCanvas}></canvas>
                    </div>
                    : <div className='nocamera'></div>
                }
            </div>
			<div className='startstop'>
                {
                    !captureVideo ?
                    <button onClick={startCamera}>start camera</button>
                    : <button onClick={stopCamera}>stop camera</button>
                }
                {
                    <button>upload file</button>
                }
			</div>
		</div>
	);
}; export default Ai;