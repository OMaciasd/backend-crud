let items = [];
let statusMessage = document.getElementById('statusMessage');

window.onload = () => {
    fetchItems();
};

function fetchItems() {
    statusMessage.textContent = "Loading items...";
    fetch('/api/items')
        .then(response => response.json())
        .then(data => {
            items = data;
            renderItems();
            statusMessage.textContent = "";
        })
        .catch(() => {
            statusMessage.textContent = "An error occurred while loading items.";
        });
}

function renderItems() {
    const itemsList = document.getElementById('itemsList');
    itemsList.innerHTML = '';
    items.forEach((item, index) => {
        const row = `
            <tr>
                <td>${item.name}</td>
                <td>
                    <button onclick="editItem(${index})">Edit</button>
                    <button onclick="deleteItem(${index})">Delete</button>
                </td>
            </tr>`;
        itemsList.innerHTML += row;
    });
}

document.getElementById('crudForm').onsubmit = function(event) {
    event.preventDefault();
    const itemName = document.getElementById('itemName').value;
    const itemId = document.getElementById('itemId').value;

    if (itemId) {
        statusMessage.textContent = "Updating the item...";
        fetch(`/api/items/${itemId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: itemName })
        }).then(() => {
            items[itemId].name = itemName;
            renderItems();
            resetForm();
            statusMessage.textContent = "";
        }).catch(() => {
            statusMessage.textContent = "An error occurred while updating the item.";
        });
    } else {
        statusMessage.textContent = "Creating a new item...";
        fetch('/api/items', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: itemName })
        }).then(response => response.json())
        .then(newItem => {
            items.push(newItem);
            renderItems();
            resetForm();
            statusMessage.textContent = "";
        }).catch(() => {
            statusMessage.textContent = "An error occurred while creating the item.";
        });
    }
};

function deleteItem(index) {
    statusMessage.textContent = "Deleting the item...";
    fetch(`/api/items/${index}`, { method: 'DELETE' })
        .then(() => {
            items.splice(index, 1);
            renderItems();
            statusMessage.textContent = "";
        })
        .catch(() => {
            statusMessage.textContent = "An error occurred while deleting the item.";
        });
}

function editItem(index) {
    const item = items[index];
    document.getElementById('itemName').value = item.name;
    document.getElementById('itemId').value = index;
}

function resetForm() {
    document.getElementById('itemName').value = '';
    document.getElementById('itemId').value = '';
}
