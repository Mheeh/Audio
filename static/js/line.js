/**
 * Created by Dariusz Urbański on 2016-04-12.
 */
function drawRedline(){
    var tt = $('#audio');
    var currTime = $("#audio").prop("currentTime");
    console.log(currTime);
    //console.log('Test')
    var duration = $("#audio").prop("duration");
    var percentage = currTime/duration;

    var redLineAreas = $(".redLine");
    for(var i = 0; i < redLineAreas.length;i++){
        var canva = redLineAreas[i];
        //canva.clearRect(0,0,canva.width,canva.height);
        var ctx = canva.getContext("2d");
        ctx.clearRect(0,0,canva.width,canva.height);

        ctx.beginPath();
        ctx.moveTo(percentage*canva.width,0);
        ctx.lineTo(percentage*canva.width,canva.height);
        ctx.strokeStyle="red";
        ctx.stroke();
    }

}