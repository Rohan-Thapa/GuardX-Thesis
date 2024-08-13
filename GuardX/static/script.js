let items = document.querySelectorAll('.slider .list .item');
let next = document.getElementById('next');
let prev = document.getElementById('prev');
let thumbnails = document.querySelectorAll('.thumbnail .item');

// Configuring the Parameters
let countItem = items.length;
let itemActive = 0;

// Event Next clicked
next.onclick = function(){
    itemActive = itemActive + 1;
    if(itemActive >= countItem){
        itemActive = 0;
    }
    showSlider();
}

// Event Prev clicked
prev.onclick = function(){
    itemActive = itemActive - 1;
    if(itemActive < 0){
        itemActive = countItem - 1;
    }
    showSlider();
}

// auto run slider
let refreshInterval = setInterval(() => {
    next.click();
}, 5000)

function showSlider(){
    // remove old active item
    let itemActiveOld = document.querySelector('.slider .list .item.active');
    let thumbnailActiveOld = document.querySelector('.thumbnail .item.active');
    itemActiveOld.classList.remove('active');
    thumbnailActiveOld.classList.remove('active');

    // active new item
    items[itemActive].classList.add('active');
    thumbnails[itemActive].classList.add('active');

    // clear auto time run slider
    clearInterval(refreshInterval);
    refreshInterval = setInterval(() => {
        next.click();
    }, 5000)
}

// click thumbnail
thumbnails.forEach((thumbnail, index) => {
    thumbnail.addEventListener('click', () => {
        itemActive = index;
        showSlider();
    })
})

// This is just for nav scrolling
function scrollToSection(sectionId) {
    var targetElement = document.getElementById(sectionId);

    if (targetElement) {
        targetElement.scrollIntoView({ behavior: 'smooth' });
    }
}

// This is just when home is clicked.
const goLink = (link) => {
    window.location.href = link;
}

// Javascript for the tab navigation horizontal scroll buttons
const btnLeft = document.querySelector(".left-btn");
const btnRight = document.querySelector(".right-btn");
const tabMenu = document.querySelector(".tab-menu");

const IconVisibility = () => {
    let scrollLeftValue = Math.ceil(tabMenu.scrollLeft);
    // console.log(scrollLeftValue);
    let scrollableWidth = tabMenu.scrollWidth - tabMenu.clientWidth;
    // console.log(scrollableWidth);

    btnLeft.style.display = scrollLeftValue > 0 ? "block" : "none";
    btnRight.style.display = scrollableWidth > scrollLeftValue ? "block" : "none";
}

btnRight.addEventListener("click", () =>{
    tabMenu.scrollLeft += 150;
    setTimeout(() => IconVisibility(), 50);
});

btnLeft.addEventListener("click", () =>{
    tabMenu.scrollLeft -= 150;
    setTimeout(() => IconVisibility(), 50);
});

window.onload = function(){
    btnRight.style.display = tabMenu.scrollWidth > tabMenu.clientWidth || tabMenu.scrollWidth >= window.innerWidth ? "block" : "none";
    btnLeft.style.display = tabMenu.scrollWidth >= window.innerWidth ? "" : "none";
}

window.onresize = function(){
    btnRight.style.display = tabMenu.scrollWidth > tabMenu.clientWidth || tabMenu.scrollWidth >= window.innerWidth ? "block" : "none";
    btnLeft.style.display = tabMenu.scrollWidth >= window.innerWidth ? "" : "none";

    let scrollLeftValue = Math.round(tabMenu.scrollLeft);

    btnLeft.style.display = scrollLeftValue > 0 ? "block" : "none";
}


// Javascript to make the tab navigation draggable
let activeDrag = false;

tabMenu.addEventListener("mousemove", (drag) => {
    if (!activeDrag) return;
    tabMenu.scrollLeft -= drag.movementX;
    IconVisibility();
    tabMenu.classList.add("dragging");
});

document.addEventListener("mouseup", () => {
    activeDrag = false;
    tabMenu.classList.remove("dragging");
});

tabMenu.addEventListener("mousedown", () => {
    activeDrag = true;
});

// Javascript to view tab contents on click tab buttons
const tabs = document.querySelectorAll(".tab");
const tabBtns = document.querySelectorAll(".tab-btn");

const tab_Nav = function(tabBtnClick){
    tabBtns.forEach((tabBtn) => {
        tabBtn.classList.remove("active");
    });

    tabs.forEach((tab) => {
        tab.classList.remove("active");
    });

    tabBtns[tabBtnClick].classList.add("active");
    tabs[tabBtnClick].classList.add("active");
}

tabBtns.forEach((tabBtn, i) => {
    tabBtn.addEventListener("click", () => {
        tab_Nav(i);
    });
});


// JS for the flag card.
let card_button = document.querySelector('.report-gen');
let card_container = document.querySelector('.card_container');
let close_btn = document.querySelector('.card_close');
let send_req = document.querySelector('.req_send');
let leave_me = document.querySelector('.leave_it');

card_button.addEventListener('click', function(){
    card_container.classList.add('active');
});

close_btn.addEventListener('click', function(){
    card_container.classList.remove('active');
});

