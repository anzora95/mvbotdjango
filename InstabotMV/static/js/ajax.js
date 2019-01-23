$(document).ready(function(){
    $("#loadtags").submit(function(e){
    e.preventDefault();
    $.ajax({
    url:$(this).attr('action'),
    type: $(this).attr('method'),
    data: $(this).serialize(),
    succes:function(json){
    console.log(json)
    }
    })
    })
})