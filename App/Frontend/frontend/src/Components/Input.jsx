import React from 'react'
import { useState } from 'react';
import {Modal} from 'react-responsive-modal';
import 'react-responsive-modal/styles.css';
import Button from '@material-ui/core/Button';
import '../CSS/Input.css'

export default function Input(props) {
    const Backend_URL = props.Backend_URL;
    const [isModalOpen, setIsModalOpen] = useState(false);

    const [name,setName] = useState();

    const onNameChange = (e) =>{
        setName(e.target.value);
    }

    const[video,setVideo] = useState();
    const handleVideo = (e) =>{
        localStorage.setItem('video',e.target.value);
        setVideo(e.target.value);
    }

    const[gprData,setGprData] = useState();
    const handleFile = (e) =>{
        localStorage.setItem('GPR-data',e.target.value);
        setGprData(e.target.value);
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
                                    <input type='file' id='input-video' accept='.mp4' multiple={false} onChange={handleVideo}/>
                                </label>
                            </div>
                        </form>
                    </div>

                    <div className='GPR-file-upload'>
                        <form className='file-upload-form'>
                            <p className='label-p'>Upload GPR data file <span style={spanStyle}>*</span></p>
                            <div className='buttons'>
                                <label className='label-file-upload' htmlFor='input-file'>
                                    <input type='file' id='input-file' accept='.csv' multiple={false} onChange={handleFile}/>
                                </label>
                            </div>
                        </form>
                    </div>
                </div>
                <div className='video-preview'>

                </div>
            </div>
            <div className='Input-preview'>

            </div>
        </div>
    )
}
