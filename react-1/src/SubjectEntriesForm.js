import React, { useState } from "react";


const SubjectEntriesForm = ({ addItem }) => {
    const subjForm = {
        noun: "",
        noun2: "",
        adjective: "",
        color: ""
    }
    const [formData, setFormData] = useState(subjForm);
    const handleChange = e => {
        const { name, value } = e.target;
        setFormData(formData => ({
            ...formData,
            [name]: value
        }))
    }
    const handleSubmit = (e) => {
        e.preventDefault();
        addItem({ ...formData });
        setFormData(subjForm)
    }

    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="noun">Noun</label>
            <input
                id="noun"
                type="text"
                name="noun"
                placeholder="place"
                value={formData.noun}
                onChange={handleChange}
            />

            <label htmlFor="noun2">Noun2</label>
            <input
                id="noun2"
                type="text"
                name="noun2"
                placeholder="person"
                value={formData.noun2}
                onChange={handleChange}
            />

            <label htmlFor="adjective">Adjective</label>
            <input
                id="adjective"
                type="text"
                name="adjective"
                placeholder="adjective"
                value={formData.adjective}
                onChange={handleChange}
            />

            <label htmlFor="color">Color</label>
            <input
                id="color"
                type="text"
                name="color"
                placeholder="color"
                value={formData.color}
                onChange={handleChange}
            />

            <button>create a lib</button>
        </form>
    )
}

export default SubjectEntriesForm;
