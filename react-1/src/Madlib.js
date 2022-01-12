import React, { useState } from "react";
import { v4 as uuid } from 'uuid';
import Lib from "./Lib";
import SubjectEntriesForm from "./SubjectEntriesForm";

const Madlib = () => {
    const INITIAL_STATE = [
        {id: uuid(), noun: '', noun2: '', adjective: '', color: ''}
    ]
    const [libs, setLibs] = useState(INITIAL_STATE);
    const addItem = (newItem) => {
        setLibs(libs => [...libs, { ...newItem, id: uuid() }])
    }
    return (
        <div>
            <h3>Madlib Entertainment</h3>
            <SubjectEntriesForm addItem={addItem} />
            <div>
                {libs.map(({ id, noun, noun2, adjective, color }) => <Lib id={id} noun={noun} noun2={noun2} adjective={adjective} color={color} />)}
            </div>
        </div>
    )
}

export default Madlib;