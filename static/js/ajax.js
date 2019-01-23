$(document).ready(function(){
    $("#loadtags").submit(function(e){
    e.preventDefault();
    $.ajax({
    url:$(this).attr('action'),
    type: $(this).attr('method'),
    data: $(this).serialize(),
    success:function(json){
    var output = document.getElementById('tags')
    var txt=''
     for ( i=0;i<json.length;i++) {
       txt+=" "+json[i].name
     }
    output.innerHTML=txt
    console.log(json)
    }
    })
    })
})