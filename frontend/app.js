
let allNotes = []

console.log("JavaScript Loaded")

async function login(){

const username = document.getElementById("username").value
const password = document.getElementById("password").value

const response = await fetch("http://127.0.0.1:5000/login",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
username:username,
password:password
})
})

const data = await response.json()

console.log("LOGIN RESPONSE:", data)

const token = data.token || data.access_token

if(token){
    localStorage.setItem("token", token)
    window.location.href = "dashboard.html"
}else{
    alert("Login failed")
}

}

async function register() {

    const username = document.getElementById("username").value 
    const password = document.getElementById("password").value 
    
    const response = await fetch("http://127.0.0.1:5000/auth/register",{
        method: "POST",
        headers:{
            "Content-Type":"application/json"
        },
    body: JSON.stringify({
        username : username,
        password : password
    })
    })

    const data = await response.json()
    console.log(data)

    document.getElementById("result").innerText = JSON.stringify(data)
}

document.addEventListener("DOMContentLoaded", 
function(){
    const savedTheme = localStorage.getItem("theme")

    if(savedTheme === "dark"){
        this.document.body.classList.add("dark")
    }

    loadNotes()
})


async function loadNotes() {
    const token = localStorage.getItem("token")

    if(!token){
        console.log("No token found, skipping loadNotes")
        
        return
    }

    const response = await fetch("http://127.0.0.1:5000/notes",{
        method: "GET",
        headers:{
            "Content-Type":"application/json",
            "Authorization":"Bearer " + token
        }
    })
  
    allNotes = await response.json()   // ⭐ IMPORTANT
    displayNotes(allNotes)             // ⭐ ONLY THIS
}

function displayNotes(notes){
    const list = document.getElementById("notes")
    list.innerHTML = ""

    const query = document.getElementById("search").value.toLowerCase()

    if(notes.length === 0){
        list.innerHTML = "<p>No notes found</p>"
        return
    }

    notes.forEach(note => {
        const li = document.createElement("li")

        let titleText = note.title
        let contentText = note.content

        if(query){
            const regex = new RegExp(`(${query})`, "gi")
            titleText = note.title.replace(regex,'<span class = "highlight">$1</span>')
            contentText = note.content.replace(regex,'<span class ="highlight">$1</span>')
        }

        const title = document.createElement("h3")
        title.innerHTML = titleText

        const content = document.createElement("p")
        content.innerHTML = contentText

        const editBtn = document.createElement("button")
        editBtn.innerText = "EDIT"

        const delBtn = document.createElement("button")
        delBtn.innerText = "DELETE"

        editBtn.onclick = () => startEdit(note)
        delBtn.onclick = () => deleteNote(note.id)

        const buttonGroup = document.createElement("div")
        buttonGroup.className = "button-group"


        buttonGroup.appendChild(delBtn)
        buttonGroup.appendChild(editBtn)

        li.appendChild(title)
        li.appendChild(content)
        li.appendChild(buttonGroup)

        list.appendChild(li)
    })
}

async function createNote(){
    const token = localStorage.getItem("token")

    const title = document.getElementById("title").value
    const content = document.getElementById("content").value

    let url = "http://127.0.0.1:5000/notes"
    let method = "POST"

    if(editingNoteId !== null){
        url = `http://127.0.0.1:5000/notes/${editingNoteId}`
        method = "PUT"
    }

    const response = await fetch(url,{
        method: method,
        headers:{
            "Content-Type":"application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            title : title,
            content : content
        })

    })

    const data = await response.json()

    alert(data.message)

    editingNoteId = null

    document.getElementById("createBtn").innerText = "Create Note"

    loadNotes()

    console.log(localStorage.getItem("token"))
}


async function deleteNote(id) {
    const token = localStorage.getItem("token")

    if(!confirm("Are you sure you want to delete this note ?")){
        return
    }

    const response = await fetch(
        `http://127.0.0.1:5000/notes/${id}`,{
        method: "DELETE",
        headers:{
            "Authorization":"Bearer " + token
        }
        })
    
    const data = await response.json()
    
    alert(data.message)

    loadNotes()
}

let editingNoteId = null

function startEdit(note){

    document.getElementById("title").value = ""
    document.getElementById("content").value = ""

    editingNoteId = note.id

    document.getElementById("createBtn").innerText = "Update Note"
}

function searchNotes(){
    const searchvalue = document.getElementById("search").value.toLowerCase()

    const filtered = allNotes.filter(note =>
        note.title.toLowerCase().includes(searchvalue) ||
        note.content.toLowerCase().includes(searchvalue)
    )

    displayNotes(filtered)
}

function toggleTheme(){
    document.body.classList.toggle("dark")

    // Save Preference
    if(document.body.classList.contains("dark")){
        localStorage.setItems("theme","dark")
    }else{
        localStorage.setItem("theme","light")
    }
}



function logout(){
    localStorage.removeItem("token")
    window.location.href = "index.html"
}