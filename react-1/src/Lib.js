import React from "react";

const Lib = ({ id, noun, noun2, adjective, color }) => {
const finalLib = <p>Lets go to the {noun}, with {noun2}, I heard there was a {color} walrus thats {adjective}!!!!</p>
  return (
    <div>
      {finalLib}
    </div>
  )

}

export default Lib;