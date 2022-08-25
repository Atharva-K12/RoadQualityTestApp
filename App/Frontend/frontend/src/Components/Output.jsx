import React from 'react';
import { useState } from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import '../CSS/Output.css';

export default function Output() {
    var dict = {
        'name':'Sahil',
        'age':'20',
        'name2':'adwait',
        'age2':'20'
    }
    const [data, setData] = useState(dict);


    return (
        <div className='Output-Page'>
            <div>
                {
                    data && 
                    <Container>
                        <Row lg={4} xl={4}>
                            {
                                Object.entries(data).map(([key, value]) => (
                                    <Col>
                                        <div className='key-value'>
                                            <p className='key'>{key}</p>
                                            <p className='value'>{value}</p>
                                        </div>
                                    </Col>
                                ))
                            }
                        </Row>
                    </Container>
                }
            </div>
        </div>
    )
}