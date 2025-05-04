import React, { useState } from 'react';

export default function Sign_Up() {

  const [user_name, setusername] = useState('');
  const [First_name, setFirstName] = useState('');
  const [Last_name, setLastName] = useState('');
  const [Email, setEmail] = useState('');
  const [Password, setPassword] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'user_name') setusername(value);
    if (name === 'First_name') setFirstName(value);
    if (name === 'Last_name') setLastName(value);
    if (name === 'Email') setEmail(value);
    if (name === 'Password') setPassword(value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();  

    const userData = {
      username: user_name,
      firstname: First_name,
      lastname: Last_name,
      password: Password,
      gmail: Email,
    };

    try {
      const response = await fetch("http://127.0.0.1:5000/Sign_Up", {
        method: "POST",  
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),  
      });

      const data = await response.json(); 
      if (response.ok) {
        alert("הרשמה הצליחה!");
      } else {
        alert(data.error || "שגיאת הרשמה");
      }
    } catch (error) {
      alert("שגיאה בשמירת המשתמש. נסה שנית.");
    }
  };

  return (

    <div>
        <h1>
            הרשמה
            <br></br>
            </h1>
            <form onSubmit={handleSubmit}>

          <input type="text" name="user_name" placeholder="שם משתמש" value={user_name}
           onChange={handleChange} ></input> <br></br>

           <input type="text" name="First_name" placeholder="שם פרטי" value={First_name}
           onChange={handleChange} ></input> <br></br>

           <input type="text" name="Last_name" placeholder="שם משפחה" value={Last_name}
           onChange={handleChange} ></input> <br></br>

           <input type="text" name="Email" placeholder="מייל " value={Email}
           onChange={handleChange} ></input> <br></br>

          <input type="password" name="Password" placeholder="סיסמא " value={Password}
           onChange={handleChange} ></input> <br></br>

            {/* <input type="text" name="Verification" placeholder="אימות סיסמא " value={Verification}
           onChange={handleChange} ></input> */}
           <button>אישור </button>
           </form>

    </div>
  
);
}



