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
    document.querySelector("#ledon").onclick = () =>{
        console.log("You pressed LED ON!");
        sendCommand("LED ON");
    };
    document.querySelector("#ledoff").onclick = () =>{
        console.log("You pressed LED OFF!");
        sendCommand("LED OFF");
    };
    document.querySelector("#flash").onclick = () =>{
        let startPos = document.querySelector("#nums").value;
        let endPos = document.querySelector("#period").value;
        sendCommand(`FLASH ${startPos} ${endPos}`);

    };               
}

main();