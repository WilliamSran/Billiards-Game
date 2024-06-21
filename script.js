$(document).ready(function() {
    initializePage();
});
function initializePage(){
    let isDragging = false;
    let line = null;
    let velX =0.0;
    let velY =0.0;
    let accx = 0.0;
    let accy = 0.0;
    let drag = 150.0;
    let vep =  0.01;
    let shoota = ""
    const svgContainer = $('#svg-container svg').get(0); // Direct reference to the SVG elementa
    // Adjust this based on the actual radius of the cue ball


    // Function to get the cue ball's center dynamically
    function getCueBallCenter() {
        const cueBall = $('#WHITE', svgContainer);
        return {
            x: parseFloat(cueBall.attr('cx')),
            y: parseFloat(cueBall.attr('cy'))
        };
    }

    // Function to create a new line
    function createLine(x1, y1, x2, y2) {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2);
        line.setAttribute('stroke', 'brown');
        line.setAttribute('stroke-width', 10);
        svgContainer.appendChild(line);
        return line;
    }

    $('#WHITE').on('mousedown',centerevent);
    function centerevent(event) {

        //Get the cueBallCenter 
        const cueBallCenter = getCueBallCenter();

        isDragging = true;
        event.preventDefault();
        // Start the line from the center of the cue ball
        line = createLine(cueBallCenter.x, cueBallCenter.y, cueBallCenter.x, cueBallCenter.y);
    };

    $(document).on('mousemove', movevent);
     function movevent(event) {
        if (isDragging && line) {
            const newPos = getRelativePosition(event, svgContainer);
            // Update the line to extend from the cue ball's center to the new position
            line.setAttribute('x2', newPos.x);
            line.setAttribute('y2', newPos.y);


        }
    };

    $(document).on('mouseup',mausupevent);
     function mausupevent(event) {
        isDragging = false;
        if (line) {

            //Get the cueBallCenter 
            const cueBallCenter = getCueBallCenter();

            const releasePos = getRelativePosition(event, svgContainer);
            // Calculate velocity based on the difference
            velX = (cueBallCenter.x - releasePos.x) * 10; // Define or adjust CONSTANT as needed
            velY = (cueBallCenter.y - releasePos.y) * 10; // Define or adjust CONSTANT as needed
            // Finalize the line's position or remove it, depending on your needs


            //settings the limit of the shot velocity
            if (Math.abs(velX) > 10000) {
                //if the shot velocity is positive
                if(velX * -1 > 0){
                    velX = -10000;
                }
                // if the shot velocity is negative
                if(velX *-1 < 0){
                    velX = 10000;
                }
            }
            if (Math.abs(velY) > 10000) {
                //if the shot velocity is positive
                if(velY * -1 > 0){
                    velY = -10000;
                }
                // if the shot velocity is negative
                if(velY * -1 < 0){
                    velY = 10000;
                }
            }
            let speed = length(velX,velY)
            Accademics(speed,velX,velY);
            var postData = {
                xvel: velX, 
                yvel: velY,
                xacc: accx,
                yacc: accy,
              }; 

            $.post("/Playing.html", postData) 
                .done(function(response) {
                    let parts = response.split('oga')
                    Shoota= parts[1]
                     wincon = parseInt(parts[2])
                     LowHih = parts[3]
                     p1orp2 = parseInt(parts[4])
                    winner = parseInt(parts[5])
                    // console.log(Shoota)
                    // console.log(wincon)
                    // console.log(winner)
                    // console.log(LowHih)
                    svgData = parts[0]
                        var svgs = svgData.split('</svg>\n');
                        replaceSVGs(0, svgs,wincon,winner);

                    if(LowHih == 0 && (p1orp2 ==1 )){
                        $('#Ball').html('Player 1: is Lowballs');
                        $('#Ballt').html('Player 2: is Highballs');
                    }
                    else if(LowHih == 0 && (p1orp2 ==2 ))
                    {
                        $('#Ball').html('Player 1: is Highballs');
                        $('#Ballt').html('Player 2: is Lowballs ');
                    }
                    else if(LowHih == 1 && (p1orp2 ==2 )){
                        $('#Ball').html('Player 1: is Lowballs');
                        $('#Ballt').html('Player 2: is Highballs');
                    }
                    else if(LowHih == 1 && (p1orp2 ==1 ))
                    {
                        $('#Ball').html('Player 1: is Highballs');
                        $('#Ballt').html('Player 2: is Lowballs ');
                    }

                    
                    
                    //$.getScript('script.js')
                    //$('#svg-container').html(response)
                    //console.log(response)
                    
            });

            console.log(velX);
            console.log(velY);
            console.log(accx);
            console.log(accy);
            svgContainer.removeChild(line); // Example: remove the line
            line = null;
        }
    };
    function replaceSVGs(svgIndex, svgs,wincon,winner) {
        if (svgIndex < svgs.length-1) {
            // Replace the content of #svg-container with the current SVG
            $('#svg-container').html(svgs[svgIndex]);
            
    
            // Increment index for the next SVG
            svgIndex++;
    
            // Delay before replacing with the next SVG (adjust as needed)
            setTimeout(function() {
                replaceSVGs(svgIndex, svgs,wincon,winner);
            }, 10); // Change the delay time as needed
        }
         else if (svgIndex = svgs.length-1){
            //initializePage();
            // console.log(wincon)
            // console.log(winner)
            console.log("before entering wincon")
            if(wincon == 0)
            { console.log("after entering wincon")
                if(winner ==0)
                    $('#svg-container').html("<div style='color: gold; font-size: 100px;'> WINNER is PLAYER1</div>")
                else
                    $('#svg-container').html("<div style='color: gold; font-size: 100px;'> WINNER is PLAYER2</div>")
            }    
            else if(wincon == 1)
            { 
                if(winner==0)
                    $('#svg-container').html("<div style='color: brown; font-size: 100px;'> LOSER is PLAYER1</div>")
                else
                    $('#svg-container').html("<div style='color: brown; font-size: 100px;'> LOSER is PLAYER2</div>")
            }
            $('#firstShooter').html('Turn: ' + Shoota);
            $.getScript('script.js')
         }
        //$.getScript('script.js')
        
    }

    // Convert screen coordinates to SVG coordinates
    function getRelativePosition(event, svgElement) {
        var point = svgElement.createSVGPoint();
        point.x = event.clientX;
        point.y = event.clientY;
        var CTM = svgElement.getScreenCTM();
        if (CTM) {
            return point.matrixTransform(CTM.inverse());
        }
        return { x: 0, y: 0 };
    }
    
    function length(velX,velY)
    {
        let len = (velX * velX) + (velY * velY)
        return Math.sqrt(len)
    }


    function Accademics(speed, velX, velY)
    {
        if(speed > vep)
        {
            accx = (-velX / speed) * drag;
            accy = (-velY / speed) * drag;
        }
    }

    

   

    

};