send_req.addEventListener('click', function(){
    fetch('http://127.0.0.1:5000/generate_report', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to generate report');
        }
    })
    .then(data => {
        console.log(data.message);
        // Changing the button functionlaity on success
        const button = document.getElementById('generateReportButton');
        button.onclick = openPDF;
        button.innerHTML = "Open Report";
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

function openPDF() {
    card_container.classList.remove('active');  // This is to remove the card when opening the report file.
    window.open('/static/report.pdf', '_blank');
}

// leave_me will also works as a close button.
leave_me.addEventListener('click', function(){
    card_container.classList.remove('active');
});

// Function to get the current date in YYYY-MM-DD format
function getCurrentDate() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// Get the element with class "current_dates"
const dateElement = document.querySelector('.current_dates');

// Insert the current date into the element
dateElement.textContent = getCurrentDate();

// JS for the API requests
document.addEventListener('DOMContentLoaded', () => {
    // url = 'http://127.0.0.1:5000/results'
    function fetchAndDisplayResults() {
        fetch('http://127.0.0.1:5000/results')
            .then(response => response.json())
            .then(data => {
                const results = data.results;
                const tableBody = document.querySelector('.result-body tbody');

                // Clear existing rows
                tableBody.innerHTML = '';

                // Iterate over the results and create table rows
                results.forEach(result => {
                    const row = document.createElement('tr');

                    // Create cells in the order of the table headers
                    const idCell = document.createElement('td');
                    idCell.textContent = result.id;
                    row.appendChild(idCell);

                    const testTypeCell = document.createElement('td');
                    testTypeCell.textContent = result.testType;
                    row.appendChild(testTypeCell);

                    const payloadCell = document.createElement('td');
                    // Convert `<` to &lt; and `>` to &gt;
                    let payload_res = result.payload.replace(/</g, '&lt;').replace(/>/g, '&gt;');
                    if (payload_res.length > 25) {
                        payload_res = payload_res.substring(0, 25) + '...';  // managing if it is more than 20 characters
                    }
                    payloadCell.innerHTML = payload_res;
                    row.appendChild(payloadCell);

                    const logisticCell = document.createElement('td');
                    const logisticStatus = document.createElement('p');
                    const logisticDetected = result.testType === 'all'
                        ? result.logic !== 'normal'
                        : result.testType === result.logistic;
                    logisticStatus.className = `status ${logisticDetected ? 'fail' : 'pass'}`;
                    logisticStatus.textContent = logisticDetected ? 'Detected!' : 'Clear!';
                    logisticCell.appendChild(logisticStatus);
                    row.appendChild(logisticCell);

                    const imbalanceCell = document.createElement('td');
                    const imbalanceStatus = document.createElement('p');
                    const imbalanceDetected = result.testType === 'all'
                        ? result.imbalance !== 'normal'
                        : result.testType === result.imbalance
                    imbalanceStatus.className = `status ${imbalanceDetected ? 'fail' : 'pass'}`;
                    imbalanceStatus.textContent = imbalanceDetected ? 'Detected!' : 'Clear!';
                    imbalanceCell.appendChild(imbalanceStatus);
                    row.appendChild(imbalanceCell);

                    const balanceCell = document.createElement('td');
                    const balanceStatus = document.createElement('p');
                    const balanceDetected = result.testType === 'all'
                        ? result.balance !== 'normal'
                        : result.testType === result.balance;
                    balanceStatus.className = `status ${balanceDetected ? 'fail' : 'pass'}`;
                    balanceStatus.textContent = balanceDetected ? 'Detected!' : 'Clear!';
                    balanceCell.appendChild(balanceStatus);
                    row.appendChild(balanceCell);

                    const foundCell = document.createElement('td');
                    foundCell.textContent = `${result.logistic} / ${result.imbalance} / ${result.balance}`;
                    row.appendChild(foundCell);

                    const deleteCell = document.createElement('td');
                    const deleteIcon = document.createElement('i');
                    deleteIcon.className = 'fas fa-trash delete-icon';
                    deleteIcon.addEventListener('click', () => deleteResult(result.id));
                    deleteCell.appendChild(deleteIcon);
                    row.appendChild(deleteCell);

                    // Append the new row to the table body
                    tableBody.appendChild(row);
                });
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    }

    // url = 'http://127.0.0.1:5000/test_payload'
    // api_request = {"testType": userTestType, "payload": userPrompt}
    async function fetchData(userTestType, userPrompt) {
        const url = "http://127.0.0.1:5000/test_payload";
        const api_request = {
            testType: userTestType,
            payload: userPrompt
        };

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(api_request)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching data: ', error);
            throw error;
        }
    }

    // JS for deleting the result through ID of the result
    // url = 'http://127.0.0.1:5000/delete_result/<int:user_id>'
    async function deleteResult(id) {
        const url = `http://127.0.0.1:5000/delete_result/${id}`;
        
        try {
            const response = await fetch(url, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            console.log('Success:', data);
            fetchAndDisplayResults();
        } catch (error) {
            console.error('Error deleting data:', error);
        }
    }

    // JS for the looking at the form entry data for data entry
    const generateForm = document.querySelector(".generate-form");

    const handleFormSubmission = (e) => {
        e.preventDefault();

        // Get user input and image quantity values from the form.
        const userPrompt = e.target[0].value;
        const userTestType = e.target[1].value;

        // console.log(userPrompt, userTestType); // Here I have got the input data which I need to feed on my AI machine.

        fetchData(userTestType, userPrompt)
            .then(data => {
                console.log('Data received:', data);
                fetchAndDisplayResults();
                generateForm.reset(); // Clear the form content
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    generateForm.addEventListener("submit", handleFormSubmission);

    // Call the function when the webpage loads
    fetchAndDisplayResults();
});


// Coded by Rohan Thapa for the project.

