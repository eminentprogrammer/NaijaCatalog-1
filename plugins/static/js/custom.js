const listItem = document.querySelectorAll("#list");
const tabPane = document.querySelectorAll(".tab-pane");

function getActiveList() {
    listItem.forEach(list => {
        if (list.classList.contains("active")) {
            list.classList.remove("active")
        }
    });

    tabPane.forEach(tab => {
        if(tab.classList.contains("active")){
            tab.classList.remove("active");
        }
    })
}

listItem.forEach(item =>{
    item.addEventListener('click', e=>{
        if (e.target.classList.contains("active")) {}
        else{
            getActiveList();
            // tab = e.target.getAttribute("data-toggle");
            var tab = "#"+e.target.getAttribute("data-toggle")
            e.target.classList.add("animate__animated");
            e.target.classList.add("animate__fadeInLeft");
            e.target.classList.add("active");
            tab = document.querySelector(tab);

            tab.classList.add("animate__animated");
            tab.classList.add("animate__bounce");
            tab.classList.add("active");
        }
    })
})


var Category = document.getElementById('category');
var selectedOption; 
const institutionDiv = document.getElementById('institution_div');

Category.addEventListener("click", e=>{  
    selectedOption = Category.value;
    if(selectedOption == 'Student'){
        institutionDiv.classList.remove('d-none');
    }
    else{
        if(institutionDiv.classList.contains('d-none')){
        }
        else{
            institutionDiv.classList.add('d-none');
        }
    }
    console.log(selectedOption);
})