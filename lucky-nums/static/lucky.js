const BASE_URL = "http://localhost:5000/api";
/** processForm: get data from form and make AJAX call to our API. */
//alert("im here")
//async function processForm(evt) {
   // evt.preventDefault();

    //let name = $("#name").val();
    //let year = $("#year").val();
    //let email = $("#email").val();
  //  let color = $("#color").val();

//    JSON.stringify(name)
    
   // let res = await axios.post("BASE_URL", { name, year, email, color })
    //console.log(res)
//}

/** handleResponse: deal with response from our lucky-num API. */

//async function handleResponse(resp) {
//    const response = await axios.get(`${BASE_URL}/`);
//}


$("#lucky-form").on("submit", processForm);
