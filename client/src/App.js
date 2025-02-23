import React, { useEffect, useState } from "react";

const App = () => {
  // הגדרת state עבור name, email ו-response
  const [items, setItems] = useState([]);
  const [nameInput, setNameInput] = useState("");  // השתמש בשם שונה מ-"name"
  const [emailInput, setEmailInput] = useState("");  // השתמש בשם שונה מ-"email"
  const [response, setResponse] = useState("");

  // בקשה לקבלת פריטים (GET)
  useEffect(() => {
    fetch("http://127.0.0.1:8000/items")
      .then((response) => response.json())
      .then((data) => setItems(data));
  }, []);

  // טיפול בהגשת טופס הוספת משתמש
  const handleAddUser = async (e) => {
    e.preventDefault();

    // שליחת בקשה ל-POST להוספת משתמש
    const result = await fetch("http://127.0.0.1:8000/users/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: nameInput,
        email: emailInput,
      }),
    });

    const data = await result.json();
    setResponse(`User added: ${data.name} (${data.email})`);
  };

  return (
    <div>
      <h1>Items from Server:</h1>
      <ul>
        {items.map((item, index) => (
          <li key={index}>
            {item.name} - ${item.price}
          </li>
        ))}
      </ul>

      <h1>Add a New User:</h1>
      <form onSubmit={handleAddUser}>
        <label>
          Name:
          <input
            type="text"
            value={nameInput}
            onChange={(e) => setNameInput(e.target.value)}  // עדכון המשתנה nameInput
          />
        </label>
        <br />
        <label>
          Email:
          <input
            type="email"
            value={emailInput}
            onChange={(e) => setEmailInput(e.target.value)}  // עדכון המשתנה emailInput
          />
        </label>
        <br />
        <button type="submit">Add User</button>
      </form>

      <p>{response}</p>
    </div>
  );
};

export default App;
