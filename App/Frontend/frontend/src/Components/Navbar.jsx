import React from 'react'
import '../CSS/Navbar.css';

export default function Navbar() {
    return (
        <div>
            <nav>
                <div className='Navbar'>
                    <div className='Nav-Title'>
                        <h2>Perceptibles</h2>
                    </div>
                    <div className='Nav-Links'>
                        <div className='Links'>
                            <a href='/'>Home</a>
                        </div>
                        <div className='Links'>
                            <a href='/New-Record'>Create new record</a>
                        </div>
                        <div className='Links'>
                            <a href='/Saved'>Saved records</a>
                        </div>
                    </div>
                </div>
            </nav>
        </div>
    )
}
