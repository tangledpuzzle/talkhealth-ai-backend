import { ChangeEventHandler, MutableRefObject, RefObject, useEffect, useRef, useState } from 'react';

import * as faceapi from 'face-api.js';
import Webcam from 'react-webcam';

import './Ai.css';

const Ai = () => {
	const videoRef = useRef<HTMLVideoElement>(null);
	const cameraCanvas = useRef<HTMLCanvasElement>(null);

	const [results, setResults] = useState<Array<any> | undefined>([]);
    const [loading, setLoading] = useState(false);
	async function detectFaces(image: HTMLVideoElement | HTMLImageElement): Promise<Array<any>> {
		if (!image) {
            console.log('no image')
			return [];
		}

		const imgSize: DOMRect = image.getBoundingClientRect();
		const displaySize: {width: number; height: number;} = { width: imgSize.width, height: imgSize.height };

		if (displaySize.height === 0) {
            console.log('image size err')
			return [];
		}

		const faces = await faceapi
			.detectAllFaces(image, new faceapi.TinyFaceDetectorOptions({ inputSize: 320 }))
			.withFaceLandmarks()
			.withFaceExpressions()
			.withAgeAndGender();

		return faceapi.resizeResults(faces, displaySize);
	};
	async function drawResults(image: HTMLVideoElement, canvas:HTMLCanvasElement, results:Array<any>): Promise<void> {
		if (image && canvas && results) {
			const imgSize: DOMRect = image.getBoundingClientRect();
			const displaySize: {width: number; height: number;} = { width: imgSize.width, height: imgSize.height };

			faceapi.matchDimensions(canvas, displaySize);
			canvas.getContext('2d')!.clearRect(0, 0, canvas.width, canvas.height);
			const resizedDetections = faceapi.resizeResults(results, displaySize);
            faceapi.draw.drawDetections(canvas, resizedDetections);
            faceapi.draw.drawFaceExpressions(canvas, resizedDetections);
            faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);

            resizedDetections.forEach((face: any) => {

                const box = face.detection.box
                const drawBox = new faceapi.draw.DrawBox(
                    box,
                    {
                        label: Math.round(face.age) + " year old " + face.gender
                    }
                )
                drawBox.draw(canvas)
            })

		}
        else {
            console.log('no image, canvas, or results')
        }
	};

	async function getFaces(): Promise<void> {
        console.log('get faces')
		if (videoRef.current !== null && videoRef.current !== undefined) {
			const faces: Array<any> = await detectFaces(videoRef.current/* .video */);
			await drawResults(videoRef.current/* .video */, cameraCanvas.current!, faces);
			setResults(faces);
		}
        console.log('finished get faces')
        if (loading) {
            setLoading(false)
        }
	};

	const clearOverlay = (canvas: any) => {
		canvas.current.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
	};

    let [fileUploadProcessing, setFileUploadProcessing] = useState<boolean>(false);
    const [captureVideo, setCaptureVideo] = useState<boolean>(false);
    function startCamera() {
        setFileUploadProcessing(false);
        setCaptureVideo(true);
        setLoading(true);
        setFileOk(false);
        navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
            videoRef!.current!.srcObject = stream;
        }).catch((err) => {
            console.log(err)
        });
    }
    function stopCamera() {
        videoRef.current!.pause();
        videoRef.current!.srcObject = null;
        setCaptureVideo(false);
        clearOverlay(cameraCanvas);
    }

    const imgCanvas: any = useRef();

    function startFile() {
        if (captureVideo) {
            stopCamera();
        }
        setFileUploadProcessing(true);
        setFileOk(false);
    }
    function cancelFile() {
        setFileUploadProcessing(false);
    }
    let [file, setFile] = useState<any>();
    let [fileOk, setFileOk] = useState<boolean>(false);
    let [imgLoading, setImgLoading] = useState<boolean>(false);
    async function fileUpload(e: React.ChangeEvent<HTMLInputElement>) {
        console.log('file upload')
        const { files } = e.target;
        const selectedFiles: FileList = files as FileList;
        setFile(selectedFiles?.[0]);
        setFileUploadProcessing(false);
        setFileOk(true);
        setImgLoading(true);

        const img: HTMLImageElement = await faceapi.bufferToImage(selectedFiles?.[0]);
        let faces = await faceapi.detectAllFaces(img, new faceapi.TinyFaceDetectorOptions({ inputSize: 320 }))
            .withFaceLandmarks()
            .withFaceExpressions()
            .withAgeAndGender()
        
        console.log(faces)

        if (faces.length === 0) {
            console.log('no faces')
            return;
        }

        const canvas = imgCanvas.current;
        faceapi.matchDimensions(canvas, img)
        faces = faceapi.resizeResults(faces, img)
        faceapi.draw.drawDetections(canvas, faces)
        faceapi.draw.drawFaceLandmarks(canvas, faces)
        faceapi.draw.drawFaceExpressions(canvas, faces)

        //draw gender and age
        faces.forEach((face: any) => {

            const box = face.detection.box
            const drawBox = new faceapi.draw.DrawBox(
                box,
                {
                    label: Math.round(face.age) + " year old " + face.gender
                }
            )
            drawBox.draw(canvas)
        })

        setImgLoading(false);


        
        
    }

    const intervalRef = useRef<any>(null)
	useEffect(() => {
        if (captureVideo) {
            console.log('video enabled')

            if (videoRef !== null && videoRef !== undefined) {
                intervalRef.current = setInterval(async () => {
                    await getFaces();
                    /* if (loading) {
                        setLoading(false)
                    } */
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
                        {loading ? <div className='loading'> <div className='loader'></div> </div> : ''}
                        <video ref={videoRef} width="480px" height="365px" autoPlay></video>
                        <canvas className={'webcam-overlay'} ref={cameraCanvas}></canvas>
                    </div>
                    : (fileUploadProcessing ? 
                        <label className="upload">
                            <input type="file" onChange={fileUpload}/>
                            <div className='graphic'>
                                upload
                                <i className="fas fa-file-upload"></i>
                            </div>
                        </label>
                        :
                        <div className='nocamera'>
                            {
                                fileOk ?
                                <div className='uploaded'>
                                    {imgLoading ? <div className='loading'> <div className='loader'></div> </div> : ''}
                                    <img src={URL.createObjectURL(file)} id="create" alt="uploaded file" onLoad={() => console.log('hi')}/>
                                    <canvas ref={imgCanvas}></canvas>
                                </div> :
                                ''
                            }
                        </div>)
                }
            </div>
			<div className='startstop'>
                {
                    !captureVideo ?
                    <button onClick={startCamera}>start camera</button>
                    : <button onClick={stopCamera}>stop camera</button>
                }
                {
                    !fileUploadProcessing ?
                    <button onClick={startFile}>upload file</button>
                    : <button onClick={cancelFile}>cancel upload</button>
                }
			</div>
		</div>
	);
}; export default Ai;