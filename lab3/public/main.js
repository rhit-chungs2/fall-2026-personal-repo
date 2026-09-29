async function sendCommand(command){
    let response = await fetch(`/api/${command}`);
    let replyText = await response.text();
    console.log(replyText);

    document.querySelector("#replyText").innerHTML = replyText;

    return replyText;
}

function main() {
    console.log("Hello JavaScript!");

    //document.querySelector("#reset").innerHTML = "Hello";
    document.querySelector("#reset").onclick = () =>{
        console.log("You pressed the button!");
        sendCommand("RESET");
    };


    document.querySelector("#XAXIS1").onclick = () =>{
        console.log("You pressed XAXIS1!");
        sendCommand("X-AXIS 1");
    };    
    document.querySelector("#XAXIS2").onclick = () =>{
        console.log("You pressed XAXIS2!");
        sendCommand("X-AXIS 2");
    };  
    document.querySelector("#XAXIS3").onclick = () =>{
        console.log("You pressed XAXIS3!");
        sendCommand("X-AXIS 3");
    };  
    document.querySelector("#XAXIS4").onclick = () =>{
        console.log("You pressed XAXIS4!");
        sendCommand("X-AXIS 4");
    }; 
    document.querySelector("#XAXIS5").onclick = () =>{
        console.log("You pressed XAXIS5!");
        sendCommand("X-AXIS 5");
    };   
    document.querySelector("#ZEXTEND").onclick = () =>{
        console.log("You pressed ZEXTEND!");
        sendCommand("Z-AXIS EXTEND");
    };     
    document.querySelector("#ZRETRACT").onclick = () =>{
        console.log("You pressed ZRETRACT!");
        sendCommand("Z-AXIS RETRACT");
    };  
    document.querySelector("#GRIPPEROPEN").onclick = () =>{
        console.log("You pressed GRIPPEROPEN!");
        sendCommand("GRIPPER OPEN");
    }; 
    document.querySelector("#GRIPPERCLOSE").onclick = () =>{
        console.log("You pressed GRIPPERCLOSE!");
        sendCommand("GRIPPER CLOSE");
    };  
    document.querySelector("#move").onclick = () =>{
        let startPos = document.querySelector("#moveFrom").value;
        let endPos = document.querySelector("#moveTo").value;
        sendCommand(`MOVE ${startPos} ${endPos}`);

    };               
}

main();