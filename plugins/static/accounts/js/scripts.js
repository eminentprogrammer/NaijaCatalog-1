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