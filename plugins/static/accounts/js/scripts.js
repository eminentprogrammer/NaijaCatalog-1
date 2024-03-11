const category = document.getElementById('category');
const institutionDiv = document.getElementById('institution_div');
institutionDiv.classList.add('d-none');
category.addEventListener('change', (e) => {
    const selectedOption = e.target.value;
    if (selectedOption == "Others") {
        institutionDiv.classList.remove('d-none');
    }
    else{
        institutionDiv.classList.add('d-none');
    }
    console.log(selectedOption);
});


const decryptBtn = document.querySelector("#decrypt");
const passwordInput = document.querySelector("#signup_password");
decryptBtn.addEventListener("click", e = () => {
    if(decryptBtn.value == "Decrypt Password"){
        decryptBtn.value = "Encrypt Password";
        passwordInput.type = "text";
    }
    else{
        decryptBtn.value = "Decrypt Password";
        passwordInput.type = "password";
    }
})