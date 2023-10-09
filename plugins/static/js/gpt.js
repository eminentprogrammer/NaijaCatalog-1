    // Select elements
    const messageInput = document.getElementById("gpt_chat");
    const sendBtn = document.getElementById("send");
    const messageBox = document.getElementById("message_chat");

    // Function to create the typing indicator element
    function createTypingElement() {
        const typingElement = document.createElement("div");
        typingElement.classList.add("my-2", "bg-secondary-c", "border", "rounded", "animate__animated", "animate__fadeInUp");
        return typingElement;
    }

    // Function to create a message element
    function createMessageElement(message) {
        const messageElement = document.createElement("p");
        messageElement.classList.add("px-3", "my-2");
        messageElement.style.textAlign = "end";
        messageElement.textContent = message;        
        return messageElement;
    }

    // Function to send a message
    function sendMessage(e) {
        const message = messageInput.value;
        if (message) {
            // Create typing indicator element
            const typing = createTypingElement();

            // Create a new message element
            const messageElement = createMessageElement(message);

            // Add the message to the Typing                        
            typing.appendChild(messageElement);

            // Add the message to the message box            
            messageBox.appendChild(typing);
            
            // Clear the input field
            messageInput.value = '';
        }
    }
    // Add click event listener to the send button
    sendBtn.addEventListener("click", sendMessage);   