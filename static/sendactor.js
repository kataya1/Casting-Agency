jwt = localStorage.getItem("token")
send = (e) => {
    fetch('/actors',
    {
        method: "POST",
        body: JSON.stringify({
            name: nameinputfield.value,
            DOB: dobinputfield.value,
            gender: genderinputfield.value
        }),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `bearer ${jwt}`
        }
    }).then(res => res.json())
    .then((data) =>{
        if(data['success']){
            alert('success')
            nameinputfield.value = ""
            dobinputfield.value = ""
            genderinputfield = ""
        }
    })
}