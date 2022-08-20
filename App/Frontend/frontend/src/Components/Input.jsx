import React from 'react'
import { useState } from 'react';
import {Modal} from 'react-responsive-modal';
import 'react-responsive-modal/styles.css';
import Button from '@material-ui/core/Button';
import '../CSS/Input.css'

export default function Input() {
    const [isModalOpen, setIsModalOpen] = useState(true);

    const [name,setName] = useState();
     
    const onNameChange = (e) =>{
        setName(e.targer.value);
    }

    const onSubmit = () =>{

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
        </div>
    )
}
