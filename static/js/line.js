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

        //zmienne pomocnicze dotyczace marginesu
        var leftMarginPerc = 0.0936;
        var rightMarginPerc = 0.1157;
        var leftMargin = canva.width*leftMarginPerc;
        var rightMargin = canva.width*rightMarginPerc

        var areaWidth = canva.width - (leftMargin+rightMargin);
        //


        //canva.clearRect(0,0,canva.width,canva.height);
        var ctx = canva.getContext("2d");
        ctx.clearRect(0,0,canva.width,canva.height);

        ctx.beginPath();
        ctx.moveTo(percentage*areaWidth+leftMargin,0);
        ctx.lineTo(percentage*areaWidth+leftMargin,canva.height);
        ctx.strokeStyle="red";
        ctx.stroke();
    }

}