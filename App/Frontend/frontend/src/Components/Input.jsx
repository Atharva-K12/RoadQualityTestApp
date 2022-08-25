import React from 'react'
import { useState } from 'react';
import {Modal} from 'react-responsive-modal';
import 'react-responsive-modal/styles.css';
import Button from '@material-ui/core/Button';
import '../CSS/Input.css'

export default function Input(props) {
    const Backend_URL = props.Backend_URL;
    const [isModalOpen, setIsModalOpen] = useState(true);

    const [name,setName] = useState();

    const onNameChange = (e) =>{
        setName(e.target.value);
    }

    const [video,setVideo] = useState(undefined);
    const handleVideo = (e) =>{
        setVideo(e.target.files[0]);
    }

    const[gprData,setGprData] = useState(undefined);
    const handleFile = (e) =>{
        setGprData(e.target.files[0]);
    }


    const onSubmit = () =>{
        var makeDirectoryURL = new URL(Backend_URL + "/MakeDirectory");
        var queryParams = {
            'dirName':name
        }
        for (let k in queryParams){
            makeDirectoryURL.searchParams.append(k,queryParams[k]);
        }
        fetch(makeDirectoryURL,{
            method:'POST',
            headers:{
                "Content-Type": "application/JSON"
            },
            body:JSON.stringify({
                "filename": "string"
            })
        })
        .then(response => response.json())
        .then(data => {
            if(data.message === "Directory created"){
                setIsModalOpen(false);
            }else{
                alert("Name already used, try different name.")
            }
        });
    }

    const onSave = () =>{
        var inputVideoURL = new URL(Backend_URL + "/InputVideo");
        const inputData = new FormData();
        inputData.append('file', video);
        fetch(inputVideoURL,{
            method: 'POST',
            body: inputData,
        })
        .then(response=> response.json())
        .then(data => {
            if(data.filename !== video.filename){
                alert("Unable to upload video");
            }else{
                var inputGPRURL = new URL(Backend_URL + '/InputGPRData');
                const inputGPR = new FormData();
                inputGPR.append('file', gprData);
                fetch(inputGPRURL, {
                    method: 'POST',
                    body: inputGPR,
                })
                .then(response => response.json())
                .then(data => {
                    if(data.filename !== gprData.filename){
                        alert("Unable to upload GPR data file");
                    }else{

                    }
                })
            }
        })

        
    }

    const spanStyle = {
        color: "#ff0000",
        fontSize: 15
    };

    return (
        <div className='Input-Page'>
            <Modal 
                open={isModalOpen}
                center
                closeOnOverlayClick={false}
                showCloseIcon={false}
                styles={{
                    overlay:{
                        height:"auto",
                    }
                }}
            >
                <div className='modal-view'>
                    <label className='input-label' htmlFor='name'>
                        <p>Provide unique name to the record <span style={spanStyle}>*</span></p>
                        <input type='text' id='name' placeholder='XYZ Road' onChange={onNameChange} />
                    </label>
                    <Button onClick={onSubmit} className='submit' variant="contained" color="primary">
                        Save Name
                    </Button>
                </div>
            </Modal>
            <div className='Input-Box'>
                <div className='Inputs'>
                    <div className='video-upload'>
                        <form className='video-upload-form'>
                            <p className='label-p'>Upload video file <span style={spanStyle}>*</span></p>
                            <div className='buttons'>
                                <label className='label-video-upload' htmlFor='input-video'>
                                    <input type='file' id='input-video' accept='.mp4,.mkv' multiple={false} onChange={handleVideo}/>
                                </label>
                            </div>
                        </form>
                    </div>

                    <div className='GPR-file-upload'>
                        <form className='file-upload-form'>
                            <p className='label-p'>Upload GPR data file <span style={spanStyle}>*</span></p>
                            <div className='buttons'>
                                <label className='label-file-upload' htmlFor='input-file'>
                                    <input type='file' id='input-file' accept='.ASC, .csv' multiple={false} onChange={handleFile}/>
                                </label>
                            </div>
                        </form>
                    </div>
                </div>
                <Button onClick={onSave} className='submit' variant="contained" color="basic">
                    Submit Input
                </Button>
            </div>
            <div className='Input-preview'>
                <div className='video-preview-class'>
                    <p className='label-p'>Preview of uploaded video</p>
                    { 
                        video && 
                        <video 
                            className='video-preview'
                            width="600px" 
                            controls
                            src = {URL.createObjectURL(video)}
                        />
                    }  
                </div>
                {/* <div className='GPR-data-preview-class'>
                    <p className='label-p'>Preview of uploaded GPR data file</p>
                    {
                        gprData &&
                        <FilePreviewer file = {{
                            url : URL.createObjectURL(gprData)
                        }}
                        />
                    }
                </div> */}
                <Button onClick={onSave} className='submit' variant="contained" color="basic">
                    Submit Input
                </Button>
            </div>
        </div>
    )
}
