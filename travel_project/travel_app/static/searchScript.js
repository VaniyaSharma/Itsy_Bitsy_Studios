const search = () =>{
    const searchbox = document.getElementById("search-item").value.toUpperCase();
    const storeitems = document.getElementById("location-list")
    const location = document.querySelectorAll(".location")
    const lname = document.getElementsByTagName("h2")

    for(var i=0; i < lname.length; i++) {
        let match = location[i].getElementsByTagName('h2')[0];

        if(match){
            let textvalue = match.textContent || match.innerHTML

            if(textvalue.toUpperCase().indexOf(searchbox) > -1){
                location[i].style.display = "";
            }else{
                location[i].style.display = "none";
            }
        }
    }
}

