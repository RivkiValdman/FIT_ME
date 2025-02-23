// users.js (בצד הלקוח ב-React)

import React, { useState } from "react";

const Users = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [response, setResponse] = useState("");

  // טיפול בהגשת טופס הוספת משתמש
  const handleAddUser = async (e) => {
    e.preventDefault();

    // שליחת בקשה ל-POST לשרת כדי להוסיף משתמש
    const result = await fetch("http://127.0.0.1:8000/users/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name,
        email: email,
      }),
    });

    const data = await result.json();
    setResponse(`User added: ${data.name} (${data.email})`);
  };

  return (
    <div>
      <h1>Add a New User:</h1>
      <form onSubmit={handleAddUser}>
        <label>
          Name:
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </label>
        <br />
        <label>
          Email:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <br />
        <button type="submit">Add User</button>
      </form>

      <p>{response}</p>
    </div>
  );
};

export default Users;
