function getTags(){
var txt=''
var id = document.querySelector('select');
var tagname=id.options[id.selectedIndex].value;
var xhttp = new XMLHttpRequest();
xhttp.open("GET", "/instabotmv/tags/"+tagname+"/", true);
    xhttp.send();
var output = document.getElementById('tagx');
output.innerHTML=tagname;
console.log(tagname);

}